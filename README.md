## NIFTY IT Company Data Scraper

A comprehensive Python scraper for extracting financial and service data from NIFTY IT companies.

## Features

- **Financial Data**: Revenue, profit, quarterly results from Screener.in
- **Services/Products**: Extracted from company sitemaps and websites
- **Excel Export**: Clean, formatted Excel output with multiple sheets
- **Resilient Scraping**: Handles 403 errors, retries, and fallback strategies

## Data Extracted

- Annual Revenue (Cr)
- Quarterly Revenue (Cr)
- Annual Profit (Cr)
- Products & Services
- Financial Year

## Tech Stack

- Python 3.10+
- BeautifulSoup4
- Requests
- Pandas
- OpenPyXL

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/nifty-it-scraper.git
cd nifty-it-scraper

# Create conda environment
conda create -n nifty_scraper python=3.10
conda activate nifty_scraper

# Install dependencies
pip install -r requirements.txt
```

**Run full scraper**

python main.py

**Test service extraction**

python test_services_with_registry.py

**Debug sitemap**

python debug_sitemap.py

### Project Structure


nifty-it-scraper/
├── config/          # Company configurations
├── scrapers/        # Scraping logic
├── parsers/         # HTML/XML parsers
├── output/          # Generated Excel files
├── main.py          # Main execution
└── requirements.txt # Dependencies
