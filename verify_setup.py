# verify_setup.py (updated)
import sys
import os
import glob

def verify_imports():
    """Verify all imports work correctly"""
    try:
        print("✓ Checking imports...")
        
        # Check each import
        import requests
        print("  ✓ requests")
        
        from bs4 import BeautifulSoup
        print("  ✓ beautifulsoup4")
        
        import pandas as pd
        print("  ✓ pandas")
        
        import openpyxl
        print("  ✓ openpyxl")
        
        import lxml
        print("  ✓ lxml")
        
        # Check our modules
        print("\n✓ Checking project modules...")
        
        # Add project root to path
        sys.path.insert(0, os.getcwd())
        
        from config.companies import NIFTY_IT_COMPANIES
        print(f"  ✓ companies config loaded ({len(NIFTY_IT_COMPANIES)} companies)")
        
        from scrapers.base_scraper import BaseScraper
        print("  ✓ base_scraper")
        
        from parsers.quarterly_parser import ScreenerQuarterlyParser
        print("  ✓ quarterly_parser")
        
        print("\n✅ All imports successful! Ready to run scraper.")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\nPlease install missing dependencies:")
        print("pip install requests beautifulsoup4 pandas openpyxl lxml")
        return False

def verify_project_structure():
    """Verify project directory structure"""
    print("\n✓ Checking project structure...")
    
    # Directories to check
    required_dirs = ['config', 'scrapers', 'parsers', 'output']
    
    # Files to check (with their correct paths)
    required_files = {
        'config/companies.py': 'Companies configuration',
        'scrapers/base_scraper.py': 'Base scraper class',
        'scrapers/screener_scraper.py': 'Screener scraper',
        'parsers/quarterly_parser.py': 'Quarterly parser',
        'test_screener.py': 'Test script',
        'main.py': 'Main script'
    }
    
    # Check directories
    all_dirs_exist = True
    for dir_name in required_dirs:
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ (missing)")
            all_dirs_exist = False
    
    # Check files
    all_files_exist = True
    for file_path, description in required_files.items():
        if os.path.exists(file_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (missing) - {description}")
            all_files_exist = False
    
    if all_dirs_exist and all_files_exist:
        print("\n✅ Project structure verified")
        return True
    else:
        print("\n⚠️  Some files/directories are missing")
        print("   Make sure you're running this from the project root directory")
        print("   Current directory:", os.getcwd())
        return False

def check_output_dir():
    """Check or create output directory"""
    print("\n✓ Checking output directory...")
    if os.path.exists('output'):
        print("  ✓ output/ directory exists")
        return True
    else:
        print("  ℹ️  output/ directory not found - will be created when saving data")
        return True  # Not a critical error

if __name__ == "__main__":
    print("=" * 50)
    print("Environment Verification")
    print("=" * 50)
    
    imports_ok = verify_imports()
    structure_ok = verify_project_structure()
    output_ok = check_output_dir()
    
    if imports_ok and structure_ok and output_ok:
        print("\n✅ Everything is ready! You can now run:")
        print("   python test_screener.py  # Test with one company")
        print("   python main.py           # Scrape all companies")
    else:
        print("\n⚠️  Some issues found. Please fix them before running.")
        print("\nTo fix missing directories:")
        print("   mkdir output")
        print("   mkdir config scrapers parsers")