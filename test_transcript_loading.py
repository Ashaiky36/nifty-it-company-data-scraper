# test_transcript_loading.py
import os
import sys
sys.path.insert(0, os.getcwd())

from processors.pdfplumber_processor import PDFPlumberProcessor
from config.investor_docs import INVESTOR_DOCUMENTS
import json

def test_transcript_loading():
    """Test loading and inspecting the transcript"""
    print("=" * 60)
    print("Testing Transcript Loading")
    print("=" * 60)
    
    processor = PDFPlumberProcessor()
    
    # Get TCS transcript URL
    tcs_docs = INVESTOR_DOCUMENTS.get('TCS', {})
    transcript_url = tcs_docs.get('transcript')
    
    if not transcript_url:
        print("❌ No transcript URL found for TCS")
        return
    
    print(f"Transcript URL: {transcript_url}")
    
    # Try to find existing transcript PDF
    pdf_dir = "data/pdfs"
    pdf_files = [f for f in os.listdir(pdf_dir) if f.startswith("TCS_transcript") and f.endswith(".pdf")]
    
    if not pdf_files:
        print("❌ No transcript PDF found in data/pdfs/")
        print("Available PDFs:")
        for f in os.listdir(pdf_dir):
            print(f"  - {f}")
        return
    
    pdf_path = os.path.join(pdf_dir, pdf_files[0])
    print(f"Using PDF: {pdf_path}")
    
    # Process with pdfplumber
    try:
        markdown = processor.process_pdf(pdf_path)
        
        print(f"\n📄 Transcript Stats:")
        print(f"  Total characters: {len(markdown)}")
        print(f"  Total lines: {len(markdown.splitlines())}")
        
        # Check if there's content
        if len(markdown) < 100:
            print("❌ Transcript text is too short - PDF extraction may have failed")
            return
        
        print(f"\n📝 First 500 characters:")
        print("-" * 40)
        print(markdown[:500])
        print("-" * 40)
        
        print(f"\n📝 Last 500 characters:")
        print("-" * 40)
        print(markdown[-500:])
        print("-" * 40)
        
        # Save sample for inspection
        sample_path = "output/transcript_sample.txt"
        os.makedirs('output', exist_ok=True)
        with open(sample_path, 'w', encoding='utf-8') as f:
            f.write(markdown[:2000])
        print(f"\n💾 Sample saved to: {sample_path}")
        
        return markdown
        
    except Exception as e:
        print(f"❌ Error processing transcript: {e}")
        return None

if __name__ == "__main__":
    test_transcript_loading()