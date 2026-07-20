# extract_pdf_text.py
import os
import sys
sys.path.insert(0, os.getcwd())

def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract text from PDF using multiple methods, pick the best result
    """
    print(f"Extracting text from: {pdf_path}")
    
    methods = []
    
    # Method 1: Try Simple Docling
    try:
        from processors.docling_processor import SimpleDoclingProcessor
        processor = SimpleDoclingProcessor()
        text = processor.process_pdf(pdf_path)
        if len(text) > 100:
            methods.append(('docling', text))
            print(f"✅ Docling: {len(text)} characters")
    except Exception as e:
        print(f"❌ Docling failed: {e}")
    
    # Method 2: Try PDFPlumber
    try:
        from processors.pdfplumber_processor import PDFPlumberProcessor
        processor = PDFPlumberProcessor()
        text = processor.process_pdf(pdf_path)
        if len(text) > 100:
            methods.append(('pdfplumber', text))
            print(f"✅ PDFPlumber: {len(text)} characters")
    except Exception as e:
        print(f"❌ PDFPlumber failed: {e}")
    
    # Method 3: Try PyPDF2
    try:
        import PyPDF2
        text = []
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        text = "\n\n".join(text)
        if len(text) > 100:
            methods.append(('pypdf2', text))
            print(f"✅ PyPDF2: {len(text)} characters")
    except Exception as e:
        print(f"❌ PyPDF2 failed: {e}")
    
    if not methods:
        raise Exception("No extraction method worked")
    
    # Choose the method with most text
    best_method, best_text = max(methods, key=lambda x: len(x[1]))
    print(f"\n📊 Best method: {best_method} with {len(best_text)} characters")
    
    return best_text

if __name__ == "__main__":
    pdf_path = "data/pdfs/TCS_press_release_20260718.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"PDF not found: {pdf_path}")
        print("Available PDFs:")
        pdf_dir = "data/pdfs"
        if os.path.exists(pdf_dir):
            for f in os.listdir(pdf_dir):
                if f.endswith('.pdf'):
                    print(f"  - {f}")
        sys.exit(1)
    
    try:
        text = extract_pdf_text(pdf_path)
        print(f"\n📝 Sample extracted text:\n{'-'*40}")
        print(text[:500] + "...")
        
        # Save extracted text
        output_path = pdf_path.replace('.pdf', '_extracted.txt')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"\n💾 Full text saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")