# parsers/quarterly_parser.py
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class ScreenerQuarterlyParser:
    """Parse quarterly results from Screener.in"""
    
    @staticmethod
    def parse_quarterly_table(html_content: str) -> Dict:
        """
        Parse the quarterly results table from Screener.in
        Returns structured data with quarter labels and values
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the quarterly results section
        quarters_section = soup.find('section', {'id': 'quarters'})
        if not quarters_section:
            print("Quarterly results section not found")
            return {}
        
        # Find the data table
        table = quarters_section.find('table', class_='data-table')
        if not table:
            print("Data table not found")
            return {}
        
        # Extract quarter labels from thead
        quarter_labels = ScreenerQuarterlyParser._extract_quarter_labels(table)
        
        # Extract sales/revenue data
        sales_data = ScreenerQuarterlyParser._extract_row_data(table, 'Sales')
        
        # Extract net profit data
        profit_data = ScreenerQuarterlyParser._extract_row_data(table, 'Net Profit')
        
        # Extract operating profit
        operating_profit = ScreenerQuarterlyParser._extract_row_data(table, 'Operating Profit')
        
        # Get upcoming result date if available
        upcoming_result = ScreenerQuarterlyParser._extract_upcoming_result(quarters_section)
        
        return {
            'quarter_labels': quarter_labels,
            'sales': sales_data,
            'net_profit': profit_data,
            'operating_profit': operating_profit,
            'upcoming_result': upcoming_result,
            'last_quarter_index': len(quarter_labels) - 1 if quarter_labels else -1,
            'total_quarters': len(quarter_labels)
        }
    
    @staticmethod
    def _extract_quarter_labels(table) -> List[str]:
        """Extract quarter labels from table header"""
        thead = table.find('thead')
        if not thead:
            return []
        
        headers = thead.find_all('th')
        # Skip first column (which is the row label column)
        labels = []
        
        for th in headers[1:]:  # Skip the first empty/text header
            # Check for date-key attribute or text
            date_key = th.get('data-date-key')
            if date_key:
                # Convert YYYY-MM-DD to readable format
                try:
                    date_obj = datetime.strptime(date_key, '%Y-%m-%d')
                    labels.append(date_obj.strftime('%b %Y'))
                except ValueError:
                    labels.append(th.get_text(strip=True))
            else:
                text = th.get_text(strip=True)
                if text:
                    labels.append(text)
        
        return labels
    
    @staticmethod
    def _extract_row_data(table, row_label: str) -> Dict[str, float]:
        """
        Extract data for a specific row by label
        Returns dict mapping quarter label to value
        """
        tbody = table.find('tbody')
        if not tbody:
            return {}
        
        # Find the row containing the label
        # Look for exact match or partial match
        rows = tbody.find_all('tr')
        
        target_row = None
        for row in rows:
            # Check if the first cell contains our label
            first_cell = row.find('td', class_='text')
            if first_cell:
                row_text = first_cell.get_text(strip=True)
                # Handle cases where the label might be in a button
                button = first_cell.find('button')
                if button:
                    button_text = button.get_text(strip=True)
                    if row_label in button_text:
                        target_row = row
                        break
                elif row_label in row_text:
                    target_row = row
                    break
        
        if not target_row:
            print(f"Row '{row_label}' not found")
            return {}
        
        # Extract all data cells
        data_cells = target_row.find_all('td')[1:]  # Skip first cell
        
        # Get quarter labels (we need to map values to labels)
        # We'll use the headers from the table
        headers = table.find('thead').find_all('th')[1:]
        
        result = {}
        for idx, cell in enumerate(data_cells):
            if idx < len(headers):
                value_text = cell.get_text(strip=True)
                # Clean and convert to float
                clean_value = ScreenerQuarterlyParser._clean_number(value_text)
                if clean_value is not None:
                    label = headers[idx].get_text(strip=True)
                    # Convert to standard format if possible
                    try:
                        date_obj = datetime.strptime(label, '%b %Y')
                        result[label] = clean_value
                    except:
                        result[label] = clean_value
        
        return result
    
    @staticmethod
    def _extract_upcoming_result(section) -> Optional[str]:
        """Extract upcoming result date if present"""
        badge = section.find('span', class_='badge')
        if badge:
            text = badge.get_text(strip=True)
            match = re.search(r'(\d+\s+[A-Za-z]+\s+\d{4})', text)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def _clean_number(text: str) -> Optional[float]:
        """
        Clean number strings and convert to float
        Handles: commas, percentages, negative numbers
        """
        if not text or text.strip() == '-':
            return None
        
        # Remove whitespace
        text = text.strip()
        
        # Check if it's a percentage (like 27%)
        if text.endswith('%'):
            text = text[:-1].strip()
        
        # Remove commas and convert
        try:
            # Handle negative numbers
            if text.startswith('-'):
                text = text.replace(',', '')
                return float(text)
            else:
                text = text.replace(',', '')
                return float(text)
        except ValueError:
            # If it contains currency symbols or other text
            # Extract just the numbers
            numbers = re.findall(r'[\d,.]+', text)
            if numbers:
                try:
                    return float(numbers[0].replace(',', ''))
                except:
                    pass
            return None
    
    @staticmethod
    def get_latest_financial_year_data(quarterly_data: Dict) -> Dict:
        """
        Calculate financial year totals from quarterly data
        Returns revenue and profit for the latest completed financial year
        """
        if not quarterly_data or not quarterly_data.get('quarter_labels'):
            return {}
        
        # Get the last 4 quarters (assuming financial year ends in March)
        labels = quarterly_data['quarter_labels']
        sales = quarterly_data.get('sales', {})
        
        # Look for last 4 quarters ending in March
        # Screener data usually has 12 quarters (3 years)
        # We want the last completed financial year (Apr-Mar)
        
        # Find the last March quarter
        march_indices = [i for i, label in enumerate(labels) if 'Mar' in label]
        
        if not march_indices:
            # Fallback: take last 4 quarters
            return ScreenerQuarterlyParser._get_last_n_quarters(quarterly_data, 4)
        
        # Get the last March and take 4 quarters from there
        last_march_idx = march_indices[-1]
        start_idx = max(0, last_march_idx - 3)  # 4 quarters including March
        
        # Get data for these 4 quarters
        year_labels = labels[start_idx:last_march_idx + 1]
        year_sales = []
        year_profit = []
        
        for label in year_labels:
            if label in sales:
                year_sales.append(sales[label])
            
            # Also get net profit
            profit = quarterly_data.get('net_profit', {})
            if label in profit:
                year_profit.append(profit[label])
        
        return {
            'financial_year': f"{year_labels[0]} - {year_labels[-1]}" if year_labels else "Unknown",
            'total_revenue': sum(year_sales) if year_sales else None,
            'total_profit': sum(year_profit) if year_profit else None,
            'quarterly_breakdown': year_labels,
            'quarterly_revenue': year_sales,
            'quarterly_profit': year_profit
        }
    
    @staticmethod
    def _get_last_n_quarters(quarterly_data: Dict, n: int) -> Dict:
        """Get data for last N quarters"""
        labels = quarterly_data['quarter_labels']
        sales = quarterly_data.get('sales', {})
        
        last_n_labels = labels[-n:] if len(labels) >= n else labels
        last_n_sales = []
        
        for label in last_n_labels:
            if label in sales:
                last_n_sales.append(sales[label])
        
        return {
            'financial_year': f"Last {n} quarters",
            'total_revenue': sum(last_n_sales) if last_n_sales else None,
            'total_profit': None,
            'quarterly_breakdown': last_n_labels,
            'quarterly_revenue': last_n_sales,
            'quarterly_profit': []
        }