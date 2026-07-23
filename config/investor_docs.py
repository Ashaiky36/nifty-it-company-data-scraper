# # # config/investor_docs.py
# # INVESTOR_DOCUMENTS = {
# #     'TCS': {
# #         'press_release': 'https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/IND%20AS/Press%20Release%20-%20INR.pdf',
# #         'fact_sheet': 'https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/Presentations/Q1%202026-27%20Fact%20Sheet.pdf'
# #     },
# #     'INFY': {
# #         'press_release': 'https://www.infosys.com/investors/reports-filings/quarterly-results/2025-2026/q4/documents/ifrs-inr-press-release.pdf'
# #     },
# #     'HCLTECH': {
# #         'press_release': 'https://www.hcltech.com/investor-relations/financial-results?year=2025-26'  #instead of direct web view of pdfs, HCLTech provides download only links
# #     },
# #     'TECHM': {
# #         'press_release': 'https://insights.techmahindra.com/investors/tml-q1-fy-27-earnings-presentation.pdf'
# #     },
# #     'WIPRO': {
# #         'press_release': 'https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2026-2027/q1fy27/press-release-q1fy27.pdf'
# #     },
# #     'PERSISTENT': {
# #         'press_release': 'https://www.persistent.com/wp-content/uploads/2026/04/press-release-q4fy26.pdf'
# #     },
# #     'COFORGE': {
# #         'presentation': 'https://investors.coforge.com/hubfs/Investor-Presentation-and-Factsheet-Q4FY26.pdf?hsLang=en'
# #     },
# #     'LTIM': {
# #         'factsheet': 'https://www.ltm.com/content/dam/ltimcorporatewebsite/uploads/news-and-events/2026/07/earnings-release-factsheet-q1fy27.pdf'
# #     },
# #     'MPHASIS': {
# #         'press_release': 'https://www.mphasis.com/content/dam/mphasis-com/global/en/investors/financial-results/2026/q4-earnings-press-release.pdf'
# #     },
# #     'OFSS': {
# #         'press_release': 'https://www.oracle.com/a/ocom/docs/industries/financial-services/ofss-q4fy26-pr.pdf'
# #     }
# # }

# # config/investor_docs.py (UPDATED)
# import logging
# from utils.hcltech_pdf_finder import HCLTechPDFFinder

# logger = logging.getLogger(__name__)

# def get_hcltech_links():
#     """Dynamic link fetcher for HCLTech"""
#     finder = HCLTechPDFFinder()
#     links = finder.get_pdf_links(year="2025-26")
    
#     if not links:
#         logger.warning("Could not find HCLTech PDF links, using fallback")
#         links = {
#             'press_release': 'https://www.hcltech.com/investor-relations/financial-results',
#             'presentation': 'https://www.hcltech.com/investor-relations/financial-results'
#         }
    
#     return links

# # Base configuration
# INVESTOR_DOCUMENTS = {
#     'TCS': {
#         'press_release': 'https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/IND%20AS/Press%20Release%20-%20INR.pdf',
#         'fact_sheet': 'https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/Presentations/Q1%202026-27%20Fact%20Sheet.pdf'
#     },
#     'INFY': {
#         'press_release': 'https://www.infosys.com/investors/reports-filings/quarterly-results/2025-2026/q4/documents/ifrs-inr-press-release.pdf'
#     },
#     'HCLTECH': get_hcltech_links(),  # Dynamic fetching
#     'TECHM': {
#         'press_release': 'https://insights.techmahindra.com/investors/tml-q1-fy-27-earnings-presentation.pdf'
#     },
#     'WIPRO': {
#         'press_release': 'https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2026-2027/q1fy27/press-release-q1fy27.pdf'
#     },
#     'PERSISTENT': {
#         'press_release': 'https://www.persistent.com/wp-content/uploads/2026/04/press-release-q4fy26.pdf'
#     },
#     'COFORGE': {
#         'presentation': 'https://investors.coforge.com/hubfs/Investor-Presentation-and-Factsheet-Q4FY26.pdf?hsLang=en'
#     },
#     'LTIM': {
#         'factsheet': 'https://www.ltm.com/content/dam/ltimcorporatewebsite/uploads/news-and-events/2026/07/earnings-release-factsheet-q1fy27.pdf'
#     },
#     'MPHASIS': {
#         'press_release': 'https://www.mphasis.com/content/dam/mphasis-com/global/en/investors/financial-results/2026/q4-earnings-press-release.pdf'
#     },
#     'OFSS': {
#         'press_release': 'https://www.oracle.com/a/ocom/docs/industries/financial-services/ofss-q4fy26-pr.pdf'
#     }
# }

# config/investor_docs.py (UPDATED with transcripts)
"""
Investor document URLs for each company
Prioritizes earnings call transcripts over press releases
"""

INVESTOR_DOCUMENTS = {
    'TCS': {
        'transcript': 'https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/Management%20Commentary/Transcript%20of%20the%20Q1%202026-27%20Earnings%20Conference%20Call%20held%20on%20Jul%209,%202026.pdf',
        'press_release': 'https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/IND%20AS/Press%20Release%20-%20INR.pdf',
        'fact_sheet': 'https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/Presentations/Q1%202026-27%20Fact%20Sheet.pdf'
    },
    'INFY': {
        'transcript': 'https://www.infosys.com/investors/reports-filings/quarterly-results/2025-2026/q4/documents/transcripts/earningscall.pdf',
        'press_release': 'https://www.infosys.com/investors/reports-filings/quarterly-results/2025-2026/q4/documents/ifrs-inr-press-release.pdf'
    },
    'HCLTECH': {
        # Will need dynamic fetching for HCLTech transcripts
        'transcript_url': 'https://www.hcltech.com/investor-relations/financial-results',
        'doc_type': 'transcript'
    },
    'TECHM': {
        'transcript': 'https://insights.techmahindra.com/investors/tml-q4-fy-26-earnings-transcript.pdf',
        'press_release': 'https://insights.techmahindra.com/investors/tml-q1-fy-27-earnings-presentation.pdf'
    },
    'WIPRO': {
        'transcript': 'https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2026-2027/q1fy27/q1fy27-earnings-transcript.pdf',
        'press_release': 'https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2026-2027/q1fy27/press-release-q1fy27.pdf'
    },
    'PERSISTENT': {
        'transcript': 'https://www.persistent.com/wp-content/uploads/2026/04/Analyst-Call-Transcript-Q4FY26.pdf',
        'press_release': 'https://www.persistent.com/wp-content/uploads/2026/04/press-release-q4fy26.pdf'
    },
    'COFORGE': {
        'transcript': 'https://investors.coforge.com/hubfs/Coforge-Limited-Earnings-Call-Transcript-Q4FY26%20_AJ.pdf?hsLang=en',
        'presentation': 'https://investors.coforge.com/hubfs/Investor-Presentation-and-Factsheet-Q4FY26.pdf?hsLang=en'
    },
    'LTIM': {
        'transcript': 'https://www.ltm.com/content/dam/ltimcorporatewebsite/uploads/news-and-events/2026/07/earnings-release-factsheet-q1fy27.pdf',  # This is a factsheet, need transcript
        'factsheet': 'https://www.ltm.com/content/dam/ltimcorporatewebsite/uploads/news-and-events/2026/07/earnings-release-factsheet-q1fy27.pdf'
    },
    'MPHASIS': {
        'transcript': 'https://www.mphasis.com/content/dam/mphasis-com/global/en/investors/financial-results/2026/q4-earnings-press-release.pdf',  # This is a press release, need transcript
        'press_release': 'https://www.mphasis.com/content/dam/mphasis-com/global/en/investors/financial-results/2026/q4-earnings-press-release.pdf'
    },
    'OFSS': {
        'transcript': 'https://www.oracle.com/a/ocom/docs/industries/financial-services/ofss-q4fy26-pr.pdf',  # This is a press release, need transcript
        'press_release': 'https://www.oracle.com/a/ocom/docs/industries/financial-services/ofss-q4fy26-pr.pdf'
    }
}