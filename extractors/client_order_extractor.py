# extractors/client_order_extractor.py
import re
import json
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ClientOrderExtractor:
    """Extract client and order book information from text"""
    
    def __init__(self):
        # Keywords for different sections
        self.section_keywords = {
            'deal_wins': [
                r'(?:deal|contract|agreement|engagement|partnership|selection|win)s?\s*(?:announced|signed|secured|won|selected)',
                r'(?:TCV|total contract value|deal value|contract value)',
                r'mega deal',
                r'large deal',
                r'deal(s)? worth'
            ],
            'client_info': [
                r'client',
                r'customer',
                r'partner',
                r'bank',
                r'insurance',
                r'retailer',
                r'manufacturer',
                r'telecommunications?',
                r'healthcare',
                r'energy',
                r'financial services?',
                r'government',
                r'U\.?S\.?-based',
                r'Europe-based',
                r'UK-based',
                r'Asia-based',
                r'Fortune 500',
                r'Global 2000',
                r'leading [\w\s]+ (?:bank|insurer|retailer|manufacturer)'
            ],
            'order_book': [
                r'TCV',
                r'total contract value',
                r'deal win(?:s)?',
                r'order inflow',
                r'bookings?',
                r'pipeline',
                r'backlog',
                r'unbilled revenue'
            ]
        }
        
        # TCV value patterns
        self.value_patterns = [
            r'\$\s*([\d,]+(?:\.[\d]+)?)\s*(?:billion|bn|million|mn|B|M)',
            r'INR\s*([\d,]+(?:\.[\d]+)?)\s*(?:crore|Cr)',
            r'([\d,]+(?:\.[\d]+)?)\s*(?:billion|bn|million|mn)\s*(?:USD|dollars|INR)?'
        ]
    
    def extract_sections(self, text: str) -> Dict:
        """Extract relevant sections from markdown text"""
        sections = {}
        
        # Find deal wins section
        deal_section = self._find_section(text, [
            r'deal wins?',
            r'deal(s)?? announcements?',
            r'contract awards?',
            r'key wins?',
            r'deal wins? highlight',
            r'significant deals?'
        ])
        if deal_section:
            sections['deal_wins'] = deal_section
        
        # Find client section
        client_section = self._find_section(text, [
            r'client',
            r'customer',
            r'clients? base',
            r'client metrics?',
            r'client relationships?'
        ])
        if client_section:
            sections['client_info'] = client_section
        
        # Find order book section
        order_section = self._find_section(text, [
            r'TCV',
            r'total contract value',
            r'order inflow',
            r'bookings?',
            r'order book'
        ])
        if order_section:
            sections['order_book'] = order_section
        
        # If no sections found, use entire document (fallback)
        if not sections:
            sections['full_text'] = text
            
        return sections
    
    def _find_section(self, text: str, patterns: List[str]) -> Optional[str]:
        """Find a section based on heading patterns"""
        lines = text.split('\n')
        section_lines = []
        found = False
        
        for i, line in enumerate(lines):
            if not found:
                for pattern in patterns:
                    if re.search(pattern, line, re.I):
                        found = True
                        section_lines.append(line)
                        break
            else:
                # Check if we've reached a new major section
                if re.match(r'^#{1,3}\s+[A-Z]', line) and i > 0:
                    break
                section_lines.append(line)
        
        return '\n'.join(section_lines) if section_lines else None
    
    def extract_tcv_values(self, text: str) -> List[Dict]:
        """Extract TCV values from text"""
        values = []
        
        for pattern in self.value_patterns:
            matches = re.finditer(pattern, text, re.I)
            for match in matches:
                value_str = match.group(1).replace(',', '')
                try:
                    value = float(value_str)
                    context = self._get_context(text, match.start(), 100)
                    
                    # Determine unit
                    unit = 'unknown'
                    if 'billion' in match.group(0).lower() or 'bn' in match.group(0).lower():
                        unit = 'billion'
                    elif 'million' in match.group(0).lower() or 'mn' in match.group(0).lower():
                        unit = 'million'
                    elif 'crore' in match.group(0).lower() or 'cr' in match.group(0).lower():
                        unit = 'crore'
                    
                    values.append({
                        'value': value,
                        'unit': unit,
                        'context': context[:200],
                        'matched_text': match.group(0)
                    })
                except:
                    continue
        
        return values
    
    def _get_context(self, text: str, position: int, window: int = 100) -> str:
        """Get context around a position"""
        start = max(0, position - window)
        end = min(len(text), position + window)
        return text[start:end]