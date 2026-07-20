# processors/pypdf2_processor.py
import os
import PyPDF2
import logging

logger = logging.getLogger(__name__)

class PyPDF2Processor:
    """Minimal PDF processor using PyPDF2"""
    
    def process_pdf(self, pdf_path: str) -> str:
        """Extract text using PyPDF2"""
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF not found: {pdf_path}")
            
            logger.info(f"Processing PDF with PyPDF2: {pdf_path}")
            
            all_text = []
            
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(reader.pages, 1):
                    text = page.extract_text()
                    if text:
                        all_text.append(f"--- Page {page_num} ---\n{text}")
            
            markdown_content = "\n\n".join(all_text)
            
            # Save markdown for debugging
            markdown_path = pdf_path.replace('.pdf', '.md')
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.info(f"Saved markdown to: {markdown_path}")
            return markdown_content
            
        except Exception as e:
            logger.error(f"Failed to process PDF {pdf_path}: {e}")
            raise