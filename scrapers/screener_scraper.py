# scrapers/screener_scraper.py
from scrapers.base_scraper import BaseScraper
from parsers.quarterly_parser import ScreenerQuarterlyParser
from typing import Dict, Optional, List
import re

class ScreenerScraper(BaseScraper):
    """Scrape financial data from Screener.in"""
    
    def __init__(self):
        super().__init__()
        self.parser = ScreenerQuarterlyParser()
        
        # Add specific headers for Screener
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def scrape_company(self, company_name: str, company_code: str, url: str) -> Dict:
        """
        Scrape all relevant data for a company
        """
        print(f"Scraping {company_name} ({company_code})...")
        
        try:
            response = self.get(url)
            
            # Parse quarterly data
            quarterly_data = self.parser.parse_quarterly_table(response.text)
            
            if not quarterly_data:
                print(f"Warning: No quarterly data found for {company_name}")
                return self._get_empty_result(company_name, company_code)
            
            # Get latest financial year data
            annual_data = self.parser.get_latest_financial_year_data(quarterly_data)
            
            # Extract last 3 quarters summary
            last_3_summary = self._get_last_3_quarters_summary(quarterly_data)
            
            # Get current quarter revenue
            current_revenue = self._get_current_quarter_revenue(quarterly_data)
            
            return {
                'company_name': company_name,
                'company_code': company_code,
                'current_quarter_revenue': current_revenue,
                'last_3_quarters_summary': last_3_summary,
                'annual_revenue': annual_data.get('total_revenue'),
                'annual_profit': annual_data.get('total_profit'),
                'financial_year': annual_data.get('financial_year'),
                'quarterly_labels': quarterly_data.get('quarter_labels', []),
                'quarterly_sales': list(quarterly_data.get('sales', {}).values()),
                'quarterly_profits': list(quarterly_data.get('net_profit', {}).values()),
                'upcoming_result': quarterly_data.get('upcoming_result'),
                'total_quarters': quarterly_data.get('total_quarters', 0),
                'raw_data': quarterly_data  # Keep for debugging
            }
            
        except Exception as e:
            print(f"Error scraping {company_name}: {e}")
            return self._get_empty_result(company_name, company_code)
    
    def _get_last_3_quarters_summary(self, quarterly_data: Dict) -> str:
        """Generate summary string for last 3 quarters"""
        labels = quarterly_data.get('quarter_labels', [])
        sales = quarterly_data.get('sales', {})
        
        if len(labels) < 3:
            return "Insufficient data"
        
        # Get last 3 labels
        last_3_labels = labels[-3:]
        summary_parts = []
        
        for label in last_3_labels:
            if label in sales:
                value = sales[label]
                summary_parts.append(f"{label}: ₹{value:,.2f} Cr")
            else:
                summary_parts.append(f"{label}: N/A")
        
        return " | ".join(summary_parts)
    
    def _get_current_quarter_revenue(self, quarterly_data: Dict) -> Optional[float]:
        """Get revenue for the current/most recent quarter"""
        labels = quarterly_data.get('quarter_labels', [])
        sales = quarterly_data.get('sales', {})
        
        if not labels or not sales:
            return None
        
        # Get the most recent quarter
        latest_label = labels[-1]
        return sales.get(latest_label)
    
    def _get_empty_result(self, company_name: str, company_code: str) -> Dict:
        """Return empty result structure"""
        return {
            'company_name': company_name,
            'company_code': company_code,
            'current_quarter_revenue': None,
            'last_3_quarters_summary': 'Data not available',
            'annual_revenue': None,
            'annual_profit': None,
            'financial_year': None,
            'quarterly_labels': [],
            'quarterly_sales': [],
            'quarterly_profits': [],
            'upcoming_result': None,
            'total_quarters': 0,
            'raw_data': {}
        }