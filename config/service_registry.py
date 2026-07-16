# # config/service_registry.py
# """
# Declarative configuration for service extraction across all companies
# This makes it easy to update selectors without touching core logic
# """

# COMPANY_SERVICE_REGISTRY = {
#     'TCS': {
#         'strategy': 'sitemap_fallback',  # Use sitemap but with fallback
#         'sitemap_url': 'https://www.tcs.com/sitemap.xml',
#         'base_prefix': 'https://www.tcs.com/what-we-do/services',
#         'depth_offset': 1,
#         'service_type': 'services',
#         'fallback_url': 'https://www.tcs.com/what-we-do/services',
#         'fallback_selectors': {
#             'category': ['h2', 'h3', 'h4'],
#             'keywords': ['cloud', 'ai', 'data', 'cyber', 'digital', 'consulting', 
#                         'automation', 'analytics', 'blockchain', 'iot']
#         }
#     },
#     'INFY': {
#         'strategy': 'sitemap_fallback',
#         'sitemap_url': 'https://www.infosys.com/sitemap.xml',
#         'base_prefix': 'https://www.infosys.com/services',
#         'depth_offset': 1,
#         'service_type': 'services',
#         'fallback_url': 'https://www.infosys.com/services/',
#         'fallback_selectors': {
#             'container': ['div', 'li', 'a'],
#             'class_pattern': r'(service|card|nav|menu|offering|tile)',
#             'link_pattern': '/services/'
#         }
#     },
#     'HCLTECH': {
#         'strategy': 'direct_dom',
#         'target_url': 'https://www.hcltech.com/products-platforms',
#         'service_type': 'products',
#         'selectors': {
#             'container': 'div.gray-card-with-icon-info',
#             'heading': 'h3.card-heading-flex',
#             'list': 'ul',  # The ul inside the container
#             'list_item': 'li',
#             # Alternative: if ul has specific class
#             'list_class': None  # Set to class name if present, e.g., 'product-list'
#         }
#     },
#     'TECHM': {
#         'strategy': 'sitemap',
#         'sitemap_url': 'https://www.techmahindra.com/sitemap.xml?page=1',
#         'base_prefix': 'https://www.techmahindra.com/services',
#         'depth_offset': 1,
#         'service_type': 'services'
#     },
#     'WIPRO': {
#         'strategy': 'wipro_special',
#         'sitemap_url': 'https://www.wipro.com/sitemap.xml',
#         'service_type': 'services',
#         'categories': {
#             'Consulting': ['/consulting/'],
#             'Cloud': ['/cloud/'],
#             'Cybersecurity': ['/cybersecurity/'],
#             'Data & Analytics': ['/data/', '/analytics/'],
#             'AI & Automation': ['/ai/', '/automation/'],
#             'Digital': ['/digital/'],
#             'Applications': ['/applications/'],
#             'Engineering': ['/engineering/'],
#             'IoT': ['/iot/'],
#             'Blockchain': ['/blockchain/']
#         }
#     },
#     'PERSISTENT': {
#         'strategy': 'sitemap',
#         'sitemap_url': 'https://www.persistent.com/page-sitemap.xml',
#         'base_prefix': 'https://www.persistent.com/services',
#         'depth_offset': 1,
#         'service_type': 'services'
#     },
#     'COFORGE': {
#         'strategy': 'sitemap',
#         'sitemap_url': 'https://www.coforge.com/sitemap-main.xml',
#         'base_prefix': 'https://www.coforge.com/capabilities',
#         'depth_offset': 1,
#         'service_type': 'capabilities'
#     },
#     'LTIM': {
#         'strategy': 'sitemap',
#         'sitemap_url': 'https://www.ltm.com/us.sitemap.xml',
#         'base_prefix': 'https://www.ltm.com/services',
#         'depth_offset': 1,
#         'service_type': 'services'
#     },
#     'MPHASIS': {
#         'strategy': 'sitemap',
#         'sitemap_url': 'https://www.mphasis.com/sitemap_home.xml',
#         'base_prefix': 'https://www.mphasis.com/home/services',
#         'depth_offset': 1,
#         'service_type': 'services'
#     },
#     'OFSS': {
#         'strategy': 'oracle_special',
#         'sitemap_url': 'https://www.oracle.com/in/sitemap-wcs.xml',
#         'base_prefix': 'https://www.oracle.com/in/financial-services',
#         'service_type': 'solutions'
#     }
# }

# config/service_registry.py (UPDATE for all companies)
COMPANY_SERVICE_REGISTRY = {
    'TCS': {
        'strategy': 'sitemap_fallback',
        'sitemap_url': 'https://www.tcs.com/sitemap.xml',
        'base_prefix': 'https://www.tcs.com/what-we-do/services',
        'depth_offset': 1,
        'service_type': 'services'
    },
    'INFY': {
        'strategy': 'sitemap_fallback',
        'sitemap_url': 'https://www.infosys.com/sitemap.xml',
        'base_prefix': 'https://www.infosys.com/services',
        'depth_offset': 1,
        'service_type': 'services'
    },
    'HCLTECH': {
        'strategy': 'direct_dom',
        'target_url': 'https://www.hcltech.com/products-platforms',
        'service_type': 'products',
        'selectors': {
            'container': 'div.gray-card-with-icon-info',
            'heading': 'h3.card-heading-flex',
            'list': 'ul',
            'list_item': 'li'
        }
    },
    'TECHM': {
        'strategy': 'sitemap',
        'sitemap_url': 'https://www.techmahindra.com/sitemap.xml?page=1',
        'base_prefix': 'https://www.techmahindra.com/services',
        'depth_offset': 1,
        'service_type': 'services'
    },
    'WIPRO': {
        'strategy': 'wipro_special',
        'sitemap_url': 'https://www.wipro.com/sitemap.xml',
        'service_type': 'services',
        'categories': {
            'Consulting': ['/consulting/'],
            'Cloud': ['/cloud/'],
            'Cybersecurity': ['/cybersecurity/'],
            'Data & Analytics': ['/data/', '/analytics/'],
            'AI & Automation': ['/ai/', '/automation/'],
            'Digital': ['/digital/'],
            'Applications': ['/applications/'],
            'Engineering': ['/engineering/'],
            'IoT': ['/iot/'],
            'Blockchain': ['/blockchain/']
        }
    },
    'PERSISTENT': {
        'strategy': 'sitemap',
        'sitemap_url': 'https://www.persistent.com/page-sitemap.xml',
        'base_prefix': 'https://www.persistent.com/services',
        'depth_offset': 1,
        'service_type': 'services'
    },
    'COFORGE': {
        'strategy': 'sitemap',
        'sitemap_url': 'https://www.coforge.com/sitemap-main.xml',
        'base_prefix': 'https://www.coforge.com/capabilities',
        'depth_offset': 1,
        'service_type': 'capabilities'
    },
    'LTIM': {
        'strategy': 'sitemap',
        'sitemap_url': 'https://www.ltm.com/us.sitemap.xml',
        'base_prefix': 'https://www.ltm.com/services',
        'depth_offset': 1,
        'service_type': 'services'
    },
    'MPHASIS': {
        'strategy': 'sitemap',
        'sitemap_url': 'https://www.mphasis.com/sitemap_home.xml',
        'base_prefix': 'https://www.mphasis.com/home/services',
        'depth_offset': 1,
        'service_type': 'services'
    },
    'OFSS': {
        'strategy': 'oracle_special',
        'sitemap_url': 'https://www.oracle.com/in/sitemap-wcs.xml',
        'base_prefix': 'https://www.oracle.com/in/financial-services',
        'service_type': 'solutions'
    }
}