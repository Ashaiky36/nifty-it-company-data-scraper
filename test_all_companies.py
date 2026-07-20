# test_all_companies.py
from pipeline.investor_pipeline import InvestorPipeline

def test_limited_companies():
    print("Testing limited set of companies...")
    pipeline = InvestorPipeline()
    
    # Start with companies with known working URLs
    companies = ['TCS', 'INFY', 'TECHM', 'WIPRO']
    
    results = {}
    for company in companies:
        print(f"\n{'='*50}")
        print(f"Processing {company}...")
        print('='*50)
        
        try:
            result = pipeline.process_company(company)
            results[company] = result
            print(f"✓ Completed {company}")
            print(f"  Deal Wins: {len(result.get('deal_wins', []))}")
        except Exception as e:
            print(f"✗ Failed {company}: {e}")
    
    return results

if __name__ == "__main__":
    test_limited_companies()