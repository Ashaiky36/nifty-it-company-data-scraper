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

# extractors/llm_extractor.py (FIXED)
import json
import ollama
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class LLMExtractor:
    """Extract structured information using local LLM"""
    
    def __init__(self, model: str = 'llama3.2:3b'):  # or 'gemma:2b'
        self.model = model
        self.system_prompt = """
        You are a financial data extractor specializing in extracting client information 
        and order book details from IT company earnings presentations and press releases.
        
        Extract the following information:
        1. **Client Wins/Partnerships**: For each client engagement mentioned, extract:
           - client_description: Industry, location, size (e.g., "US-based bank")
           - deal_details: What service/solution is being provided
           - deal_value: TCV/contract value in $/INR with unit
           - is_new_client: true/false
           - industry: Sector (banking, retail, telecom, etc.)
           - location: Geography (US, Europe, Asia, etc.)
        
        2. **Order Book / TCV Metrics**:
           - total_tcv: Total TCV for the quarter
           - deal_count: Number of deals won
           - large_deals: List of mega deals (>$50M)
           - backlog: Order backlog if mentioned
        
        3. **Client Metrics**:
           - total_clients: Number of clients
           - client_distribution: Distribution by revenue size
           - concentration: Client concentration percentage
        
        Return ONLY valid JSON. Do not include any other text.
        """
    
    def extract_from_text(self, text: str, context_type: str = "press_release") -> Dict:
        """
        Extract structured information from text using LLM
        """
        try:
            # Truncate text if too long (LLM context window)
            max_length = 8000
            if len(text) > max_length:
                # Try to find key sections first
                text = self._extract_relevant_sections(text, max_length)
            
            # Prepare prompt
            user_prompt = f"""
            The following is a {context_type} from an IT company's earnings report.
            Please extract all client wins, partnerships, and order book information.
            
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
                    "large_deals": ["deal1", "deal2"]
                }},
                "client_metrics": {{
                    "total_clients": "string",
                    "client_distribution": "string",
                    "concentration": "string"
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
            
            # Validate structure
            if 'deal_wins' not in result:
                result['deal_wins'] = []
            if 'order_book' not in result:
                result['order_book'] = {}
            if 'client_metrics' not in result:
                result['client_metrics'] = {}
            
            logger.info(f"Extracted {len(result['deal_wins'])} deal wins")
            return result
            
        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
            return {
                'deal_wins': [],
                'order_book': {},
                'client_metrics': {},
                'error': str(e)
            }
    
    def _extract_relevant_sections(self, text: str, max_length: int) -> str:
        """Extract most relevant sections when text is too long"""
        # Look for key sections
        sections = []
        keywords = ['TCV', 'deal', 'client', 'contract', 'agreement', 'win', 'partnership']
        
        lines = text.split('\n')
        relevant_lines = []
        
        for i, line in enumerate(lines):
            # Check if line contains keywords
            if any(keyword.lower() in line.lower() for keyword in keywords):
                # Get context (surrounding lines)
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                relevant_lines.extend(lines[start:end])
        
        # If we found relevant lines, use them
        if relevant_lines:
            extracted = '\n'.join(relevant_lines)
            if len(extracted) > max_length:
                extracted = extracted[:max_length]
            return extracted
        
        # Fallback: first page and last few pages (often contain key metrics)
        pages = text.split('--- Page')
        if len(pages) > 3:
            extracted = pages[0] + pages[-2] + pages[-1]
            if len(extracted) > max_length:
                extracted = extracted[:max_length]
            return extracted
        
        # Last resort: truncate
        return text[:max_length]