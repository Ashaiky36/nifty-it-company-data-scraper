            
# # extractors/llm_extractor.py (COMPLETE FIXED VERSION)
# import json
# import ollama
# from typing import Dict, List, Optional
# import logging
# import re

# logger = logging.getLogger(__name__)

# class LLMExtractor:
#     """Extract structured information from earnings call transcripts and text"""
    
#     def __init__(self, model: str = 'llama3.2:3b'):
#         self.model = model
#         self.system_prompt = """
#         You are a financial data extractor specializing in earnings call transcripts and press releases.
#         Extract the following information:
        
#         1. **Deal Wins/Client Engagements**: For each deal mentioned, extract:
#            - client_description: Industry, location, size (e.g., "US-based bank")
#            - deal_details: What service/solution is being provided
#            - deal_value: TCV/contract value if mentioned
#            - is_new_client: true/false if specified
#            - industry: Sector (banking, retail, telecom, healthcare, etc.)
#            - location: Geography (US, Europe, Asia, UK, etc.)
        
#         2. **Order Book / TCV Metrics**:
#            - total_tcv: Total TCV for the quarter (exact number with unit)
#            - deal_count: Number of deals won
#            - large_deals: List of mega deals (>$50M)
#            - order_book_value: 12-month executable order book if mentioned
        
#         3. **Client Metrics**:
#            - total_clients: Number of clients
#            - client_distribution: Distribution by revenue size
#            - concentration: Client concentration percentage
#            - client_buckets: Client count by revenue range
        
#         Return ONLY valid JSON. Do not include any other text.
#         """
    
#     def extract_from_transcript(self, text: str, company_name: str) -> Dict:
#         """
#         Extract structured information from earnings call transcript
#         """
#         try:
#             # Extract key sections (prepared remarks and Q&A)
#             key_sections = self._extract_key_sections(text)
            
#             # Truncate if needed
#             max_length = 8000
#             if len(key_sections) > max_length:
#                 key_sections = key_sections[:max_length]
            
#             # Prepare prompt
#             user_prompt = f"""
#             This is the earnings call transcript for {company_name}.
#             Extract all deal wins, client information, and order book metrics.
            
#             Pay special attention to:
#             - Management's prepared remarks (usually at the start)
#             - Any mention of "deal wins", "client wins", "contracts", "engagements"
#             - TCV (Total Contract Value) or order book numbers
#             - Client metrics by revenue size
            
#             Transcript sections:
#             {key_sections}
            
#             Return ONLY valid JSON with this structure:
#             {{
#                 "deal_wins": [
#                     {{
#                         "client_description": "string",
#                         "deal_details": "string",
#                         "deal_value": "string",
#                         "is_new_client": boolean,
#                         "industry": "string",
#                         "location": "string"
#                     }}
#                 ],
#                 "order_book": {{
#                     "total_tcv": "string",
#                     "deal_count": "string",
#                     "large_deals": ["deal1", "deal2"],
#                     "order_book_value": "string"
#                 }},
#                 "client_metrics": {{
#                     "total_clients": "string",
#                     "client_distribution": "string",
#                     "concentration": "string",
#                     "client_buckets": "string"
#                 }}
#             }}
#             """
            
#             # Call LLM
#             response = ollama.chat(
#                 model=self.model,
#                 messages=[
#                     {"role": "system", "content": self.system_prompt},
#                     {"role": "user", "content": user_prompt}
#                 ],
#                 format='json'
#             )
            
#             # Parse response
#             result = json.loads(response['message']['content'])
            
#             # Ensure required keys exist
#             result.setdefault('deal_wins', [])
#             result.setdefault('order_book', {})
#             result.setdefault('client_metrics', {})
            
#             # Post-process to clean up
#             self._clean_extraction(result)
            
#             logger.info(f"Extracted {len(result['deal_wins'])} deal wins for {company_name}")
#             return result
            
#         except Exception as e:
#             logger.error(f"LLM extraction failed for {company_name}: {e}")
#             return {
#                 'deal_wins': [],
#                 'order_book': {},
#                 'client_metrics': {},
#                 'error': str(e)
#             }
    
#     def extract_from_text(self, text: str, doc_type: str = "press_release") -> Dict:
#         """
#         Extract structured information from any text (press release, factsheet, etc.)
#         """
#         try:
#             # Truncate if needed
#             max_length = 8000
#             if len(text) > max_length:
#                 text = self._extract_relevant_sections(text, max_length)
            
#             # Prepare prompt based on document type
#             if doc_type == "transcript":
#                 return self.extract_from_transcript(text, "Unknown")
            
#             user_prompt = f"""
#             This is a {doc_type} from an IT company.
#             Extract all deal wins, client information, and order book metrics.
            
#             Text:
#             {text}
            
#             Return ONLY valid JSON with this structure:
#             {{
#                 "deal_wins": [
#                     {{
#                         "client_description": "string",
#                         "deal_details": "string",
#                         "deal_value": "string",
#                         "is_new_client": boolean,
#                         "industry": "string",
#                         "location": "string"
#                     }}
#                 ],
#                 "order_book": {{
#                     "total_tcv": "string",
#                     "deal_count": "string",
#                     "large_deals": ["deal1", "deal2"],
#                     "order_book_value": "string"
#                 }},
#                 "client_metrics": {{
#                     "total_clients": "string",
#                     "client_distribution": "string",
#                     "concentration": "string",
#                     "client_buckets": "string"
#                 }}
#             }}
#             """
            
#             # Call LLM
#             response = ollama.chat(
#                 model=self.model,
#                 messages=[
#                     {"role": "system", "content": self.system_prompt},
#                     {"role": "user", "content": user_prompt}
#                 ],
#                 format='json'
#             )
            
#             # Parse response
#             result = json.loads(response['message']['content'])
            
#             # Ensure required keys exist
#             result.setdefault('deal_wins', [])
#             result.setdefault('order_book', {})
#             result.setdefault('client_metrics', {})
            
#             self._clean_extraction(result)
            
#             logger.info(f"Extracted {len(result['deal_wins'])} deal wins from {doc_type}")
#             return result
            
#         except Exception as e:
#             logger.error(f"LLM extraction failed: {e}")
#             return {
#                 'deal_wins': [],
#                 'order_book': {},
#                 'client_metrics': {},
#                 'error': str(e)
#             }
    
#     def _extract_key_sections(self, text: str) -> str:
#         """Extract key sections from transcript"""
#         sections = []
        
#         # Look for prepared remarks
#         prepared_patterns = [
#             r'(?:operational|business|financial)\s+(?:review|performance|summary)',
#             r'prepared\s+remarks',
#             r'opening\s+comments'
#         ]
        
#         lines = text.split('\n')
#         current_section = []
#         in_prepared = False
        
#         for i, line in enumerate(lines):
#             line_lower = line.lower()
            
#             # Check if this is a prepared remarks section
#             if any(re.search(pattern, line_lower, re.I) for pattern in prepared_patterns):
#                 in_prepared = True
#                 current_section = [line]
#             elif in_prepared:
#                 # Stop at Q&A
#                 if 'question' in line_lower or 'answer' in line_lower or 'q&a' in line_lower:
#                     in_prepared = False
#                     if current_section:
#                         sections.append('\n'.join(current_section))
#                 else:
#                     current_section.append(line)
        
#         # If no prepared remarks found, take first 500 lines (usually contains key info)
#         if not sections:
#             sections.append('\n'.join(lines[:500]))
        
#         # Also look for management commentary sections
#         for i, line in enumerate(lines):
#             if 'ceo' in line.lower() or 'cfo' in line.lower() or 'md' in line.lower():
#                 if i < len(lines) - 50:
#                     start = max(0, i - 10)
#                     end = min(len(lines), i + 50)
#                     sections.append('\n'.join(lines[start:end]))
#                     break
        
#         return '\n\n'.join(sections)
    
#     def _extract_relevant_sections(self, text: str, max_length: int) -> str:
#         """Extract most relevant sections when text is too long"""
#         keywords = ['TCV', 'deal', 'client', 'contract', 'agreement', 'win', 'partnership']
        
#         lines = text.split('\n')
#         relevant_lines = []
        
#         for i, line in enumerate(lines):
#             if any(keyword.lower() in line.lower() for keyword in keywords):
#                 start = max(0, i - 2)
#                 end = min(len(lines), i + 3)
#                 relevant_lines.extend(lines[start:end])
        
#         if relevant_lines:
#             extracted = '\n'.join(relevant_lines)
#             if len(extracted) > max_length:
#                 extracted = extracted[:max_length]
#             return extracted
        
#         # Fallback: first few pages
#         pages = text.split('--- Page')
#         if len(pages) > 2:
#             extracted = pages[0] + pages[1] + pages[2]
#             if len(extracted) > max_length:
#                 extracted = extracted[:max_length]
#             return extracted
        
#         return text[:max_length]
    
#     def _clean_extraction(self, result: Dict):
#         """Clean and validate extraction results"""
#         # Clean deal wins
#         if result.get('deal_wins'):
#             for deal in result['deal_wins']:
#                 # Ensure boolean for is_new_client
#                 if 'is_new_client' in deal and isinstance(deal['is_new_client'], str):
#                     deal['is_new_client'] = deal['is_new_client'].lower() in ['true', 'yes', 'new']
        
#         # Clean TCV values
#         if result.get('order_book', {}).get('total_tcv'):
#             tcv = result['order_book']['total_tcv']
#             result['order_book']['total_tcv'] = ' '.join(tcv.split())            

# # extractors/llm_extractor.py (UPDATED with Qwen + Chunking)
# import json
# import ollama
# from typing import Dict, List, Optional
# import logging
# import re

# logger = logging.getLogger(__name__)

# class LLMExtractor:
#     """Extract structured information using Qwen2.5 with chunking"""
    
#     def __init__(self, model: str = 'qwen2.5:3b-instruct'):
#         self.model = model
#         self.chunk_size = 6000  # Characters per chunk (~8k tokens)
#         self.overlap = 500      # Overlap between chunks to avoid missing data at boundaries
        
#         self.system_prompt = """
#         You are a precise financial data extractor for IT company earnings call transcripts.
#         Extract ONLY information that is explicitly stated in the text.
        
#         Extract:
#         1. Deal Wins/Client Engagements: For each deal, extract client_description, 
#            deal_details, deal_value (with currency/unit), industry, location.
#         2. Order Book: total_tcv, deal_count, large_deals list, order_book_value.
#         3. Client Metrics: total_clients, client_distribution, concentration.
        
#         Return ONLY valid JSON with this exact structure. If something is not found,
#         use null or empty list.
#         """
    
#     def extract_from_transcript(self, text: str, company_name: str) -> Dict:
#         """Extract using chunked processing for long documents"""
#         try:
#             # Split into chunks
#             chunks = self._split_into_chunks(text)
#             logger.info(f"Split {company_name} transcript into {len(chunks)} chunks")
            
#             all_deal_wins = []
#             order_book = {}
#             client_metrics = {}
            
#             for i, chunk in enumerate(chunks):
#                 logger.info(f"Processing chunk {i+1}/{len(chunks)} for {company_name}")
                
#                 chunk_result = self._extract_from_chunk(chunk, company_name, i+1)
                
#                 # Merge deal wins (avoid duplicates)
#                 if chunk_result.get('deal_wins'):
#                     all_deal_wins.extend(chunk_result['deal_wins'])
                
#                 # Merge order book (take latest/complete)
#                 if chunk_result.get('order_book'):
#                     # Prefer non-empty values
#                     for key, value in chunk_result['order_book'].items():
#                         if value and (not order_book.get(key) or key == 'large_deals'):
#                             order_book[key] = value
                
#                 # Merge client metrics
#                 if chunk_result.get('client_metrics'):
#                     for key, value in chunk_result['client_metrics'].items():
#                         if value and not client_metrics.get(key):
#                             client_metrics[key] = value
            
#             # Clean up duplicates
#             all_deal_wins = self._deduplicate_deals(all_deal_wins)
            
#             logger.info(f"Extracted {len(all_deal_wins)} unique deal wins for {company_name}")
            
#             return {
#                 'deal_wins': all_deal_wins,
#                 'order_book': order_book,
#                 'client_metrics': client_metrics
#             }
            
#         except Exception as e:
#             logger.error(f"LLM extraction failed for {company_name}: {e}")
#             return {
#                 'deal_wins': [],
#                 'order_book': {},
#                 'client_metrics': {},
#                 'error': str(e)
#             }
    
#     def _split_into_chunks(self, text: str) -> List[str]:
#         """Split text into overlapping chunks"""
#         chunks = []
        
#         # Try to split by pages first (if marked with "--- Page")
#         if '--- Page' in text:
#             pages = text.split('--- Page')
#             chunks = []
#             current_chunk = []
#             current_size = 0
            
#             for page in pages:
#                 if not page.strip():
#                     continue
#                 page_text = f"--- Page{page}"
#                 page_len = len(page_text)
                
#                 if current_size + page_len > self.chunk_size and current_chunk:
#                     chunks.append('\n'.join(current_chunk))
#                     # Keep last page for overlap
#                     current_chunk = [current_chunk[-1], page_text]
#                     current_size = len(current_chunk[-1])
#                 else:
#                     current_chunk.append(page_text)
#                     current_size += page_len
            
#             if current_chunk:
#                 chunks.append('\n'.join(current_chunk))
            
#             if len(chunks) > 1:
#                 return chunks
        
#         # Fallback: split by character count with overlap
#         if len(text) > self.chunk_size:
#             chunks = []
#             for i in range(0, len(text), self.chunk_size - self.overlap):
#                 chunk = text[i:i + self.chunk_size]
#                 if chunk.strip():
#                     chunks.append(chunk)
#             return chunks
        
#         return [text]
    
#     def _extract_from_chunk(self, chunk: str, company_name: str, chunk_num: int) -> Dict:
#         """Extract from a single chunk"""
        
#         user_prompt = f"""
#         This is part {chunk_num} of the earnings call transcript for {company_name}.
#         Extract all deal wins, client information, and order book metrics from this section.
        
#         Transcript section:
#         {chunk}
        
#         Return ONLY valid JSON with this structure:
#         {{
#             "deal_wins": [
#                 {{
#                     "client_description": "string",
#                     "deal_details": "string", 
#                     "deal_value": "string",
#                     "is_new_client": boolean,
#                     "industry": "string",
#                     "location": "string"
#                 }}
#             ],
#             "order_book": {{
#                 "total_tcv": "string",
#                 "deal_count": "string",
#                 "large_deals": ["deal1", "deal2"],
#                 "order_book_value": "string"
#             }},
#             "client_metrics": {{
#                 "total_clients": "string",
#                 "client_distribution": "string",
#                 "concentration": "string",
#                 "client_buckets": "string"
#             }}
#         }}
#         """
        
#         try:
#             response = ollama.chat(
#                 model=self.model,
#                 messages=[
#                     {"role": "system", "content": self.system_prompt},
#                     {"role": "user", "content": user_prompt}
#                 ],
#                 options={
#                     "num_ctx": 8192,      # 8k context window
#                     "temperature": 0.0,   # Deterministic
#                     "top_k": 10,
#                     "top_p": 0.9
#                 },
#                 format='json'
#             )
            
#             result = json.loads(response['message']['content'])
#             result.setdefault('deal_wins', [])
#             result.setdefault('order_book', {})
#             result.setdefault('client_metrics', {})
            
#             return result
            
#         except Exception as e:
#             logger.error(f"Chunk {chunk_num} extraction failed: {e}")
#             return {'deal_wins': [], 'order_book': {}, 'client_metrics': {}}
    
#     def _deduplicate_deals(self, deals: List[Dict]) -> List[Dict]:
#         """Remove duplicate deals based on client description and value"""
#         seen = set()
#         unique_deals = []
        
#         for deal in deals:
#             client = deal.get('client_description', '').lower()[:50]
#             value = deal.get('deal_value', '').lower()[:30]
#             key = f"{client}_{value}"
            
#             if key not in seen and client:
#                 seen.add(key)
#                 unique_deals.append(deal)
        
#         return unique_deals
    
#     def extract_from_text(self, text: str, doc_type: str = "press_release") -> Dict:
#         """Generic extraction for other document types"""
#         # Use same chunking strategy
#         chunks = self._split_into_chunks(text)
        
#         all_deal_wins = []
#         order_book = {}
#         client_metrics = {}
        
#         for i, chunk in enumerate(chunks):
#             result = self._extract_from_chunk(chunk, "Unknown", i+1)
            
#             if result.get('deal_wins'):
#                 all_deal_wins.extend(result['deal_wins'])
#             if result.get('order_book'):
#                 for key, value in result['order_book'].items():
#                     if value and not order_book.get(key):
#                         order_book[key] = value
#             if result.get('client_metrics'):
#                 for key, value in result['client_metrics'].items():
#                     if value and not client_metrics.get(key):
#                         client_metrics[key] = value
        
#         all_deal_wins = self._deduplicate_deals(all_deal_wins)
        
#         return {
#             'deal_wins': all_deal_wins,
#             'order_book': order_book,
#             'client_metrics': client_metrics
#         }

# extractors/llm_extractor.py (FIXED with robust error handling)
import json
import ollama
from typing import Dict, List, Optional
import logging
import re

logger = logging.getLogger(__name__)

class LLMExtractor:
    """Extract structured information using Qwen2.5 with chunking"""
    
    def __init__(self, model: str = 'qwen2.5:3b-instruct'):
        self.model = model
        self.chunk_size = 6000  # Characters per chunk (~8k tokens)
        self.overlap = 500      # Overlap between chunks to avoid missing data at boundaries
        
        self.system_prompt = """
You are a precise financial data extractor for IT company earnings call transcripts.

Your task is to extract EXACT deal wins, client engagements, and order book metrics.

Rules:
1. Only extract information that is explicitly mentioned in the text
2. For deal wins, extract the client description, deal details, and deal value
3. For order book, extract TCV numbers and deal counts
4. Return ONLY valid JSON

Key patterns to look for:
- "deal with", "contract with", "agreement with", "selected by", "chosen by"
- "TCV", "Total Contract Value", "deal value", "contract value"
- "$", "million", "billion", "crore", "Cr"
- "client", "customer", "partner", "bank", "insurance", "retailer"

If a field is not found, use null.
"""
        
        # self.system_prompt = """
        # You are a precise financial data extractor for IT company earnings call transcripts.
        # Extract ONLY information that is explicitly stated in the text.
        
        # Extract:
        # 1. Deal Wins/Client Engagements: For each deal, extract client_description, 
        #    deal_details, deal_value (with currency/unit), industry, location.
        # 2. Order Book: total_tcv, deal_count, large_deals list, order_book_value.
        # 3. Client Metrics: total_clients, client_distribution, concentration.
        
        # Return ONLY valid JSON with this exact structure. If something is not found,
        # use null or empty list.
        # """
    
    # def extract_from_transcript(self, text: str, company_name: str) -> Dict:
    #     """Extract using chunked processing for long documents"""
    #     try:
    #         if not text or len(text.strip()) < 100:
    #             logger.warning(f"Text too short for {company_name}")
    #             return {'deal_wins': [], 'order_book': {}, 'client_metrics': {}}
            
    #         # Split into chunks
    #         chunks = self._split_into_chunks(text)
    #         logger.info(f"Split {company_name} transcript into {len(chunks)} chunks")
            
    #         all_deal_wins = []
    #         order_book = {}
    #         client_metrics = {}
            
    #         for i, chunk in enumerate(chunks):
    #             logger.info(f"Processing chunk {i+1}/{len(chunks)} for {company_name}")
                
    #             chunk_result = self._extract_from_chunk(chunk, company_name, i+1)
                
    #             # Merge deal wins (avoid duplicates)
    #             if chunk_result.get('deal_wins'):
    #                 all_deal_wins.extend(chunk_result['deal_wins'])
                
    #             # Merge order book (take latest/complete)
    #             if chunk_result.get('order_book'):
    #                 for key, value in chunk_result['order_book'].items():
    #                     if value and (not order_book.get(key) or key == 'large_deals'):
    #                         order_book[key] = value
                
    #             # Merge client metrics
    #             if chunk_result.get('client_metrics'):
    #                 for key, value in chunk_result['client_metrics'].items():
    #                     if value and not client_metrics.get(key):
    #                         client_metrics[key] = value
            
    #         # Clean up duplicates
    #         all_deal_wins = self._deduplicate_deals(all_deal_wins)
            
    #         logger.info(f"Extracted {len(all_deal_wins)} unique deal wins for {company_name}")
            
    #         return {
    #             'deal_wins': all_deal_wins,
    #             'order_book': order_book,
    #             'client_metrics': client_metrics
    #         }
            
    #     except Exception as e:
    #         logger.error(f"LLM extraction failed for {company_name}: {e}")
    #         return {
    #             'deal_wins': [],
    #             'order_book': {},
    #             'client_metrics': {},
    #             'error': str(e)
    #         }
    
    # def _split_into_chunks(self, text: str) -> List[str]:
    #     """Split text into overlapping chunks"""
    #     if not text:
    #         return [""]
        
    #     chunks = []
        
    #     # Try to split by pages first (if marked with "--- Page")
    #     if '--- Page' in text:
    #         pages = text.split('--- Page')
    #         current_chunk = []
    #         current_size = 0
            
    #         for page in pages:
    #             if not page.strip():
    #                 continue
    #             page_text = f"--- Page{page}"
    #             page_len = len(page_text)
                
    #             if current_size + page_len > self.chunk_size and current_chunk:
    #                 chunks.append('\n'.join(current_chunk))
    #                 # Keep last page for overlap
    #                 current_chunk = [current_chunk[-1], page_text]
    #                 current_size = len(current_chunk[-1])
    #             else:
    #                 current_chunk.append(page_text)
    #                 current_size += page_len
            
    #         if current_chunk:
    #             chunks.append('\n'.join(current_chunk))
            
    #         if len(chunks) > 1:
    #             return chunks
        
    #     # Fallback: split by character count with overlap
    #     if len(text) > self.chunk_size:
    #         chunks = []
    #         for i in range(0, len(text), self.chunk_size - self.overlap):
    #             chunk = text[i:i + self.chunk_size]
    #             if chunk.strip():
    #                 chunks.append(chunk)
    #         return chunks
        
    #     return [text] if text.strip() else [""]
    
# extractors/llm_extractor.py (ADD this improved method)
    def extract_from_transcript(self, text: str, company_name: str) -> Dict:
        """Extract using chunked processing for long documents with better error handling"""
        try:
            if not text or len(text.strip()) < 100:
                logger.warning(f"Text too short for {company_name}")
                return {'deal_wins': [], 'order_book': {}, 'client_metrics': {}}
            
            # Split into smaller chunks (reduce from 6000 to 4000 chars for reliability)
            chunks = self._split_into_chunks(text, chunk_size=4000)
            logger.info(f"Split {company_name} transcript into {len(chunks)} chunks")
            
            all_deal_wins = []
            order_book = {}
            client_metrics = {}
            
            for i, chunk in enumerate(chunks):
                if not chunk or len(chunk.strip()) < 100:
                    continue
                    
                logger.info(f"Processing chunk {i+1}/{len(chunks)} for {company_name}")
                
                # Process chunk with retry
                chunk_result = None
                for attempt in range(2):
                    try:
                        chunk_result = self._extract_from_chunk(chunk, company_name, i+1)
                        if chunk_result and chunk_result.get('deal_wins'):
                            break
                    except Exception as e:
                        logger.warning(f"Chunk {i+1} attempt {attempt+1} failed: {e}")
                        if attempt == 0:
                            # Try with smaller chunk on retry
                            chunk = chunk[:3000]
                
                if not chunk_result:
                    continue
                
                # Merge deal wins
                if chunk_result.get('deal_wins'):
                    all_deal_wins.extend(chunk_result['deal_wins'])
                
                # Merge order book
                if chunk_result.get('order_book'):
                    for key, value in chunk_result['order_book'].items():
                        if value and not order_book.get(key):
                            order_book[key] = value
                
                # Merge client metrics
                if chunk_result.get('client_metrics'):
                    for key, value in chunk_result['client_metrics'].items():
                        if value and not client_metrics.get(key):
                            client_metrics[key] = value
            
            # Clean up duplicates
            all_deal_wins = self._deduplicate_deals(all_deal_wins)
            
            logger.info(f"Extracted {len(all_deal_wins)} unique deal wins for {company_name}")
            
            return {
                'deal_wins': all_deal_wins,
                'order_book': order_book,
                'client_metrics': client_metrics
            }
            
        except Exception as e:
            logger.error(f"LLM extraction failed for {company_name}: {e}")
            return {
                'deal_wins': [],
                'order_book': {},
                'client_metrics': {},
                'error': str(e)
            }

    def _split_into_chunks(self, text: str, chunk_size: int = 4000) -> List[str]:
        """Split text into overlapping chunks with better page handling"""
        if not text:
            return [""]
        
        chunks = []
        
        # Try to split by pages first
        if '--- Page' in text:
            pages = text.split('--- Page')
            current_chunk = []
            current_size = 0
            
            for page in pages:
                if not page.strip():
                    continue
                page_text = f"--- Page{page}"
                page_len = len(page_text)
                
                if current_size + page_len > chunk_size and current_chunk:
                    chunks.append('\n'.join(current_chunk))
                    # Keep last page for overlap
                    current_chunk = [current_chunk[-1], page_text]
                    current_size = len(current_chunk[-1])
                else:
                    current_chunk.append(page_text)
                    current_size += page_len
            
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
            
            if len(chunks) > 1:
                return chunks
        
        # Fallback: split by character count with overlap
        if len(text) > chunk_size:
            chunks = []
            overlap = 300
            for i in range(0, len(text), chunk_size - overlap):
                chunk = text[i:i + chunk_size]
                if chunk.strip():
                    chunks.append(chunk)
            return chunks
        
        return [text] if text.strip() else [""] 
    
    def _extract_from_chunk(self, chunk: str, company_name: str, chunk_num: int) -> Dict:
        """Extract from a single chunk with improved prompt"""
        if not chunk or len(chunk.strip()) < 50:
            return {'deal_wins': [], 'order_book': {}, 'client_metrics': {}}
        
        if len(chunk) > 8000:
            chunk = chunk[:8000]
        
        user_prompt = f"""
        Extract ALL deal wins, client information, and order book metrics from this section of the {company_name} earnings call transcript.

        For each deal win, extract:
        - client_description: Who is the client? (e.g., "SKF", "US-based bank", "Europe-based Fortune Global 50 firm")
        - deal_details: What service/solution is being provided? (brief description)
        - deal_value: What is the contract value? (e.g., "$800 million", "Multi-million $", "$9.5 billion")
        - industry: What industry is the client in? (e.g., "Manufacturing", "Banking", "Retail")
        - location: Where is the client based? (e.g., "US", "Europe", "UK")

        Also extract:
        - total_tcv: Total Contract Value for the quarter
        - deal_count: Number of deals won
        - large_deals: List of mega deals (>$50M)
        - total_clients: Total number of clients
        - client_buckets: Client distribution by revenue size

        Transcript section:
        {chunk}

        Return ONLY valid JSON with this structure:
        {{
            "deal_wins": [
                {{
                    "client_description": "string",
                    "deal_details": "string",
                    "deal_value": "string",
                    "industry": "string",
                    "location": "string"
                }}
            ],
            "order_book": {{
                "total_tcv": "string",
                "deal_count": "string",
                "large_deals": ["deal1", "deal2"]
            }},
            "client_metrics": {{
                "total_clients": "string",
                "client_buckets": "string"
            }}
        }}
        """
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                options={
                    "num_ctx": 4096,
                    "temperature": 0.0,
                    "top_k": 10,
                    "top_p": 0.9
                },
                format='json'
            )
            
            content = response['message']['content']
            
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    return {'deal_wins': [], 'order_book': {}, 'client_metrics': {}}
            
            result.setdefault('deal_wins', [])
            result.setdefault('order_book', {})
            result.setdefault('client_metrics', {})
            
            # Clean up empty values
            result['deal_wins'] = [d for d in result['deal_wins'] if d and d.get('client_description')]
            
            return result
            
        except Exception as e:
            logger.error(f"Chunk {chunk_num} extraction failed: {e}")
            return {'deal_wins': [], 'order_book': {}, 'client_metrics': {}}
       
    
    # def _extract_from_chunk(self, chunk: str, company_name: str, chunk_num: int) -> Dict:
    #     """Extract from a single chunk"""
    #     if not chunk or len(chunk.strip()) < 50:
    #         return {'deal_wins': [], 'order_book': {}, 'client_metrics': {}}
        
    #     # Truncate chunk if too long for model
    #     if len(chunk) > 8000:
    #         chunk = chunk[:8000]
        
    #     user_prompt = f"""
    #     This is part {chunk_num} of the earnings call transcript for {company_name}.
    #     Extract all deal wins, client information, and order book metrics from this section.
        
    #     Transcript section:
    #     {chunk}
        
    #     Return ONLY valid JSON with this structure:
    #     {{
    #         "deal_wins": [
    #             {{
    #                 "client_description": "string",
    #                 "deal_details": "string", 
    #                 "deal_value": "string",
    #                 "is_new_client": boolean,
    #                 "industry": "string",
    #                 "location": "string"
    #             }}
    #         ],
    #         "order_book": {{
    #             "total_tcv": "string",
    #             "deal_count": "string",
    #             "large_deals": ["deal1", "deal2"],
    #             "order_book_value": "string"
    #         }},
    #         "client_metrics": {{
    #             "total_clients": "string",
    #             "client_distribution": "string",
    #             "concentration": "string",
    #             "client_buckets": "string"
    #         }}
    #     }}
    #     """
        
    #     try:
    #         response = ollama.chat(
    #             model=self.model,
    #             messages=[
    #                 {"role": "system", "content": self.system_prompt},
    #                 {"role": "user", "content": user_prompt}
    #             ],
    #             options={
    #                 "num_ctx": 4096,       # Reduced to 4k for reliability
    #                 "temperature": 0.0,
    #                 "top_k": 10,
    #                 "top_p": 0.9
    #             },
    #             format='json'
    #         )
            
    #         # Parse response
    #         content = response['message']['content']
            
    #         # Try to extract JSON if there's extra text
    #         try:
    #             result = json.loads(content)
    #         except json.JSONDecodeError:
    #             # Try to find JSON in the response
    #             json_match = re.search(r'\{.*\}', content, re.DOTALL)
    #             if json_match:
    #                 result = json.loads(json_match.group())
    #             else:
    #                 logger.warning(f"Could not parse JSON from chunk {chunk_num}")
    #                 return {'deal_wins': [], 'order_book': {}, 'client_metrics': {}}
            
    #         result.setdefault('deal_wins', [])
    #         result.setdefault('order_book', {})
    #         result.setdefault('client_metrics', {})
            
    #         # Clean empty values
    #         if not result['deal_wins']:
    #             result['deal_wins'] = []
    #         if not result['order_book']:
    #             result['order_book'] = {}
    #         if not result['client_metrics']:
    #             result['client_metrics'] = {}
            
    #         return result
            
    #     except Exception as e:
    #         logger.error(f"Chunk {chunk_num} extraction failed: {e}")
    #         return {'deal_wins': [], 'order_book': {}, 'client_metrics': {}}
    
    def _deduplicate_deals(self, deals: List[Dict]) -> List[Dict]:
        """Remove duplicate deals based on client description and value"""
        seen = set()
        unique_deals = []
        
        for deal in deals:
            if not deal:
                continue
                
            # Safely get values with defaults
            client = str(deal.get('client_description', '')).lower()[:50]
            value = str(deal.get('deal_value', '')).lower()[:30]
            
            # Skip if both are empty
            if not client and not value:
                continue
                
            key = f"{client}_{value}"
            
            if key not in seen:
                seen.add(key)
                unique_deals.append(deal)
        
        return unique_deals
    
    def extract_from_text(self, text: str, doc_type: str = "press_release") -> Dict:
        """Generic extraction for other document types"""
        if not text or len(text.strip()) < 100:
            return {'deal_wins': [], 'order_book': {}, 'client_metrics': {}}
        
        chunks = self._split_into_chunks(text)
        
        all_deal_wins = []
        order_book = {}
        client_metrics = {}
        
        for i, chunk in enumerate(chunks):
            result = self._extract_from_chunk(chunk, "Unknown", i+1)
            
            if result.get('deal_wins'):
                all_deal_wins.extend(result['deal_wins'])
            if result.get('order_book'):
                for key, value in result['order_book'].items():
                    if value and not order_book.get(key):
                        order_book[key] = value
            if result.get('client_metrics'):
                for key, value in result['client_metrics'].items():
                    if value and not client_metrics.get(key):
                        client_metrics[key] = value
        
        all_deal_wins = self._deduplicate_deals(all_deal_wins)
        
        return {
            'deal_wins': all_deal_wins,
            'order_book': order_book,
            'client_metrics': client_metrics
        }