# processors/pdfplumber_processor.py
import os
import pdfplumber
import logging

logger = logging.getLogger(__name__)

class PDFPlumberProcessor:
    """Fallback PDF processor using pdfplumber"""
    
    def __init__(self):
        self.text = ""
    
    def process_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF using pdfplumber
        Returns: Plain text with structure preserved
        """
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF not found: {pdf_path}")
            
            logger.info(f"Processing PDF with pdfplumber: {pdf_path}")
            
            all_text = []
            
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text
                    text = page.extract_text()
                    if text:
                        all_text.append(f"--- Page {page_num} ---\n{text}")
                    
                    # Also extract tables if present
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            table_text = self._format_table(table)
                            all_text.append(table_text)
            
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
    
    def _format_table(self, table: list) -> str:
        """Format table as markdown"""
        if not table:
            return ""
        
        # Find headers (first row)
        headers = table[0] if table else []
        
        # Format as markdown table
        result = []
        if headers:
            result.append("| " + " | ".join(str(h) if h else "" for h in headers) + " |")
            result.append("|" + "---|" * len(headers))
            
            # Add data rows
            for row in table[1:]:
                result.append("| " + " | ".join(str(cell) if cell else "" for cell in row) + " |")
        
        return "\n".join(result)