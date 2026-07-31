# # test_qwen_chunking.py
# import os
# import sys
# sys.path.insert(0, os.getcwd())

# from pipeline.investor_pipeline import InvestorPipeline
# import json

# def test_qwen_extraction():
#     """Test Qwen2.5 with chunking on TCS transcript"""
#     print("=" * 60)
#     print("Testing Qwen2.5 with Chunking")
#     print("=" * 60)
    
#     pipeline = InvestorPipeline()
    
#     # Test with TCS
#     result = pipeline.process_company('TCS')
    
#     print(f"\n✅ Extraction Results:")
#     print(f"  Deal Wins: {len(result.get('deal_wins', []))}")
#     print(f"  Order Book: {result.get('order_book', {})}")
#     print(f"  Client Metrics: {result.get('client_metrics', {})}")
    
#     print("\n📋 Deal Wins:")
#     for i, deal in enumerate(result.get('deal_wins', [])[:5], 1):
#         print(f"\n  {i}. {deal.get('client_description', 'Unknown')}")
#         print(f"     Details: {deal.get('deal_details', 'N/A')[:100]}...")
#         print(f"     Value: {deal.get('deal_value', 'N/A')}")
    
#     # Save result
#     with open('output/tcs_qwen_extraction.json', 'w') as f:
#         json.dump(result, f, indent=2, default=str)
    
#     return result

# if __name__ == "__main__":
#     os.makedirs('output', exist_ok=True)
#     test_qwen_extraction()

# test_qwen_chunking.py (FIXED display)
import os
import sys
sys.path.insert(0, os.getcwd())

from pipeline.investor_pipeline import InvestorPipeline
import json

def test_qwen_extraction():
    """Test Qwen2.5 with chunking on TCS transcript"""
    print("=" * 60)
    print("Testing Qwen2.5 with Chunking")
    print("=" * 60)
    
    pipeline = InvestorPipeline()
    
    # Test with TCS
    result = pipeline.process_company('TCS')
    
    print(f"\n✅ Extraction Results:")
    print(f"  Deal Wins: {len(result.get('deal_wins', []))}")
    print(f"  Order Book: {result.get('order_book', {})}")
    print(f"  Client Metrics: {result.get('client_metrics', {})}")
    
    print("\n📋 Deal Wins:")
    for i, deal in enumerate(result.get('deal_wins', [])[:10], 1):
        client = deal.get('client_description', 'Unknown')
        # Handle None values safely
        details = deal.get('deal_details')
        details_str = details[:100] if details else 'N/A'
        value = deal.get('deal_value', 'N/A')
        
        print(f"\n  {i}. {client}")
        print(f"     Details: {details_str}...")
        print(f"     Value: {value}")
    
    # Save result
    os.makedirs('output', exist_ok=True)
    with open('output/tcs_qwen_extraction.json', 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    return result

if __name__ == "__main__":
    test_qwen_extraction()