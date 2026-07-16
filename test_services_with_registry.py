# # test_services_with_registry.py
# from scrapers.service_scraper import ServiceScraper
# from config.companies import NIFTY_IT_COMPANIES
# from config.service_registry import COMPANY_SERVICE_REGISTRY
# import json

# def test_services():
#     """Test service extraction with declarative registry"""
#     scraper = ServiceScraper()
    
#     for company in NIFTY_IT_COMPANIES:
#         print(f"\n{'='*60}")
#         print(f"Company: {company['name']} ({company['code']})")
#         print(f"{'='*60}")
        
#         services = scraper.scrape_company_services(company)
        
#         print(f"Strategy: {COMPANY_SERVICE_REGISTRY.get(company['code'], {}).get('strategy', 'unknown')}")
#         print(f"Categories found: {services.get('total_categories', 0)}")
        
#         if services.get('categories'):
#             print("\nTop 5 categories:")
#             for cat in services['categories'][:5]:
#                 print(f"  • {cat['name']}")
#                 if cat.get('sub_services'):
#                     print(f"    Products: {', '.join(cat['sub_services'][:3])}")
        
#         # Show formatted Excel output
#         formatted = scraper.format_services_for_excel(services)
#         print(f"\nFormatted for Excel:\n{formatted[:200]}...")
#         print("-" * 60)

# if __name__ == "__main__":
#     test_services()

# test_services_with_registry.py (FIXED)
from scrapers.service_scraper import ServiceScraper
from config.companies import NIFTY_IT_COMPANIES
from config.service_registry import COMPANY_SERVICE_REGISTRY # 
from config.manual_services import MANUAL_SERVICES
import json

def test_services():
    """Test service extraction with declarative registry"""
    scraper = ServiceScraper()
    
    for company in NIFTY_IT_COMPANIES:
        print(f"\n{'='*60}")
        print(f"Company: {company['name']} ({company['code']})")
        print(f"{'='*60}")
        
        services = scraper.scrape_company_services(company)
        
        # FIX: Use the imported registry
        registry_config = COMPANY_SERVICE_REGISTRY.get(company['code'], {})
        print(f"Strategy: {registry_config.get('strategy', 'unknown')}")
        print(f"Categories found: {services.get('total_categories', 0)}")
        
        if services.get('categories'):
            print("\nTop 5 categories:")
            for cat in services['categories'][:5]:
                print(f"  • {cat['name']}")
                if cat.get('sub_services'):
                    #  Fixed curly brace added before the closing quote
                    print(f"    Products: {', '.join(cat['sub_services'][:3])}")
        
        # Show formatted Excel output
        formatted = scraper.format_services_for_excel(services)
        print(f"\nFormatted for Excel:\n{formatted[:200]}...")
        print("-" * 60)

if __name__ == "__main__":
    test_services()