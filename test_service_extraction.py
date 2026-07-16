# test_service_extraction.py
from scrapers.service_scraper import ServiceScraper
from config.companies import NIFTY_IT_COMPANIES

def test_specific_company(code):
    """Test extraction for a specific company"""
    scraper = ServiceScraper()
    
    company = next((c for c in NIFTY_IT_COMPANIES if c['code'] == code), None)
    if not company:
        print(f"Company {code} not found")
        return
    
    print(f"\n{'='*60}")
    print(f"Testing extraction for {company['name']}")
    print(f"Method: {company.get('extraction_method', 'default')}")
    print(f"{'='*60}")
    
    result = scraper.scrape_company_services(company)
    
    print(f"\n✅ Extraction completed using: {result.get('method', 'unknown')}")
    print(f"Total services found: {result.get('total_services', 0)}")
    
    # Show sample
    print("\nSample services:")
    if 'categories' in result:
        for category, services in list(result['categories'].items())[:3]:
            print(f"  {category}: {', '.join(services[:3])}")
    elif 'services' in result:
        for service in result['services'][:5]:
            if isinstance(service, dict):
                print(f"  {service.get('name', 'Unknown')}")
            else:
                print(f"  {service}")
    
    # Show formatted Excel cell
    print("\nFormatted for Excel:")
    print("-" * 60)
    formatted = scraper.format_services_for_excel(result)
    print(formatted[:500] + "..." if len(formatted) > 500 else formatted)

if __name__ == "__main__":
    # Test HCL first (since it has clean HTML)
    print("Testing HCL Technologies (HTML extraction)...")
    test_specific_company('HCLTECH')
    
    print("\n" + "="*60)
    print("Testing TCS (sitemap extraction)...")
    test_specific_company('TCS')