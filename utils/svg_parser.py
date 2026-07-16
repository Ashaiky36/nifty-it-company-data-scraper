# utils/svg_parser.py
from bs4 import BeautifulSoup
import re
from typing import List, Tuple, Optional

class MoneycontrolSVGParser:
    """Parse SVG chart data from Moneycontrol HTML"""
    
    @staticmethod
    def extract_revenue_data(html_content: str) -> Tuple[List[str], List[float]]:
        """
        Extract quarter labels and revenue values from SVG chart.
        Returns: (quarters_list, revenue_list) as tuples of aligned data
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Strategy: Find all SVG text elements that look like revenue numbers
        # Highcharts typically wraps numbers in <tspan> with specific styling
        
        # Look for the main chart container
        chart_containers = soup.find_all('div', class_=re.compile(r'highcharts.*?chart'))
        
        if not chart_containers:
            # Fallback: search for SVG elements directly
            return MoneycontrolSVGParser._extract_from_svg(soup)
        
        # Extract from the most relevant chart container (usually first or largest)
        for container in chart_containers:
            try:
                quarters, revenues = MoneycontrolSVGParser._extract_from_container(container)
                if quarters and revenues:
                    return quarters, revenues
            except Exception as e:
                print(f"Error parsing container: {e}")
                continue
        
        # If no structured container found, try general SVG search
        return MoneycontrolSVGParser._extract_from_svg(soup)
    
    @staticmethod
    def _extract_from_container(container) -> Tuple[List[str], List[float]]:
        """Extract data from a specific chart container"""
        
        # Find all text elements
        all_text_elements = container.find_all('text')
        
        quarters = []
        revenues = []
        
        for text_elem in all_text_elements:
            # Get all tspan elements within this text element
            tspans = text_elem.find_all('tspan')
            
            for tspan in tspans:
                text_content = tspan.get_text(strip=True)
                
                # Check if it's a quarter (pattern like "Dec 25", "Mar 26", "Q3 2025")
                if re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{2}$', text_content):
                    # Convert "Dec 25" to "Dec 2025" format
                    quarter = text_content.replace(' ', ' 20')  # Simple conversion
                    quarters.append(quarter)
                    
                # Check if it's a revenue number (large digits, often with commas)
                elif re.match(r'^[\d,]+$', text_content) and len(text_content.replace(',', '')) >= 4:
                    # Clean and convert to float
                    clean_num = text_content.replace(',', '')
                    revenue = float(clean_num)
                    revenues.append(revenue)
        
        # If we have both quarters and revenues, align them
        if quarters and revenues:
            # Sometimes the numbers appear before the labels, so ensure alignment
            # We want to pair by visual position (left-to-right)
            
            # Sort both lists by their visual position
            # For simplicity, we'll assume the HTML order matches visual order
            return quarters[-3:], revenues[-3:]  # Last 3 quarters
            
        return [], []
    
    @staticmethod
    def _extract_from_svg(soup: BeautifulSoup) -> Tuple[List[str], List[float]]:
        """Fallback: Extract directly from SVG elements"""
        quarters = []
        revenues = []
        
        # Find all tspan elements
        tspans = soup.find_all('tspan')
        
        # Track which elements have the highcharts-text-outline class (often numbers)
        for tspan in tspans:
            text = tspan.get_text(strip=True)
            
            # Skip empty or very short text
            if len(text) < 2:
                continue
                
            # Check for quarter patterns
            if re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{2}$', text):
                quarters.append(text.replace(' ', ' 20'))
                
            # Check for revenue numbers (4+ digits or with commas)
            elif re.match(r'^[\d,]+$', text) and len(text.replace(',', '')) >= 4:
                clean_num = text.replace(',', '')
                revenues.append(float(clean_num))
        
        # Return last 3 values if both lists have data
        if quarters and revenues:
            # Trim to last 3 values
            return quarters[-3:], revenues[-3:]
        
        return [], []