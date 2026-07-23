# # # pipeline/investor_pipeline.py
# # import os
# # from utils.pdf_downloader import PDFDownloader
# # from processors.docling_processor import DoclingProcessor
# # from extractors.client_order_extractor import ClientOrderExtractor
# # from extractors.llm_extractor import LLMExtractor
# # from config.investor_docs import INVESTOR_DOCUMENTS
# # import logging
# # import json
# # from datetime import datetime
# # from processors.docling_processor import SimpleDoclingProcessor
# # from typing import Dict, List, Optional

# # logger = logging.getLogger(__name__)

# # class InvestorPipeline:
# #     """End-to-end pipeline for extracting client and order book data"""
    
# #     def __init__(self):
# #         self.downloader = PDFDownloader()
# #         # self.processor = DoclingProcessor()
# #         # Use the simple processor to avoid memory issues
# #         self.processor = SimpleDoclingProcessor()  # Changed from DoclingProcessor
# #         self.extractor = ClientOrderExtractor()
# #         self.llm_extractor = LLMExtractor()
# #         self.results = {}
    
# #     def process_company(self, company_code: str) -> Dict:
# #         """Process all documents for a company"""
# #         company_docs = INVESTOR_DOCUMENTS.get(company_code, {})
# #         if not company_docs:
# #             logger.warning(f"No documents configured for {company_code}")
# #             return {}
        
# #         all_extractions = {
# #             'deal_wins': [],
# #             'order_book': {},
# #             'client_metrics': {},
# #             'raw_data': {}
# #         }
        
# #         for doc_type, url in company_docs.items():
# #             try:
# #                 logger.info(f"Processing {company_code} - {doc_type}")
                
# #                 # Download PDF
# #                 pdf_path = self.downloader.download_pdf(url, company_code, doc_type)
                
# #                 # Process with Docling
# #                 markdown = self.processor.process_pdf(pdf_path)
                
# #                 # Extract relevant sections
# #                 sections = self.extractor.extract_sections(markdown)
                
# #                 # Combine sections for LLM
# #                 combined_text = "\n\n".join(sections.values())
                
# #                 # Extract with LLM
# #                 extraction = self.llm_extractor.extract_from_text(
# #                     combined_text,
# #                     doc_type
# #                 )
                
# #                 # Merge results
# #                 if extraction.get('deal_wins'):
# #                     all_extractions['deal_wins'].extend(extraction['deal_wins'])
                
# #                 if extraction.get('order_book'):
# #                     all_extractions['order_book'].update(extraction['order_book'])
                
# #                 if extraction.get('client_metrics'):
# #                     all_extractions['client_metrics'].update(extraction['client_metrics'])
                
# #                 # Store raw for debugging
# #                 all_extractions['raw_data'][doc_type] = extraction
                
# #             except Exception as e:
# #                 logger.error(f"Failed to process {company_code} {doc_type}: {e}")
# #                 all_extractions['raw_data'][doc_type] = {'error': str(e)}
        
# #         return all_extractions
    
# #     def run_all(self, companies: List[str] = None) -> Dict:
# #         """Run pipeline for all or specified companies"""
# #         if not companies:
# #             companies = list(INVESTOR_DOCUMENTS.keys())
        
# #         for company in companies:
# #             logger.info(f"Processing {company}...")
# #             self.results[company] = self.process_company(company)
        
# #         # Save results
# #         self.save_results()
# #         return self.results
    
# #     def save_results(self):
# #         """Save extraction results to file"""
# #         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
# #         output_path = f'output/investor_extractions_{timestamp}.json'
        
# #         os.makedirs('output', exist_ok=True)
        
# #         with open(output_path, 'w') as f:
# #             json.dump(self.results, f, indent=2, default=str)
        
# #         logger.info(f"Results saved to {output_path}")

# # # Usage script
# # if __name__ == "__main__":
# #     pipeline = InvestorPipeline()
# #     results = pipeline.run_all()
    
# #     # Print summary
# #     for company, data in results.items():
# #         print(f"\n{company}:")
# #         print(f"  Deal Wins: {len(data.get('deal_wins', []))}")
# #         print(f"  Order Book: {data.get('order_book', {}).get('total_tcv', 'N/A')}")
# #         print(f"  Clients: {data.get('client_metrics', {}).get('total_clients', 'N/A')}")

# # pipeline/investor_pipeline.py (UPDATED)
# import os
# from utils.pdf_downloader import PDFDownloader
# from processors.docling_processor import SimpleDoclingProcessor
# from extractors.llm_extractor import LLMExtractor
# from config.investor_docs import INVESTOR_DOCUMENTS
# import logging
# import json
# from datetime import datetime
# from typing import Dict, List, Optional

# logger = logging.getLogger(__name__)

# class InvestorPipeline:
#     """End-to-end pipeline for extracting client and order book data from transcripts"""
    
#     def __init__(self):
#         self.downloader = PDFDownloader()
#         self.processor = SimpleDoclingProcessor()  # Memory-efficient
#         self.llm_extractor = LLMExtractor()
#         self.results = {}
    
#     def process_company(self, company_code: str) -> Dict:
#         """Process all documents for a company, prioritizing transcripts"""
#         company_docs = INVESTOR_DOCUMENTS.get(company_code, {})
#         if not company_docs:
#             logger.warning(f"No documents configured for {company_code}")
#             return {}
        
#         all_extractions = {
#             'deal_wins': [],
#             'order_book': {},
#             'client_metrics': {},
#             'raw_data': {}
#         }
        
#         # Priority order: transcript > press_release > other
#         doc_priority = ['transcript', 'press_release', 'fact_sheet', 'presentation']
        
#         for doc_type in doc_priority:
#             if doc_type not in company_docs:
#                 continue
            
#             url = company_docs[doc_type]
#             try:
#                 logger.info(f"Processing {company_code} - {doc_type}")
                
#                 # Download PDF
#                 pdf_path = self.downloader.download_pdf(url, company_code, doc_type)
                
#                 # Process with Docling
#                 markdown = self.processor.process_pdf(pdf_path)
                
#                 # Extract with LLM (using transcript-specific extraction)
#                 if doc_type == 'transcript':
#                     extraction = self.llm_extractor.extract_from_transcript(markdown, company_code)
#                 else:
#                     # For press releases, use standard extraction
#                     extraction = self.llm_extractor.extract_from_text(markdown, doc_type)
                
#                 # Merge results (prioritize transcript results)
#                 if extraction.get('deal_wins'):
#                     # If we already have deal wins from a higher priority doc, merge and deduplicate
#                     existing_wins = {self._normalize_deal_key(deal) for deal in all_extractions['deal_wins']}
#                     for deal in extraction['deal_wins']:
#                         key = self._normalize_deal_key(deal)
#                         if key not in existing_wins:
#                             all_extractions['deal_wins'].append(deal)
#                             existing_wins.add(key)
                
#                 # Override order book with higher priority doc
#                 if extraction.get('order_book') and extraction['order_book']:
#                     all_extractions['order_book'] = extraction['order_book']
                
#                 if extraction.get('client_metrics') and extraction['client_metrics']:
#                     all_extractions['client_metrics'] = extraction['client_metrics']
                
#                 all_extractions['raw_data'][doc_type] = extraction
                
#                 # If we have a transcript, we can stop (it's the best source)
#                 if doc_type == 'transcript' and extraction.get('deal_wins'):
#                     logger.info(f"Found {len(extraction['deal_wins'])} deal wins in transcript for {company_code}")
#                     break
                
#             except Exception as e:
#                 logger.error(f"Failed to process {company_code} {doc_type}: {e}")
#                 all_extractions['raw_data'][doc_type] = {'error': str(e)}
        
#         return all_extractions
    
#     def _normalize_deal_key(self, deal: Dict) -> str:
#         """Create a unique key for deduplication"""
#         client = deal.get('client_description', '').lower()
#         value = deal.get('deal_value', '').lower()
#         return f"{client}_{value}"[:100]
    
#     def run_all(self, companies: List[str] = None) -> Dict:
#         """Run pipeline for all or specified companies"""
#         if not companies:
#             companies = list(INVESTOR_DOCUMENTS.keys())
        
#         for company in companies:
#             logger.info(f"Processing {company}...")
#             self.results[company] = self.process_company(company)
        
#         # Save results
#         self.save_results()
#         return self.results
    
#     def save_results(self):
#         """Save extraction results to file"""
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         output_path = f'output/investor_extractions_{timestamp}.json'
        
#         os.makedirs('output', exist_ok=True)
        
#         with open(output_path, 'w') as f:
#             json.dump(self.results, f, indent=2, default=str)
        
#         logger.info(f"Results saved to {output_path}")


# pipeline/investor_pipeline.py (UPDATED - Use pdfplumber only)
import os
from utils.pdf_downloader import PDFDownloader
from processors.pdfplumber_processor import PDFPlumberProcessor  # Primary processor
from extractors.llm_extractor import LLMExtractor
from config.investor_docs import INVESTOR_DOCUMENTS
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class InvestorPipeline:
    """End-to-end pipeline for extracting client and order book data from transcripts"""
    
    def __init__(self):
        self.downloader = PDFDownloader()
        # Use pdfplumber exclusively (lightweight, no memory issues)
        self.processor = PDFPlumberProcessor()
        self.llm_extractor = LLMExtractor()
        self.results = {}
    
    def process_company(self, company_code: str) -> Dict:
        """Process all documents for a company, prioritizing transcripts"""
        company_docs = INVESTOR_DOCUMENTS.get(company_code, {})
        if not company_docs:
            logger.warning(f"No documents configured for {company_code}")
            return {}
        
        all_extractions = {
            'deal_wins': [],
            'order_book': {},
            'client_metrics': {},
            'raw_data': {}
        }
        
        # Priority order: transcript > press_release > other
        doc_priority = ['transcript', 'press_release', 'fact_sheet', 'presentation']
        
        for doc_type in doc_priority:
            if doc_type not in company_docs:
                continue
            
            url = company_docs[doc_type]
            try:
                logger.info(f"Processing {company_code} - {doc_type}")
                
                # Download PDF
                pdf_path = self.downloader.download_pdf(url, company_code, doc_type)
                
                # Process with pdfplumber (no memory issues)
                markdown = self.processor.process_pdf(pdf_path)
                
                # Extract with LLM
                if doc_type == 'transcript':
                    extraction = self.llm_extractor.extract_from_transcript(markdown, company_code)
                else:
                    extraction = self.llm_extractor.extract_from_text(markdown, doc_type)
                
                # Merge results (prioritize transcript results)
                if extraction.get('deal_wins'):
                    existing_wins = {self._normalize_deal_key(deal) for deal in all_extractions['deal_wins']}
                    for deal in extraction['deal_wins']:
                        key = self._normalize_deal_key(deal)
                        if key not in existing_wins:
                            all_extractions['deal_wins'].append(deal)
                            existing_wins.add(key)
                
                # Override order book with higher priority doc
                if extraction.get('order_book') and extraction['order_book']:
                    all_extractions['order_book'] = extraction['order_book']
                
                if extraction.get('client_metrics') and extraction['client_metrics']:
                    all_extractions['client_metrics'] = extraction['client_metrics']
                
                all_extractions['raw_data'][doc_type] = extraction
                
                # If we have a transcript, we can stop (it's the best source)
                if doc_type == 'transcript' and extraction.get('deal_wins'):
                    logger.info(f"Found {len(extraction['deal_wins'])} deal wins in transcript for {company_code}")
                    break
                
            except Exception as e:
                logger.error(f"Failed to process {company_code} {doc_type}: {e}")
                all_extractions['raw_data'][doc_type] = {'error': str(e)}
        
        return all_extractions
    
    def _normalize_deal_key(self, deal: Dict) -> str:
        """Create a unique key for deduplication"""
        client = deal.get('client_description', '').lower()
        value = deal.get('deal_value', '').lower()
        return f"{client}_{value}"[:100]
    
    def run_all(self, companies: List[str] = None) -> Dict:
        """Run pipeline for all or specified companies"""
        if not companies:
            companies = list(INVESTOR_DOCUMENTS.keys())
        
        for company in companies:
            logger.info(f"Processing {company}...")
            self.results[company] = self.process_company(company)
        
        # Save results
        self.save_results()
        return self.results
    
    def save_results(self):
        """Save extraction results to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f'output/investor_extractions_{timestamp}.json'
        
        os.makedirs('output', exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        logger.info(f"Results saved to {output_path}")