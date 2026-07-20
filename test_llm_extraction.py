# # test_llm_extraction.py
# from extractors.llm_extractor import LLMExtractor

# def test_llm():
#     print("Testing LLM extraction...")
#     extractor = LLMExtractor(model='llama3.2:3b')  # or 'gemma:2b'
    
#     # Sample text (use real extracted text from previous test)
#     sample_text = """
#     TCS Q1 FY27 Highlights:
#     - Total Contract Value (TCV) of $8.5 billion
#     - Won 12 large deals, including a $125M deal with a US-based bank
#     - Added 3 new clients in the $100M+ revenue bucket
#     - Client base: 1,234 active clients
#     """
    
#     result = extractor.extract_from_text(sample_text, "press_release")
    
#     print("\nExtraction result:")
#     import json
#     print(json.dumps(result, indent=2))
    
#     return result

# if __name__ == "__main__":
#     test_llm()

# test_llm_extraction.py
import os
import sys
sys.path.insert(0, os.getcwd())

from extractors.llm_extractor import LLMExtractor
import json

def test_llm_on_tcs():
    """Test LLM extraction on TCS extracted text"""
    print("=" * 60)
    print("Testing LLM Extraction on TCS Text")
    print("=" * 60)
    
    # Load the extracted text
    text_path = "data/pdfs/TCS_press_release_20260718_extracted.txt"
    
    if not os.path.exists(text_path):
        print(f"❌ Extracted text not found: {text_path}")
        print("Run extract_pdf_text.py first")
        return
    
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"✅ Loaded {len(text)} characters of text")
    
    # Initialize LLM extractor
    print("\n🔧 Initializing LLM Extractor...")
    extractor = LLMExtractor(model='llama3.2:3b')
    
    print("\n🤖 Sending to LLM for extraction...")
    print("   (This may take 10-30 seconds)")
    
    try:
        result = extractor.extract_from_text(text, "press_release")
        
        print("\n" + "=" * 60)
        print("EXTRACTION RESULTS")
        print("=" * 60)
        
        # Deal Wins
        deal_wins = result.get('deal_wins', [])
        print(f"\n📋 Deal Wins Found: {len(deal_wins)}")
        for i, deal in enumerate(deal_wins, 1):
            print(f"\n  {i}. {deal.get('client_description', 'Unknown')}")
            print(f"     Details: {deal.get('deal_details', 'N/A')[:100]}...")
            print(f"     Value: {deal.get('deal_value', 'N/A')}")
            print(f"     Industry: {deal.get('industry', 'N/A')}")
            print(f"     Location: {deal.get('location', 'N/A')}")
        
        # Order Book
        order_book = result.get('order_book', {})
        print(f"\n📊 Order Book:")
        print(f"   Total TCV: {order_book.get('total_tcv', 'N/A')}")
        print(f"   Deal Count: {order_book.get('deal_count', 'N/A')}")
        large_deals = order_book.get('large_deals', [])
        if large_deals:
            print(f"   Large Deals: {', '.join(large_deals)}")
        
        # Client Metrics
        client_metrics = result.get('client_metrics', {})
        print(f"\n👥 Client Metrics:")
        print(f"   Total Clients: {client_metrics.get('total_clients', 'N/A')}")
        print(f"   Distribution: {client_metrics.get('client_distribution', 'N/A')}")
        print(f"   Concentration: {client_metrics.get('concentration', 'N/A')}")
        
        # Save result
        output_path = "output/tcs_llm_extraction.json"
        os.makedirs('output', exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\n💾 Full results saved to: {output_path}")
        
        return result
        
    except Exception as e:
        print(f"❌ LLM extraction failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_with_sample_text():
    """Test LLM with a small sample text"""
    print("=" * 60)
    print("Testing LLM with Sample Text")
    print("=" * 60)
    
    sample_text = """
    TCS Q1 FY27 Highlights:
    - Total Contract Value (TCV) of $9.5 billion
    - US$ 800 million mega deal with SKF
    - Multi-million $ strategic partnership with a Europe-based Fortune Global 50 company
    - US$ 200 million deal with a US-based bank
    - Signed a strategic partnership with a US-based insurance company
    - AI-led business transformation deals worth $1.2 billion
    """
    
    extractor = LLMExtractor(model='llama3.2:3b')
    
    print("Sample text:", sample_text)
    print("\n🤖 Sending to LLM...")
    
    try:
        result = extractor.extract_from_text(sample_text, "press_release")
        
        print("\n✅ Extraction Result:")
        print(json.dumps(result, indent=2, default=str))
        return result
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        return None

if __name__ == "__main__":
    # First test with sample text
    sample_result = test_with_sample_text()
    
    # Then test with actual TCS data
    if sample_result:
        print("\n" + "=" * 60)
        print("Now testing with actual TCS data...")
        print("=" * 60)
        tcs_result = test_llm_on_tcs()