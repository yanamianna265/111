import requests
import json
import time
import os
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import re
import hashlib

class ImageSpider:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
    def search_images(self, keyword, page_count=1, save_dir='images'):
        """
        搜索并下载图片
        :param keyword: 搜索关键词
        :param page_count: 要爬取的页数
        :param save_dir: 图片保存目录
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        downloaded_urls = set()
        
        for page in range(page_count):
            print(f'正在爬取第 {page + 1} 页...')
            
            # 百度图片搜索URL（实际中需要根据网站结构调整）
            search_url = self.build_search_url(keyword, page)
            
            try:
                # 获取搜索页面
                response = self.session.get(search_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                # 解析图片URL（这里需要根据具体网站结构调整解析方法）
                image_urls = self.parse_image_urls(response.text)
                
                # 下载图片
                for img_url in image_urls:
                    if img_url not in downloaded_urls:
                        self.download_image(img_url, save_dir, keyword)
                        downloaded_urls.add(img_url)
                        time.sleep(0.5)  # 添加延迟避免请求过快
                        
            except Exception as e:
                print(f'爬取第 {page + 1} 页时出错: {e}')
                continue
                
            time.sleep(1)  # 页间延迟
    
    def build_search_url(self, keyword, page):
        """构建搜索URL（以百度图片为例）"""
        # 百度图片搜索的实际URL结构比较复杂，这里简化处理
        params = {
            'word': keyword,
            'pn': page * 20,  # 每页20张图片
            'tn': 'baiduimage',
            'ie': 'utf-8',
        }
        return f"https://image.baidu.com/search/index?{urlencode(params)}"
    
    def parse_image_urls(self, html):
        """从HTML中解析图片URL"""
        image_urls = []
        
        # 方法1: 使用正则表达式提取（针对百度图片）
        # 百度图片的实际图片URL在JSON数据中
        pattern = r'"objURL":"(.*?)"'
        urls = re.findall(pattern, html)
        image_urls.extend(urls)
        
        # 方法2: 使用BeautifulSoup解析
        soup = BeautifulSoup(html, 'html.parser')
        img_tags = soup.find_all('img', {'src': True})
        
        for img in img_tags:
            src = img.get('src')
            if src and src.startswith(('http', '//')):
                if src.startswith('//'):
                    src = 'https:' + src
                image_urls.append(src)
        
        # 去重
        return list(set(image_urls))
    
    def download_image(self, img_url, save_dir, keyword):
        """下载单张图片"""
        try:
            # 设置图片请求头
            img_headers = self.headers.copy()
            img_headers['Referer'] = 'https://image.baidu.com/'
            
            response = self.session.get(img_url, headers=img_headers, timeout=15)
            response.raise_for_status()
            
            # 生成文件名
            file_ext = self.get_file_extension(img_url, response.headers)
            file_hash = hashlib.md5(img_url.encode()).hexdigest()[:8]
            filename = f"{keyword}_{file_hash}{file_ext}"
            filepath = os.path.join(save_dir, filename)
            
            # 保存图片
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            print(f'下载成功: {filename}')
            
        except Exception as e:
            print(f'下载图片失败 {img_url}: {e}')
    
    def get_file_extension(self, url, headers):
        """获取文件扩展名"""
        # 从Content-Type获取
        content_type = headers.get('Content-Type', '')
        if 'jpeg' in content_type or 'jpg' in content_type:
            return '.jpg'
        elif 'png' in content_type:
            return '.png'
        elif 'gif' in content_type:
            return '.gif'
        elif 'webp' in content_type:
            return '.webp'
        
        # 从URL获取
        if url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            return '.' + url.split('.')[-1].lower()
        
        # 默认
        return '.jpg'

# 使用示例
if __name__ == "__main__":
    spider = ImageSpider()
    
    # 搜索关键词
    keyword = "风景"
    
    # 爬取2页图片
    spider.search_images(keyword, page_count=2, save_dir='downloaded_images')