
# utils/pdf_downloader.py
import requests
import os
from urllib.parse import urlparse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PDFDownloader:
    """Download and manage investor relations PDFs"""
    
    def __init__(self, download_dir='data/pdfs'):
        self.download_dir = download_dir
        os.makedirs(download_dir, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def download_pdf(self, url: str, company_code: str, doc_type: str = 'press_release') -> str:
        """
        Download PDF and save with structured filename
        Returns: path to downloaded file
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d')
            filename = f"{company_code}_{doc_type}_{timestamp}.pdf"
            filepath = os.path.join(self.download_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Downloaded: {filename}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to download {url}: {e}")
            raise

# # utils/pdf_downloader.py (UPDATED)
# import requests
# import os
# from urllib.parse import urlparse
# from datetime import datetime
# import logging

# logger = logging.getLogger(__name__)

# class PDFDownloader:
#     """Download and manage investor relations PDFs"""
    
#     def __init__(self, download_dir='data/pdfs'):
#         self.download_dir = download_dir
#         os.makedirs(download_dir, exist_ok=True)
#         self.session = requests.Session()
#         self.session.headers.update({
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             'Accept': 'application/pdf,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.9',
#         })
    
#     def download_pdf(self, url: str, company_code: str, doc_type: str = 'press_release') -> str:
#         """
#         Download PDF and save with structured filename
#         Returns: path to downloaded file
#         """
#         try:
#             logger.info(f"Downloading {company_code} {doc_type} from {url}")
            
#             # For HTML pages (like HCLTech), try to find PDF links
#             if url.endswith('.html') or 'financial-results' in url:
#                 return self._download_from_html_page(url, company_code, doc_type)
            
#             # Direct PDF download
#             response = self.session.get(url, timeout=30)
#             response.raise_for_status()
            
#             # Check if it's actually a PDF
#             content_type = response.headers.get('content-type', '')
#             if 'pdf' not in content_type.lower() and not url.endswith('.pdf'):
#                 logger.warning(f"URL may not be a PDF: {url} (Content-Type: {content_type})")
#                 return self._download_from_html_page(url, company_code, doc_type)
            
#             # Generate filename
#             timestamp = datetime.now().strftime('%Y%m%d')
#             filename = f"{company_code}_{doc_type}_{timestamp}.pdf"
#             filepath = os.path.join(self.download_dir, filename)
            
#             with open(filepath, 'wb') as f:
#                 f.write(response.content)
            
#             logger.info(f"Downloaded: {filename} ({len(response.content)} bytes)")
#             return filepath
            
#         except Exception as e:
#             logger.error(f"Failed to download {url}: {e}")
#             raise
    
#     def _download_from_html_page(self, url: str, company_code: str, doc_type: str) -> str:
#         """
#         Try to find and download PDF from an HTML page
#         """
#         from bs4 import BeautifulSoup
#         import re
        
#         try:
#             response = self.session.get(url, timeout=30)
#             response.raise_for_status()
            
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             # Look for PDF links
#             pdf_links = []
#             for link in soup.find_all('a', href=True):
#                 href = link['href']
#                 if href.endswith('.pdf') or '.pdf?' in href:
#                     # Make absolute URL
#                     if href.startswith('/'):
#                         href = f"https://www.{company_code.lower()}.com{href}"
#                     pdf_links.append(href)
            
#             # Look for download buttons
#             for button in soup.find_all(['button', 'a'], class_=re.compile(r'(download|pdf|report|result)', re.I)):
#                 if button.get('href') and '.pdf' in button['href']:
#                     pdf_links.append(button['href'])
            
#             if pdf_links:
#                 # Download the first PDF link
#                 logger.info(f"Found {len(pdf_links)} PDF links, downloading first one")
#                 return self.download_pdf(pdf_links[0], company_code, doc_type)
#             else:
#                 raise Exception(f"No PDF links found on page: {url}")
                
#         except Exception as e:
#             logger.error(f"Failed to find PDF on HTML page {url}: {e}")
#             raise