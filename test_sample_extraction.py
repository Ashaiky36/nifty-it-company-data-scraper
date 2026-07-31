# test_sample_extraction.py
import os
import sys
sys.path.insert(0, os.getcwd())

from extractors.llm_extractor import LLMExtractor

def test_sample():
    """Test extraction on a small sample text"""
    print("Testing sample extraction...")
    
    extractor = LLMExtractor(model='qwen2.5:3b-instruct')
    
    sample_text = """
    TCS Q1 FY27 Highlights:
    - Total Contract Value (TCV) of $9.5 billion
    - Won 12 large deals, including a $125M deal with a US-based bank
    - Added 3 new clients in the $100M+ revenue bucket
    - Client base: 1,234 active clients
    """
    
    result = extractor.extract_from_transcript(sample_text, "TCS")
    
    print(f"\nResult:")
    print(f"  Deal Wins: {len(result.get('deal_wins', []))}")
    print(f"  Order Book: {result.get('order_book', {})}")
    print(f"  Client Metrics: {result.get('client_metrics', {})}")
    
    return result

if __name__ == "__main__":
    test_sample()