# test_transcript_extraction.py
import os
import sys
sys.path.insert(0, os.getcwd())
from typing import Dict, List, Optional

from pipeline.investor_pipeline import InvestorPipeline
import json

def test_transcript_extraction():
    """Test extraction from Coforge transcript"""
    print("=" * 60)
    print("Testing Transcript Extraction - Coforge")
    print("=" * 60)
    
    pipeline = InvestorPipeline()
    
    # Test Coforge (we have the transcript)
    result = pipeline.process_company('COFORGE')
    
    print(f"\n📊 Extraction Results:")
    print(f"  Deal Wins: {len(result.get('deal_wins', []))}")
    print(f"  TCV: {result.get('order_book', {}).get('total_tcv', 'N/A')}")
    print(f"  Order Book: {result.get('order_book', {}).get('order_book_value', 'N/A')}")
    print(f"  Client Metrics: {result.get('client_metrics', {})}")
    
    print("\n📋 Deal Wins:")
    for i, deal in enumerate(result.get('deal_wins', []), 1):
        print(f"\n  {i}. {deal.get('client_description', 'Unknown')}")
        print(f"     Details: {deal.get('deal_details', 'N/A')[:100]}...")
        print(f"     Value: {deal.get('deal_value', 'N/A')}")
        print(f"     Industry: {deal.get('industry', 'N/A')}")
        print(f"     Location: {deal.get('location', 'N/A')}")
    
    # Save result
    with open('output/coforge_transcript_extraction.json', 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    return result

if __name__ == "__main__":
    os.makedirs('output', exist_ok=True)
    test_transcript_extraction()