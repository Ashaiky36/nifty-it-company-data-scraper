# # # scrapers/service_scraper.py (updated)
# # from parsers.sitemap_parser import SitemapParser
# # from scrapers.base_scraper import BaseScraper
# # from bs4 import BeautifulSoup
# # from typing import List, Dict, Optional
# # import re
# # import logging

# # logger = logging.getLogger(__name__)

# # class ServiceScraper(BaseScraper):
# #     """Scrape product and service information from company websites"""
    
# #     def __init__(self):
# #         super().__init__()
# #         self.sitemap_parser = SitemapParser()
    
# #     def scrape_company_services(self, company_config: Dict) -> Dict:
# #         """
# #         Scrape services/products for a company using sitemap approach
# #         """
# #         try:
# #             # Special case for HCLTech - use direct HTML parsing
# #             if company_config['code'] == 'HCLTECH':
# #                 return self._scrape_hcl_direct(company_config)
            
# #             # Fetch all URLs from sitemap
# #             all_urls = self.sitemap_parser.fetch_sitemap_urls(company_config['sitemap_url'])
            
# #             if not all_urls:
# #                 logger.warning(f"No URLs found for {company_config['name']}")
# #                 return self._get_empty_services(company_config['name'])
            
# #             # Extract service URLs using company-specific logic
# #             service_urls = self.sitemap_parser.extract_service_urls(all_urls, company_config)
            
# #             if not service_urls:
# #                 logger.warning(f"No service URLs found for {company_config['name']}")
# #                 return self._get_empty_services(company_config['name'])
            
# #             # For each service URL, get details
# #             services_data = {
# #                 'company': company_config['name'],
# #                 'service_type': company_config.get('service_type', 'services'),
# #                 'categories': [],
# #                 'total_categories': len(service_urls)
# #             }
            
# #             for service in service_urls[:15]:  # Limit to 15 categories
# #                 try:
# #                     category_info = self._scrape_category_page(service, company_config)
# #                     services_data['categories'].append(category_info)
# #                 except Exception as e:
# #                     logger.error(f"Error scraping {service['name']}: {e}")
# #                     services_data['categories'].append({
# #                         'name': service['name'],
# #                         'url': service['url'],
# #                         'description': 'Description not available',
# #                         'sub_services': []
# #                     })
            
# #             return services_data
            
# #         except Exception as e:
# #             logger.error(f"Error scraping services for {company_config['name']}: {e}")
# #             return self._get_empty_services(company_config['name'])
    
# #     def _scrape_hcl_direct(self, company_config: Dict) -> Dict:
# #         """
# #         Special handler for HCLTech - scrape from products-platforms page
# #         """
# #         try:
# #             url = 'https://www.hcltech.com/products-platforms'
# #             response = self.get(url)
# #             soup = BeautifulSoup(response.text, 'html.parser')
            
# #             # Find product cards
# #             cards = soup.find_all('div', class_=re.compile(r'gray-card-with-icon-info'))
            
# #             categories = []
# #             for card in cards[:10]:
# #                 heading = card.find('h3', class_=re.compile(r'card-heading-flex'))
# #                 if heading:
# #                     category_name = heading.text.strip()
                    
# #                     # Extract products from list
# #                     ul = card.find('ul')
# #                     products = []
# #                     if ul:
# #                         products = [li.text.strip() for li in ul.find_all('li')]
                    
# #                     # Also check for paragraphs with links
# #                     paragraphs = card.find_all('p')
# #                     for p in paragraphs:
# #                         links = p.find_all('a')
# #                         for link in links:
# #                             products.append(link.text.strip())
                    
# #                     categories.append({
# #                         'name': category_name,
# #                         'url': url,
# #                         'description': f"HCLTech {category_name} offerings",
# #                         'sub_services': products[:10]  # Limit to 10
# #                     })
            
# #             return {
# #                 'company': company_config['name'],
# #                 'service_type': 'products',
# #                 'categories': categories,
# #                 'total_categories': len(categories)
# #             }
            
# #         except Exception as e:
# #             logger.error(f"Error scraping HCLTech direct: {e}")
# #             return self._get_empty_services(company_config['name'])
    
# #     def _scrape_category_page(self, service: Dict, company_config: Dict) -> Dict:
# #         """Scrape a specific service category page for details"""
# #         try:
# #             response = self.get(service['url'])
# #             soup = BeautifulSoup(response.text, 'html.parser')
            
# #             # Extract description
# #             description = self._extract_description(soup)
            
# #             # Extract sub-services
# #             sub_services = self._extract_sub_services(soup)
            
# #             return {
# #                 'name': service['name'],
# #                 'url': service['url'],
# #                 'description': description,
# #                 'sub_services': sub_services[:5]
# #             }
            
# #         except Exception as e:
# #             logger.error(f"Error scraping {service['url']}: {e}")
# #             return {
# #                 'name': service['name'],
# #                 'url': service['url'],
# #                 'description': 'Error fetching description',
# #                 'sub_services': []
# #             }
    
# #     def _extract_description(self, soup: BeautifulSoup) -> str:
# #         """Extract the main description from a service page"""
# #         # Look for meta description first
# #         meta_desc = soup.find('meta', {'name': 'description'})
# #         if meta_desc and meta_desc.get('content'):
# #             return meta_desc['content'][:500]
        
# #         # Look for first substantial paragraph
# #         paragraphs = soup.find_all('p')
# #         for p in paragraphs:
# #             text = p.get_text(strip=True)
# #             if len(text) > 50 and not text.startswith(('Contact', 'Learn', 'Download')):
# #                 return text[:500]
        
# #         return "No description available"
    
# #     def _extract_sub_services(self, soup: BeautifulSoup) -> List[str]:
# #         """Extract sub-services from the page"""
# #         sub_services = set()
        
# #         # Look for list items
# #         lists = soup.find_all(['ul', 'ol'])
# #         for list_elem in lists:
# #             items = list_elem.find_all('li')
# #             for item in items:
# #                 text = item.get_text(strip=True)
# #                 if 5 < len(text) < 100:
# #                     sub_services.add(text)
        
# #         # Look for headings that might be sub-services
# #         headings = soup.find_all(['h2', 'h3', 'h4'])
# #         for heading in headings:
# #             text = heading.get_text(strip=True)
# #             if 3 < len(text) < 60 and not text.isdigit():
# #                 sub_services.add(text)
        
# #         return list(sub_services)[:10]
    
# #     def _get_empty_services(self, company_name: str) -> Dict:
# #         """Return empty services structure"""
# #         return {
# #             'company': company_name,
# #             'service_type': 'unknown',
# #             'categories': [],
# #             'total_categories': 0,
# #             'error': 'No services found'
# #         }
    
# #     def format_services_for_excel(self, services_data: Dict) -> str:
# #         """Format services data for Excel cell display"""
# #         if not services_data or not services_data.get('categories'):
# #             return "No services data available"
        
# #         result = []
# #         for category in services_data['categories'][:15]:
# #             sub_services_str = ", ".join(category.get('sub_services', [])[:5])
# #             if sub_services_str:
# #                 result.append(f"{category['name']}: {sub_services_str}")
# #             else:
# #                 result.append(category['name'])
        
# #         return "\n".join(result)

# # scrapers/service_scraper.py (updated with all company handlers)
# from parsers.sitemap_parser import SitemapParser
# from scrapers.base_scraper import BaseScraper
# from bs4 import BeautifulSoup
# from typing import List, Dict, Optional
# import re
# import logging

# logger = logging.getLogger(__name__)

# class ServiceScraper(BaseScraper):
#     """Scrape product and service information from company websites"""
    
#     def __init__(self):
#         super().__init__()
#         self.sitemap_parser = SitemapParser()
    
#     def scrape_company_services(self, company_config: Dict) -> Dict:
#         """Main entry point for scraping services"""
#         company_code = company_config.get('code', '')
        
#         # Company-specific handlers
#         if company_code == 'TCS':
#             return self._scrape_tcs_services(company_config)
#         elif company_code == 'INFY':
#             return self._scrape_infosys_services(company_config)
#         elif company_code == 'HCLTECH':
#             return self._scrape_hcl_direct(company_config)
#         elif company_code == 'WIPRO':
#             return self._scrape_wipro_services(company_config)
#         elif company_code == 'OFSS':
#             return self._scrape_oracle_services(company_config)
#         else:
#             return self._scrape_generic_services(company_config)
    
#     def _scrape_tcs_services(self, company_config: Dict) -> Dict:
#         """Special handler for TCS - they block sitemap, use navigation structure"""
#         try:
#             # TCS services are organized under /what-we-do/services/
#             # We'll scrape the main services page
#             url = 'https://www.tcs.com/what-we-do/services'
#             response = self.get(url)
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             categories = []
            
#             # Look for service cards or navigation items
#             # TCS uses various structures, try multiple selectors
#             service_containers = soup.find_all(['div', 'section'], 
#                 class_=re.compile(r'(service|card|nav|menu|offering)', re.I))
            
#             for container in service_containers:
#                 # Find headings that look like service names
#                 headings = container.find_all(['h2', 'h3', 'h4'])
#                 for heading in headings:
#                     text = heading.get_text(strip=True)
#                     if len(text) > 3 and len(text) < 50:
#                         # Check if it's a service category
#                         if any(keyword in text.lower() for keyword in 
#                               ['cloud', 'ai', 'data', 'cyber', 'digital', 'consulting', 
#                                'automation', 'analytics', 'blockchain', 'iot']):
#                             categories.append({
#                                 'name': text,
#                                 'url': url,
#                                 'description': f'TCS {text} services',
#                                 'sub_services': []
#                             })
            
#             # If no categories found, use manual list from sitemap analysis
#             if not categories:
#                 tcs_services = [
#                     'Cloud', 'Artificial Intelligence', 'Cybersecurity', 'Data & Analytics',
#                     'Digital Transformation', 'Consulting', 'Automation', 'Blockchain',
#                     'IoT', 'Application Development', 'Enterprise Solutions'
#                 ]
#                 categories = [{
#                     'name': service,
#                     'url': url,
#                     'description': f'TCS {service} services',
#                     'sub_services': []
#                 } for service in tcs_services]
            
#             return {
#                 'company': company_config['name'],
#                 'service_type': 'services',
#                 'categories': categories,
#                 'total_categories': len(categories)
#             }
            
#         except Exception as e:
#             logger.error(f"Error scraping TCS services: {e}")
#             return self._get_empty_services(company_config['name'])
    
#     def _scrape_infosys_services(self, company_config: Dict) -> Dict:
#         """Special handler for Infosys - they block sitemap"""
#         try:
#             # Infosys services are under /services/
#             url = 'https://www.infosys.com/services/'
#             response = self.get(url)
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             categories = []
            
#             # Look for service cards or navigation
#             service_elements = soup.find_all(['div', 'li', 'a'], 
#                 class_=re.compile(r'(service|card|nav|menu|offering|tile)', re.I))
            
#             seen = set()
#             for elem in service_elements:
#                 # Check if it's a link to a service
#                 link = elem.find('a')
#                 if link and link.get('href'):
#                     href = link['href']
#                     if '/services/' in href and not href.endswith('/'):
#                         name = link.get_text(strip=True)
#                         if name and len(name) > 3 and len(name) < 60:
#                             if name not in seen:
#                                 seen.add(name)
#                                 categories.append({
#                                     'name': name,
#                                     'url': url + href.lstrip('/'),
#                                     'description': f'Infosys {name}',
#                                     'sub_services': []
#                                 })
            
#             # Fallback if no categories found
#             if not categories:
#                 infosys_services = [
#                     'Application Development', 'Cloud Services', 'Data & Analytics',
#                     'Digital Experience', 'Enterprise Solutions', 'Cybersecurity',
#                     'AI & Automation', 'Blockchain', 'IoT', 'Consulting'
#                 ]
#                 categories = [{
#                     'name': service,
#                     'url': url,
#                     'description': f'Infosys {service}',
#                     'sub_services': []
#                 } for service in infosys_services]
            
#             return {
#                 'company': company_config['name'],
#                 'service_type': 'services',
#                 'categories': categories,
#                 'total_categories': len(categories)
#             }
            
#         except Exception as e:
#             logger.error(f"Error scraping Infosys services: {e}")
#             return self._get_empty_services(company_config['name'])
    
#     def _scrape_hcl_direct(self, company_config: Dict) -> Dict:
#         """Special handler for HCLTech - clean HTML on products page"""
#         try:
#             url = 'https://www.hcltech.com/products-platforms'
#             response = self.get(url)
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             categories = []
            
#             # Find product cards
#             cards = soup.find_all('div', class_=re.compile(r'gray-card-with-icon-info'))
            
#             for card in cards[:15]:
#                 heading = card.find('h3', class_=re.compile(r'card-heading-flex'))
#                 if heading:
#                     category_name = heading.text.strip()
                    
#                     # Extract products from list
#                     ul = card.find('ul')
#                     products = []
#                     if ul:
#                         products = [li.text.strip() for li in ul.find_all('li')]
                    
#                     # Also check for paragraphs with links
#                     paragraphs = card.find_all('p')
#                     for p in paragraphs:
#                         links = p.find_all('a')
#                         for link in links:
#                             text = link.text.strip()
#                             if text and len(text) > 3:
#                                 products.append(text)
                    
#                     categories.append({
#                         'name': category_name,
#                         'url': url,
#                         'description': f"HCLTech {category_name} offerings",
#                         'sub_services': products[:10]
#                     })
            
#             return {
#                 'company': company_config['name'],
#                 'service_type': 'products',
#                 'categories': categories,
#                 'total_categories': len(categories)
#             }
            
#         except Exception as e:
#             logger.error(f"Error scraping HCLTech: {e}")
#             return self._get_empty_services(company_config['name'])
    
#     def _scrape_wipro_services(self, company_config: Dict) -> Dict:
#         """Special handler for Wipro - filter and categorize URLs"""
#         try:
#             # Fetch sitemap
#             all_urls = self.sitemap_parser.fetch_sitemap_urls(company_config['sitemap_url'])
            
#             if not all_urls:
#                 return self._get_empty_services(company_config['name'])
            
#             # Define Wipro's main service categories (from navigation)
#             wipro_categories = {
#                 'Consulting': ['/consulting/'],
#                 'Cloud': ['/cloud/'],
#                 'Cybersecurity': ['/cybersecurity/'],
#                 'Data & Analytics': ['/data/', '/analytics/'],
#                 'AI & Automation': ['/ai/', '/automation/'],
#                 'Digital': ['/digital/'],
#                 'Applications': ['/applications/'],
#                 'Engineering': ['/engineering/'],
#                 'IoT': ['/iot/'],
#                 'Blockchain': ['/blockchain/']
#             }
            
#             # Group URLs by category
#             categorized_urls = {}
#             for url in all_urls:
#                 for category, keywords in wipro_categories.items():
#                     if any(keyword in url for keyword in keywords):
#                         if category not in categorized_urls:
#                             categorized_urls[category] = []
#                         categorized_urls[category].append(url)
#                         break
            
#             # Build categories
#             categories = []
#             for category, urls in categorized_urls.items():
#                 # Get the main page for this category if exists
#                 main_url = None
#                 for url in urls:
#                     # Look for the root category URL (without sub-pages)
#                     if url.endswith('/') and url.count('/') <= 4:
#                         main_url = url
#                         break
                
#                 if not main_url and urls:
#                     main_url = urls[0]
                
#                 categories.append({
#                     'name': category,
#                     'url': main_url or f'https://www.wipro.com/{category.lower()}/',
#                     'description': f'Wipro {category} services',
#                     'sub_services': [url.split('/')[-2] if url.endswith('/') else url.split('/')[-1] 
#                                    for url in urls[:5]]
#                 })
            
#             return {
#                 'company': company_config['name'],
#                 'service_type': 'services',
#                 'categories': categories,
#                 'total_categories': len(categories)
#             }
            
#         except Exception as e:
#             logger.error(f"Error scraping Wipro: {e}")
#             return self._get_empty_services(company_config['name'])
    
#     def _scrape_oracle_services(self, company_config: Dict) -> Dict:
#         """Special handler for Oracle - financial services categories"""
#         try:
#             # Oracle has many sub-categories under financial-services
#             # Use sitemap to extract categories
#             all_urls = self.sitemap_parser.fetch_sitemap_urls(company_config['sitemap_url'])
            
#             if not all_urls:
#                 return self._get_empty_services(company_config['name'])
            
#             # Filter for financial services URLs
#             fin_services = [url for url in all_urls if '/financial-services/' in url]
            
#             # Extract categories (second level after financial-services)
#             categories = {}
#             for url in fin_services:
#                 parts = url.split('/financial-services/')
#                 if len(parts) > 1:
#                     path_parts = parts[1].split('/')
#                     if len(path_parts) > 1:
#                         category = path_parts[0].replace('-', ' ').title()
#                         if category not in categories:
#                             categories[category] = []
#                         categories[category].append(url)
            
#             result_categories = []
#             for category, urls in categories.items():
#                 result_categories.append({
#                     'name': category,
#                     'url': f'https://www.oracle.com/in/financial-services/{category.lower().replace(" ", "-")}/',
#                     'description': f'Oracle Financial Services - {category}',
#                     'sub_services': [url.split('/')[-2] if url.endswith('/') else url.split('/')[-1] 
#                                    for url in urls[:5]]
#                 })
            
#             return {
#                 'company': company_config['name'],
#                 'service_type': 'solutions',
#                 'categories': result_categories[:20],
#                 'total_categories': len(result_categories)
#             }
            
#         except Exception as e:
#             logger.error(f"Error scraping Oracle: {e}")
#             return self._get_empty_services(company_config['name'])
    
#     def _scrape_generic_services(self, company_config: Dict) -> Dict:
#         """Generic handler for companies with good sitemap structure"""
#         try:
#             all_urls = self.sitemap_parser.fetch_sitemap_urls(company_config['sitemap_url'])
            
#             if not all_urls:
#                 return self._get_empty_services(company_config['name'])
            
#             service_urls = self.sitemap_parser.extract_service_urls(all_urls, company_config)
            
#             if not service_urls:
#                 return self._get_empty_services(company_config['name'])
            
#             categories = []
#             for service in service_urls[:15]:
#                 categories.append({
#                     'name': service['name'],
#                     'url': service['url'],
#                     'description': f"{company_config['name']} {service['name']}",
#                     'sub_services': []
#                 })
            
#             return {
#                 'company': company_config['name'],
#                 'service_type': company_config.get('service_type', 'services'),
#                 'categories': categories,
#                 'total_categories': len(categories)
#             }
            
#         except Exception as e:
#             logger.error(f"Error scraping {company_config['name']}: {e}")
#             return self._get_empty_services(company_config['name'])
    
#     def _get_empty_services(self, company_name: str) -> Dict:
#         """Return empty services structure"""
#         return {
#             'company': company_name,
#             'service_type': 'unknown',
#             'categories': [],
#             'total_categories': 0,
#             'error': 'No services found'
#         }
    
#     def format_services_for_excel(self, services_data: Dict) -> str:
#         """Format services data for Excel cell display"""
#         if not services_data or not services_data.get('categories'):
#             return "No services data available"
        
#         result = []
#         for category in services_data['categories'][:15]:
#             sub_services = category.get('sub_services', [])
#             if sub_services:
#                 sub_str = ", ".join(sub_services[:5])
#                 result.append(f"{category['name']}: {sub_str}")
#             else:
#                 result.append(category['name'])
        
#         return "\n".join(result)

# scrapers/service_scraper.py (REFACTORED)
from parsers.sitemap_parser import SitemapParser
from scrapers.base_scraper import BaseScraper
from config.service_registry import COMPANY_SERVICE_REGISTRY
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
import logging
from config.manual_services import MANUAL_SERVICES


logger = logging.getLogger(__name__)

class ServiceScraper(BaseScraper):
    """Scrape product and service information using declarative configuration"""
    
    def __init__(self):
        super().__init__()
        self.sitemap_parser = SitemapParser()
    
    def scrape_company_services(self, company_config: Dict) -> Dict:
        """Main entry point using registry-based strategy"""
        company_code = company_config.get('code', '')
        
        # Get registry configuration
        registry = COMPANY_SERVICE_REGISTRY.get(company_code, {})
        strategy = registry.get('strategy', 'sitemap')
        
        # Route to appropriate handler
        if strategy == 'direct_dom':
            return self._scrape_direct_dom(company_config, registry)
        elif strategy == 'wipro_special':
            return self._scrape_wipro_services(company_config, registry)
        elif strategy == 'oracle_special':
            return self._scrape_oracle_services(company_config, registry)
        elif strategy == 'sitemap_fallback':
            return self._scrape_with_fallback(company_config, registry)
        else:  # 'sitemap'
            return self._scrape_generic_sitemap(company_config, registry)
        
    def _scrape_direct_dom(self, company_config: Dict, registry: Dict) -> Dict:
        """Direct DOM scraping with explicit selectors (HCLTech)"""
        try:
            target_url = registry.get('target_url')
            selectors = registry.get('selectors', {})
            
            response = self.get(target_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            categories = []
            
            # Use scoped CSS selectors if available
            container_selector = selectors.get('container')
            if container_selector:
                containers = soup.select(container_selector)
                
                for container in containers[:15]:
                    # Extract heading
                    heading_selector = selectors.get('heading')
                    heading = container.select_one(heading_selector) if heading_selector else None
                    
                    if heading:
                        category_name = heading.get_text(strip=True)
                        
                        # Extract list items
                        products = []
                        ul = container.find('ul')
                        if ul:
                            items = ul.find_all('li')
                            products = [li.get_text(strip=True) for li in items if li.get_text(strip=True)]
                        
                        # Also check for paragraph links
                        paragraphs = container.find_all('p')
                        for p in paragraphs:
                            links = p.find_all('a')
                            for link in links:
                                text = link.get_text(strip=True)
                                if text and len(text) > 3 and text not in products:
                                    products.append(text)
                        
                        if category_name and products:  # Only add if has products
                            categories.append({
                                'name': category_name,
                                'url': target_url,
                                'description': f"{company_config['name']} {category_name}",
                                'sub_services': products[:10]
                            })
            
            # If no categories found with selectors, try alternative extraction
            if not categories:
                categories = self._extract_hcl_alternative(soup, target_url, company_config)
            
            return {
                'company': company_config['name'],
                'service_type': registry.get('service_type', 'products'),
                'categories': categories,
                'total_categories': len(categories)
            }
            
        except Exception as e:
            logger.error(f"Error in direct DOM scraping: {e}")
            return self._get_empty_services(company_config['name'])
        
    def _extract_hcl_alternative(self, soup, target_url, company_config):
        """Alternative extraction for HCLTech if main method fails"""
        categories = []
        
        # Look for any section with products
        product_sections = soup.find_all(['div', 'section'], class_=re.compile(r'(product|offering|solution)', re.I))
        
        for section in product_sections[:10]:
            # Find headings
            heading = section.find(['h2', 'h3', 'h4'])
            if heading:
                name = heading.get_text(strip=True)
                # Find lists
                ul = section.find('ul')
                products = []
                if ul:
                    products = [li.get_text(strip=True) for li in ul.find_all('li')]
                
                if name and products:
                    categories.append({
                        'name': name,
                        'url': target_url,
                        'description': f"HCLTech {name}",
                        'sub_services': products[:10]
                    })
        
        return categories        
        
    
    # def _scrape_direct_dom(self, company_config: Dict, registry: Dict) -> Dict:
    #     """Direct DOM scraping with explicit selectors (HCLTech)"""
    #     try:
    #         target_url = registry.get('target_url')
    #         selectors = registry.get('selectors', {})
            
    #         response = self.get(target_url)
    #         soup = BeautifulSoup(response.text, 'html.parser')
            
    #         categories = []
            
    #         # Use scoped CSS selectors if available
    #         container_selector = selectors.get('container')
    #         if container_selector:
    #             # Find all containers
    #             containers = soup.select(container_selector)
                
    #             for container in containers[:15]:
    #                 # Extract heading
    #                 heading_selector = selectors.get('heading')
    #                 heading = container.select_one(heading_selector) if heading_selector else None
                    
    #                 if heading:
    #                     category_name = heading.get_text(strip=True)
                        
    #                     # Extract list items with scoped selector
    #                     products = []
                        
    #                     # Check if ul has specific class
    #                     list_class = selectors.get('list_class')
    #                     if list_class:
    #                         ul = container.find('ul', class_=list_class)
    #                     else:
    #                         ul = container.find('ul')  # First ul in container
                        
    #                     if ul:
    #                         # Extract list items
    #                         items = ul.find_all('li')
    #                         products = [li.get_text(strip=True) for li in items if li.get_text(strip=True)]
                        
    #                     # Also check for paragraph links (as seen in HCLTech)
    #                     paragraphs = container.find_all('p')
    #                     for p in paragraphs:
    #                         links = p.find_all('a')
    #                         for link in links:
    #                             text = link.get_text(strip=True)
    #                             if text and len(text) > 3 and text not in products:
    #                                 products.append(text)
                        
    #                     if category_name:
    #                         categories.append({
    #                             'name': category_name,
    #                             'url': target_url,
    #                             'description': f"{company_config['name']} {category_name}",
    #                             'sub_services': products[:10]
    #                         })
            
    #         return {
    #             'company': company_config['name'],
    #             'service_type': registry.get('service_type', 'products'),
    #             'categories': categories,
    #             'total_categories': len(categories)
    #         }
            
    #     except Exception as e:
    #         logger.error(f"Error in direct DOM scraping: {e}")
    #         return self._get_empty_services(company_config['name'])
    
    # def _scrape_with_fallback(self, company_config: Dict, registry: Dict) -> Dict:
    #     """Try sitemap first, fallback to page scraping (TCS, Infosys)"""
    #     # First try sitemap approach
    #     result = self._scrape_generic_sitemap(company_config, registry)
        
    #     # If no categories found, use fallback
    #     if not result.get('categories'):
    #         logger.info(f"Sitemap failed for {company_config['name']}, using fallback")
    #         return self._scrape_fallback_page(company_config, registry)
        
        # return result

    def _scrape_with_fallback(self, company_config: Dict, registry: Dict) -> Dict:
        """Try sitemap first, fallback to page scraping, then manual mapping"""
        
        # First try sitemap approach
        result = self._scrape_generic_sitemap(company_config, registry)
        
        # If no categories found, use fallback
        if not result.get('categories'):
            logger.info(f"Sitemap failed for {company_config['name']}, using fallback")
            result = self._scrape_fallback_page(company_config, registry)
        
        # If still no categories, use manual mapping
        if not result.get('categories'):
            company_code = company_config.get('code', '')
            if company_code in MANUAL_SERVICES:
                logger.info(f"Using manual service mapping for {company_config['name']}")
                manual_services = MANUAL_SERVICES[company_code]
                categories = []
                for service in manual_services.get('services', []):
                    categories.append({
                        'name': service['name'],
                        'url': f"https://www.{company_config['name'].lower().replace(' ', '')}.com",
                        'description': f"{company_config['name']} {service['name']} services",
                        'sub_services': service.get('sub_services', [])
                    })
                result['categories'] = categories
                result['total_categories'] = len(categories)
        
        return result    
    
    def _scrape_fallback_page(self, company_config: Dict, registry: Dict) -> Dict:
        """Scrape fallback page when sitemap fails"""
        try:
            fallback_url = registry.get('fallback_url')
            fallback_selectors = registry.get('fallback_selectors', {})
            
            response = self.get(fallback_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            categories = []
            seen = set()
            
            # Look for container elements
            container_tags = fallback_selectors.get('container', ['div', 'li', 'a'])
            class_pattern = fallback_selectors.get('class_pattern', r'(service|card|nav|menu)')
            
            for tag in container_tags:
                elements = soup.find_all(tag, class_=re.compile(class_pattern, re.I))
                
                for elem in elements:
                    # Try to find links
                    link = elem.find('a')
                    if link:
                        href = link.get('href', '')
                        # Check if it's a service link
                        if fallback_selectors.get('link_pattern') in href:
                            name = link.get_text(strip=True)
                            if name and len(name) > 3 and len(name) < 60 and name not in seen:
                                seen.add(name)
                                categories.append({
                                    'name': name,
                                    'url': href if href.startswith('http') else fallback_url.rstrip('/') + href,
                                    'description': f"{company_config['name']} {name}",
                                    'sub_services': []
                                })
            
            # If still no categories, use keywords from registry
            if not categories:
                keywords = fallback_selectors.get('keywords', [])
                for keyword in keywords:
                    category_name = keyword.title()
                    categories.append({
                        'name': category_name,
                        'url': fallback_url,
                        'description': f"{company_config['name']} {category_name}",
                        'sub_services': []
                    })
            
            return {
                'company': company_config['name'],
                'service_type': registry.get('service_type', 'services'),
                'categories': categories[:15],
                'total_categories': len(categories)
            }
            
        except Exception as e:
            logger.error(f"Error in fallback scraping: {e}")
            return self._get_empty_services(company_config['name'])
    
    def _scrape_wipro_services(self, company_config: Dict, registry: Dict) -> Dict:
        """Special handler for Wipro using registry categories"""
        try:
            all_urls = self.sitemap_parser.fetch_sitemap_urls(registry['sitemap_url'])
            
            if not all_urls:
                return self._get_empty_services(company_config['name'])
            
            categories_map = registry.get('categories', {})
            categorized_urls = {}
            
            for url in all_urls:
                for category, keywords in categories_map.items():
                    if any(keyword in url for keyword in keywords):
                        if category not in categorized_urls:
                            categorized_urls[category] = []
                        categorized_urls[category].append(url)
                        break
            
            categories = []
            for category, urls in categorized_urls.items():
                # Find main category page
                main_url = None
                for url in urls:
                    if url.endswith('/') and url.count('/') <= 4:
                        main_url = url
                        break
                
                if not main_url and urls:
                    main_url = urls[0]
                
                # Extract sub-services from URLs
                sub_services = []
                for url in urls[:5]:
                    parts = url.rstrip('/').split('/')
                    if parts:
                        sub = parts[-1].replace('-', ' ').title()
                        if sub and sub not in ['Wipro', 'Services']:
                            sub_services.append(sub)
                
                categories.append({
                    'name': category,
                    'url': main_url or f'https://www.wipro.com/{category.lower()}/',
                    'description': f'Wipro {category} services',
                    'sub_services': sub_services[:5]
                })
            
            return {
                'company': company_config['name'],
                'service_type': registry.get('service_type', 'services'),
                'categories': categories,
                'total_categories': len(categories)
            }
            
        except Exception as e:
            logger.error(f"Error scraping Wipro: {e}")
            return self._get_empty_services(company_config['name'])
    
    # def _scrape_generic_sitemap(self, company_config: Dict, registry: Dict) -> Dict:
    #     """Generic sitemap-based extraction"""
    #     try:
    #         all_urls = self.sitemap_parser.fetch_sitemap_urls(registry['sitemap_url'])
            
    #         if not all_urls:
    #             return self._get_empty_services(company_config['name'])
            
    #         service_urls = self.sitemap_parser.extract_service_urls(
    #             all_urls, 
    #             {
    #                 'base_prefix': registry.get('base_prefix', ''),
    #                 'depth_offset': registry.get('depth_offset', 1)
    #             }
    #         )
            
    #         if not service_urls:
    #             return self._get_empty_services(company_config['name'])
            
    #         categories = []
    #         for service in service_urls[:15]:
    #             categories.append({
    #                 'name': service['name'],
    #                 'url': service['url'],
    #                 'description': f"{company_config['name']} {service['name']}",
    #                 'sub_services': []
    #             })
            
    #         return {
    #             'company': company_config['name'],
    #             'service_type': registry.get('service_type', 'services'),
    #             'categories': categories,
    #             'total_categories': len(categories)
    #         }
            
    #     except Exception as e:
    #         logger.error(f"Error in generic sitemap scraping: {e}")
    #         return self._get_empty_services(company_config['name'])
    
# scrapers/service_scraper.py (FIX _scrape_generic_sitemap)
    def _scrape_generic_sitemap(self, company_config: Dict, registry: Dict) -> Dict:
        """Generic sitemap-based extraction"""
        try:
            all_urls = self.sitemap_parser.fetch_sitemap_urls(registry.get('sitemap_url'))
            
            if not all_urls:
                logger.warning(f"No URLs found for {company_config['name']}")
                return self._get_empty_services(company_config['name'])
            
            # Get service URLs with proper config
            service_config = {
                'code': company_config.get('code'),
                'name': company_config.get('name'),
                'base_prefix': registry.get('base_prefix', ''),
                'depth_offset': registry.get('depth_offset', 1)
            }
            
            service_urls = self.sitemap_parser.extract_service_urls(all_urls, service_config)
            
            if not service_urls:
                logger.warning(f"No service URLs found for {company_config['name']}")
                return self._get_empty_services(company_config['name'])
            
            # Build categories from service URLs
            categories = []
            for service in service_urls[:15]:
                # Ensure service has 'name' key
                if 'name' in service:
                    categories.append({
                        'name': service['name'],
                        'url': service.get('url', ''),
                        'description': f"{company_config['name']} {service['name']}",
                        'sub_services': []
                    })
                else:
                    # Fallback: use slug or url as name
                    name = service.get('slug', service.get('url', 'Unknown')).replace('-', ' ').title()
                    categories.append({
                        'name': name,
                        'url': service.get('url', ''),
                        'description': f"{company_config['name']} {name}",
                        'sub_services': []
                    })
            
            return {
                'company': company_config['name'],
                'service_type': registry.get('service_type', 'services'),
                'categories': categories,
                'total_categories': len(categories)
            }
            
        except Exception as e:
            logger.error(f"Error in generic sitemap scraping: {e}")
            return self._get_empty_services(company_config['name'])
        
    def _get_empty_services(self, company_name: str) -> Dict:
        """Return empty services structure"""
        return {
            'company': company_name,
            'service_type': 'unknown',
            'categories': [],
            'total_categories': 0,
            'error': 'No services found'
        }
    
    def format_services_for_excel(self, services_data: Dict) -> str:
        """Format services data for Excel cell display"""
        if not services_data or not services_data.get('categories'):
            return "No services data available"
        
        result = []
        for category in services_data['categories'][:15]:
            sub_services = category.get('sub_services', [])
            if sub_services:
                sub_str = ", ".join(sub_services[:5])
                result.append(f"{category['name']}: {sub_str}")
            else:
                result.append(category['name'])
        
        return "\n".join(result)
    
    # scrapers/service_scraper.py (ADD ORACLE HANDLER)
    def _scrape_oracle_services(self, company_config: Dict, registry: Dict) -> Dict:
        """Special handler for Oracle Financial Services"""
        try:
            all_urls = self.sitemap_parser.fetch_sitemap_urls(registry['sitemap_url'])
            
            if not all_urls:
                return self._get_empty_services(company_config['name'])
            
            # Filter for financial services URLs
            fin_services = [url for url in all_urls if '/financial-services/' in url]
            
            # Extract categories (second level after financial-services)
            categories_dict = {}
            for url in fin_services:
                parts = url.split('/financial-services/')
                if len(parts) > 1:
                    path_parts = parts[1].split('/')
                    if len(path_parts) > 1:
                        category = path_parts[0].replace('-', ' ').title()
                        if category not in categories_dict:
                            categories_dict[category] = []
                        categories_dict[category].append(url)
            
            categories = []
            for category, urls in categories_dict.items():
                # Get sub-services from URLs
                sub_services = []
                for url in urls[:5]:
                    sub = url.rstrip('/').split('/')[-1].replace('-', ' ').title()
                    if sub and sub.lower() != category.lower():
                        sub_services.append(sub)
                
                categories.append({
                    'name': category,
                    'url': f'https://www.oracle.com/in/financial-services/{category.lower().replace(" ", "-")}/',
                    'description': f'Oracle Financial Services - {category}',
                    'sub_services': sub_services[:5]
                })
            
            return {
                'company': company_config['name'],
                'service_type': registry.get('service_type', 'solutions'),
                'categories': categories[:20],
                'total_categories': len(categories)
            }
            
        except Exception as e:
            logger.error(f"Error scraping Oracle: {e}")
            return self._get_empty_services(company_config['name'])