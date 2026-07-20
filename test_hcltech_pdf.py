# # test_hcltech_pdf.py
# from utils.hcltech_pdf_finder import HCLTechPDFFinder

# finder = HCLTechPDFFinder()
# links = finder.get_pdf_links()
# print(f"Found links: {links}")

# test_hcltech_pdf.py
from utils.hcltech_pdf_finder import HCLTechPDFFinder
import json

def test_hcltech_finder():
    print("Testing HCLTech PDF Finder...")
    finder = HCLTechPDFFinder()
    links = finder.get_pdf_links(year="2025-26")
    
    print(f"\nFound {len(links)} PDF links:")
    for doc_type, url in links.items():
        print(f"  {doc_type}: {url}")
    
    # Save for reference
    with open('hcltech_links.json', 'w') as f:
        json.dump(links, f, indent=2)
    
    return links

if __name__ == "__main__":
    test_hcltech_finder()