# # test_docling.py
# from processors.docling_processor import DoclingProcessor
# import os

# def test_docling():
#     print("Testing Docling processor...")
#     processor = DoclingProcessor()
    
#     # Use a PDF you already downloaded
#     pdf_path = "data/pdfs/TCS_press_release_20260718.pdf"  # Adjust path as needed
    
#     if not os.path.exists(pdf_path):
#         print(f"PDF not found: {pdf_path}")
#         print("Please run test_pdf_download.py first")
#         return
    
#     try:
#         markdown = processor.process_pdf(pdf_path)
#         print(f"✓ Markdown extracted ({len(markdown)} characters)")
#         print("\nFirst 500 characters:")
#         print(markdown[:500])
#     except Exception as e:
#         print(f"✗ Failed: {e}")

# if __name__ == "__main__":
#     test_docling()

# # test_docling_updated.py
# import os
# import sys

# # Add project root to path
# sys.path.insert(0, os.getcwd())

# def test_processing():
#     """Test both Docling and pdfplumber processors"""
#     print("=" * 60)
#     print("Testing PDF Processing")
#     print("=" * 60)
    
#     # Test with a PDF that exists
#     pdf_path = "data/pdfs/TCS_press_release_20260718.pdf"
    
#     if not os.path.exists(pdf_path):
#         print(f"⚠️ PDF not found: {pdf_path}")
#         print("\nFirst, download a PDF using:")
#         print("python test_pdf_download.py")
#         return
    
#     # Test Docling
#     print("\n1. Testing Docling processor...")
#     try:
#         from processors.docling_processor import DoclingProcessor
#         processor = DoclingProcessor(use_ocr=False)
#         markdown = processor.process_pdf(pdf_path)
#         print(f"✅ Docling succeeded! Extracted {len(markdown)} characters")
#         print(f"Sample: {markdown[:200]}...")
#     except Exception as e:
#         print(f"❌ Docling failed: {e}")
        
#         # Try simplified version
#         try:
#             print("\n   Trying simplified Docling...")
#             from processors.docling_processor import SimpleDoclingProcessor
#             processor = SimpleDoclingProcessor()
#             markdown = processor.process_pdf(pdf_path)
#             print(f"✅ Simple Docling succeeded! Extracted {len(markdown)} characters")
#         except Exception as e2:
#             print(f"❌ Simple Docling also failed: {e2}")
            
#             # Fallback to pdfplumber
#             print("\n2. Trying pdfplumber fallback...")
#             try:
#                 from processors.pdfplumber_processor import PDFPlumberProcessor
#                 processor = PDFPlumberProcessor()
#                 markdown = processor.process_pdf(pdf_path)
#                 print(f"✅ pdfplumber succeeded! Extracted {len(markdown)} characters")
#                 print(f"Sample: {markdown[:200]}...")
#             except Exception as e3:
#                 print(f"❌ pdfplumber also failed: {e3}")

# if __name__ == "__main__":
#     test_processing()

# test_docling_working.py
import os
import sys

# Add project root to path
sys.path.insert(0, os.getcwd())

def test_processing():
    """Test both Docling and pdfplumber processors"""
    print("=" * 60)
    print("Testing PDF Processing")
    print("=" * 60)
    
    # Test with a PDF that exists
    pdf_path = "data/pdfs/TCS_press_release_20260718.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"⚠️ PDF not found: {pdf_path}")
        print("\nChecking available PDFs...")
        pdf_dir = "data/pdfs"
        if os.path.exists(pdf_dir):
            pdfs = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
            if pdfs:
                print(f"Available PDFs:")
                for p in pdfs:
                    print(f"  - {p}")
                pdf_path = os.path.join(pdf_dir, pdfs[0])
                print(f"\nUsing: {pdf_path}")
            else:
                print("No PDFs found. Please download one first:")
                print("python test_pdf_download.py")
                return
        else:
            print(f"Directory '{pdf_dir}' not found")
            return
    
    # Test Docling
    print(f"\n1. Testing Docling processor on: {os.path.basename(pdf_path)}")
    try:
        from processors.docling_processor import DoclingProcessor
        processor = DoclingProcessor(use_ocr=False)
        markdown = processor.process_pdf(pdf_path)
        print(f"✅ Docling succeeded! Extracted {len(markdown)} characters")
        print(f"Sample: {markdown[:200]}...")
    except Exception as e:
        print(f"❌ Docling failed: {e}")
        
        # Try simplified version
        try:
            print("\n   Trying simplified Docling...")
            from processors.docling_processor import SimpleDoclingProcessor
            processor = SimpleDoclingProcessor()
            markdown = processor.process_pdf(pdf_path)
            print(f"✅ Simple Docling succeeded! Extracted {len(markdown)} characters")
        except Exception as e2:
            print(f"❌ Simple Docling also failed: {e2}")
            
            # Fallback to pdfplumber
            print("\n2. Trying pdfplumber fallback...")
            try:
                from processors.pdfplumber_processor import PDFPlumberProcessor
                processor = PDFPlumberProcessor()
                markdown = processor.process_pdf(pdf_path)
                print(f"✅ pdfplumber succeeded! Extracted {len(markdown)} characters")
                print(f"Sample: {markdown[:200]}...")
            except Exception as e3:
                print(f"❌ pdfplumber also failed: {e3}")

if __name__ == "__main__":
    test_processing()