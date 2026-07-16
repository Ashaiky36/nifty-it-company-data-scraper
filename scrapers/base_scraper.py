# # # scrapers/base_scraper.py
# # import requests
# # import time
# # import random
# # from typing import Optional, Dict
# # from requests.adapters import HTTPAdapter
# # from urllib3.util.retry import Retry

# # # class BaseScraper:
# # #     """Base scraper with robust session management and retry logic"""
    
# # #     def __init__(self, base_headers: Optional[Dict] = None):
# # #         self.session = self._create_session()
# # #         self.headers = base_headers or {
# # #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
# # #             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# # #             'Accept-Language': 'en-US,en;q=0.9',
# # #             'Accept-Encoding': 'gzip, deflate, br',
# # #             'Connection': 'keep-alive',
# # #             'Upgrade-Insecure-Requests': '1',
# # #             'Sec-Fetch-Dest': 'document',
# # #             'Sec-Fetch-Mode': 'navigate',
# # #             'Sec-Fetch-Site': 'none',
# # #             'Sec-Fetch-User': '?1',
# # #         }
# # # scrapers/base_scraper.py (update headers)
# # class BaseScraper:
# #     def __init__(self):
# #         self.session = requests.Session()
# #         # Enhanced headers to bypass corporate firewalls
# #         self.session.headers.update({
# #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
# #             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
# #             'Accept-Language': 'en-US,en;q=0.9',
# #             'Accept-Encoding': 'gzip, deflate, br',
# #             'Connection': 'keep-alive',
# #             'Upgrade-Insecure-Requests': '1',
# #             'Sec-Fetch-Dest': 'document',
# #             'Sec-Fetch-Mode': 'navigate',
# #             'Sec-Fetch-Site': 'none',
# #             'Sec-Fetch-User': '?1',
# #             'Cache-Control': 'max-age=0',
# #             'Referer': 'https://www.google.com/',
# #         })
        
# #         # Add retry logic
# #         retry_strategy = Retry(
# #             total=3,
# #             backoff_factor=1,
# #             status_forcelist=[403, 429, 500, 502, 503, 504],
# #         )
# #         adapter = HTTPAdapter(max_retries=retry_strategy)
# #         self.session.mount("http://", adapter)
# #         self.session.mount("https://", adapter)

# #     def _create_session(self) -> requests.Session:
# #         """Create session with retry strategy"""
# #         session = requests.Session()
        
# #         # Retry strategy for network issues
# #         retry_strategy = Retry(
# #             total=3,
# #             backoff_factor=1,
# #             status_forcelist=[429, 500, 502, 503, 504],
# #         )
# #         adapter = HTTPAdapter(max_retries=retry_strategy)
# #         session.mount("http://", adapter)
# #         session.mount("https://", adapter)
        
# #         return session
    
# #     def get(self, url: str, headers: Optional[Dict] = None) -> requests.Response:
# #         """Make GET request with throttling and error handling"""
# #         try:
# #             # Random delay to avoid rate limiting
# #             time.sleep(random.uniform(1.5, 3.5))
            
# #             final_headers = {**self.headers, **(headers or {})}
# #             response = self.session.get(url, headers=final_headers, timeout=15)
# #             response.raise_for_status()
# #             return response
            
# #         except requests.exceptions.RequestException as e:
# #             print(f"Request failed for {url}: {e}")
# #             raise

# # scrapers/base_scraper.py (FIXED)
# import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# from typing import Optional, Dict
# import time
# import random

# class BaseScraper:
#     """Base scraper with robust session management and retry logic"""
    
#     def __init__(self):
#         self.session = self._create_session()
#         # Define headers at instance level for reference
#         self.default_headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.9',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Connection': 'keep-alive',
#             'Upgrade-Insecure-Requests': '1',
#             'Sec-Fetch-Dest': 'document',
#             'Sec-Fetch-Mode': 'navigate',
#             'Sec-Fetch-Site': 'none',
#             'Sec-Fetch-User': '?1',
#             'Cache-Control': 'max-age=0',
#             'Referer': 'https://www.google.com/',
#         }
#         self.session.headers.update(self.default_headers)
    
#     def _create_session(self) -> requests.Session:
#         """Create session with retry strategy"""
#         session = requests.Session()
        
#         # Retry strategy for network issues
#         retry_strategy = Retry(
#             total=3,
#             backoff_factor=1,
#             status_forcelist=[429, 500, 502, 503, 504], #removedd 403 from status_forcelist to avoid blocking, since retrying a 403 forbidden is pointless if the the server has deliberately blocked the request.
#             raise_on_status=False
#         )
#         adapter = HTTPAdapter(max_retries=retry_strategy)
#         session.mount("http://", adapter)
#         session.mount("https://", adapter)
        
#         return session
    
#     def get(self, url: str, headers: Optional[Dict] = None) -> requests.Response:
#         """Make GET request with throttling and error handling"""
#         try:
#             # Random delay to avoid rate limiting
#             time.sleep(random.uniform(1.5, 3.5))
            
#             # FIX: Use session.headers instead of self.headers
#             final_headers = {**dict(self.session.headers), **(headers or {})}
            
#             response = self.session.get(url, headers=final_headers, timeout=15)
#             response.raise_for_status()
#             return response
            
#         except requests.exceptions.RequestException as e:
#             print(f"Request failed for {url}: {e}")
#             raise

# scrapers/base_scraper.py (ENHANCED ANTI-BLOCKING) 
#1:34 PM, 15/7/26
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Dict
import time
import random
import logging

logger = logging.getLogger(__name__)

class BaseScraper:
    """Enhanced scraper with anti-blocking measures"""
    
    def __init__(self):
        self.session = self._create_session()
        self._setup_headers()
        self._setup_proxies()  # Optional: add proxy support
        
    def _setup_headers(self):
        """Set up browser-mimicking headers"""
        # Rotate user agents to avoid detection
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Sec-GPC': '1'
        })
        
    # Add a property for backward compatibility
    @property
    def headers(self):
        """Provide backward compatibility for self.headers access"""
        return dict(self.session.headers)
    
    @headers.setter
    def headers(self, value):
        """Allow setting headers via self.headers"""
        if isinstance(value, dict):
            self.session.headers.update(value)     
    
    def _setup_proxies(self):
        """Optional: Configure proxy support"""
        # You can add proxy configuration here if needed
        # self.session.proxies = {...}
        pass
    
    def _create_session(self) -> requests.Session:
        """Create session with retry strategy"""
        session = requests.Session()
        
        # Retry strategy - exclude 403 as it's usually permanent
        retry_strategy = Retry(
            total=2,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],  # Removed 403
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def get(self, url: str, headers: Optional[Dict] = None, max_retries: int = 2) -> requests.Response:
        """Make GET request with throttling and retry logic"""
        for attempt in range(max_retries + 1):
            try:
                # Random delay with jitter
                delay = random.uniform(2.0, 5.0) + (attempt * 1.0)
                time.sleep(delay)
                
                # Rotate user agent on retry
                if attempt > 0:
                    self._rotate_user_agent()
                
                # Build final headers
                final_headers = {**dict(self.session.headers), **(headers or {})}
                
                # Add cookies from a previous session if available
                if not self.session.cookies:
                    self._initialize_cookies(url)
                
                response = self.session.get(url, headers=final_headers, timeout=20)
                
                # Handle 403 with retry
                if response.status_code == 403:
                    logger.warning(f"403 Forbidden for {url} (attempt {attempt + 1})")
                    if attempt < max_retries:
                        # Rotate IP or use different strategy
                        self._rotate_user_agent()
                        continue
                    else:
                        response.raise_for_status()
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                if attempt < max_retries:
                    logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                    continue
                else:
                    logger.error(f"All retries failed for {url}")
                    raise
    
    def _rotate_user_agent(self):
        """Rotate user agent to avoid detection"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        ]
        self.session.headers['User-Agent'] = random.choice(user_agents)
    
    def _initialize_cookies(self, url: str):
        """Initialize cookies by visiting the homepage first"""
        try:
            # Visit the main domain to get cookies
            from urllib.parse import urlparse
            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            self.session.get(base_url, timeout=10)
            logger.info(f"Initialized cookies from {base_url}")
        except:
            pass
    
    def get_with_cookies(self, url: str) -> requests.Response:
        """Get page with cookie initialization"""
        # First get the main page to establish session
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            self.session.get(base_url, timeout=10)
        except:
            pass
        
        # Now get the target URL
        return self.get(url)