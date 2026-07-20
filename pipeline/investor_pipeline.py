# pipeline/investor_pipeline.py
import os
from utils.pdf_downloader import PDFDownloader
from processors.docling_processor import DoclingProcessor
from extractors.client_order_extractor import ClientOrderExtractor
from extractors.llm_extractor import LLMExtractor
from config.investor_docs import INVESTOR_DOCUMENTS
import logging
import json
from datetime import datetime
from processors.docling_processor import SimpleDoclingProcessor
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class InvestorPipeline:
    """End-to-end pipeline for extracting client and order book data"""
    
    def __init__(self):
        self.downloader = PDFDownloader()
        # self.processor = DoclingProcessor()
        # Use the simple processor to avoid memory issues
        self.processor = SimpleDoclingProcessor()  # Changed from DoclingProcessor
        self.extractor = ClientOrderExtractor()
        self.llm_extractor = LLMExtractor()
        self.results = {}
    
    def process_company(self, company_code: str) -> Dict:
        """Process all documents for a company"""
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
        
        for doc_type, url in company_docs.items():
            try:
                logger.info(f"Processing {company_code} - {doc_type}")
                
                # Download PDF
                pdf_path = self.downloader.download_pdf(url, company_code, doc_type)
                
                # Process with Docling
                markdown = self.processor.process_pdf(pdf_path)
                
                # Extract relevant sections
                sections = self.extractor.extract_sections(markdown)
                
                # Combine sections for LLM
                combined_text = "\n\n".join(sections.values())
                
                # Extract with LLM
                extraction = self.llm_extractor.extract_from_text(
                    combined_text,
                    doc_type
                )
                
                # Merge results
                if extraction.get('deal_wins'):
                    all_extractions['deal_wins'].extend(extraction['deal_wins'])
                
                if extraction.get('order_book'):
                    all_extractions['order_book'].update(extraction['order_book'])
                
                if extraction.get('client_metrics'):
                    all_extractions['client_metrics'].update(extraction['client_metrics'])
                
                # Store raw for debugging
                all_extractions['raw_data'][doc_type] = extraction
                
            except Exception as e:
                logger.error(f"Failed to process {company_code} {doc_type}: {e}")
                all_extractions['raw_data'][doc_type] = {'error': str(e)}
        
        return all_extractions
    
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

# Usage script
if __name__ == "__main__":
    pipeline = InvestorPipeline()
    results = pipeline.run_all()
    
    # Print summary
    for company, data in results.items():
        print(f"\n{company}:")
        print(f"  Deal Wins: {len(data.get('deal_wins', []))}")
        print(f"  Order Book: {data.get('order_book', {}).get('total_tcv', 'N/A')}")
        print(f"  Clients: {data.get('client_metrics', {}).get('total_clients', 'N/A')}")