# # # parsers/sitemap_parser.py
# # import requests
# # import xml.etree.ElementTree as ET
# # from urllib.parse import urlparse, urljoin
# # from typing import List, Dict, Optional, Set
# # import re
# # from datetime import datetime
# # import logging

# # logger = logging.getLogger(__name__)

# # class SitemapParser:
# #     """Parse XML sitemaps and extract service/product URLs at specific depths"""
    
# #     def __init__(self):
# #         self.session = requests.Session()
# #         self.session.headers.update({
# #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
# #         })
    
# #     def fetch_sitemap(self, sitemap_url: str) -> List[str]:
# #         """Fetch and parse sitemap XML, return all URLs"""
# #         try:
# #             response = self.session.get(sitemap_url, timeout=15)
# #             response.raise_for_status()
            
# #             # Parse XML
# #             root = ET.fromstring(response.content)
            
# #             # Handle both standard sitemap and sitemap index
# #             urls = []
            
# #             # Check if it's a sitemap index (contains sitemap tags)
# #             if root.find('.//sitemap') is not None:
# #                 # It's a sitemap index - fetch all child sitemaps
# #                 for sitemap in root.findall('.//sitemap'):
# #                     loc = sitemap.find('loc')
# #                     if loc is not None:
# #                         child_urls = self.fetch_sitemap(loc.text)
# #                         urls.extend(child_urls)
# #             else:
# #                 # Standard sitemap
# #                 for url in root.findall('.//url'):
# #                     loc = url.find('loc')
# #                     if loc is not None and loc.text:
# #                         urls.append(loc.text.strip())
            
# #             logger.info(f"Fetched {len(urls)} URLs from {sitemap_url}")
# #             return urls
            
# #         except Exception as e:
# #             logger.error(f"Error fetching sitemap {sitemap_url}: {e}")
# #             return []
    
# #     def filter_urls_by_depth(self, urls: List[str], base_prefix: str, depth_offset: int = 1) -> List[str]:
# #         """
# #         Filter URLs that are exactly 'depth_offset' levels deeper than base_prefix
        
# #         Args:
# #             urls: List of URLs to filter
# #             base_prefix: Base URL to measure depth from
# #             depth_offset: How many levels deeper to target (1 = immediate children)
# #         """
# #         # Parse base path
# #         base_path = urlparse(base_prefix).path.strip('/')
# #         base_segments = [seg for seg in base_path.split('/') if seg]
# #         baseline_count = len(base_segments)
        
# #         filtered_urls = []
# #         for url in urls:
# #             if not url.startswith(base_prefix):
# #                 continue
            
# #             # Parse current path
# #             current_path = urlparse(url).path.strip('/')
# #             current_segments = [seg for seg in current_path.split('/') if seg]
            
# #             # Check if at target depth
# #             if len(current_segments) == baseline_count + depth_offset:
# #                 filtered_urls.append(url)
        
# #         logger.info(f"Filtered {len(filtered_urls)} URLs at depth {depth_offset} from {len(urls)} total")
# #         return filtered_urls
    
# #     def extract_category_name(self, url: str) -> str:
# #         """Extract the category name from URL (last segment)"""
# #         return urlparse(url).path.strip('/').split('/')[-1].replace('-', ' ').title()
    
# #     def get_service_categories(self, company_config: Dict) -> List[Dict]:
# #         """
# #         Get all service/product categories for a company using sitemap
        
# #         Args:
# #             company_config: Company configuration with sitemap_url and base_prefix
# #         """
# #         all_urls = self.fetch_sitemap(company_config['sitemap_url'])
        
# #         if not all_urls:
# #             logger.warning(f"No URLs found for {company_config['name']}")
# #             return []
        
# #         # Filter to get service/product URLs at correct depth
# #         service_urls = self.filter_urls_by_depth(
# #             all_urls,
# #             company_config['base_prefix'],
# #             company_config.get('depth_offset', 1)
# #         )
        
# #         # Extract category names
# #         categories = []
# #         for url in service_urls:
# #             category_name = self.extract_category_name(url)
# #             categories.append({
# #                 'name': category_name,
# #                 'url': url,
# #                 'slug': urlparse(url).path.strip('/').split('/')[-1]
# #             })
        
# #         return categories

# # parsers/sitemap_parser.py (COMPLETE REWRITE)
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urlparse
# from typing import List, Dict, Optional
# import logging
# import re

# logger = logging.getLogger(__name__)

# class SitemapParser:
#     """Enterprise-grade sitemap parser handling namespaces and corporate structures"""
    
#     def __init__(self):
#         self.session = requests.Session()
#         self.session.headers.update({
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.9',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Connection': 'keep-alive',
#             'Upgrade-Insecure-Requests': '1'
#         })
    
#     def fetch_sitemap_urls(self, sitemap_url: str) -> List[str]:
#         """
#         Fetch and parse sitemap, handling XML namespaces properly
#         Returns list of all URLs found
#         """
#         try:
#             logger.info(f"Fetching sitemap: {sitemap_url}")
#             response = self.session.get(sitemap_url, timeout=30)
            
#             if response.status_code != 200:
#                 logger.error(f"Failed to fetch {sitemap_url}: Status {response.status_code}")
#                 return []
            
#             # Check if it's actually XML
#             content_type = response.headers.get('content-type', '')
#             if 'xml' not in content_type and 'text' not in content_type:
#                 logger.warning(f"Unexpected content-type: {content_type}")
            
#             # Parse with BeautifulSoup using xml parser (handles namespaces)
#             soup = BeautifulSoup(response.content, 'xml')
            
#             # Find all <loc> tags regardless of namespace
#             urls = soup.find_all('loc')
            
#             extracted_links = [url.text.strip() for url in urls]
            
#             # Check if it's a sitemap index (has sitemap tags)
#             if soup.find_all('sitemap'):
#                 logger.info(f"Found sitemap index with {len(extracted_links)} sub-sitemaps")
#                 # Recursively fetch all sub-sitemaps
#                 all_links = []
#                 for sub_sitemap_url in extracted_links[:20]:  # Limit to 20 to avoid overload
#                     child_links = self.fetch_sitemap_urls(sub_sitemap_url)
#                     all_links.extend(child_links)
#                 return all_links
            
#             logger.info(f"Extracted {len(extracted_links)} URLs from sitemap")
#             return extracted_links
            
#         except Exception as e:
#             logger.error(f"Error parsing sitemap {sitemap_url}: {e}")
#             return []
    


# parsers/sitemap_parser.py (ENHANCED)
# import requests
# from bs4 import BeautifulSoup
# from typing import List, Dict, Optional
# import logging
# import time
# import random

# logger = logging.getLogger(__name__)

# class SitemapParser:
#     """Enhanced sitemap parser with anti-blocking measures"""
    
#     def __init__(self):
#         self.session = requests.Session()
#         self._setup_headers()
    
#     def _setup_headers(self):
#         """Set up specialized headers for sitemap fetching"""
#         self.session.headers.update({
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             'Accept': 'application/xml,text/xml,text/html,application/xhtml+xml;q=0.9',
#             'Accept-Language': 'en-US,en;q=0.9',
#             'Accept-Encoding': 'gzip, deflate',
#             'Connection': 'keep-alive',
#             'Cache-Control': 'no-cache'
#         })
    
#     def fetch_sitemap_urls(self, sitemap_url: str, max_retries: int = 3) -> List[str]:
#         """Fetch sitemap with robust retry logic"""
#         for attempt in range(max_retries):
#             try:
#                 # Add delay between retries
#                 if attempt > 0:
#                     time.sleep(random.uniform(3, 7))
                
#                 # Try different user agents
#                 if attempt == 1:
#                     self.session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
#                 elif attempt == 2:
#                     self.session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                
#                 response = self.session.get(sitemap_url, timeout=30)
                
#                 if response.status_code == 200:
#                     # Parse with BeautifulSoup
#                     soup = BeautifulSoup(response.content, 'xml')
#                     urls = [url.text.strip() for url in soup.find_all('loc')]
                    
#                     if urls:
#                         logger.info(f"Found {len(urls)} URLs in {sitemap_url}")
#                         return urls
#                     else:
#                         # Try alternative parsing
#                         soup = BeautifulSoup(response.text, 'html.parser')
#                         urls = [url.text.strip() for url in soup.find_all('loc')]
#                         if urls:
#                             return urls
                
#                 logger.warning(f"Attempt {attempt + 1} failed for {sitemap_url}: Status {response.status_code}")
                
#             except Exception as e:
#                 logger.warning(f"Attempt {attempt + 1} failed: {e}")
        
#         logger.error(f"All retries failed for {sitemap_url}")
#         return []

#     def extract_service_urls(self, urls: List[str], company_config: Dict) -> List[Dict]:
#         """
#         Extract service/product URLs based on company-specific patterns
#         """
#         company_code = company_config.get('code', '')
        
#         # Special handlers for specific companies
#         if company_code == 'HCLTECH':
#             return self._extract_hcl_services(urls, company_config)
#         elif company_code == 'WIPRO':
#             return self._extract_wipro_services(urls, company_config)
#         elif company_code == 'OFSS':
#             return self._extract_oracle_services(urls, company_config)
#         else:
#             return self._extract_by_pattern(urls, company_config)
        
    
#     def _extract_by_pattern(self, urls: List[str], company_config: Dict) -> List[Dict]:
#         """Generic extraction using base_prefix and depth_offset"""
#         base_prefix = company_config.get('base_prefix', '')
#         depth_offset = company_config.get('depth_offset', 1)
        
#         if not base_prefix:
#             return []
        
#         # Filter URLs that start with base_prefix
#         matching_urls = [url for url in urls if url.startswith(base_prefix)]
        
#         if not matching_urls:
#             logger.warning(f"No URLs match base_prefix: {base_prefix}")
#             return []
        
#         # Filter by depth
#         base_path = urlparse(base_prefix).path.strip('/')
#         base_segments = [seg for seg in base_path.split('/') if seg]
#         baseline_count = len(base_segments)
        
#         result = []
#         for url in matching_urls:
#             current_path = urlparse(url).path.strip('/')
#             current_segments = [seg for seg in current_path.split('/') if seg]
            
#             # Check depth
#             if len(current_segments) == baseline_count + depth_offset:
#                 # Extract category name from last segment
#                 category_name = current_segments[-1].replace('-', ' ').replace('_', ' ').title()
#                 result.append({
#                     'name': category_name,
#                     'url': url,
#                     'slug': current_segments[-1]
#                 })
        
#         logger.info(f"Extracted {len(result)} service URLs for {company_config['name']}")
#         return result
    
#     def _extract_hcl_services(self, urls: List[str], company_config: Dict) -> List[Dict]:
#         """
#         Special handler for HCLTech - they have messy sitemap but clean HTML on products page
#         """
#         # Look for product platform URLs
#         product_patterns = [
#             r'/products-platforms/',
#             r'/ai-factory',
#             r'/data-ai-foundary',
#             r'/cloud-services'
#         ]
        
#         result = []
#         for url in urls:
#             for pattern in product_patterns:
#                 if re.search(pattern, url):
#                     path = urlparse(url).path.strip('/')
#                     segments = path.split('/')
#                     category_name = segments[-1].replace('-', ' ').title()
#                     result.append({
#                         'name': category_name,
#                         'url': url,
#                         'slug': segments[-1]
#                     })
#                     break
        
#         logger.info(f"HCLTech: Extracted {len(result)} service URLs")
#         return result
    
#     def _extract_wipro_services(self, urls: List[str], company_config: Dict) -> List[Dict]:
#         """
#         Special handler for Wipro - flat structure with category keywords
#         """
#         # Wipro uses top-level categories without /services/ prefix
#         wipro_keywords = [
#             '/engineering/', '/applications/', '/cloud/', '/cybersecurity/',
#             '/ai/', '/data/', '/digital/', '/consulting/'
#         ]
        
#         result = []
#         for url in urls:
#             for keyword in wipro_keywords:
#                 if keyword in url:
#                     # Extract category from URL
#                     path = urlparse(url).path.strip('/')
#                     segments = path.split('/')
#                     if len(segments) >= 1:
#                         category_name = segments[0].replace('-', ' ').title()
#                         result.append({
#                             'name': category_name,
#                             'url': url,
#                             'slug': segments[0]
#                         })
#                     break
        
#         # Remove duplicates
#         unique_results = []
#         seen = set()
#         for item in result:
#             if item['url'] not in seen:
#                 seen.add(item['url'])
#                 unique_results.append(item)
        
#         logger.info(f"Wipro: Extracted {len(unique_results)} service URLs")
#         return unique_results
    
#     def _extract_oracle_services(self, urls: List[str], company_config: Dict) -> List[Dict]:
#         """
#         Special handler for Oracle - deep nested financial services structure
#         """
#         base_prefix = company_config.get('base_prefix', '')
        
#         # Filter for financial services URLs
#         matching_urls = [url for url in urls if base_prefix in url]
        
#         result = []
#         for url in matching_urls:
#             path = urlparse(url).path.strip('/')
#             segments = [seg for seg in path.split('/') if seg]
            
#             # Oracle uses /financial-services/category/sub-category
#             if len(segments) >= 3:
#                 # Take the second level as category
#                 category_name = segments[2].replace('-', ' ').title()
#                 result.append({
#                     'name': category_name,
#                     'url': url,
#                     'slug': segments[2]
#                 })
        
#         logger.info(f"Oracle: Extracted {len(result)} service URLs")
#         return result     
# parsers/sitemap_parser.py (ENHANCED)
import logging
import random
import re
import time
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class SitemapParser:
    """Enhanced sitemap parser with anti-blocking measures"""
    
    def __init__(self):
        self.session = requests.Session()
        self._setup_headers()
    
    def _setup_headers(self):
        """Set up specialized headers for sitemap fetching"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/xml,text/xml,text/html,application/xhtml+xml;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        })
    
    def fetch_sitemap_urls(self, sitemap_url: str, max_retries: int = 3) -> List[str]:
        """Fetch sitemap with robust retry logic"""
        for attempt in range(max_retries):
            try:
                # Add delay between retries
                if attempt > 0:
                    time.sleep(random.uniform(3, 7))
                
                # Try different user agents
                if attempt == 1:
                    self.session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                elif attempt == 2:
                    self.session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                
                response = self.session.get(sitemap_url, timeout=30)
                
                if response.status_code == 200:
                    # Parse with BeautifulSoup
                    soup = BeautifulSoup(response.content, 'xml')
                    urls = [url.text.strip() for url in soup.find_all('loc')]
                    
                    if urls:
                        logger.info(f"Found {len(urls)} URLs in {sitemap_url}")
                        return urls
                    else:
                        # Try alternative parsing
                        soup = BeautifulSoup(response.text, 'html.parser')
                        urls = [url.text.strip() for url in soup.find_all('loc')]
                        if urls:
                            return urls
                
                logger.warning(f"Attempt {attempt + 1} failed for {sitemap_url}: Status {response.status_code}")
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
        
        logger.error(f"All retries failed for {sitemap_url}")
        return []

    # def extract_service_urls(self, urls: List[str], company_config: Dict) -> List[Dict]:
    #     """
    #     Extract service/product URLs based on company-specific patterns
    #     """
    #     company_code = company_config.get('code', '')
        
    #     # Special handlers for specific companies
    #     if company_code == 'HCLTECH':
    #         return self._extract_hcl_services(urls, company_config)
    #     elif company_code == 'WIPRO':
    #         return self._extract_wipro_services(urls, company_config)
    #     elif company_code == 'OFSS':
    #         return self._extract_oracle_services(urls, company_config)
    #     else:
    #         return self._extract_by_pattern(urls, company_config)
    
    
        
    # def _extract_by_pattern(self, urls: List[str], company_config: Dict) -> List[Dict]:
    #     """Generic extraction using base_prefix and depth_offset"""
    #     base_prefix = company_config.get('base_prefix', '')
    #     depth_offset = company_config.get('depth_offset', 1)
        
    #     if not base_prefix:
    #         return []
        
    #     # Filter URLs that start with base_prefix
    #     matching_urls = [url for url in urls if url.startswith(base_prefix)]
        
    #     if not matching_urls:
    #         logger.warning(f"No URLs match base_prefix: {base_prefix}")
    #         return []
        
    #     # Filter by depth
    #     base_path = urlparse(base_prefix).path.strip('/')
    #     base_segments = [seg for seg in base_path.split('/') if seg]
    #     baseline_count = len(base_segments)
        
    #     result = []
    #     for url in matching_urls:
    #         current_path = urlparse(url).path.strip('/')
    #         current_segments = [seg for seg in current_path.split('/') if seg]
            
    #         # Check depth
    #         if len(current_segments) == baseline_count + depth_offset:
    #             # Extract category name from last segment
    #             category_name = current_segments[-1].replace('-', ' ').replace('_', ' ').title()
    #             result.append({
    #                 'name': category_name,
    #                 'url': url,
    #                 'slug': current_segments[-1]
    #             })
        
    #     logger.info(f"Extracted {len(result)} service URLs for {company_config['name']}")
    #     return result
    
# parsers/sitemap_parser.py (FIX extract_service_urls)
    def extract_service_urls(self, urls: List[str], company_config: Dict) -> List[Dict]:
        """
        Extract service/product URLs based on company-specific patterns
        Returns list of dicts with 'name', 'url', 'slug' keys
        """
        company_code = company_config.get('code', '')
        
        # Special handlers for specific companies
        if company_code == 'HCLTECH':
            return self._extract_hcl_services(urls, company_config)
        elif company_code == 'WIPRO':
            return self._extract_wipro_services(urls, company_config)
        elif company_code == 'OFSS':
            return self._extract_oracle_services(urls, company_config)
        else:
            return self._extract_by_pattern(urls, company_config)

    def _extract_by_pattern(self, urls: List[str], company_config: Dict) -> List[Dict]:
        """Generic extraction using base_prefix and depth_offset"""
        base_prefix = company_config.get('base_prefix', '')
        depth_offset = company_config.get('depth_offset', 1)
        
        if not base_prefix:
            return []
        
        # Filter URLs that start with base_prefix
        matching_urls = [url for url in urls if url.startswith(base_prefix)]
        
        if not matching_urls:
            logger.warning(f"No URLs match base_prefix: {base_prefix}")
            return []
        
        # Filter by depth
        base_path = urlparse(base_prefix).path.strip('/')
        base_segments = [seg for seg in base_path.split('/') if seg]
        baseline_count = len(base_segments)
        
        result = []
        for url in matching_urls:
            current_path = urlparse(url).path.strip('/')
            current_segments = [seg for seg in current_path.split('/') if seg]
            
            # Check depth
            if len(current_segments) == baseline_count + depth_offset:
                # Extract category name from last segment
                category_name = current_segments[-1].replace('-', ' ').replace('_', ' ').title()
                if category_name:  # Ensure we have a name
                    result.append({
                        'name': category_name,
                        'url': url,
                        'slug': current_segments[-1]
                    })
        
        logger.info(f"Extracted {len(result)} service URLs for {company_config.get('name', 'Unknown')}")
        return result    
    
    def _extract_hcl_services(self, urls: List[str], company_config: Dict) -> List[Dict]:
        """
        Special handler for HCLTech - they have messy sitemap but clean HTML on products page
        """
        # Look for product platform URLs
        product_patterns = [
            r'/products-platforms/',
            r'/ai-factory',
            r'/data-ai-foundary',
            r'/cloud-services'
        ]
        
        result = []
        for url in urls:
            for pattern in product_patterns:
                if re.search(pattern, url):
                    path = urlparse(url).path.strip('/')
                    segments = path.split('/')
                    category_name = segments[-1].replace('-', ' ').title()
                    result.append({
                        'name': category_name,
                        'url': url,
                        'slug': segments[-1]
                    })
                    break
        
        logger.info(f"HCLTech: Extracted {len(result)} service URLs")
        return result
    
    def _extract_wipro_services(self, urls: List[str], company_config: Dict) -> List[Dict]:
        """
        Special handler for Wipro - flat structure with category keywords
        """
        # Wipro uses top-level categories without /services/ prefix
        wipro_keywords = [
            '/engineering/', '/applications/', '/cloud/', '/cybersecurity/',
            '/ai/', '/data/', '/digital/', '/consulting/'
        ]
        
        result = []
        for url in urls:
            for keyword in wipro_keywords:
                if keyword in url:
                    # Extract category from URL
                    path = urlparse(url).path.strip('/')
                    segments = path.split('/')
                    if len(segments) >= 1:
                        category_name = segments[0].replace('-', ' ').title()
                        result.append({
                            'name': category_name,
                            'url': url,
                            'slug': segments[0]
                        })
                    break
        
        # Remove duplicates
        unique_results = []
        seen = set()
        for item in result:
            if item['url'] not in seen:
                seen.add(item['url'])
                unique_results.append(item)
        
        logger.info(f"Wipro: Extracted {len(unique_results)} service URLs")
        return unique_results
    
    def _extract_oracle_services(self, urls: List[str], company_config: Dict) -> List[Dict]:
        """
        Special handler for Oracle - deep nested financial services structure
        """
        base_prefix = company_config.get('base_prefix', '')
        
        # Filter for financial services URLs
        matching_urls = [url for url in urls if base_prefix in url]
        
        result = []
        for url in matching_urls:
            path = urlparse(url).path.strip('/')
            segments = [seg for seg in path.split('/') if seg]
            
            # Oracle uses /financial-services/category/sub-category
            if len(segments) >= 3:
                # Take the second level as category
                category_name = segments[2].replace('-', ' ').title()
                result.append({
                    'name': category_name,
                    'url': url,
                    'slug': segments[2]
                })
        
        logger.info(f"Oracle: Extracted {len(result)} service URLs")
        return result 

