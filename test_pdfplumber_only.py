# test_pdfplumber_only.py
import os
import sys
sys.path.insert(0, os.getcwd())

from processors.pdfplumber_processor import PDFPlumberProcessor

def test_pdfplumber():
    """Test pdfplumber on TCS transcript"""
    print("=" * 60)
    print("Testing pdfplumber on TCS Transcript")
    print("=" * 60)
    
    processor = PDFPlumberProcessor()
    
    # Use the downloaded transcript
    pdf_path = "data/pdfs/TCS_transcript_20260721.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        return
    
    try:
        markdown = processor.process_pdf(pdf_path)
        
        print(f"✅ Success! Extracted {len(markdown)} characters")
        print(f"\n📝 First 500 characters:")
        print("-" * 40)
        print(markdown[:500])
        print("-" * 40)
        
        # Save for inspection
        output_path = "output/tcs_transcript_extracted.txt"
        os.makedirs('output', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"\n💾 Full text saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    test_pdfplumber()