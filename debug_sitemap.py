# debug_sitemap.py (updated)
from parsers.sitemap_parser import SitemapParser
from config.companies import NIFTY_IT_COMPANIES
import json

def debug_company(company):
    """Debug a single company's sitemap"""
    print(f"\n{'='*60}")
    print(f"Debugging: {company['name']} ({company['code']})")
    print(f"Sitemap: {company['sitemap_url']}")
    print(f"Base Prefix: {company['base_prefix']}")
    print(f"{'='*60}")
    
    parser = SitemapParser()
    
    # Fetch URLs
    all_urls = parser.fetch_sitemap_urls(company['sitemap_url'])
    
    if not all_urls:
        print("❌ No URLs found! Check sitemap URL.")
        return
    
    print(f"✅ Found {len(all_urls)} total URLs")
    
    # Extract service URLs
    service_urls = parser.extract_service_urls(all_urls, company)
    
    if not service_urls:
        print(f"❌ No service URLs extracted for {company['code']}")
        print("Sample URLs from sitemap (first 10):")
        for url in all_urls[:10]:
            print(f"  {url}")
    else:
        print(f"✅ Extracted {len(service_urls)} service URLs")
        print("\nSample service URLs:")
        for svc in service_urls[:10]:
            print(f"  • {svc['name']}: {svc['url']}")

if __name__ == "__main__":
    for company in NIFTY_IT_COMPANIES:
        debug_company(company)