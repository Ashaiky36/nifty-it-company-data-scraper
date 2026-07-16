# config/manual_services.py
"""
Manual service mappings for companies that block scraping
"""
MANUAL_SERVICES = {
    'TCS': {
        'services': [
            {'name': 'Cloud', 'sub_services': ['Cloud Migration', 'Cloud Native', 'Multi-Cloud']},
            {'name': 'AI & Analytics', 'sub_services': ['AI Strategy', 'Data Analytics', 'Machine Learning']},
            {'name': 'Cybersecurity', 'sub_services': ['Security Services', 'Risk Management', 'Compliance']},
            {'name': 'Digital Transformation', 'sub_services': ['Digital Strategy', 'UX Design', 'Digital Marketing']},
            {'name': 'Consulting', 'sub_services': ['Business Consulting', 'IT Strategy', 'Digital Advisory']},
            {'name': 'Application Development', 'sub_services': ['Custom Development', 'Legacy Modernization', 'DevOps']},
            {'name': 'Enterprise Solutions', 'sub_services': ['ERP', 'CRM', 'Supply Chain']}
        ]
    },
    'INFY': {
        'services': [
            {'name': 'Application Development', 'sub_services': ['DevOps', 'Microservices', 'API Economy']},
            {'name': 'Cloud Services', 'sub_services': ['Cloud Migration', 'Hybrid Cloud', 'Cloud Security']},
            {'name': 'Data & Analytics', 'sub_services': ['Big Data', 'Analytics', 'Data Governance']},
            {'name': 'Digital Experience', 'sub_services': ['UX/UI', 'Digital Marketing', 'Commerce']},
            {'name': 'Cybersecurity', 'sub_services': ['Security Strategy', 'Risk Management', 'Compliance']},
            {'name': 'AI & Automation', 'sub_services': ['AI Strategy', 'RPA', 'Cognitive Services']},
            {'name': 'Enterprise Solutions', 'sub_services': ['ERP', 'CRM', 'Supply Chain']}
        ]
    }
}