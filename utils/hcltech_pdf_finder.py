# utils/hcltech_pdf_finder.py
import requests
from bs4 import BeautifulSoup
import re
import json
import logging

logger = logging.getLogger(__name__)

class HCLTechPDFFinder:
    """Find and download HCLTech PDFs from their dynamic investor relations page"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        })
    
    def get_pdf_links(self, year: str = "2025-26") -> dict:
        """
        Extract PDF links from HCLTech's financial results page
        Returns dict with press_release and presentation links
        """
        base_url = f"https://www.hcltech.com/investor-relations/financial-results?year={year}"
        
        try:
            response = self.session.get(base_url, timeout=30)
            response.raise_for_status()
            
            # Check for JavaScript-rendered content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for PDF links in various formats
            pdf_links = {}
            
            # Method 1: Look for direct PDF links
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.endswith('.pdf'):
                    self._categorize_pdf(href, link.text.strip(), pdf_links)
            
            # Method 2: Look for JSON-LD data
            json_ld = soup.find('script', type='application/ld+json')
            if json_ld and json_ld.string:
                try:
                    data = json.loads(json_ld.string)
                    self._extract_from_json(data, pdf_links)
                except:
                    pass
            
            # Method 3: Look for data attributes or patterns
            for element in soup.find_all(['div', 'section', 'article']):
                # Check for class patterns that might contain PDFs
                classes = element.get('class', [])
                for cls in classes:
                    if 'download' in cls.lower() or 'pdf' in cls.lower() or 'report' in cls.lower():
                        links = element.find_all('a', href=True)
                        for link in links:
                            if '.pdf' in link['href']:
                                self._categorize_pdf(link['href'], link.text.strip(), pdf_links)
            
            # Method 4: Look for pattern in script tags
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    # Look for PDF URLs in JavaScript
                    pdf_matches = re.findall(r'(https?://[^\s"\']+\.pdf)', script.string)
                    for match in pdf_matches:
                        self._categorize_pdf(match, '', pdf_links)
            
            # If no PDFs found, try alternative approach
            if not pdf_links:
                logger.warning("No PDF links found directly, trying alternative approach")
                pdf_links = self._try_alternative_patterns(base_url)
            
            return pdf_links
            
        except Exception as e:
            logger.error(f"Error fetching HCLTech PDFs: {e}")
            return {}
    
    def _categorize_pdf(self, url: str, text: str, pdf_links: dict):
        """Categorize PDF based on URL and link text"""
        url_lower = url.lower()
        text_lower = text.lower()
        
        if 'press' in url_lower or 'release' in url_lower or 'press' in text_lower:
            pdf_links['press_release'] = self._ensure_absolute_url(url)
        elif 'presentation' in url_lower or 'factsheet' in url_lower or 'presentation' in text_lower:
            pdf_links['presentation'] = self._ensure_absolute_url(url)
        elif 'financial' in url_lower or 'results' in url_lower:
            if 'press' not in pdf_links:
                pdf_links['press_release'] = self._ensure_absolute_url(url)
        else:
            # Default to press_release if nothing else
            if 'press_release' not in pdf_links:
                pdf_links['press_release'] = self._ensure_absolute_url(url)
    
    def _ensure_absolute_url(self, url: str) -> str:
        """Ensure URL is absolute"""
        if url.startswith('http'):
            return url
        elif url.startswith('/'):
            return f"https://www.hcltech.com{url}"
        else:
            return f"https://www.hcltech.com/{url}"
    
    def _extract_from_json(self, data, pdf_links):
        """Extract PDFs from JSON-LD data"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and value.endswith('.pdf'):
                    self._categorize_pdf(value, '', pdf_links)
                elif isinstance(value, (dict, list)):
                    self._extract_from_json(value, pdf_links)
        elif isinstance(data, list):
            for item in data:
                self._extract_from_json(item, pdf_links)
    
    def _try_alternative_patterns(self, base_url: str) -> dict:
        """
        Try alternative patterns to find PDFs
        HCLTech often uses predictable URL patterns for their PDFs
        """
        pdf_links = {}
        
        # Common HCLTech PDF URL patterns
        base_domain = "https://www.hcltech.com"
        patterns = [
            f"/sites/default/files/documents/FY25-26/Q4/press_release.pdf",
            f"/sites/default/files/documents/FY25-26/Q4/earnings_presentation.pdf",
            f"/investor-relations/financial-results/pdfs/q4fy26_press_release.pdf",
            f"/investor-relations/financial-results/pdfs/q4fy26_presentation.pdf"
        ]
        
        for pattern in patterns:
            url = f"{base_domain}{pattern}"
            try:
                head_response = self.session.head(url, timeout=10)
                if head_response.status_code == 200:
                    if 'press' in pattern:
                        pdf_links['press_release'] = url
                    elif 'presentation' in pattern:
                        pdf_links['presentation'] = url
            except:
                pass
        
        return pdf_links

# Usage in your pipeline
def get_hcltech_documents():
    """Get HCLTech document URLs"""
    finder = HCLTechPDFFinder()
    links = finder.get_pdf_links(year="2025-26")
    
    # If still no links, use manual fallback
    if not links:
        links = {
            'press_release': 'https://www.hcltech.com/investor-relations/financial-results',  # Will need to scrape page
            'presentation': 'https://www.hcltech.com/investor-relations/financial-results'
        }
    
    return links