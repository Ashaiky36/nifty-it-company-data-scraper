# scrapers/revenue_scraper.py
from scrapers.base_scraper import BaseScraper
from utils.svg_parser import MoneycontrolSVGParser
from typing import Dict, List, Optional
import re

class RevenueScraper(BaseScraper):
    """Scrape revenue and quarterly data from Moneycontrol"""
    
    def __init__(self):
        super().__init__()
        self.svg_parser = MoneycontrolSVGParser()
        
    def scrape_company_revenue(self, company_code: str, url: str) -> Dict:
        """
        Scrape revenue data for a specific company
        Args:
            company_code: Ticker symbol (e.g., 'TCS')
            url: Moneycontrol financials URL
        Returns:
            Dict with quarterly data
        """
        try:
            response = self.get(url)
            
            # Extract revenue data from SVG
            quarters, revenues = self.svg_parser.extract_revenue_data(response.text)
            
            if not quarters or not revenues:
                print(f"Warning: No revenue data found for {company_code}")
                return self._get_empty_revenue_data()
            
            # Structure the data
            revenue_data = {
                'company': company_code,
                'recent_revenue': revenues[-1] if revenues else None,  # Most recent quarter
                'quarter_labels': quarters,
                'quarterly_revenues': revenues,
                'last_3_quarters_summary': self._format_quarterly_summary(quarters, revenues)
            }
            
            return revenue_data
            
        except Exception as e:
            print(f"Error scraping {company_code}: {e}")
            return self._get_empty_revenue_data()
    
    def _format_quarterly_summary(self, quarters: List[str], revenues: List[float]) -> str:
        """Format last 3 quarters as a readable summary"""
        if len(quarters) < 3 or len(revenues) < 3:
            return "Insufficient data"
        
        # Take last 3
        last_3_quarters = quarters[-3:]
        last_3_revenues = revenues[-3:]
        
        summary_parts = []
        for q, r in zip(last_3_quarters, last_3_revenues):
            formatted_revenue = f"₹{r:,.2f} Cr"
            summary_parts.append(f"{q}: {formatted_revenue}")
        
        return " | ".join(summary_parts)
    
    def _get_empty_revenue_data(self) -> Dict:
        """Return empty data structure"""
        return {
            'company': None,
            'recent_revenue': None,
            'quarter_labels': [],
            'quarterly_revenues': [],
            'last_3_quarters_summary': 'Data not available'
        }