# # test_services.py
# from scrapers.service_scraper import ServiceScraper
# from config.companies import NIFTY_IT_COMPANIES

# def test_services():
#     """Test the service scraper on a single company"""
#     scraper = ServiceScraper()
    
#     # Test with TCS
#     tcs = NIFTY_IT_COMPANIES[0]
#     print(f"Testing services for {tcs['name']}...")
#     print(f"Sitemap: {tcs['sitemap_url']}")
#     print(f"Base prefix: {tcs['base_prefix']}")
#     print("-" * 60)
    
#     services = scraper.scrape_company_services(tcs)
    
#     print(f"\n✅ Found {services.get('total_categories', 0)} service categories")
#     print("\nService Categories:")
#     print("-" * 60)
    
#     for idx, category in enumerate(services.get('categories', [])[:10]):
#         print(f"{idx+1}. {category['name']}")
#         if category.get('sub_services'):
#             print(f"   Sub-services: {', '.join(category['sub_services'][:3])}")
#         print(f"   Description: {category.get('description', 'N/A')[:100]}...")
#         print()
    
#     print("\nFormatted for Excel:")
#     print("-" * 60)
#     formatted = scraper.format_services_for_excel(services)
#     print(formatted)
    
#     return services

# if __name__ == "__main__":
#     test_services()

# test_services_complete.py
from scrapers.service_scraper import ServiceScraper
from config.companies import NIFTY_IT_COMPANIES
import json

def test_all_services():
    """Test service extraction for all companies"""
    scraper = ServiceScraper()
    
    for company in NIFTY_IT_COMPANIES:
        print(f"\n{'='*60}")
        print(f"Testing: {company['name']} ({company['code']})")
        print(f"{'='*60}")
        
        services = scraper.scrape_company_services(company)
        
        print(f"Total Categories: {services.get('total_categories', 0)}")
        print(f"Service Type: {services.get('service_type', 'unknown')}")
        
        if services.get('categories'):
            print("\nCategories:")
            for cat in services['categories'][:5]:
                print(f"  • {cat['name']}")
                if cat.get('sub_services'):
                    print(f"    Sub-services: {', '.join(cat['sub_services'][:3])}")
        else:
            print("  No categories found")
        
        # Show formatted output
        formatted = scraper.format_services_for_excel(services)
        print(f"\nFormatted for Excel:\n{formatted[:200]}...")

if __name__ == "__main__":
    test_all_services()