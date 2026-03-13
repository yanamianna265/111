import requests
import os
import time
import hashlib
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlencode
import json
import re

class BangumiImageSpider:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://chii.in/',
        }
        self.base_url = 'https://chii.in'
        self.image_base_url = 'https://lain.bgm.tv'
        
    def search_subjects(self, keyword, page_count=1, save_dir='bangumi_images'):
        """
        搜索Bangumi条目并下载封面图片
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        downloaded_urls = set()
        
        for page in range(1, page_count + 1):
            print(f'正在搜索第 {page} 页...')
            
            try:
                # 使用POST请求获取数据
                search_url = f"{self.base_url}/subject_search/{keyword}?cat=all&page={page}"
                print(f'搜索URL: {search_url}')
                
                # 获取搜索页面
                response = self.session.get(search_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                response.encoding = 'utf-8'
                
                # 解析搜索结果
                image_urls = self.parse_javascript_data(response.text)
                
                if len(image_urls) == 0:
                    print("未找到图片，尝试备用解析方法...")
                    image_urls = self.parse_from_html_fallback(response.text)
                
                print(f'在第 {page} 页找到 {len(image_urls)} 张图片')
                
                # 下载图片
                for img_url in image_urls:
                    if img_url and img_url not in downloaded_urls:
                        success = self.download_image(img_url, save_dir, keyword)
                        if success:
                            downloaded_urls.add(img_url)
                        time.sleep(1)
                        
            except Exception as e:
                print(f'爬取第 {page} 页时出错: {e}')
                continue
                
            time.sleep(2)
    
    def parse_javascript_data(self, html):
        """
        解析JavaScript中的数据
        """
        image_urls = []
        
        # 方法1: 查找JSON数据
        json_patterns = [
            r'var\s+jsonData\s*=\s*(\{.*?\});',
            r'data:\s*(\{.*?\})',
            r'window\.__DATA__\s*=\s*(\{.*?\});',
            r'searchResult\s*:\s*(\[.*?\])',
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, html, re.DOTALL)
            for match in matches:
                try:
                    data = json.loads(match)
                    urls = self.extract_urls_from_json(data)
                    image_urls.extend(urls)
                    print(f"从JSON找到 {len(urls)} 个图片URL")
                except json.JSONDecodeError:
                    continue
        
        # 方法2: 查找图片URL模式
        url_patterns = [
            r'https?://lain\.bgm\.tv/pic/cover/[^\'"]+\.(jpg|jpeg|png|webp)',
            r'//lain\.bgm\.tv/pic/cover/[^\'"]+\.(jpg|jpeg|png|webp)',
            r'/pic/cover/[^\'"]+\.(jpg|jpeg|png|webp)',
            r'coverUrl[\'"]?\s*:\s*[\'"]([^\'"]+)[\'"]',
            r'image[\'"]?\s*:\s*[\'"]([^\'"]+)[\'"]',
            r'img[\'"]?\s*:\s*[\'"]([^\'"]+)[\'"]',
        ]
        
        for pattern in url_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    url = match[0]
                else:
                    url = match
                
                full_url = self.process_image_url(url)
                if full_url and full_url not in image_urls:
                    image_urls.append(full_url)
                    print(f"通过正则找到: {full_url}")
        
        return image_urls
    
    def extract_urls_from_json(self, data):
        """从JSON数据中提取图片URL"""
        urls = []
        
        def search_dict(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, str) and self.is_cover_image(value):
                        urls.append(value)
                    else:
                        search_dict(value)
            elif isinstance(obj, list):
                for item in obj:
                    search_dict(item)
        
        search_dict(data)
        return urls
    
    def parse_from_html_fallback(self, html):
        """备用HTML解析方法"""
        soup = BeautifulSoup(html, 'html.parser')
        image_urls = []
        
        # 查找可能的图片容器
        containers = soup.find_all(['div', 'li', 'span'], class_=re.compile(r'item|subject|cover'))
        for container in containers:
            # 查找data属性中的图片URL
            for attr in container.attrs:
                if 'data' in attr.lower() and 'src' in attr.lower():
                    value = container[attr]
                    if self.is_cover_image(value):
                        full_url = self.process_image_url(value)
                        if full_url and full_url not in image_urls:
                            image_urls.append(full_url)
            
            # 查找图片标签
            imgs = container.find_all('img', src=True)
            for img in imgs:
                src = img.get('src') or img.get('data-src')
                if src and self.is_cover_image(src):
                    full_url = self.process_image_url(src)
                    if full_url and full_url not in image_urls:
                        image_urls.append(full_url)
        
        return image_urls
    
    def search_with_api(self, keyword, page=1):
        """
        尝试使用API方式搜索
        """
        try:
            # Bangumi可能有API接口
            api_url = f"https://api.bgm.tv/search/subject/{keyword}"
            params = {
                'type': 2,  # 动画
                'responseGroup': 'large',
                'start': (page-1) * 20,
                'max_results': 20
            }
            
            headers = self.headers.copy()
            headers.update({
                'Accept': 'application/json',
                'User-Agent': 'bangumi-spider/1.0 (https://example.com)'
            })
            
            response = self.session.get(api_url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return self.extract_urls_from_api(data)
                
        except Exception as e:
            print(f"API搜索失败: {e}")
        
        return []
    
    def extract_urls_from_api(self, data):
        """从API响应中提取图片URL"""
        urls = []
        
        if isinstance(data, dict) and 'list' in data:
            for item in data['list']:
                if 'images' in item and isinstance(item['images'], dict):
                    # 获取不同尺寸的图片
                    for size in ['large', 'medium', 'small']:
                        if size in item['images']:
                            url = item['images'][size]
                            if url and self.is_cover_image(url):
                                urls.append(url)
        
        return urls
    
    def is_cover_image(self, url):
        """判断是否为封面图片"""
        if not url:
            return False
            
        url_lower = url.lower()
        
        positive_patterns = [
            r'lain\.bgm\.tv',
            r'/pic/cover/',
            r'cover',
        ]
        
        negative_patterns = [
            r'icon',
            r'avatar',
            r'small',
            r'thumb',
        ]
        
        has_positive = any(re.search(pattern, url_lower) for pattern in positive_patterns)
        has_negative = any(re.search(pattern, url_lower) for pattern in negative_patterns)
        
        return has_positive and not has_negative
    
    def process_image_url(self, img_url):
        """处理图片URL"""
        if not img_url:
            return None
            
        img_url = img_url.strip()
        
        if img_url.startswith('//'):
            return 'https:' + img_url
        elif img_url.startswith('/'):
            if '/pic/' in img_url:
                return self.image_base_url + img_url
            else:
                return self.base_url + img_url
        elif img_url.startswith('http'):
            return img_url
        else:
            return self.image_base_url + '/' + img_url.lstrip('/')
    
    def download_image(self, img_url, save_dir, keyword):
        """下载单张图片"""
        try:
            print(f'正在下载: {img_url}')
            
            img_headers = self.headers.copy()
            img_headers['Referer'] = self.base_url
            
            response = self.session.get(img_url, headers=img_headers, timeout=15)
            response.raise_for_status()
            
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                print(f'不是图片文件: {content_type}')
                return False
            
            filename = self.generate_filename(img_url, keyword, response.headers)
            filepath = os.path.join(save_dir, filename)
            
            counter = 1
            original_filepath = filepath
            while os.path.exists(filepath):
                name, ext = os.path.splitext(original_filepath)
                filepath = f"{name}_{counter}{ext}"
                counter += 1
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            self.save_metadata(filepath, img_url, keyword)
                
            file_size = len(response.content) // 1024
            print(f'✓ 下载成功: {os.path.basename(filepath)} ({file_size}KB)')
            return True
            
        except Exception as e:
            print(f'✗ 下载失败 {img_url}: {e}')
            return False
    
    def generate_filename(self, img_url, keyword, headers):
        """生成文件名"""
        match = re.search(r'/(\d+)_([^/]+)\.(jpg|jpeg|png|webp)', img_url)
        if match:
            subject_id = match.group(1)
            image_code = match.group(2)
            ext = match.group(3)
            filename = f"bgm_{subject_id}_{image_code}.{ext}"
        else:
            file_ext = self.get_file_extension(img_url, headers)
            file_hash = hashlib.md5(img_url.encode()).hexdigest()[:8]
            filename = f"bgm_{keyword}_{file_hash}{file_ext}"
        
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return filename
    
    def get_file_extension(self, url, headers):
        """获取文件扩展名"""
        content_type = headers.get('Content-Type', '').lower()
        if 'jpeg' in content_type or 'jpg' in content_type:
            return '.jpg'
        elif 'png' in content_type:
            return '.png'
        elif 'gif' in content_type:
            return '.gif'
        elif 'webp' in content_type:
            return '.webp'
        
        if '.' in url:
            ext = url.split('.')[-1].lower().split('?')[0]
            if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                return '.' + ext
        
        return '.jpg'
    
    def save_metadata(self, filepath, img_url, keyword):
        """保存元数据"""
        meta_file = filepath + '.json'
        metadata = {
            'source_url': img_url,
            'keyword': keyword,
            'download_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'filename': os.path.basename(filepath),
        }
        
        try:
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f'保存元数据失败: {e}')

# 使用示例
if __name__ == "__main__":
    spider = BangumiImageSpider()
    
    # 搜索关键词
    keyword = "进击的巨人"
    
    print(f"开始搜索: {keyword}")
    spider.search_subjects(keyword, page_count=1, save_dir=f'bangumi_{keyword}')