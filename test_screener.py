# test_screener.py
import sys
import os
import traceback
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.getcwd())

from scrapers.screener_scraper import ScreenerScraper
from config.companies import NIFTY_IT_COMPANIES

def test_parser():
    """Test the parser with a single company"""
    print("=" * 60)
    print("Testing Screener.in Scraper")
    print("=" * 60)
    
    try:
        scraper = ScreenerScraper()
        
        # Test with TCS (first company in list)
        tcs = NIFTY_IT_COMPANIES[0]
        print(f"\n📊 Testing with {tcs['name']} ({tcs['code']})...")
        print(f"URL: {tcs['screener_url']}")
        print("-" * 60)
        
        # Time the request
        import time
        start_time = time.time()
        
        result = scraper.scrape_company(tcs['name'], tcs['code'], tcs['screener_url'])
        
        elapsed_time = time.time() - start_time
        
        print(f"\n✅ Success! (Completed in {elapsed_time:.2f} seconds)")
        
        # Print results in a formatted way
        print("\n📈 COMPANY SUMMARY")
        print("=" * 60)
        print(f"Company Name: {result['company_name']}")
        print(f"Ticker: {result['company_code']}")
        print(f"Current Quarter Revenue: ₹{result['current_quarter_revenue']:,.2f} Cr")
        print(f"Annual Revenue: ₹{result['annual_revenue']:,.2f} Cr")
        print(f"Annual Profit: ₹{result['annual_profit']:,.2f} Cr")
        print(f"Financial Year: {result['financial_year']}")
        print(f"Total Quarters Available: {result['total_quarters']}")
        print(f"Upcoming Result Date: {result['upcoming_result'] or 'Not available'}")
        
        print("\n📊 LAST 3 QUARTERS SUMMARY")
        print("-" * 60)
        print(result['last_3_quarters_summary'])
        
        print("\n📅 QUARTERLY DATA")
        print("-" * 60)
        print(f"{'Quarter':<12} {'Revenue (Cr)':>15} {'Profit (Cr)':>15}")
        print("-" * 60)
        
        # Display quarterly data
        for label, revenue, profit in zip(
            result['quarterly_labels'],
            result['quarterly_sales'],
            result['quarterly_profits'] + [None] * (len(result['quarterly_labels']) - len(result['quarterly_profits']))
        ):
            rev_str = f"₹{revenue:,.2f}" if revenue else "N/A"
            profit_str = f"₹{profit:,.2f}" if profit else "N/A"
            print(f"{label:<12} {rev_str:>15} {profit_str:>15}")
        
        print("\n" + "=" * 60)
        print("✅ Test completed successfully!")
        return result
        
    except Exception as e:
        print(f"\n❌ Error occurred:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        return None

def test_all_companies():
    """Test scraping all companies (limited to first 3 for testing)"""
    print("\n" + "=" * 60)
    print("Testing All Companies (First 3)")
    print("=" * 60)
    
    try:
        scraper = ScreenerScraper()
        results = []
        
        # Test first 3 companies
        for company in NIFTY_IT_COMPANIES[:3]:
            print(f"\n📊 Scraping {company['name']}...")
            try:
                result = scraper.scrape_company(company['name'], company['code'], company['screener_url'])
                if result and result['current_quarter_revenue']:
                    results.append(result)
                    print(f"  ✅ Revenue: ₹{result['current_quarter_revenue']:,.2f} Cr")
                else:
                    print(f"  ⚠️  No data found")
            except Exception as e:
                print(f"  ❌ Error: {str(e)[:100]}")
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Successfully scraped: {len(results)}/{len(NIFTY_IT_COMPANIES[:3])} companies")
        if results:
            print("\nRevenue comparison:")
            for result in results:
                print(f"  {result['company_name']:30} ₹{result['current_quarter_revenue']:>12,.2f} Cr")
        
        return results
        
    except Exception as e:
        print(f"\n❌ Error in test: {e}")
        traceback.print_exc()
        return []

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("NIFTY IT SCRAPER - TEST RUN")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Run test
    result = test_parser()
    
    if result:
        print("\n💡 Next steps:")
        print("1. If successful, run main.py to scrape all 10 companies")
        print("2. Check the output folder for the Excel file")
        print("3. Verify the data looks correct")
        print("\nRun: python main.py")
    else:
        print("\n❌ Test failed. Please check:")
        print("1. Internet connection")
        print("2. Screener.in URL is accessible")
        print("3. HTML structure hasn't changed")
        
    print("\n" + "=" * 60)
    print("Test completed")
    print("=" * 60)