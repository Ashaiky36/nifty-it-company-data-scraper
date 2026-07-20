# test_all_processors.py
import os
import sys

sys.path.insert(0, os.getcwd())

def test_all_processors():
    """Test all available PDF processors"""
    print("=" * 60)
    print("Testing All PDF Processors")
    print("=" * 60)
    
    # Find a PDF to test
    pdf_dir = "data/pdfs"
    if not os.path.exists(pdf_dir):
        print(f"❌ Directory '{pdf_dir}' not found")
        return
    
    pdfs = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    if not pdfs:
        print("❌ No PDFs found. Run test_pdf_download.py first")
        return
    
    pdf_path = os.path.join(pdf_dir, pdfs[0])
    print(f"Testing with: {os.path.basename(pdf_path)}")
    print("=" * 60)
    
    processors = [
        ("Docling", "processors.docling_processor", "DoclingProcessor"),
        ("Simple Docling", "processors.docling_processor", "SimpleDoclingProcessor"),
        ("PDFPlumber", "processors.pdfplumber_processor", "PDFPlumberProcessor"),
        ("PyPDF2", "processors.pypdf2_processor", "PyPDF2Processor")
    ]
    
    for name, module, class_name in processors:
        print(f"\n{name}:")
        try:
            # Import dynamically
            mod = __import__(module, fromlist=[class_name])
            processor_class = getattr(mod, class_name)
            processor = processor_class()
            
            markdown = processor.process_pdf(pdf_path)
            print(f"  ✅ Success! {len(markdown)} characters extracted")
            print(f"  Sample: {markdown[:100]}...")
        except ImportError as e:
            print(f"  ⚠️ Module not available: {e}")
        except Exception as e:
            print(f"  ❌ Failed: {e}")

if __name__ == "__main__":
    test_all_processors()