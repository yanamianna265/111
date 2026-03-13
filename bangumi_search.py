#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bangumi 番剧图片搜索工具 - 带自动下载功能
根据用户输入的番剧名称，搜索并获取封面图片，自动下载到本地
支持中英文及日文名搜索
"""

import requests
from bs4 import BeautifulSoup
import sys
import os
from datetime import datetime

# 全局调试开关
DEBUG = True

def log(msg):
    """调试日志输出"""
    if DEBUG:
        print(f"[DEBUG] {msg}")

def fix_image_url(url):
    """补全图片URL协议头"""
    if url and url.startswith('//'):
        return 'https:' + url
    return url

def search_bangumi_api(name):
    """
    使用 Bangumi API 搜索番剧
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }
    
    encoded_name = requests.utils.quote(name)
    search_url = f"https://api.bgm.tv/search/subject/{encoded_name}"
    log(f"API搜索URL: {search_url}")
    
    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        log(f"API HTTP状态码: {response.status_code}")
        
        if response.status_code == 404:
            log("API返回404，未找到结果")
            return None
            
        response.raise_for_status()
        data = response.json()
        log(f"API返回数据: {data}")
        
        if data.get('code') == 404:
            log("API返回错误码404")
            return None
        
        anime_results = [item for item in data.get('list', []) if item.get('type') == 2]
        log(f"找到 {len(anime_results)} 个动画结果")
        
        if not anime_results:
            log("API搜索未找到动画结果")
            return None
        
        best_result = select_best_match(name, anime_results)
        log(f"选择最佳匹配: {best_result}")
        
        return {
            'id': best_result['id'],
            'name_cn': best_result.get('name_cn', ''),
            'name_jp': best_result.get('name', ''),
            'url': f"https://bgm.tv/subject/{best_result['id']}"
        }
        
    except requests.exceptions.HTTPError as e:
        log(f"API HTTP错误: {e}")
        return None
    except Exception as e:
        log(f"API搜索出错: {e}")
        return None

def select_best_match(query, results):
    """
    从搜索结果中选择最佳匹配
    优先级：1.标题完全匹配 2.无副标题的TV动画 3.最早播出的
    """
    query_lower = query.lower()
    
    def score(item):
        score_val = 0
        name_cn = item.get('name_cn', '').lower()
        name_jp = item.get('name', '').lower()
        air_date = item.get('air_date', '9999-99-99')
        
        if query_lower == name_cn or query_lower == name_jp:
            score_val += 100
        elif query_lower in name_cn or query_lower in name_jp:
            score_val += 50
            
        title = name_cn or name_jp
        if not any(keyword in title for keyword in ['剧场版', '特别篇', '前篇', '后篇', 'oad', 'ova', 'movie', 'special']):
            score_val += 30
            
        if air_date < '2015-01-01':
            score_val += 10
            
        return score_val
    
    sorted_results = sorted(results, key=score, reverse=True)
    return sorted_results[0]

def get_subject_details(subject_id):
    """
    获取番剧详细信息和大图
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    
    url = f"https://bgm.tv/subject/{subject_id}"
    log(f"详情页URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        log(f"详情页HTTP状态码: {response.status_code}")
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        result = {
            'image_large': '',
            'image_small': '',
        }
        
        og_image = soup.find('meta', property='og:image')
        if og_image:
            result['image_large'] = fix_image_url(og_image.get('content', ''))
            log(f"从og:image获取大图: {result['image_large']}")
        
        cover_img = soup.select_one('a.cover img')
        if cover_img:
            src = cover_img.get('src', '')
            log(f"封面图片src: {src}")
            if src:
                result['image_small'] = fix_image_url(src)
                result['image_large'] = fix_image_url(src.replace('/s/', '/l/').replace('/g/', '/l/'))
                log(f"转换后大图: {result['image_large']}")
        
        api_url = f"https://api.bgm.tv/v0/subjects/{subject_id}"
        try:
            api_response = requests.get(api_url, headers=headers, timeout=10)
            log(f"详情API状态码: {api_response.status_code}")
            if api_response.status_code == 200:
                api_data = api_response.json()
                images = api_data.get('images', {})
                log(f"详情API图片数据: {images}")
                if images:
                    if not result['image_large']:
                        result['image_large'] = fix_image_url(images.get('large', ''))
                    if not result['image_small']:
                        result['image_small'] = fix_image_url(images.get('common', ''))
        except Exception as e:
            log(f"详情API请求出错: {e}")
        
        return result
        
    except Exception as e:
        log(f"获取详情出错: {e}")
        return None

def get_anime_image(anime_name):
    """
    获取动漫图片
    """
    print(f"\n{'='*50}")
    print(f"开始搜索: {anime_name}")
    print(f"{'='*50}")
    
    result = {
        'name': anime_name,
        'success': False,
        'id': None,
        'name_cn': '',
        'name_jp': '',
        'image_small': '',
        'image_large': '',
        'url': '',
        'error': ''
    }
    
    subject = search_bangumi_api(anime_name)
    
    if not subject:
        result['error'] = '未找到相关番剧，请尝试使用日文名或英文名'
        log("搜索失败")
        return result
    
    log(f"搜索成功: {subject}")
    result['id'] = subject['id']
    result['name_cn'] = subject.get('name_cn', '')
    result['name_jp'] = subject.get('name_jp', '')
    result['url'] = subject['url']
    
    print(f"找到番剧: {result['name_cn'] or result['name_jp'] or '未知'}")
    details = get_subject_details(subject['id'])
    if details:
        result['image_large'] = details.get('image_large', '')
        result['image_small'] = details.get('image_small', '')
        result['success'] = bool(result['image_large'])
        log(f"图片获取结果: large={result['image_large'][:50]}..., small={result['image_small'][:50]}...")
    
    if not result['success']:
        result['error'] = '获取图片失败'
        log("图片获取失败")
    
    return result

def create_download_folder():
    """创建下载文件夹"""
    folder_name = "bangumi_images"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        log(f"创建下载文件夹: {folder_name}")
    return folder_name

def sanitize_filename(filename):
    """清理文件名中的非法字符"""
    illegal_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    return filename.strip()

def generate_filename(result):
    """根据番剧信息生成安全的文件名"""
    # 优先使用中文名，其次使用日文名
    name = result['name_cn'] or result['name_jp'] or result['name'] or "unknown"
    name = sanitize_filename(name)
    
    # 限制文件名长度
    if len(name) > 50:
        name = name[:50]
    
    return f"{name}_{result['id']}"

def download_image(image_url, save_path, description="图片"):
    """下载图片到指定路径"""
    try:
        if not image_url:
            print(f"✗ {description}URL为空，跳过下载")
            return False
        
        print(f"正在下载{description}: {os.path.basename(save_path)}")
        
        response = requests.get(image_url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = os.path.getsize(save_path)
        print(f"✓ {description}下载成功: {save_path} ({file_size/1024:.1f} KB)")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ {description}下载失败: {e}")
        return False
    except Exception as e:
        print(f"✗ {description}保存失败: {e}")
        return False

def download_anime_images(result, folder=None):
    """下载番剧的所有图片"""
    if not result['success']:
        print(f"✗ 搜索失败，无法下载图片")
        return False
    
    if folder is None:
        folder = create_download_folder()
    
    downloaded_files = []
    
    # 生成基础文件名
    base_filename = generate_filename(result)
    
    # 下载大图
    if result['image_large']:
        large_ext = os.path.splitext(result['image_large'])[-1] or '.jpg'
        large_path = os.path.join(folder, f"{base_filename}_large{large_ext}")
        if download_image(result['image_large'], large_path, "大图"):
            downloaded_files.append(large_path)
    
    # 下载小图
    if result['image_small']:
        small_ext = os.path.splitext(result['image_small'])[-1] or '.jpg'
        small_path = os.path.join(folder, f"{base_filename}_small{small_ext}")
        if download_image(result['image_small'], small_path, "小图"):
            downloaded_files.append(small_path)
    
    return downloaded_files

def print_result(result, downloaded_files=None):
    """格式化打印结果"""
    print(f"\n{'='*50}")
    print("搜索结果:")
    print(f"{'='*50}")
    
    if result['success']:
        print(f"✓ 搜索成功")
        print(f"  番剧ID: {result['id']}")
        print(f"  中文名: {result['name_cn'] or '无'}")
        print(f"  日文名: {result['name_jp'] or '无'}")
        print(f"  详情页: {result['url']}")
        print(f"  小图URL: {result['image_small'] or '无'}")
        print(f"  大图URL: {result['image_large'] or '无'}")
        
        if downloaded_files:
            print(f"\n{'='*50}")
            print("下载结果:")
            print(f"{'='*50}")
            print(f"✓ 成功下载 {len(downloaded_files)} 个文件到 bangumi_images 文件夹:")
            for file_path in downloaded_files:
                file_size = os.path.getsize(file_path)
                print(f"  - {os.path.basename(file_path)} ({file_size/1024:.1f} KB)")
    else:
        print(f"✗ 搜索失败")
        print(f"  错误信息: {result['error']}")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python bangumi_search.py <番剧名称> [-d]")
        print("参数说明:")
        print("  <番剧名称>   要搜索的番剧名称（支持中文/英文/日文）")
        print("  -d          仅下载大图（默认下载大小图）")
        print("")
        print("示例:")
        print("  python bangumi_search.py '进击的巨人'")
        print("  python bangumi_search.py 'Attack on Titan'")
        print("  python bangumi_search.py '鬼灭之刃' -d")
        sys.exit(1)
    
    anime_name = sys.argv[1]
    
    # 检查是否只下载大图
    only_large = '-d' in sys.argv
    
    # 搜索番剧
    result = get_anime_image(anime_name)
    
    # 下载图片
    downloaded_files = []
    if result['success']:
        downloaded_files = download_anime_images(result)
        
        # 如果指定只下载大图，删除小图文件
        if only_large and downloaded_files:
            folder = "bangumi_images"
            base_filename = generate_filename(result)
            small_file = os.path.join(folder, f"{base_filename}_small.jpg")
            if small_file in downloaded_files:
                os.remove(small_file)
                downloaded_files.remove(small_file)
                print(f"已删除小图文件（仅保留大图模式）")
    
    # 打印结果
    print_result(result, downloaded_files)

if __name__ == "__main__":
    main()