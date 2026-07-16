# parsers/service_extractor.py
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional, Set
from scrapers.base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)

class ServiceExtractor(BaseScraper):
    """Hybrid service extractor using sitemap, HTML, and special handlers"""
    
    def __init__(self):
        super().__init__()
        self.sitemap_parser = None  # Will be injected
    
    def extract_services(self, company_config: Dict, html_content: str = None) -> Dict:
        """
        Extract services using the best method for each company
        """
        company_code = company_config['code']
        
        # Use company-specific extraction strategy
        if company_code == 'HCLTECH':
            return self._extract_hcl_services(html_content)
        elif company_code == 'TCS':
            return self._extract_tcs_services(html_content)
        elif company_code == 'INFY':
            return self._extract_infy_services(html_content)
        elif company_code == 'WIPRO':
            return self._extract_wipro_services(html_content)
        elif company_code == 'TECHM':
            return self._extract_techm_services(html_content)
        elif company_code == 'PERSISTENT':
            return self._extract_persistent_services(html_content)
        elif company_code == 'COFORGE':
            return self._extract_coforge_services(html_content)
        elif company_code == 'LTIM':
            return self._extract_ltim_services(html_content)
        elif company_code == 'MPHASIS':
            return self._extract_mphasis_services(html_content)
        elif company_code == 'OFSS':
            return self._extract_oracle_services(html_content)
        else:
            return self._extract_generic_services(html_content)
    
    def _extract_hcl_services(self, html_content: str) -> Dict:
        """Extract HCL's structured product offerings from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        products = {}
        
        # Find the "Key Product Offerings" section
        section = soup.find('div', class_='page-title')
        if section and 'Key Product Offerings' in section.get_text():
            # Find all product cards
            cards = soup.find_all('div', class_='gray-card-with-icon-box')
            
            for card in cards:
                # Get category name
                heading = card.find('h3', class_='card-heading-flex')
                if not heading:
                    continue
                
                category = heading.get_text(strip=True)
                
                # Get product list
                ul = card.find('ul')
                if ul:
                    products_list = [li.get_text(strip=True) for li in ul.find_all('li')]
                    products[category] = products_list
                else:
                    # Check for paragraphs (some categories have different structure)
                    p_tags = card.find_all('p')
                    if p_tags:
                        products[category] = [p.get_text(strip=True) for p in p_tags]
        
        return {
            'company': 'HCL Technologies',
            'method': 'html_products_section',
            'categories': products,
            'total_categories': len(products),
            'all_services': self._flatten_services(products)
        }
    
    def _extract_tcs_services(self, html_content: str) -> Dict:
        """Extract TCS services from sitemap or HTML"""
        # TCS has clean sitemap structure we can use
        # But we need to handle the variable depth
        
        # For now, use sitemap approach with proper depth filtering
        return self._extract_from_sitemap_with_depth(
            base_prefix='https://www.tcs.com/what-we-do/services',
            depth_levels=[1, 2]  # Get both /services/cloud and /services/cloud/ai
        )
    
    def _extract_infy_services(self, html_content: str) -> Dict:
        """Extract Infosys services from sitemap"""
        # Infosys has clean /services/ with .html pages
        return self._extract_from_sitemap_with_depth(
            base_prefix='https://www.infosys.com/services',
            depth_levels=[1]
        )
    
    def _extract_wipro_services(self, html_content: str) -> Dict:
        """
        Extract Wipro services - special case since they don't have clear structure
        """
        # Since Wipro doesn't have a clean services structure,
        # we'll use their navigation menu pattern
        soup = BeautifulSoup(html_content, 'html.parser')
        
        services = []
        
        # Look for navigation elements that might contain services
        nav = soup.find('nav')
        if nav:
            # Find all links that might be services
            links = nav.find_all('a')
            for link in links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # Check if it looks like a service
                if href and any(term in href.lower() for term in ['service', 'solution', 'platform']):
                    services.append({
                        'name': text,
                        'url': href
                    })
        
        # Also look for sections that might list services
        service_sections = soup.find_all(['section', 'div'], class_=re.compile(r'service|solution|offering', re.I))
        
        for section in service_sections:
            headings = section.find_all(['h2', 'h3', 'h4'])
            for heading in headings:
                text = heading.get_text(strip=True)
                if len(text) > 5 and len(text) < 100:
                    services.append({
                        'name': text,
                        'url': None
                    })
        
        return {
            'company': 'Wipro',
            'method': 'html_navigation_extraction',
            'services': services[:50],
            'total_services': len(services)
        }
    
    def _extract_techm_services(self, html_content: str) -> Dict:
        """Extract Tech Mahindra services"""
        # TechM has services under /services/ with variable depth
        return self._extract_from_sitemap_with_depth(
            base_prefix='https://www.techmahindra.com/services',
            depth_levels=[1, 2]
        )
    
    def _extract_persistent_services(self, html_content: str) -> Dict:
        """Extract Persistent Systems services"""
        return self._extract_from_sitemap_with_depth(
            base_prefix='https://www.persistent.com/services',
            depth_levels=[2]  # /services/category/sub-service
        )
    
    def _extract_coforge_services(self, html_content: str) -> Dict:
        """Extract Coforge services"""
        return self._extract_from_sitemap_with_depth(
            base_prefix='https://www.coforge.com/capabilities',
            depth_levels=[1, 2]
        )
    
    def _extract_ltim_services(self, html_content: str) -> Dict:
        """Extract LTIMindtree services"""
        return self._extract_from_sitemap_with_depth(
            base_prefix='https://www.ltm.com/services',
            depth_levels=[1, 2]
        )
    
    def _extract_mphasis_services(self, html_content: str) -> Dict:
        """Extract Mphasis services"""
        return self._extract_from_sitemap_with_depth(
            base_prefix='https://www.mphasis.com/home/services',
            depth_levels=[2]  # /home/services/category
        )
    
    def _extract_oracle_services(self, html_content: str) -> Dict:
        """Extract Oracle services"""
        return self._extract_from_sitemap_with_depth(
            base_prefix='https://www.oracle.com/in/financial-services',
            depth_levels=[2, 3]  # Deeper structure
        )
    
    def _extract_from_sitemap_with_depth(self, base_prefix: str, depth_levels: List[int]) -> Dict:
        """
        Generic method to extract from sitemap with multiple depth levels
        This needs to be integrated with the sitemap parser
        """
        # This is a placeholder - actual implementation would use sitemap parser
        return {
            'method': 'sitemap_based',
            'base_prefix': base_prefix,
            'depth_levels': depth_levels,
            'note': 'Needs sitemap parser integration'
        }
    
    def _extract_generic_services(self, html_content: str) -> Dict:
        """Generic fallback extraction from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        services = []
        
        # Look for common service/solution sections
        service_keywords = ['service', 'solution', 'offering', 'capability', 'platform']
        
        for keyword in service_keywords:
            elements = soup.find_all(class_=re.compile(keyword, re.I))
            for elem in elements[:20]:
                text = elem.get_text(strip=True)
                if len(text) > 5 and len(text) < 200:
                    services.append(text)
        
        return {
            'method': 'generic_html',
            'services': list(set(services))[:50],  # Remove duplicates
            'total_services': len(set(services))
        }
    
    def _flatten_services(self, categories: Dict) -> List[str]:
        """Flatten categorized services into a single list"""
        all_services = []
        for category, services in categories.items():
            all_services.extend(services)
        return list(set(all_services))
    
    def format_for_excel(self, extracted_data: Dict) -> str:
        """Format extracted services for Excel cell"""
        if not extracted_data:
            return "No service data available"
        
        result = []
        
        # Handle different extraction methods
        if 'categories' in extracted_data:
            for category, services in extracted_data['categories'].items():
                services_str = ", ".join(services[:5])  # Limit to 5 per category
                result.append(f"{category}: {services_str}")
        
        elif 'services' in extracted_data:
            services = extracted_data['services']
            if isinstance(services, list) and services:
                # If it's a list of dicts
                if isinstance(services[0], dict):
                    for service in services[:20]:
                        if service.get('name'):
                            result.append(service['name'])
                else:
                    # Simple list
                    result.extend(services[:20])
        
        return "\n".join(result)