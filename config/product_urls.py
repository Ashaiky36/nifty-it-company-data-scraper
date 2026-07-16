# config/product_urls.py
"""
Configuration for product/service page URLs for each NIFTY IT company
Each company has different URL patterns and structures
"""

PRODUCT_SOURCES = {
    'TCS': {
        'name': 'Tata Consultancy Services',
        'url': 'https://www.tcs.com/what-we-do',
        'type': 'cards_grid',  # Structure type for parser selection
        'selector': '.service-card, .offerings-item',
        'title_selector': 'h3, .title',
        'description_selector': '.description, p'
    },
    'INFY': {
        'name': 'Infosys',
        'url': 'https://www.infosys.com/services.html',
        'type': 'accordion_tabs',  # Complex accordion structure
        'accordion_container': '#whatWeContentwhatwedo',
        'tab_selector': '.tab-pane',
        'header_selector': '.accordion-header button span',
        'list_selector': '.what-we-do-list-items li',
        'link_selector': 'a'
    },
    'HCLTECH': {
        'name': 'HCL Technologies',
        'url': 'https://www.hcltech.com/technology-services',
        'type': 'grid_cards',
        'card_selector': '.offering-card, .service-item',
        'title_selector': '.title, h3',
        'description_selector': '.desc, p'
    },
    'TECHM': {
        'name': 'Tech Mahindra',
        'url': 'https://www.techmahindra.com/en-in/services/',
        'type': 'list_grid',
        'container': '.service-listing, .services-grid',
        'item_selector': '.service-item',
        'title_selector': '.service-title, h3'
    },
    'WIPRO': {
        'name': 'Wipro',
        'url': 'https://www.wipro.com/services/',
        'type': 'cards',
        'card_selector': '.service-card, .capability-card',
        'title_selector': '.card-title, h3',
        'description_selector': '.card-text, p'
    },
    'PERSISTENT': {
        'name': 'Persistent Systems',
        'url': 'https://www.persistent.com/services/',
        'type': 'grid',
        'item_selector': '.service-item, .grid-item',
        'title_selector': '.title, h3'
    },
    'COFORGE': {
        'name': 'Coforge',
        'url': 'https://www.coforge.com/services',
        'type': 'cards',
        'card_selector': '.service-block, .service-card',
        'title_selector': '.heading, h3'
    },
    'LTIM': {
        'name': 'LTIMindtree',
        'url': 'https://www.ltimindtree.com/services/',
        'type': 'grid',
        'item_selector': '.service-tile, .grid-item',
        'title_selector': '.title, h3'
    },
    'MPHASIS': {
        'name': 'Mphasis',
        'url': 'https://www.mphasis.com/services.html',
        'type': 'cards',
        'card_selector': '.service-box, .service-card',
        'title_selector': '.title, h3'
    },
    'OFSS': {
        'name': 'Oracle Financial Services Software',
        'url': 'https://www.oracle.com/financial-services/',
        'type': 'grid_cards',
        'card_selector': '.product-card, .offer-card',
        'title_selector': '.title, h3'
    }
}