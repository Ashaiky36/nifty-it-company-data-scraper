# # config/companies.py
# NIFTY_IT_COMPANIES = [
#     {
#         'name': 'Tata Consultancy Services',
#         'code': 'TCS',
#         'screener_url': 'https://www.screener.in/company/TCS/consolidated/',
#         'screener_id': 3365,  # We can extract this dynamically
#         'sitemap_url': 'https://www.tcs.com/sitemap.xml',
#         'base_prefix': 'https://www.tcs.com/what-we-do/services',
#         'depth_offset': 1,  # Get immediate children like /cloud, /ai, etc.
#         'service_type': 'services'
#     },
#     {
#         'name': 'Infosys',
#         'code': 'INFY',
#         'screener_url': 'https://www.screener.in/company/INFY/consolidated/',
#         'screener_id': 469,  # We can extract dynamically
#         'sitemap_url': 'https://www.infosys.com/sitemap.xml',
#         'base_prefix': 'https://www.infosys.com/services',
#         'depth_offset': 1,
#         'service_type': 'services'
#     },
#     {
#         'name': 'HCL Technologies',
#         'code': 'HCLTECH',
#         'screener_url': 'https://www.screener.in/company/HCLTECH/consolidated/',
#         'screener_id': None,  # Will extract from HTML
#         'sitemap_url': 'https://www.hcltech.com/sitemap.xml',
#         'base_prefix': 'https://www.hcltech.com/products-platforms',
#         'depth_offset': 1,
#         'service_type': 'products'
#     },
#     {
#         'name': 'Tech Mahindra',
#         'code': 'TECHM',
#         'screener_url': 'https://www.screener.in/company/TECHM/consolidated/',
#         'screener_id': None,
#         'sitemap_url': 'https://www.techmahindra.com/sitemap.xml',
#         'base_prefix': 'https://www.techmahindra.com/products-and-platforms',
#         'depth_offset': 1,
#         'service_type': 'products'
#     },
#     {
#         'name': 'Wipro',
#         'code': 'WIPRO',
#         'screener_url': 'https://www.screener.in/company/WIPRO/consolidated/',
#         'screener_id': None,
#         'sitemap_url': 'https://www.wipro.com/sitemap.xml',
#         'base_prefix': 'https://www.wipro.com/services', #wipros internal link structure is different, so we would need to handle it separately
#         'depth_offset': 1,
#         'service_type': 'services'
#     },
#     {
#         'name': 'Persistent Systems',
#         'code': 'PERSISTENT',
#         'screener_url': 'https://www.screener.in/company/PERSISTENT/consolidated/',
#         'screener_id': None,
#         'sitemap_url': 'https://www.persistent.com/page-sitemap.xml',
#         'base_prefix': 'https://www.persistent.com/services',
#         'depth_offset': 1,
#         'service_type': 'services'
#     },
#     {
#         'name': 'Coforge',
#         'code': 'COFORGE',
#         'screener_url': 'https://www.screener.in/company/COFORGE/consolidated/',
#         'screener_id': None,
#         'sitemap_url': 'https://www.coforge.com/sitemap-main.xml',
#         'base_prefix': 'https://www.coforge.com/capabilities',
#         'depth_offset': 1,
#         'service_type': 'capabilities'
#     },
#     {
#         'name': 'LTIMindtree',
#         'code': 'LTM',
#         'screener_url': 'https://www.screener.in/company/LTM/consolidated/',
#         'screener_id': None,
#         'sitemap_url': 'https://www.ltm.com/us.sitemap.xml',
#         'base_prefix': 'https://www.ltm.com/services',
#         'depth_offset': 1,
#         'service_type': 'services'
#     },
#     {
#         'name': 'Mphasis',
#         'code': 'MPHASIS',
#         'screener_url': 'https://www.screener.in/company/MPHASIS/consolidated/',
#         'screener_id': None,
#         'sitemap_url': 'https://www.mphasis.com/sitemap_home.xml',
#         'base_prefix': 'https://www.mphasis.com/home/services',
#         'depth_offset': 1,
#         'service_type': 'services'
#     },
#     {
#         'name': 'Oracle Financial Services Software',
#         'code': 'OFSS',
#         'screener_url': 'https://www.screener.in/company/OFSS/consolidated/',
#         'screener_id': None,
#         'sitemap_url': 'https://www.oracle.com/in/sitemap-wcs.xml',  #sitemap-url for india
#         'base_prefix': 'https://www.oracle.com/in/financial-services', #base url, services to search under this
#         'depth_offset': 1,
#         'service_type': 'solutions'
#     }
# ]

# config/companies.py (final version)
NIFTY_IT_COMPANIES = [
    {
        'name': 'Tata Consultancy Services',
        'code': 'TCS',
        'screener_url': 'https://www.screener.in/company/TCS/consolidated/',
        'sitemap_url': 'https://www.tcs.com/sitemap.xml',
        'base_prefix': 'https://www.tcs.com/what-we-do/services',
        'extraction_method': 'sitemap_depth_1_2',
        'service_type': 'services'
    },
    {
        'name': 'Infosys',
        'code': 'INFY',
        'screener_url': 'https://www.screener.in/company/INFY/consolidated/',
        'sitemap_url': 'https://www.infosys.com/sitemap.xml',
        'base_prefix': 'https://www.infosys.com/services',
        'extraction_method': 'sitemap',
        'service_type': 'services'
    },
    {
        'name': 'HCL Technologies',
        'code': 'HCLTECH',
        'screener_url': 'https://www.screener.in/company/HCLTECH/consolidated/',
        'sitemap_url': 'https://www.hcltech.com/sitemap.xml',
        'base_prefix': 'https://www.hcltech.com/products-platforms',
        'extraction_method': 'html_structured',  # Uses HTML product section
        'service_type': 'products',
        'html_url': 'https://www.hcltech.com/products-platforms'
    },
    {
        'name': 'Tech Mahindra',
        'code': 'TECHM',
        'screener_url': 'https://www.screener.in/company/TECHM/consolidated/',
        'sitemap_url': 'https://www.techmahindra.com/sitemap.xml?page=1',
        'base_prefix': 'https://www.techmahindra.com/services',
        'extraction_method': 'sitemap_depth_1_2',
        'service_type': 'services'
    },
    {
        'name': 'Wipro',
        'code': 'WIPRO',
        'screener_url': 'https://www.screener.in/company/WIPRO/consolidated/',
        'sitemap_url': 'https://www.wipro.com/sitemap.xml',
        'base_prefix': 'https://www.wipro.com',
        'depth_offset': 1,
        'service_type': 'services',
        'special_handler': 'wipro'  # Flag for special handling
    },
    # {
    #     'name': 'Wipro',
    #     'code': 'WIPRO',
    #     'screener_url': 'https://www.screener.in/company/WIPRO/consolidated/',
    #     'sitemap_url': 'https://www.wipro.com/sitemap.xml',
    #     'base_prefix': 'https://www.wipro.com',  # No clear structure
    #     'extraction_method': 'special_wipro',
    #     'service_type': 'services'
    # },
    {
        'name': 'Persistent Systems',
        'code': 'PERSISTENT',
        'screener_url': 'https://www.screener.in/company/PERSISTENT/consolidated/',
        'sitemap_url': 'https://www.persistent.com/page-sitemap.xml',
        'base_prefix': 'https://www.persistent.com/services',
        'extraction_method': 'sitemap_depth_2',
        'service_type': 'services'
    },
    {
        'name': 'Coforge',
        'code': 'COFORGE',
        'screener_url': 'https://www.screener.in/company/COFORGE/consolidated/',
        'sitemap_url': 'https://www.coforge.com/sitemap-main.xml',
        'base_prefix': 'https://www.coforge.com/capabilities',
        'extraction_method': 'sitemap_depth_1_2',
        'service_type': 'capabilities'
    },
    {
        'name': 'LTIMindtree',
        'code': 'LTIM',
        'screener_url': 'https://www.screener.in/company/LTIM/consolidated/',
        'sitemap_url': 'https://www.ltm.com/us.sitemap.xml',
        'base_prefix': 'https://www.ltm.com/services',
        'extraction_method': 'sitemap_depth_1_2',
        'service_type': 'services'
    },
    {
        'name': 'Mphasis',
        'code': 'MPHASIS',
        'screener_url': 'https://www.screener.in/company/MPHASIS/consolidated/',
        'sitemap_url': 'https://www.mphasis.com/sitemap_home.xml',
        'base_prefix': 'https://www.mphasis.com/home/services',
        'extraction_method': 'sitemap_depth_2',
        'service_type': 'services'
    },
    {
        'name': 'Oracle Financial Services',
        'code': 'OFSS',
        'screener_url': 'https://www.screener.in/company/OFSS/consolidated/',
        'sitemap_url': 'https://www.oracle.com/in/sitemap-wcs.xml',
        'base_prefix': 'https://www.oracle.com/in/financial-services',
        'extraction_method': 'sitemap_depth_2_3',
        'service_type': 'solutions'
    }
]