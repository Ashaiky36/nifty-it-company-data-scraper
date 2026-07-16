# # # main.py
# # from scrapers.screener_scraper import ScreenerScraper
# # from config.companies import NIFTY_IT_COMPANIES
# # import pandas as pd
# # from datetime import datetime
# # import json
# # from typing import List, Dict
# # import logging

# # # Setup logging
# # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# # logger = logging.getLogger(__name__)

# # class NiftyITScraper:
# #     """Main orchestrator for scraping NIFTY IT companies"""
    
# #     def __init__(self):
# #         self.scraper = ScreenerScraper()
# #         self.results = []
    
# #     def scrape_all_companies(self) -> List[Dict]:
# #         """Scrape all companies in the NIFTY IT index"""
# #         logger.info(f"Starting scrape of {len(NIFTY_IT_COMPANIES)} NIFTY IT companies")
        
# #         for company in NIFTY_IT_COMPANIES:
# #             try:
# #                 result = self.scraper.scrape_company(
# #                     company['name'],
# #                     company['code'],
# #                     company['screener_url']
# #                 )
# #                 self.results.append(result)
# #                 logger.info(f"✓ Completed: {company['name']}")
# #             except Exception as e:
# #                 logger.error(f"✗ Failed: {company['name']} - {e}")
# #                 # Add error entry
# #                 self.results.append({
# #                     'company_name': company['name'],
# #                     'company_code': company['code'],
# #                     'current_quarter_revenue': None,
# #                     'last_3_quarters_summary': f'Error: {str(e)[:50]}',
# #                     'annual_revenue': None,
# #                     'annual_profit': None,
# #                     'financial_year': None,
# #                     'quarterly_labels': [],
# #                     'quarterly_sales': [],
# #                     'quarterly_profits': [],
# #                     'upcoming_result': None,
# #                     'total_quarters': 0,
# #                     'raw_data': {}
# #                 })
        
# #         return self.results
    
# #     def generate_summary(self) -> Dict:
# #         """Generate summary statistics"""
# #         successful = sum(1 for r in self.results if r['current_quarter_revenue'] is not None)
# #         total = len(self.results)
        
# #         revenues = [r['current_quarter_revenue'] for r in self.results if r['current_quarter_revenue'] is not None]
        
# #         return {
# #             'total_companies': total,
# #             'successful_scrapes': successful,
# #             'failed_scrapes': total - successful,
# #             'success_rate': (successful / total * 100) if total > 0 else 0,
# #             'avg_current_revenue': sum(revenues) / len(revenues) if revenues else 0,
# #             'max_revenue': max(revenues) if revenues else 0,
# #             'min_revenue': min(revenues) if revenues else 0
# #         }
    
# #     def save_to_excel(self, filename: str = None):
# #         """Save results to Excel file"""
# #         if not filename:
# #             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
# #             filename = f'output/nifty_it_data_{timestamp}.xlsx'
        
# #         # Prepare data for Excel
# #         excel_data = []
# #         for result in self.results:
# #             excel_data.append({
# #                 'Company Name': result['company_name'],
# #                 'Ticker': result['company_code'],
# #                 'Current Quarter Revenue (Cr)': result['current_quarter_revenue'],
# #                 'Last 3 Quarters Summary': result['last_3_quarters_summary'],
# #                 'Annual Revenue (Cr)': result['annual_revenue'],
# #                 'Annual Profit (Cr)': result['annual_profit'],
# #                 'Financial Year': result['financial_year'],
# #                 'Upcoming Result Date': result['upcoming_result'],
# #                 'Total Quarters Available': result['total_quarters']
# #             })
        
# #         df = pd.DataFrame(excel_data)
# #         # Ensure output directory exists
# #         os.makedirs(os.path.dirname(filename), exist_ok=True)
        
# #         # Create Excel writer with formatting
# #         with pd.ExcelWriter(filename, engine='openpyxl') as writer:
# #             # Main data sheet
# #             df.to_excel(writer, sheet_name='Summary', index=False)
            
# #             # Detailed data sheet
# #             detailed_data = []
# #             for result in self.results:
# #                 if result['quarterly_labels']:
# #                     for label, sales, profit in zip(
# #                         result['quarterly_labels'],
# #                         result['quarterly_sales'] + [None] * (len(result['quarterly_labels']) - len(result['quarterly_sales'])),
# #                         result['quarterly_profits'] + [None] * (len(result['quarterly_labels']) - len(result['quarterly_profits']))
# #                     ):
# #                         detailed_data.append({
# #                             'Company': result['company_name'],
# #                             'Quarter': label,
# #                             'Revenue (Cr)': sales,
# #                             'Profit (Cr)': profit
# #                         })
            
# #             if detailed_data:
# #                 df_detailed = pd.DataFrame(detailed_data)
# #                 df_detailed.to_excel(writer, sheet_name='Quarterly Details', index=False)
            
# #             # Auto-adjust column widths for both sheets
# #             for sheet_name in writer.sheets:
# #                 worksheet = writer.sheets[sheet_name]
# #                 for column in worksheet.columns:
# #                     max_length = 0
# #                     column_letter = column[0].column_letter
# #                     for cell in column:
# #                         try:
# #                             if len(str(cell.value)) > max_length:
# #                                 max_length = len(str(cell.value))
# #                         except:
# #                             pass
# #                     adjusted_width = min(max_length + 2, 50)
# #                     worksheet.column_dimensions[column_letter].width = adjusted_width
        
# #         logger.info(f"Data saved to {filename}")
# #         return filename

# # def main():
# #     """Main execution"""
# #     print("=" * 70)
# #     print("NIFTY IT Financial Data Scraper")
# #     print("Source: Screener.in")
# #     print("=" * 70)
    
# #     scraper = NiftyITScraper()
    
# #     # Scrape all companies
# #     results = scraper.scrape_all_companies()
    
# #     # Generate summary
# #     summary = scraper.generate_summary()
    
# #     # Save to Excel
# #     filename = scraper.save_to_excel()
    
# #     # Print summary
# #     print("\n" + "=" * 70)
# #     print("SCRAPING SUMMARY")
# #     print("=" * 70)
# #     print(f"Total Companies: {summary['total_companies']}")
# #     print(f"✓ Successful: {summary['successful_scrapes']}")
# #     print(f"✗ Failed: {summary['failed_scrapes']}")
# #     print(f"Success Rate: {summary['success_rate']:.1f}%")
# #     print(f"\nAverage Current Revenue: ₹{summary['avg_current_revenue']:,.2f} Cr")
# #     print(f"Max Current Revenue: ₹{summary['max_revenue']:,.2f} Cr")
# #     print(f"Min Current Revenue: ₹{summary['min_revenue']:,.2f} Cr")
# #     print(f"\nData saved to: {filename}")
    
# #     # Show first few results
# #     print("\nSample Data:")
# #     print("-" * 70)
# #     for result in results[:5]:
# #         print(f"{result['company_name']:30} | "
# #               f"Revenue: ₹{result['current_quarter_revenue']:>12,.2f} Cr | "
# #               f"FY: {result['financial_year'] or 'N/A'}")

# # if __name__ == "__main__":
# #     main()

# # main.py (updated version)
# from scrapers.screener_scraper import ScreenerScraper
# from config.companies import NIFTY_IT_COMPANIES
# import pandas as pd
# from datetime import datetime
# import json
# from typing import List, Dict
# import logging
# import os  # Add this import

# # Setup logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# class NiftyITScraper:
#     """Main orchestrator for scraping NIFTY IT companies"""
    
#     def __init__(self):
#         self.scraper = ScreenerScraper()
#         self.results = []
    
#     def scrape_all_companies(self) -> List[Dict]:
#         """Scrape all companies in the NIFTY IT index"""
#         logger.info(f"Starting scrape of {len(NIFTY_IT_COMPANIES)} NIFTY IT companies")
        
#         for company in NIFTY_IT_COMPANIES:
#             try:
#                 result = self.scraper.scrape_company(
#                     company['name'],
#                     company['code'],
#                     company['screener_url']
#                 )
#                 self.results.append(result)
#                 logger.info(f"✓ Completed: {company['name']}")
#             except Exception as e:
#                 logger.error(f"✗ Failed: {company['name']} - {e}")
#                 # Add error entry
#                 self.results.append({
#                     'company_name': company['name'],
#                     'company_code': company['code'],
#                     'current_quarter_revenue': None,
#                     'last_3_quarters_summary': f'Error: {str(e)[:50]}',
#                     'annual_revenue': None,
#                     'annual_profit': None,
#                     'financial_year': None,
#                     'quarterly_labels': [],
#                     'quarterly_sales': [],
#                     'quarterly_profits': [],
#                     'upcoming_result': None,
#                     'total_quarters': 0,
#                     'raw_data': {}
#                 })
        
#         return self.results
    
#     def generate_summary(self) -> Dict:
#         """Generate summary statistics"""
#         successful = sum(1 for r in self.results if r['current_quarter_revenue'] is not None)
#         total = len(self.results)
        
#         revenues = [r['current_quarter_revenue'] for r in self.results if r['current_quarter_revenue'] is not None]
        
#         return {
#             'total_companies': total,
#             'successful_scrapes': successful,
#             'failed_scrapes': total - successful,
#             'success_rate': (successful / total * 100) if total > 0 else 0,
#             'avg_current_revenue': sum(revenues) / len(revenues) if revenues else 0,
#             'max_revenue': max(revenues) if revenues else 0,
#             'min_revenue': min(revenues) if revenues else 0
#         }
    
#     def save_to_excel(self, filename: str = None):
#         """Save results to Excel file"""
#         # Create output directory if it doesn't exist
#         output_dir = 'output'
#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)
#             logger.info(f"Created output directory: {output_dir}")
        
#         if not filename:
#             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#             filename = os.path.join(output_dir, f'nifty_it_data_{timestamp}.xlsx')
        
#         # Prepare data for Excel
#         excel_data = []
#         for result in self.results:
#             excel_data.append({
#                 'Company Name': result['company_name'],
#                 'Ticker': result['company_code'],
#                 'Current Quarter Revenue (Cr)': result['current_quarter_revenue'],
#                 'Last 3 Quarters Summary': result['last_3_quarters_summary'],
#                 'Annual Revenue (Cr)': result['annual_revenue'],
#                 'Annual Profit (Cr)': result['annual_profit'],
#                 'Financial Year': result['financial_year'],
#                 'Upcoming Result Date': result['upcoming_result'],
#                 'Total Quarters Available': result['total_quarters']
#             })
        
#         df = pd.DataFrame(excel_data)
        
#         # Create Excel writer with formatting
#         with pd.ExcelWriter(filename, engine='openpyxl') as writer:
#             # Main data sheet
#             df.to_excel(writer, sheet_name='Summary', index=False)
            
#             # Detailed data sheet
#             detailed_data = []
#             for result in self.results:
#                 if result['quarterly_labels']:
#                     # Pad lists to equal length
#                     labels = result['quarterly_labels']
#                     sales = result['quarterly_sales'] + [None] * (len(labels) - len(result['quarterly_sales']))
#                     profits = result['quarterly_profits'] + [None] * (len(labels) - len(result['quarterly_profits']))
                    
#                     for label, sales_val, profit_val in zip(labels, sales, profits):
#                         detailed_data.append({
#                             'Company': result['company_name'],
#                             'Quarter': label,
#                             'Revenue (Cr)': sales_val,
#                             'Profit (Cr)': profit_val
#                         })
            
#             if detailed_data:
#                 df_detailed = pd.DataFrame(detailed_data)
#                 df_detailed.to_excel(writer, sheet_name='Quarterly Details', index=False)
            
#             # Auto-adjust column widths for both sheets
#             for sheet_name in writer.sheets:
#                 worksheet = writer.sheets[sheet_name]
#                 for column in worksheet.columns:
#                     max_length = 0
#                     column_letter = column[0].column_letter
#                     for cell in column:
#                         try:
#                             if len(str(cell.value)) > max_length:
#                                 max_length = len(str(cell.value))
#                         except:
#                             pass
#                     adjusted_width = min(max_length + 2, 50)
#                     worksheet.column_dimensions[column_letter].width = adjusted_width
        
#         logger.info(f"Data saved to {filename}")
#         return filename

# def main():
#     """Main execution"""
#     print("=" * 70)
#     print("NIFTY IT Financial Data Scraper")
#     print("Source: Screener.in")
#     print("=" * 70)
    
#     scraper = NiftyITScraper()
    
#     # Scrape all companies
#     results = scraper.scrape_all_companies()
    
#     # Generate summary
#     summary = scraper.generate_summary()
    
#     # Save to Excel
#     filename = scraper.save_to_excel()
    
#     # Print summary
#     print("\n" + "=" * 70)
#     print("SCRAPING SUMMARY")
#     print("=" * 70)
#     print(f"Total Companies: {summary['total_companies']}")
#     print(f"✓ Successful: {summary['successful_scrapes']}")
#     print(f"✗ Failed: {summary['failed_scrapes']}")
#     print(f"Success Rate: {summary['success_rate']:.1f}%")
#     print(f"\nAverage Current Revenue: ₹{summary['avg_current_revenue']:,.2f} Cr")
#     print(f"Max Current Revenue: ₹{summary['max_revenue']:,.2f} Cr")
#     print(f"Min Current Revenue: ₹{summary['min_revenue']:,.2f} Cr")
#     print(f"\nData saved to: {filename}")
    
#     # Show first few results
#     print("\nSample Data:")
#     print("-" * 70)
#     for result in results[:5]:
#         print(f"{result['company_name']:30} | "
#               f"Revenue: ₹{result['current_quarter_revenue']:>12,.2f} Cr | "
#               f"FY: {result['financial_year'] or 'N/A'}")

# if __name__ == "__main__":
#     main()

# main.py (updated with services)
# from scrapers.screener_scraper import ScreenerScraper
# from scrapers.service_scraper import ServiceScraper
# from config.companies import NIFTY_IT_COMPANIES
# import pandas as pd
# from datetime import datetime
# import logging
# import os

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# class NiftyITScraper:
#     """Main orchestrator for scraping NIFTY IT companies"""
    
#     def __init__(self):
#         self.screener_scraper = ScreenerScraper()
#         self.service_scraper = ServiceScraper()
#         self.results = []
    
#     def scrape_all_companies(self):
#         """Scrape all companies with both financial and service data"""
#         logger.info(f"Starting scrape of {len(NIFTY_IT_COMPANIES)} NIFTY IT companies")
        
#         for company in NIFTY_IT_COMPANIES:
#             try:
#                 # Get financial data from Screener
#                 financial_data = self.screener_scraper.scrape_company(
#                     company['name'],
#                     company['code'],
#                     company['screener_url']
#                 )
                
#                 # Get services/products data
#                 services_data = self.service_scraper.scrape_company_services(company)
                
#                 # Combine results
#                 result = {
#                     **financial_data,
#                     'services_products': self.service_scraper.format_services_for_excel(services_data),
#                     'services_categories': services_data.get('categories', []),
#                     'total_service_categories': services_data.get('total_categories', 0)
#                 }
                
#                 self.results.append(result)
#                 logger.info(f"✓ Completed: {company['name']}")
                
#             except Exception as e:
#                 logger.error(f"✗ Failed: {company['name']} - {e}")
#                 self.results.append({
#                     'company_name': company['name'],
#                     'company_code': company['code'],
#                     'current_quarter_revenue': None,
#                     'last_3_quarters_summary': f'Error: {str(e)[:50]}',
#                     'annual_revenue': None,
#                     'annual_profit': None,
#                     'financial_year': None,
#                     'quarterly_labels': [],
#                     'quarterly_sales': [],
#                     'quarterly_profits': [],
#                     'upcoming_result': None,
#                     'total_quarters': 0,
#                     'services_products': 'Data not available',
#                     'services_categories': [],
#                     'total_service_categories': 0
#                 })
        
#         return self.results
    
#     def save_to_excel(self, filename: str = None):
#         """Save results to Excel file with services data"""
#         output_dir = 'output'
#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)
        
#         if not filename:
#             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#             filename = os.path.join(output_dir, f'nifty_it_data_{timestamp}.xlsx')
        
#         # Prepare summary data
#         summary_data = []
#         for result in self.results:
#             summary_data.append({
#                 'Company Name': result['company_name'],
#                 'Ticker': result['company_code'],
#                 'Current Revenue (Cr)': result.get('current_quarter_revenue'),
#                 'Annual Revenue (Cr)': result.get('annual_revenue'),
#                 'Annual Profit (Cr)': result.get('annual_profit'),
#                 'Financial Year': result.get('financial_year'),
#                 'Services/Products': result.get('services_products', 'N/A'),
#                 'Total Service Categories': result.get('total_service_categories', 0),
#                 'Upcoming Result': result.get('upcoming_result')
#             })
        
#         df_summary = pd.DataFrame(summary_data)
        
#         with pd.ExcelWriter(filename, engine='openpyxl') as writer:
#             # Summary sheet
#             df_summary.to_excel(writer, sheet_name='Summary', index=False)
            
#             # Quarterly details
#             detailed_data = []
#             for result in self.results:
#                 if result.get('quarterly_labels'):
#                     for idx, label in enumerate(result['quarterly_labels']):
#                         revenue = result['quarterly_sales'][idx] if idx < len(result['quarterly_sales']) else None
#                         profit = result['quarterly_profits'][idx] if idx < len(result['quarterly_profits']) else None
#                         detailed_data.append({
#                             'Company': result['company_name'],
#                             'Quarter': label,
#                             'Revenue (Cr)': revenue,
#                             'Profit (Cr)': profit
#                         })
            
#             if detailed_data:
#                 df_detailed = pd.DataFrame(detailed_data)
#                 df_detailed.to_excel(writer, sheet_name='Quarterly Details', index=False)
            
#             # Auto-adjust column widths
#             for sheet_name in writer.sheets:
#                 worksheet = writer.sheets[sheet_name]
#                 for column in worksheet.columns:
#                     max_length = 0
#                     column_letter = column[0].column_letter
#                     for cell in column:
#                         try:
#                             cell_length = len(str(cell.value))
#                             if cell_length > max_length:
#                                 max_length = cell_length
#                         except:
#                             pass
#                     adjusted_width = min(max_length + 2, 60)
#                     worksheet.column_dimensions[column_letter].width = adjusted_width
        
#         logger.info(f"Data saved to {filename}")
#         return filename

# def main():
#     """Main execution"""
#     print("=" * 70)
#     print("NIFTY IT Financial & Services Data Scraper")
#     print("Sources: Screener.in, Company Sitemaps")
#     print("=" * 70)
    
#     scraper = NiftyITScraper()
    
#     # Scrape all companies
#     results = scraper.scrape_all_companies()
    
#     # Save to Excel
#     filename = scraper.save_to_excel()
    
#     print(f"\n✅ Data saved to: {filename}")
#     print("\n" + "=" * 70)
#     print("SUMMARY")
#     print("=" * 70)
#     print(f"Total Companies: {len(results)}")
#     print(f"Companies with service data: {sum(1 for r in results if r.get('services_categories'))}")
#     print(f"Companies with financial data: {sum(1 for r in results if r.get('current_quarter_revenue'))}")
    
# if __name__ == "__main__":
#     main()

# main.py (ENHANCED)
from scrapers.screener_scraper import ScreenerScraper
from scrapers.service_scraper import ServiceScraper
from config.companies import NIFTY_IT_COMPANIES
import pandas as pd
from datetime import datetime
import logging
import os
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NiftyITScraper:
    """Main orchestrator for scraping NIFTY IT companies"""
    
    def __init__(self):
        self.screener_scraper = ScreenerScraper()
        self.service_scraper = ServiceScraper()
        self.results = []
    
    def scrape_all_companies(self):
        """Scrape all companies with both financial and service data"""
        logger.info(f"Starting scrape of {len(NIFTY_IT_COMPANIES)} NIFTY IT companies")
        
        for company in NIFTY_IT_COMPANIES:
            try:
                print(f"\n📊 Processing {company['name']} ({company['code']})...")
                
                # Get financial data from Screener
                financial_data = self.screener_scraper.scrape_company(
                    company['name'],
                    company['code'],
                    company['screener_url']
                )
                
                # Get services/products data
                services_data = self.service_scraper.scrape_company_services(company)
                
                # Display extracted services
                self._display_services(company['name'], services_data)
                
                # Combine results
                result = {
                    **financial_data,
                    'services_products': self.service_scraper.format_services_for_excel(services_data),
                    'services_categories': services_data.get('categories', []),
                    'total_service_categories': services_data.get('total_categories', 0),
                    'service_extraction_method': services_data.get('method', 'unknown')
                }
                
                self.results.append(result)
                logger.info(f"✓ Completed: {company['name']}")
                
            except Exception as e:
                logger.error(f"✗ Failed: {company['name']} - {e}")
                self.results.append({
                    'company_name': company['name'],
                    'company_code': company['code'],
                    'current_quarter_revenue': None,
                    'last_3_quarters_summary': f'Error: {str(e)[:50]}',
                    'annual_revenue': None,
                    'annual_profit': None,
                    'financial_year': None,
                    'quarterly_labels': [],
                    'quarterly_sales': [],
                    'quarterly_profits': [],
                    'upcoming_result': None,
                    'total_quarters': 0,
                    'services_products': 'Data not available',
                    'services_categories': [],
                    'total_service_categories': 0,
                    'service_extraction_method': 'error'
                })
        
        return self.results
    
    def _display_services(self, company_name: str, services_data: Dict):
        """Display extracted services in a readable format"""
        categories = services_data.get('categories', [])
        total = services_data.get('total_categories', 0)
        method = services_data.get('method', 'unknown')
        
        print(f"\n  📋 Services extracted for {company_name} (Method: {method})")
        print(f"  Total categories: {total}")
        
        if categories:
            print("  Sample services:")
            for cat in categories[:5]:  # Show first 5 categories
                name = cat.get('name', 'Unknown')
                sub_services = cat.get('sub_services', [])
                if sub_services:
                    sub_str = ", ".join(sub_services[:3])
                    print(f"    • {name}: {sub_str}")
                else:
                    print(f"    • {name}")
            
            if len(categories) > 5:
                print(f"    ... and {len(categories) - 5} more categories")
        else:
            print("  ⚠️ No services extracted")
    
    def save_to_excel(self, filename: str = None):
        """Save results to Excel file with enhanced service display"""
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(output_dir, f'nifty_it_data_{timestamp}.xlsx')
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 1. SUMMARY SHEET - Main overview
            summary_data = []
            for result in self.results:
                # Format services for display in summary
                services_display = result.get('services_products', 'N/A')
                # Truncate if too long for summary view
                if len(services_display) > 1000:
                    services_display = services_display[:1000] + "..."
                
                summary_data.append({
                    'Company Name': result['company_name'],
                    'Ticker': result['company_code'],
                    'Current Revenue (Cr)': self._format_currency(result.get('current_quarter_revenue')),
                    'Annual Revenue (Cr)': self._format_currency(result.get('annual_revenue')),
                    'Annual Profit (Cr)': self._format_currency(result.get('annual_profit')),
                    'Financial Year': result.get('financial_year', 'N/A'),
                    'Service Categories': result.get('total_service_categories', 0),
                    'Extraction Method': result.get('service_extraction_method', 'unknown'),
                    'Services/Products': services_display,
                    'Upcoming Result': result.get('upcoming_result', 'N/A')
                })
            
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # 2. SERVICES DETAIL SHEET - Detailed service breakdown
            services_detail = []
            for result in self.results:
                categories = result.get('services_categories', [])
                if categories:
                    for cat in categories:
                        services_detail.append({
                            'Company': result['company_name'],
                            'Ticker': result['company_code'],
                            'Category': cat.get('name', 'Unknown'),
                            'Description': cat.get('description', ''),
                            'Sub-Services': self._format_sub_services(cat.get('sub_services', [])),
                            'Sub-Service Count': len(cat.get('sub_services', [])),
                            'URL': cat.get('url', ''),
                            'Category Level': cat.get('level', 1)
                        })
            
            if services_detail:
                df_services = pd.DataFrame(services_detail)
                df_services.to_excel(writer, sheet_name='Services Detail', index=False)
            
            # 3. QUARTERLY DETAILS SHEET
            quarterly_data = []
            for result in self.results:
                if result.get('quarterly_labels'):
                    for idx, label in enumerate(result['quarterly_labels']):
                        revenue = result['quarterly_sales'][idx] if idx < len(result['quarterly_sales']) else None
                        profit = result['quarterly_profits'][idx] if idx < len(result['quarterly_profits']) else None
                        quarterly_data.append({
                            'Company': result['company_name'],
                            'Ticker': result['company_code'],
                            'Quarter': label,
                            'Revenue (Cr)': revenue,
                            'Profit (Cr)': profit
                        })
            
            if quarterly_data:
                df_quarterly = pd.DataFrame(quarterly_data)
                df_quarterly.to_excel(writer, sheet_name='Quarterly Details', index=False)
            
            # 4. COMPARISON SHEET - Key metrics comparison
            comparison_data = []
            for result in self.results:
                comparison_data.append({
                    'Company': result['company_name'],
                    'Ticker': result['company_code'],
                    'Current Revenue': result.get('current_quarter_revenue', 0),
                    'Annual Revenue': result.get('annual_revenue', 0),
                    'Annual Profit': result.get('annual_profit', 0),
                    'Profit Margin %': self._calculate_margin(
                        result.get('annual_profit'), 
                        result.get('annual_revenue')
                    ),
                    'Service Categories': result.get('total_service_categories', 0),
                    'Financial Year': result.get('financial_year', 'N/A')
                })
            
            df_comparison = pd.DataFrame(comparison_data)
            # Sort by current revenue descending
            df_comparison = df_comparison.sort_values('Current Revenue', ascending=False)
            df_comparison.to_excel(writer, sheet_name='Comparison', index=False)
            
            # Auto-adjust column widths for all sheets
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            cell_length = len(str(cell.value))
                            if cell_length > max_length:
                                max_length = cell_length
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 60)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Format currency columns (add $/₹ signs)
            for sheet_name in ['Summary', 'Comparison']:
                if sheet_name in writer.sheets:
                    worksheet = writer.sheets[sheet_name]
                    for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row):
                        for cell in row:
                            if isinstance(cell.value, (int, float)) and cell.value > 0:
                                # Check if column header contains "Revenue" or "Profit"
                                col_idx = cell.column - 1
                                header = worksheet.cell(row=1, column=cell.column).value
                                if header and any(word in str(header) for word in ['Revenue', 'Profit']):
                                    cell.number_format = '#,##0.00'
        
        logger.info(f"Data saved to {filename}")
        return filename
    
    def _format_currency(self, value):
        """Format currency value with proper commas"""
        if value is None:
            return None
        try:
            return f"{value:,.2f}"
        except:
            return value
    
    def _format_sub_services(self, sub_services: list) -> str:
        """Format sub-services list into readable string"""
        if not sub_services:
            return ""
        return ", ".join(sub_services[:10])  # Show first 10, Excel can handle
    
    def _calculate_margin(self, profit, revenue):
        """Calculate profit margin percentage"""
        if profit is None or revenue is None or revenue == 0:
            return None
        try:
            return round((profit / revenue) * 100, 2)
        except:
            return None

def main():
    """Main execution"""
    print("=" * 70)
    print("NIFTY IT Financial & Services Data Scraper")
    print("Sources: Screener.in, Company Sitemaps")
    print("=" * 70)
    
    scraper = NiftyITScraper()
    
    # Scrape all companies
    results = scraper.scrape_all_companies()
    
    # Save to Excel
    filename = scraper.save_to_excel()
    
    # Display final summary
    print("\n" + "=" * 70)
    print("SCRAPING SUMMARY")
    print("=" * 70)
    print(f"Total Companies: {len(results)}")
    print(f"Companies with service data: {sum(1 for r in results if r.get('services_categories'))}")
    print(f"Companies with financial data: {sum(1 for r in results if r.get('current_quarter_revenue'))}")
    
    # Display service extraction methods used
    methods = {}
    for r in results:
        method = r.get('service_extraction_method', 'unknown')
        methods[method] = methods.get(method, 0) + 1
    
    print("\nService Extraction Methods:")
    for method, count in methods.items():
        print(f"  • {method}: {count} companies")
    
    print(f"\n✅ Data saved to: {filename}")
    
    # Show a preview of services extracted
    print("\n" + "=" * 70)
    print("SERVICES PREVIEW (First 3 companies)")
    print("=" * 70)
    for result in results[:3]:
        print(f"\n{result['company_name']}:")
        services = result.get('services_products', 'No services')
        # Show first 3 lines of services
        lines = services.split('\n')[:3]
        for line in lines:
            print(f"  {line}")
        if len(services.split('\n')) > 3:
            print(f"   ... and {len(services.splitlines()) - 3} more services")
            

if __name__ == "__main__":
    main()