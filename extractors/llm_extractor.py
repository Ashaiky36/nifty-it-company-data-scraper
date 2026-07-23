# # extractors/llm_extractor.py
# import json
# import ollama
# from typing import Dict, List, Optional
# import logging

# logger = logging.getLogger(__name__)

# class LLMExtractor:
#     """Extract structured information using local LLM"""
    
#     def __init__(self, model: str = 'llama3.2:3b'):  # or 'gemma:2b'
#         self.model = model
#         self.system_prompt = """
#         You are a financial data extractor specializing in extracting client information 
#         and order book details from IT company earnings presentations and press releases.
        
#         Extract the following information:
#         1. **Client Wins/Partnerships**: For each client engagement mentioned, extract:
#            - Client description (industry, location, size like "US-based bank")
#            - Deal details (what service/solution is being provided)
#            - Deal value (TCV/contract value in $/INR with unit)
#            - Project/delivery timeline if mentioned
#            - Whether it's new client or existing client expansion
        
#         2. **Order Book / TCV Metrics**:
#            - Total TCV for the quarter
#            - TCV breakdown by region/industry if provided
#            - Large deal wins (>$50M, >$100M, etc.)
#            - Number of deals won
#            - Order backlog if mentioned
        
#         3. **Client Metrics**:
#            - Number of clients (total, active)
#            - Client distribution by revenue size
#            - Client concentration percentage
        
#         Return the results as a JSON object with this structure:
#         {
#             "deal_wins": [
#                 {
#                     "client_description": "string",
#                     "deal_details": "string",
#                     "deal_value": "string with unit",
#                     "is_new_client": boolean,
#                     "industry": "string",
#                     "location": "string"
#                 }
#             ],
#             "order_book": {
#                 "total_tcv": "string",
#                 "deal_count": "string",
#                 "large_deals": ["deal1", "deal2"],
#                 "backlog": "string"
#             },
#             "client_metrics": {
#                 "total_clients": "string",
#                 "client_distribution": "string",
#                 "concentration": "string"
#             }
#         }
        
#         Only include information that is explicitly mentioned. If something is not mentioned, 
#         use null or empty list. Be precise and extract exact numbers and descriptions.
#         """
    
#     def extract_from_text(self, text: str, context_type: str = "press_release") -> Dict:
#         """
#         Extract structured information from text using LLM
#         """
#         try:
#             # Truncate text if too long (LLM context window)
#             max_length = 8000
#             if len(text) > max_length:
#                 text = text[:max_length] + "\n... [truncated]"
            
#             # Prepare prompt
#             user_prompt = f"""
#             The following is a {context_type} from an IT company's earnings report.
#             Please extract all client wins, partnerships, and order book information.
            
#             Text:
#             {text}
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
            
#             # Validate structure
#             if 'deal_wins' not in result:
#                 result['deal_wins'] = []
#             if 'order_book' not in result:
#                 result['order_book'] = {}
#             if 'client_metrics' not in result:
#                 result['client_metrics'] = {}
            
#             logger.info(f"Extracted {len(result['deal_wins'])} deal wins")
#             return result
            
#         except Exception as e:
#             logger.error(f"LLM extraction failed: {e}")
#             return {
#                 'deal_wins': [],
#                 'order_book': {},
#                 'client_metrics': {},
#                 'error': str(e)
#             }
# 21/7/26 4:43pm working with investor presentations
# # extractors/llm_extractor.py (FIXED)
# import json
# import ollama
# from typing import Dict, List, Optional
# import logging

# logger = logging.getLogger(__name__)

# class LLMExtractor:
#     """Extract structured information using local LLM"""
    
#     def __init__(self, model: str = 'llama3.2:3b'):  # or 'gemma:2b'
#         self.model = model
#         self.system_prompt = """
#         You are a financial data extractor specializing in extracting client information 
#         and order book details from IT company earnings presentations and press releases.
        
#         Extract the following information:
#         1. **Client Wins/Partnerships**: For each client engagement mentioned, extract:
#            - client_description: Industry, location, size (e.g., "US-based bank")
#            - deal_details: What service/solution is being provided
#            - deal_value: TCV/contract value in $/INR with unit
#            - is_new_client: true/false
#            - industry: Sector (banking, retail, telecom, etc.)
#            - location: Geography (US, Europe, Asia, etc.)
        
#         2. **Order Book / TCV Metrics**:
#            - total_tcv: Total TCV for the quarter
#            - deal_count: Number of deals won
#            - large_deals: List of mega deals (>$50M)
#            - backlog: Order backlog if mentioned
        
#         3. **Client Metrics**:
#            - total_clients: Number of clients
#            - client_distribution: Distribution by revenue size
#            - concentration: Client concentration percentage
        
#         Return ONLY valid JSON. Do not include any other text.
#         """
    
#     def extract_from_text(self, text: str, context_type: str = "press_release") -> Dict:
#         """
#         Extract structured information from text using LLM
#         """
#         try:
#             # Truncate text if too long (LLM context window)
#             max_length = 8000
#             if len(text) > max_length:
#                 # Try to find key sections first
#                 text = self._extract_relevant_sections(text, max_length)
            
#             # Prepare prompt
#             user_prompt = f"""
#             The following is a {context_type} from an IT company's earnings report.
#             Please extract all client wins, partnerships, and order book information.
            
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
#                     "large_deals": ["deal1", "deal2"]
#                 }},
#                 "client_metrics": {{
#                     "total_clients": "string",
#                     "client_distribution": "string",
#                     "concentration": "string"
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
            
#             # Validate structure
#             if 'deal_wins' not in result:
#                 result['deal_wins'] = []
#             if 'order_book' not in result:
#                 result['order_book'] = {}
#             if 'client_metrics' not in result:
#                 result['client_metrics'] = {}
            
#             logger.info(f"Extracted {len(result['deal_wins'])} deal wins")
#             return result
            
#         except Exception as e:
#             logger.error(f"LLM extraction failed: {e}")
#             return {
#                 'deal_wins': [],
#                 'order_book': {},
#                 'client_metrics': {},
#                 'error': str(e)
#             }
    
#     def _extract_relevant_sections(self, text: str, max_length: int) -> str:
#         """Extract most relevant sections when text is too long"""
#         # Look for key sections
#         sections = []
#         keywords = ['TCV', 'deal', 'client', 'contract', 'agreement', 'win', 'partnership']
        
#         lines = text.split('\n')
#         relevant_lines = []
        
#         for i, line in enumerate(lines):
#             # Check if line contains keywords
#             if any(keyword.lower() in line.lower() for keyword in keywords):
#                 # Get context (surrounding lines)
#                 start = max(0, i - 2)
#                 end = min(len(lines), i + 3)
#                 relevant_lines.extend(lines[start:end])
        
#         # If we found relevant lines, use them
#         if relevant_lines:
#             extracted = '\n'.join(relevant_lines)
#             if len(extracted) > max_length:
#                 extracted = extracted[:max_length]
#             return extracted
        
#         # Fallback: first page and last few pages (often contain key metrics)
#         pages = text.split('--- Page')
#         if len(pages) > 3:
#             extracted = pages[0] + pages[-2] + pages[-1]
#             if len(extracted) > max_length:
#                 extracted = extracted[:max_length]
#             return extracted
        
#         # Last resort: truncate
#         return text[:max_length]

#earning transcripts support
# # extractors/llm_extractor.py (UPDATED for transcripts)
# import json
# import ollama
# from typing import Dict, List, Optional
# import logging
# import re

# logger = logging.getLogger(__name__)

# class LLMExtractor:
#     """Extract structured information from earnings call transcripts"""
    
#     def __init__(self, model: str = 'llama3.2:3b'):
#         self.model = model
#         self.system_prompt = """
#         You are a financial data extractor specializing in earnings call transcripts.
#         Extract the following information from the transcript:
        
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
    
#     def _extract_key_sections(self, text: str) -> str:
#         """Extract key sections from transcript"""
#         sections = []
        
#         # Look for prepared remarks (usually after "operational review" or "financial performance")
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
#                     sections.append('\n'.join(current_section))
#                 else:
#                     current_section.append(line)
        
#         # If no prepared remarks found, take first 500 lines (usually contains key info)
#         if not sections:
#             sections.append('\n'.join(lines[:500]))
        
#         # Also look for management commentary sections
#         for i, line in enumerate(lines):
#             if 'sudhir' in line.lower() or 'singh' in line.lower() or 'ceo' in line.lower():
#                 # Found CEO comments, capture around it
#                 start = max(0, i - 10)
#                 end = min(len(lines), i + 50)
#                 sections.append('\n'.join(lines[start:end]))
#                 break
        
#         return '\n\n'.join(sections)
    
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
#             # Remove extra spaces and normalize
#             result['order_book']['total_tcv'] = ' '.join(tcv.split())
            
# extractors/llm_extractor.py (COMPLETE FIXED VERSION)
import json
import ollama
from typing import Dict, List, Optional
import logging
import re

logger = logging.getLogger(__name__)

class LLMExtractor:
    """Extract structured information from earnings call transcripts and text"""
    
    def __init__(self, model: str = 'llama3.2:3b'):
        self.model = model
        self.system_prompt = """
        You are a financial data extractor specializing in earnings call transcripts and press releases.
        Extract the following information:
        
        1. **Deal Wins/Client Engagements**: For each deal mentioned, extract:
           - client_description: Industry, location, size (e.g., "US-based bank")
           - deal_details: What service/solution is being provided
           - deal_value: TCV/contract value if mentioned
           - is_new_client: true/false if specified
           - industry: Sector (banking, retail, telecom, healthcare, etc.)
           - location: Geography (US, Europe, Asia, UK, etc.)
        
        2. **Order Book / TCV Metrics**:
           - total_tcv: Total TCV for the quarter (exact number with unit)
           - deal_count: Number of deals won
           - large_deals: List of mega deals (>$50M)
           - order_book_value: 12-month executable order book if mentioned
        
        3. **Client Metrics**:
           - total_clients: Number of clients
           - client_distribution: Distribution by revenue size
           - concentration: Client concentration percentage
           - client_buckets: Client count by revenue range
        
        Return ONLY valid JSON. Do not include any other text.
        """
    
    def extract_from_transcript(self, text: str, company_name: str) -> Dict:
        """
        Extract structured information from earnings call transcript
        """
        try:
            # Extract key sections (prepared remarks and Q&A)
            key_sections = self._extract_key_sections(text)
            
            # Truncate if needed
            max_length = 8000
            if len(key_sections) > max_length:
                key_sections = key_sections[:max_length]
            
            # Prepare prompt
            user_prompt = f"""
            This is the earnings call transcript for {company_name}.
            Extract all deal wins, client information, and order book metrics.
            
            Pay special attention to:
            - Management's prepared remarks (usually at the start)
            - Any mention of "deal wins", "client wins", "contracts", "engagements"
            - TCV (Total Contract Value) or order book numbers
            - Client metrics by revenue size
            
            Transcript sections:
            {key_sections}
            
            Return ONLY valid JSON with this structure:
            {{
                "deal_wins": [
                    {{
                        "client_description": "string",
                        "deal_details": "string",
                        "deal_value": "string",
                        "is_new_client": boolean,
                        "industry": "string",
                        "location": "string"
                    }}
                ],
                "order_book": {{
                    "total_tcv": "string",
                    "deal_count": "string",
                    "large_deals": ["deal1", "deal2"],
                    "order_book_value": "string"
                }},
                "client_metrics": {{
                    "total_clients": "string",
                    "client_distribution": "string",
                    "concentration": "string",
                    "client_buckets": "string"
                }}
            }}
            """
            
            # Call LLM
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                format='json'
            )
            
            # Parse response
            result = json.loads(response['message']['content'])
            
            # Ensure required keys exist
            result.setdefault('deal_wins', [])
            result.setdefault('order_book', {})
            result.setdefault('client_metrics', {})
            
            # Post-process to clean up
            self._clean_extraction(result)
            
            logger.info(f"Extracted {len(result['deal_wins'])} deal wins for {company_name}")
            return result
            
        except Exception as e:
            logger.error(f"LLM extraction failed for {company_name}: {e}")
            return {
                'deal_wins': [],
                'order_book': {},
                'client_metrics': {},
                'error': str(e)
            }
    
    def extract_from_text(self, text: str, doc_type: str = "press_release") -> Dict:
        """
        Extract structured information from any text (press release, factsheet, etc.)
        """
        try:
            # Truncate if needed
            max_length = 8000
            if len(text) > max_length:
                text = self._extract_relevant_sections(text, max_length)
            
            # Prepare prompt based on document type
            if doc_type == "transcript":
                return self.extract_from_transcript(text, "Unknown")
            
            user_prompt = f"""
            This is a {doc_type} from an IT company.
            Extract all deal wins, client information, and order book metrics.
            
            Text:
            {text}
            
            Return ONLY valid JSON with this structure:
            {{
                "deal_wins": [
                    {{
                        "client_description": "string",
                        "deal_details": "string",
                        "deal_value": "string",
                        "is_new_client": boolean,
                        "industry": "string",
                        "location": "string"
                    }}
                ],
                "order_book": {{
                    "total_tcv": "string",
                    "deal_count": "string",
                    "large_deals": ["deal1", "deal2"],
                    "order_book_value": "string"
                }},
                "client_metrics": {{
                    "total_clients": "string",
                    "client_distribution": "string",
                    "concentration": "string",
                    "client_buckets": "string"
                }}
            }}
            """
            
            # Call LLM
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                format='json'
            )
            
            # Parse response
            result = json.loads(response['message']['content'])
            
            # Ensure required keys exist
            result.setdefault('deal_wins', [])
            result.setdefault('order_book', {})
            result.setdefault('client_metrics', {})
            
            self._clean_extraction(result)
            
            logger.info(f"Extracted {len(result['deal_wins'])} deal wins from {doc_type}")
            return result
            
        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
            return {
                'deal_wins': [],
                'order_book': {},
                'client_metrics': {},
                'error': str(e)
            }
    
    def _extract_key_sections(self, text: str) -> str:
        """Extract key sections from transcript"""
        sections = []
        
        # Look for prepared remarks
        prepared_patterns = [
            r'(?:operational|business|financial)\s+(?:review|performance|summary)',
            r'prepared\s+remarks',
            r'opening\s+comments'
        ]
        
        lines = text.split('\n')
        current_section = []
        in_prepared = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check if this is a prepared remarks section
            if any(re.search(pattern, line_lower, re.I) for pattern in prepared_patterns):
                in_prepared = True
                current_section = [line]
            elif in_prepared:
                # Stop at Q&A
                if 'question' in line_lower or 'answer' in line_lower or 'q&a' in line_lower:
                    in_prepared = False
                    if current_section:
                        sections.append('\n'.join(current_section))
                else:
                    current_section.append(line)
        
        # If no prepared remarks found, take first 500 lines (usually contains key info)
        if not sections:
            sections.append('\n'.join(lines[:500]))
        
        # Also look for management commentary sections
        for i, line in enumerate(lines):
            if 'ceo' in line.lower() or 'cfo' in line.lower() or 'md' in line.lower():
                if i < len(lines) - 50:
                    start = max(0, i - 10)
                    end = min(len(lines), i + 50)
                    sections.append('\n'.join(lines[start:end]))
                    break
        
        return '\n\n'.join(sections)
    
    def _extract_relevant_sections(self, text: str, max_length: int) -> str:
        """Extract most relevant sections when text is too long"""
        keywords = ['TCV', 'deal', 'client', 'contract', 'agreement', 'win', 'partnership']
        
        lines = text.split('\n')
        relevant_lines = []
        
        for i, line in enumerate(lines):
            if any(keyword.lower() in line.lower() for keyword in keywords):
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                relevant_lines.extend(lines[start:end])
        
        if relevant_lines:
            extracted = '\n'.join(relevant_lines)
            if len(extracted) > max_length:
                extracted = extracted[:max_length]
            return extracted
        
        # Fallback: first few pages
        pages = text.split('--- Page')
        if len(pages) > 2:
            extracted = pages[0] + pages[1] + pages[2]
            if len(extracted) > max_length:
                extracted = extracted[:max_length]
            return extracted
        
        return text[:max_length]
    
    def _clean_extraction(self, result: Dict):
        """Clean and validate extraction results"""
        # Clean deal wins
        if result.get('deal_wins'):
            for deal in result['deal_wins']:
                # Ensure boolean for is_new_client
                if 'is_new_client' in deal and isinstance(deal['is_new_client'], str):
                    deal['is_new_client'] = deal['is_new_client'].lower() in ['true', 'yes', 'new']
        
        # Clean TCV values
        if result.get('order_book', {}).get('total_tcv'):
            tcv = result['order_book']['total_tcv']
            result['order_book']['total_tcv'] = ' '.join(tcv.split())            