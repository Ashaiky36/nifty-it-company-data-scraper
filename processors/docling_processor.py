# # processors/docling_processor.py
# import os
# from docling.document_converter import DocumentConverter
# from docling.pipeline.simple_pipeline import SimplePipeline
# from docling.datamodel.pipeline_options import PdfPipelineOptions
# import logging

# logger = logging.getLogger(__name__)

# class DoclingProcessor:
#     """Process PDFs using Docling for markdown extraction"""
    
#     def __init__(self):
#         self.converter = DocumentConverter()
#         self.pipeline_options = PdfPipelineOptions()
#         self.pipeline_options.do_ocr = True  # Enable OCR for scanned docs
#         self.pipeline_options.do_table_structure = True  # Extract tables
#         self.converter = DocumentConverter(
#             format_options={
#                 "pdf": self.pipeline_options
#             }
#         )
    
#     def process_pdf(self, pdf_path: str) -> str:
#         """
#         Convert PDF to markdown with preserved structure
#         Returns: Markdown string
#         """
#         try:
#             logger.info(f"Processing PDF: {pdf_path}")
            
#             # Convert PDF
#             result = self.converter.convert(pdf_path)
            
#             # Extract markdown
#             markdown_content = result.document.export_to_markdown()
            
#             # Save markdown for debugging
#             markdown_path = pdf_path.replace('.pdf', '.md')
#             with open(markdown_path, 'w', encoding='utf-8') as f:
#                 f.write(markdown_content)
            
#             logger.info(f"Saved markdown to: {markdown_path}")
#             return markdown_content
            
#         except Exception as e:
#             logger.error(f"Failed to process PDF {pdf_path}: {e}")
#             raise

# # processors/docling_processor.py (UPDATED)
# import os
# from docling.document_converter import DocumentConverter
# from docling.datamodel.pipeline_options import PdfPipelineOptions
# from docling.datamodel.base_models import InputFormat
# from docling.backend.pypdfium2_backend import PyPdfium2Backend
# import logging

# logger = logging.getLogger(__name__)

# class DoclingProcessor:
#     """Process PDFs using Docling for markdown extraction"""
    
#     def __init__(self, use_ocr: bool = True):
#         self.use_ocr = use_ocr
        
#         # Configure pipeline options
#         self.pipeline_options = PdfPipelineOptions()
        
#         # New: Set the backend explicitly
#         self.pipeline_options.backend = PyPdfium2Backend  # This is the correct way
        
#         # Enable OCR if needed
#         if use_ocr:
#             self.pipeline_options.do_ocr = True
#             self.pipeline_options.ocr_options.lang = ["eng"]
        
#         # Enable table extraction
#         self.pipeline_options.do_table_structure = True
        
#         # Create converter with options
#         self.converter = DocumentConverter(
#             format_options={
#                 InputFormat.PDF: self.pipeline_options
#             }
#         )
    
#     def process_pdf(self, pdf_path: str) -> str:
#         """
#         Convert PDF to markdown with preserved structure
#         Returns: Markdown string
#         """
#         try:
#             if not os.path.exists(pdf_path):
#                 raise FileNotFoundError(f"PDF not found: {pdf_path}")
            
#             logger.info(f"Processing PDF: {pdf_path}")
            
#             # Convert PDF
#             result = self.converter.convert(pdf_path)
            
#             # Extract markdown
#             markdown_content = result.document.export_to_markdown()
            
#             # Save markdown for debugging
#             markdown_path = pdf_path.replace('.pdf', '.md')
#             with open(markdown_path, 'w', encoding='utf-8') as f:
#                 f.write(markdown_content)
            
#             logger.info(f"Saved markdown to: {markdown_path}")
#             return markdown_content
            
#         except Exception as e:
#             logger.error(f"Failed to process PDF {pdf_path}: {e}")
#             raise

# # Alternative: Simplified Version if the above fails
# class SimpleDoclingProcessor:
#     """Simplified Docling processor with minimal options"""
    
#     def __init__(self):
#         self.converter = DocumentConverter()
    
#     def process_pdf(self, pdf_path: str) -> str:
#         """
#         Convert PDF to markdown with default settings
#         """
#         try:
#             if not os.path.exists(pdf_path):
#                 raise FileNotFoundError(f"PDF not found: {pdf_path}")
            
#             logger.info(f"Processing PDF: {pdf_path}")
            
#             # Convert PDF with default settings
#             result = self.converter.convert(pdf_path)
            
#             # Extract markdown
#             markdown_content = result.document.export_to_markdown()
            
#             # Save markdown for debugging
#             markdown_path = pdf_path.replace('.pdf', '.md')
#             with open(markdown_path, 'w', encoding='utf-8') as f:
#                 f.write(markdown_content)
            
#             logger.info(f"Saved markdown to: {markdown_path}")
#             return markdown_content
            
#         except Exception as e:
#             logger.error(f"Failed to process PDF {pdf_path}: {e}")
#             raise

# # processors/docling_processor.py (FIXED)
# import os
# from docling.document_converter import DocumentConverter
# from docling.datamodel.pipeline_options import PdfPipelineOptions
# from docling.datamodel.base_models import InputFormat
# import logging

# logger = logging.getLogger(__name__)

# class DoclingProcessor:
#     """Process PDFs using Docling for markdown extraction"""
    
#     def __init__(self, use_ocr: bool = True):
#         self.use_ocr = use_ocr
        
#         # Configure pipeline options
#         self.pipeline_options = PdfPipelineOptions()
        
#         # Enable OCR if needed
#         if use_ocr:
#             self.pipeline_options.do_ocr = True
#             self.pipeline_options.ocr_options.lang = ["eng"]
        
#         # Enable table extraction
#         self.pipeline_options.do_table_structure = True
        
#         # Create converter with options
#         self.converter = DocumentConverter(
#             format_options={
#                 InputFormat.PDF: self.pipeline_options
#             }
#         )
    
#     def process_pdf(self, pdf_path: str) -> str:
#         """
#         Convert PDF to markdown with preserved structure
#         Returns: Markdown string
#         """
#         try:
#             if not os.path.exists(pdf_path):
#                 raise FileNotFoundError(f"PDF not found: {pdf_path}")
            
#             logger.info(f"Processing PDF: {pdf_path}")
            
#             # Convert PDF
#             result = self.converter.convert(pdf_path)
            
#             # Extract markdown
#             markdown_content = result.document.export_to_markdown()
            
#             # Save markdown for debugging
#             markdown_path = pdf_path.replace('.pdf', '.md')
#             with open(markdown_path, 'w', encoding='utf-8') as f:
#                 f.write(markdown_content)
            
#             logger.info(f"Saved markdown to: {markdown_path}")
#             return markdown_content
            
#         except Exception as e:
#             logger.error(f"Failed to process PDF {pdf_path}: {e}")
#             raise

# # Simplified version without OCR options
# class SimpleDoclingProcessor:
#     """Simplified Docling processor with default settings"""
    
#     def __init__(self):
#         self.converter = DocumentConverter()
    
#     def process_pdf(self, pdf_path: str) -> str:
#         """Convert PDF to markdown with default settings"""
#         try:
#             if not os.path.exists(pdf_path):
#                 raise FileNotFoundError(f"PDF not found: {pdf_path}")
            
#             logger.info(f"Processing PDF: {pdf_path}")
            
#             # Convert PDF with default settings
#             result = self.converter.convert(pdf_path)
            
#             # Extract markdown
#             markdown_content = result.document.export_to_markdown()
            
#             # Save markdown for debugging
#             markdown_path = pdf_path.replace('.pdf', '.md')
#             with open(markdown_path, 'w', encoding='utf-8') as f:
#                 f.write(markdown_content)
            
#             logger.info(f"Saved markdown to: {markdown_path}")
#             return markdown_content
            
#         except Exception as e:
#             logger.error(f"Failed to process PDF {pdf_path}: {e}")
#             raise

# processors/docling_processor.py (OPTIMIZED)
import os
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
import logging

logger = logging.getLogger(__name__)

class DoclingProcessor:
    """Process PDFs using Docling with memory optimization"""
    
    def __init__(self, use_ocr: bool = False):  # OCR disabled by default to save memory
        self.use_ocr = use_ocr
        
        # Configure pipeline options - minimal to save memory
        self.pipeline_options = PdfPipelineOptions()
        
        # Enable OCR only if explicitly requested and memory available
        if use_ocr:
            self.pipeline_options.do_ocr = True
            self.pipeline_options.ocr_options.lang = ["eng"]
        else:
            self.pipeline_options.do_ocr = False
        
        # Enable table extraction (important for financial data)
        self.pipeline_options.do_table_structure = True
        
        # Disable heavy features to save memory
        self.pipeline_options.do_ocr = False  # Force disable OCR
        self.pipeline_options.do_image_extraction = False
        
        # Create converter with options
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: self.pipeline_options
            }
        )
    
    def process_pdf(self, pdf_path: str, max_pages: int = None) -> str:
        """
        Convert PDF to markdown with memory optimization
        Args:
            pdf_path: Path to PDF file
            max_pages: Max pages to process (for large PDFs)
        """
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF not found: {pdf_path}")
            
            logger.info(f"Processing PDF: {pdf_path}")
            
            # Convert PDF with memory limits
            result = self.converter.convert(pdf_path)
            
            # If max_pages specified, limit the content
            if max_pages and hasattr(result.document, 'pages'):
                pages = result.document.pages[:max_pages]
                # Reconstruct document with limited pages (simplified)
            
            # Extract markdown
            markdown_content = result.document.export_to_markdown()
            
            # Save markdown for debugging
            markdown_path = pdf_path.replace('.pdf', '.md')
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.info(f"Saved markdown to: {markdown_path}")
            return markdown_content
            
        except MemoryError:
            logger.warning(f"Memory error processing {pdf_path}, falling back to pdfplumber")
            return self._fallback_to_pdfplumber(pdf_path)
        except Exception as e:
            logger.error(f"Failed to process PDF {pdf_path}: {e}")
            return self._fallback_to_pdfplumber(pdf_path)
    
    def _fallback_to_pdfplumber(self, pdf_path: str) -> str:
        """Fallback to pdfplumber when Docling fails"""
        try:
            from processors.pdfplumber_processor import PDFPlumberProcessor
            processor = PDFPlumberProcessor()
            return processor.process_pdf(pdf_path)
        except Exception as e:
            logger.error(f"Fallback also failed: {e}")
            raise

# Simplified processor with no options (most memory efficient)
class SimpleDoclingProcessor:
    """Simplified Docling processor with minimal memory footprint"""
    
    def __init__(self):
        self.converter = DocumentConverter()
    
    def process_pdf(self, pdf_path: str) -> str:
        """Convert PDF to markdown with default settings"""
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF not found: {pdf_path}")
            
            logger.info(f"Processing PDF: {pdf_path}")
            
            # Convert PDF with default settings
            result = self.converter.convert(pdf_path)
            
            # Extract markdown
            markdown_content = result.document.export_to_markdown()
            
            # Save markdown for debugging
            markdown_path = pdf_path.replace('.pdf', '.md')
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.info(f"Saved markdown to: {markdown_path}")
            return markdown_content
            
        except MemoryError:
            logger.warning(f"Memory error processing {pdf_path}")
            # Try to extract only text without full document conversion
            return self._extract_text_only(pdf_path)
        except Exception as e:
            logger.error(f"Failed to process PDF {pdf_path}: {e}")
            raise
    
    def _extract_text_only(self, pdf_path: str) -> str:
        """Fallback: extract raw text without full conversion"""
        try:
            import PyPDF2
            text = []
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page_num, page in enumerate(reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text.append(f"--- Page {page_num} ---\n{page_text}")
            return "\n\n".join(text)
        except Exception as e:
            logger.error(f"Text-only extraction failed: {e}")
            raise