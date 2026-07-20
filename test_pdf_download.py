# test_pdf_download.py
from utils.pdf_downloader import PDFDownloader
from config.investor_docs import INVESTOR_DOCUMENTS

def test_download():
    print("Testing PDF download...")
    downloader = PDFDownloader()
    
    # Test with TCS (known working URL)
    tcs_docs = INVESTOR_DOCUMENTS['TCS']
    for doc_type, url in tcs_docs.items():
        print(f"\nDownloading {doc_type}...")
        try:
            path = downloader.download_pdf(url, 'TCS', doc_type)
            print(f"  ✓ Downloaded to: {path}")
        except Exception as e:
            print(f"  ✗ Failed: {e}")

if __name__ == "__main__":
    test_download()