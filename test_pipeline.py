# # # # test_pipeline.py
# # # from pipeline.investor_pipeline import InvestorPipeline
# # # import json

# # # def test_pipeline():
# # #     print("Testing full investor pipeline...")
# # #     pipeline = InvestorPipeline()
    
# # #     # Test with TCS first (most reliable)
# # #     company_code = 'TCS'
# # #     print(f"\nProcessing {company_code}...")
    
# # #     result = pipeline.process_company(company_code)
    
# # #     print(f"\nResults for {company_code}:")
# # #     print(f"  Deal Wins: {len(result.get('deal_wins', []))}")
# # #     print(f"  Order Book: {result.get('order_book', {})}")
# # #     print(f"  Client Metrics: {result.get('client_metrics', {})}")
    
# # #     # Save result
# # #     with open(f'test_{company_code}_result.json', 'w') as f:
# # #         json.dump(result, f, indent=2, default=str)
    
# # #     return result

# # # if __name__ == "__main__":
# # #     test_pipeline()

# # # test_pipeline_simple.py
# # import os
# # import sys
# # sys.path.insert(0, os.getcwd())
# # from typing import Dict, List, Optional

# # from pipeline.investor_pipeline import InvestorPipeline
# # import json

# # def test_simple_pipeline():
# #     """Test the pipeline with simple Docling processor"""
# #     print("=" * 60)
# #     print("Testing Investor Pipeline with Simple Docling")
# #     print("=" * 60)
    
# #     pipeline = InvestorPipeline()
    
# #     # Test with TCS
# #     company_code = 'TCS'
# #     print(f"\nProcessing {company_code}...")
    
# #     try:
# #         result = pipeline.process_company(company_code)
        
# #         print(f"\n✅ Results for {company_code}:")
# #         print(f"  Deal Wins: {len(result.get('deal_wins', []))}")
# #         print(f"  Order Book TCV: {result.get('order_book', {}).get('total_tcv', 'N/A')}")
# #         print(f"  Client Metrics: {result.get('client_metrics', {})}")
        
# #         # Show extracted deal wins if any
# #         if result.get('deal_wins'):
# #             print("\n  Sample Deal Wins:")
# #             for deal in result['deal_wins'][:3]:
# #                 print(f"    - {deal.get('client_description', 'Unknown')}: {deal.get('deal_details', '')[:100]}...")
        
# #         # Save result
# #         with open(f'test_{company_code}_result_simple.json', 'w') as f:
# #             json.dump(result, f, indent=2, default=str)
        
# #         return result
        
# #     except Exception as e:
# #         print(f"❌ Failed: {e}")
# #         import traceback
# #         traceback.print_exc()
# #         return None

# # if __name__ == "__main__":
# #     test_simple_pipeline()

# # test_complete_pipeline.py
# import os
# import sys
# sys.path.insert(0, os.getcwd())

# from pipeline.investor_pipeline import InvestorPipeline
# from extractors.llm_extractor import LLMExtractor
# import json

# def test_complete_pipeline():
#     """Test the complete pipeline from PDF to structured data"""
#     print("=" * 60)
#     print("Complete Pipeline Test")
#     print("=" * 60)
    
#     # Step 1: Run the investor pipeline
#     print("\n📂 Step 1: Running Investor Pipeline...")
#     pipeline = InvestorPipeline()
    
#     company_code = 'TCS'
#     result = pipeline.process_company(company_code)
    
#     print(f"✅ Pipeline completed for {company_code}")
#     print(f"   Deal Wins found: {len(result.get('deal_wins', []))}")
    
#     # Step 2: Check if we have raw data
#     raw_data = result.get('raw_data', {})
#     if not raw_data:
#         print("❌ No raw data extracted")
#         return
    
#     # Step 3: Load the extracted text
#     text_path = "data/pdfs/TCS_press_release_20260718_extracted.txt"
#     if not os.path.exists(text_path):
#         print(f"❌ Extracted text not found: {text_path}")
#         return
    
#     with open(text_path, 'r', encoding='utf-8') as f:
#         text = f.read()
    
#     print(f"✅ Loaded {len(text)} characters of text")
    
#     # Step 4: Run LLM extraction
#     print("\n🤖 Step 2: Running LLM Extraction...")
#     extractor = LLMExtractor(model='llama3.2:3b')
    
#     try:
#         llm_result = extractor.extract_from_text(text, "press_release")
        
#         print("\n" + "=" * 60)
#         print("FINAL RESULTS")
#         print("=" * 60)
        
#         # Compare pipeline result vs LLM result
#         print(f"\n📊 Comparison:")
#         print(f"  Pipeline Deal Wins: {len(result.get('deal_wins', []))}")
#         print(f"  LLM Deal Wins: {len(llm_result.get('deal_wins', []))}")
#         print(f"  Pipeline TCV: {result.get('order_book', {}).get('total_tcv', 'N/A')}")
#         print(f"  LLM TCV: {llm_result.get('order_book', {}).get('total_tcv', 'N/A')}")
        
#         # Save combined results
#         combined_result = {
#             'pipeline_result': result,
#             'llm_result': llm_result
#         }
        
#         output_path = "output/complete_extraction.json"
#         os.makedirs('output', exist_ok=True)
#         with open(output_path, 'w') as f:
#             json.dump(combined_result, f, indent=2, default=str)
        
#         print(f"\n💾 Complete results saved to: {output_path}")
        
#         return combined_result
        
#     except Exception as e:
#         print(f"❌ LLM extraction failed: {e}")
#         return None

# if __name__ == "__main__":
#     # Ensure output directory exists
#     os.makedirs('output', exist_ok=True)
    
#     result = test_complete_pipeline()
    
#     if result:
#         print("\n✅ Complete pipeline test passed!")
#     else:
#         print("\n❌ Complete pipeline test failed!")

# test_pipeline.py (UPDATED)
import os
import sys
sys.path.insert(0, os.getcwd())

from pipeline.investor_pipeline import InvestorPipeline
from extractors.llm_extractor import LLMExtractor
import json

def test_complete_pipeline():
    """Test the complete pipeline from PDF to structured data"""
    print("=" * 60)
    print("Complete Pipeline Test")
    print("=" * 60)
    
    # Step 1: Run the investor pipeline
    print("\n📂 Step 1: Running Investor Pipeline...")
    pipeline = InvestorPipeline()
    
    company_code = 'TCS'
    result = pipeline.process_company(company_code)
    
    print(f"✅ Pipeline completed for {company_code}")
    print(f"   Deal Wins found: {len(result.get('deal_wins', []))}")
    
    # Step 2: Check if we have raw data
    raw_data = result.get('raw_data', {})
    if not raw_data:
        print("❌ No raw data extracted")
        return
    
    # Step 3: Load the extracted text
    text_path = "data/pdfs/TCS_transcript_20260721.md"  # Or the actual extracted file
    
    # Try to find the markdown file
    if not os.path.exists(text_path):
        # Check if there's a text file instead
        text_path = "data/pdfs/TCS_transcript_20260721.txt"
        if not os.path.exists(text_path):
            # Look for any extracted file
            pdf_dir = "data/pdfs"
            for f in os.listdir(pdf_dir):
                if f.startswith("TCS_transcript") and (f.endswith('.md') or f.endswith('.txt')):
                    text_path = os.path.join(pdf_dir, f)
                    break
        
        if not os.path.exists(text_path):
            print(f"⚠️ Extracted text not found: {text_path}")
            print("Using raw data from pipeline...")
            # Use the markdown content from pipeline if available
            if 'transcript' in raw_data and raw_data['transcript'].get('raw_text'):
                text = raw_data['transcript']['raw_text']
            else:
                print("❌ No text available")
                return
    else:
        with open(text_path, 'r', encoding='utf-8') as f:
            text = f.read()
    
    print(f"✅ Loaded {len(text)} characters of text")
    
    # Step 4: Run LLM extraction
    print("\n🤖 Step 2: Running LLM Extraction...")
    extractor = LLMExtractor(model='llama3.2:3b')
    
    try:
        # Use the appropriate extraction method
        if 'transcript' in raw_data:
            llm_result = extractor.extract_from_transcript(text, company_code)
        else:
            llm_result = extractor.extract_from_text(text, "press_release")
        
        print("\n" + "=" * 60)
        print("FINAL RESULTS")
        print("=" * 60)
        
        # Compare pipeline result vs LLM result
        print(f"\n📊 Comparison:")
        print(f"  Pipeline Deal Wins: {len(result.get('deal_wins', []))}")
        print(f"  LLM Deal Wins: {len(llm_result.get('deal_wins', []))}")
        print(f"  Pipeline TCV: {result.get('order_book', {}).get('total_tcv', 'N/A')}")
        print(f"  LLM TCV: {llm_result.get('order_book', {}).get('total_tcv', 'N/A')}")
        
        # Show extracted deal wins
        print("\n📋 Deal Wins from LLM:")
        for i, deal in enumerate(llm_result.get('deal_wins', [])[:5], 1):
            print(f"  {i}. {deal.get('client_description', 'Unknown')}")
            print(f"     Value: {deal.get('deal_value', 'N/A')}")
            print(f"     Industry: {deal.get('industry', 'N/A')}")
        
        # Save combined results
        combined_result = {
            'pipeline_result': result,
            'llm_result': llm_result
        }
        
        output_path = "output/complete_extraction.json"
        os.makedirs('output', exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(combined_result, f, indent=2, default=str)
        
        print(f"\n💾 Complete results saved to: {output_path}")
        
        return combined_result
        
    except Exception as e:
        print(f"❌ LLM extraction failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    
    result = test_complete_pipeline()
    
    if result:
        print("\n✅ Complete pipeline test passed!")
    else:
        print("\n❌ Complete pipeline test failed!")