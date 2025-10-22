# books/services/trending.py
"""
Trending Niches Taxonomy for 2025-2027
Maps sub-niches to trending topics, tools, and market opportunities
"""

TRENDING_NICHES_2025_2027 = {
    'AI & Digital Transformation': {
        'ai_business_automation': {
            'trends_2025': ['AI agents', 'No-code automation', 'RPA 2.0', 'Process mining'],
            'trends_2027': ['Autonomous workflows', 'Self-optimizing systems', 'Predictive automation'],
            'free_tools': ['Zapier Free', 'Make.com', 'n8n', 'Automate.io', 'IFTTT'],
            'audience': 'Business owners and entrepreneurs',
            'market_size': 'Growing rapidly - $19.6B by 2026'
        },
        'machine_learning_basics': {
            'trends_2025': ['AutoML platforms', 'MLOps', 'Citizen data scientists', 'No-code ML'],
            'trends_2027': ['Federated learning', 'TinyML edge devices', 'Explainable AI mainstream'],
            'free_tools': ['Google Colab', 'Kaggle', 'Teachable Machine', 'Orange', 'KNIME'],
            'audience': 'Non-technical professionals and students',
            'market_size': '$209.91B by 2029'
        },
        'digital_transformation_strategy': {
            'trends_2025': ['Digital twins', 'Cloud-native architecture', 'API-first design', 'Microservices'],
            'trends_2027': ['Quantum-ready infrastructure', 'Decentralized systems', 'Web3 integration'],
            'free_tools': ['Miro', 'Figma', 'Notion', 'Trello', 'Google Workspace'],
            'audience': 'C-suite executives and managers',
            'market_size': '$3.4T by 2026'
        },
        'ai_ethics_governance': {
            'trends_2025': ['AI auditing', 'Bias detection tools', 'Responsible AI frameworks', 'Privacy-by-design'],
            'trends_2027': ['AI regulation compliance', 'Ethical AI certification', 'Transparent AI mandates'],
            'free_tools': ['IBM AI Fairness 360', 'Google What-If Tool', 'Microsoft Fairlearn'],
            'audience': 'AI practitioners and policymakers',
            'market_size': 'Emerging - critical compliance requirement'
        },
        'chatgpt_productivity': {
            'trends_2025': ['Custom GPTs', 'Prompt marketplaces', 'AI assistants', 'Multi-modal prompts'],
            'trends_2027': ['Personalized AI tutors', 'Context-aware AI', 'Seamless AI integration'],
            'free_tools': ['ChatGPT Free', 'Claude', 'Perplexity AI', 'Microsoft Copilot', 'Bard'],
            'audience': 'Knowledge workers and content creators',
            'market_size': '$1.3B prompt engineering market by 2028'
        },
        'data_driven_decisions': {
            'trends_2025': ['Self-service BI', 'Real-time analytics', 'Embedded analytics', 'Augmented analytics'],
            'trends_2027': ['AI-powered insights', 'Predictive decision engines', 'Automated reporting'],
            'free_tools': ['Google Analytics', 'Tableau Public', 'Power BI Free', 'Looker Studio', 'Metabase'],
            'audience': 'Business analysts and managers',
            'market_size': '$346B by 2029'
        },
        'ai_content_creation': {
            'trends_2025': ['AI video generation', 'Voice cloning', 'Style transfer', 'Content personalization'],
            'trends_2027': ['Hyper-personalized content', 'Real-time content adaptation', 'Multi-modal generation'],
            'free_tools': ['Canva AI', 'Copy.ai Free', 'Jasper Trial', 'Dall-E', 'Midjourney Trial'],
            'audience': 'Marketers and content professionals',
            'market_size': '$16.3B by 2030'
        },
        'automation_workflows': {
            'trends_2025': ['Visual workflow builders', 'Pre-built integrations', 'Low-code platforms'],
            'trends_2027': ['AI-suggested workflows', 'Self-healing automations', 'Contextual triggers'],
            'free_tools': ['Zapier Free', 'IFTTT', 'n8n', 'Pipedream', 'Integromat Free'],
            'audience': 'Operations managers and tech enthusiasts',
            'market_size': '$19.6B by 2027'
        },
    },
    
    'Sustainability & Green Tech': {
        'renewable_energy_solutions': {
            'trends_2025': ['Home solar + storage', 'Community solar', 'Smart grids', 'Energy management systems'],
            'trends_2027': ['Peer-to-peer energy trading', 'Micro-grids', 'Green hydrogen homes'],
            'free_tools': ['Google Project Sunroof', 'PVWatts Calculator', 'Energy Sage', 'Home Energy Saver'],
            'audience': 'Homeowners and eco-conscious consumers',
            'market_size': '$1.5T by 2025'
        },
        'circular_economy_principles': {
            'trends_2025': ['Product-as-service', 'Refurbishment markets', 'Waste-to-value', 'Reverse logistics'],
            'trends_2027': ['Blockchain for circularity', 'Bio-material loops', 'Zero-waste manufacturing'],
            'free_tools': ['Ellen MacArthur Toolkit', 'Circularity Calculator', 'Product Circularity Indicator'],
            'audience': 'Sustainable business leaders',
            'market_size': '$4.5T opportunity by 2030'
        },
        'green_technology_innovations': {
            'trends_2025': ['Carbon capture tech', 'Green hydrogen', 'Vertical farming', 'Bio-plastics'],
            'trends_2027': ['Lab-grown materials', 'Ocean cleanup tech', 'Climate-positive materials'],
            'free_tools': ['Climate Tech VC Database', 'Crunchbase Green Tech', 'AngelList Climate'],
            'audience': 'Entrepreneurs and investors',
            'market_size': '$44.5B climate tech VC in 2023'
        },
        'carbon_neutral_living': {
            'trends_2025': ['Personal carbon trackers', 'Offset platforms', 'Eco-labels', 'Green commuting'],
            'trends_2027': ['Carbon wallets', 'Neighborhood net-zero', 'Climate-positive lifestyles'],
            'free_tools': ['UN Carbon Footprint Calculator', 'WWF Footprint', 'Ecosia Browser', 'JouleBug'],
            'audience': 'Eco-conscious individuals',
            'market_size': '$100B carbon offset market by 2030'
        },
        'sustainable_supply_chain': {
            'trends_2025': ['Supply chain transparency', 'Ethical sourcing', 'Green logistics', 'Traceability'],
            'trends_2027': ['Blockchain supply chains', 'AI-optimized routes', 'Regenerative supply chains'],
            'free_tools': ['OpenLCA', 'EcoVadis Free Resources', 'Sourcemap', 'Supply Chain CSR Self-Assessment'],
            'audience': 'Supply chain managers',
            'market_size': '$42.7B green logistics by 2027'
        },
        'eco_friendly_investing': {
            'trends_2025': ['ESG scores', 'Impact investing', 'Green bonds', 'Climate-focused ETFs'],
            'trends_2027': ['Mandatory ESG reporting', 'Carbon-adjusted returns', 'Nature-positive portfolios'],
            'free_tools': ['Yahoo Finance ESG', 'As You Sow', 'Morningstar Sustainability', 'MSCI ESG Ratings'],
            'audience': 'Individual and institutional investors',
            'market_size': '$53T ESG assets by 2025'
        },
        'green_building_design': {
            'trends_2025': ['Net-zero buildings', 'Green certifications', 'Smart HVAC', 'Biophilic design'],
            'trends_2027': ['Living buildings', 'Carbon-storing materials', 'Self-sufficient structures'],
            'free_tools': ['SketchUp Free', 'Sweet Home 3D', 'Tinkercad', 'EnergyPlus'],
            'audience': 'Architects and developers',
            'market_size': '$774B by 2030'
        },
        'climate_tech_startups': {
            'trends_2025': ['Climate adaptation tech', 'Carbon removal', 'Sustainable materials', 'Clean energy'],
            'trends_2027': ['Geoengineering', 'Climate resilience platforms', 'Regenerative agriculture tech'],
            'free_tools': ['Climate Tech VC Database', 'CTVC List', 'Greentown Labs Resources'],
            'audience': 'Founders and VCs',
            'market_size': '$1.4T climate tech opportunity'
        },
    },
    
    'Mental Health Technology': {
        'ai_mental_health_apps': {
            'trends_2025': ['AI therapists', 'Mood tracking', 'Personalized interventions', 'Crisis detection'],
            'trends_2027': ['Preventive mental health AI', 'Neuro-adaptive apps', 'Virtual reality therapy'],
            'free_tools': ['Woebot', 'Wysa', 'Youper', 'Sanvello Free', 'Calm Free'],
            'audience': 'Mental health seekers',
            'market_size': '$17B by 2030'
        },
        'digital_wellness_tools': {
            'trends_2025': ['Screen time management', 'Digital detox apps', 'Mindfulness tech', 'Sleep tech'],
            'trends_2027': ['Ambient wellness', 'Preventive digital health', 'Holistic wellbeing platforms'],
            'free_tools': ['Headspace Free', 'Insight Timer', 'Forest App', 'Freedom', 'RescueTime'],
            'audience': 'Tech users seeking balance',
            'market_size': '$6.9B wellness apps by 2027'
        },
        'teletherapy_platforms': {
            'trends_2025': ['On-demand therapy', 'AI-matched therapists', 'Group therapy online', 'Hybrid care'],
            'trends_2027': ['VR therapy rooms', 'AI co-therapists', 'Integrated health records'],
            'free_tools': ['BetterHelp Trial', 'Talkspace Trial', '7 Cups Free Support', 'OpenCounseling Directory'],
            'audience': 'Therapy seekers',
            'market_size': '$56.5B by 2030'
        },
        'mental_health_ai_diagnostics': {
            'trends_2025': ['Voice analysis', 'Facial recognition for mood', 'Pattern detection', 'Early warning systems'],
            'trends_2027': ['Predictive mental health models', 'Biomarker detection', 'Continuous monitoring'],
            'free_tools': ['PHQ-9 Online', 'GAD-7 Assessment', 'Mental Health America Screening', 'Psychology Today Tests'],
            'audience': 'Healthcare providers and patients',
            'market_size': 'Emerging - part of $280B digital health'
        },
        'stress_management_apps': {
            'trends_2025': ['Biofeedback apps', 'Breathing exercises', 'Stress tracking', 'Guided relaxation'],
            'trends_2027': ['Real-time stress intervention', 'Wearable integration', 'Context-aware calming'],
            'free_tools': ['Breathe2Relax', 'Calm Free', 'Headspace Basics', 'Sanvello', 'Happify Free'],
            'audience': 'Stressed professionals',
            'market_size': '$4.2B by 2027'
        },
        'cognitive_behavioral_tech': {
            'trends_2025': ['Digital CBT', 'Self-guided therapy', 'Thought tracking', 'Exposure therapy apps'],
            'trends_2027': ['AI-powered CBT', 'VR exposure therapy', 'Personalized treatment plans'],
            'free_tools': ['MoodGYM', 'MindShift CBT', 'What\'s Up', 'Pacifica', 'Sanvello CBT Tools'],
            'audience': 'Therapy patients and providers',
            'market_size': '$2.3B digital therapeutics by 2026'
        },
        'mental_health_wearables': {
            'trends_2025': ['Stress tracking rings', 'EEG headbands', 'HRV monitors', 'Sleep trackers'],
            'trends_2027': ['Emotion-sensing wearables', 'Brain-computer interfaces', 'Preventive alerts'],
            'free_tools': ['Oura Ring Data', 'Fitbit Stress Management', 'Apple Watch Mindfulness', 'Garmin Body Battery'],
            'audience': 'Health-conscious tech users',
            'market_size': '$27.8B wearables by 2026'
        },
        'workplace_mental_health_tech': {
            'trends_2025': ['Employee assistance platforms', 'Anonymous support', 'Wellness challenges', 'Mental health dashboards'],
            'trends_2027': ['Predictive burnout detection', 'AI coaching', 'Integrated benefits platforms'],
            'free_tools': ['Headspace for Work Trial', 'Ginger Free Resources', 'Lyra Health Info', 'Spring Health Guides'],
            'audience': 'HR professionals and employees',
            'market_size': '$14.7B corporate wellness by 2027'
        },
    },
    
    'Future Skills & Digital Economy': {
        'remote_work_mastery': {
            'trends_2025': ['Hybrid work models', 'Async communication', 'Remote-first tools', 'Digital nomad visas'],
            'trends_2027': ['VR workspaces', 'AI meeting assistants', 'Borderless employment'],
            'free_tools': ['Zoom Free', 'Slack Free', 'Notion', 'Trello', 'Google Meet', 'Loom Free'],
            'audience': 'Remote workers and managers',
            'market_size': '$418.4B remote work tech by 2030'
        },
        'blockchain_cryptocurrency': {
            'trends_2025': ['DeFi platforms', 'NFT utilities', 'Layer 2 solutions', 'Central bank digital currencies'],
            'trends_2027': ['Web3 mainstream', 'Tokenized everything', 'DAO governance standard'],
            'free_tools': ['MetaMask', 'Coinbase Learn', 'Binance Academy', 'Blockchain.com Wallet'],
            'audience': 'Crypto enthusiasts and investors',
            'market_size': '$4.94T crypto market cap (2023 peak)'
        },
        'metaverse_virtual_reality': {
            'trends_2025': ['Virtual meetings', 'Digital twins', 'VR training', 'Social VR'],
            'trends_2027': ['Persistent metaverses', 'AR overlays', 'Virtual economies'],
            'free_tools': ['Mozilla Hubs', 'VRChat', 'Rec Room', 'Spatial', 'FrameVR'],
            'audience': 'Early adopters and developers',
            'market_size': '$800B metaverse by 2024'
        },
        'cybersecurity_essentials': {
            'trends_2025': ['Zero trust architecture', 'AI threat detection', 'Cloud security', 'Privacy tools'],
            'trends_2027': ['Quantum-safe encryption', 'Automated security', 'Cyber resilience'],
            'free_tools': ['LastPass Free', 'Bitwarden', 'ProtonMail Free', 'Malwarebytes Free', 'Cloudflare WARP'],
            'audience': 'Everyone with digital presence',
            'market_size': '$345.4B by 2026'
        },
        'digital_entrepreneurship': {
            'trends_2025': ['No-code businesses', 'Creator economy', 'Micro-SaaS', 'AI-powered startups'],
            'trends_2027': ['DAO businesses', 'Autonomous companies', 'Web3 business models'],
            'free_tools': ['Gumroad', 'Carrd', 'Webflow Free', 'Notion', 'Bubble Free', 'Stripe'],
            'audience': 'Aspiring entrepreneurs',
            'market_size': '$456.7B creator economy by 2027'
        },
        'quantum_computing_basics': {
            'trends_2025': ['Quantum cloud access', 'Hybrid algorithms', 'Quantum simulations', 'Q-learning'],
            'trends_2027': ['Quantum advantage', 'Commercial quantum apps', 'Quantum-safe migration'],
            'free_tools': ['IBM Quantum Experience', 'Quirk Simulator', 'Qiskit Textbook', 'Microsoft Q# Simulator'],
            'audience': 'Tech leaders and researchers',
            'market_size': '$65B by 2030'
        },
        'iot_smart_homes': {
            'trends_2025': ['Matter standard', 'Voice assistants', 'Energy management', 'Security systems'],
            'trends_2027': ['Predictive automation', 'Health monitoring homes', 'Sustainable smart homes'],
            'free_tools': ['Google Home', 'Alexa App', 'Home Assistant', 'IFTTT', 'SmartThings'],
            'audience': 'Homeowners and tech enthusiasts',
            'market_size': '$537.0B by 2030'
        },
        'nft_digital_assets': {
            'trends_2025': ['Utility NFTs', 'Digital identity', 'Tokenized IP', 'NFT marketplaces'],
            'trends_2027': ['Real-world asset tokenization', 'NFT-backed loans', 'Dynamic NFTs'],
            'free_tools': ['OpenSea', 'Rarible', 'Mintable', 'Foundation', 'Zora'],
            'audience': 'Creators and collectors',
            'market_size': '$80B by 2025'
        },
    },
}


def get_trending_context(sub_niche: str) -> dict:
    """
    Get trending context for a sub-niche
    Returns trends, tools, audience, and market data
    """
    for category, niches in TRENDING_NICHES_2025_2027.items():
        if sub_niche in niches:
            return {
                'category': category,
                **niches[sub_niche]
            }
    
    # Default fallback
    return {
        'category': 'Professional Development',
        'trends_2025': ['Innovation', 'Digital transformation', 'Growth mindset'],
        'trends_2027': ['Future-ready skills', 'Adaptability', 'Continuous learning'],
        'free_tools': ['Google', 'YouTube', 'Coursera Free', 'edX Free', 'Khan Academy'],
        'audience': 'Modern professionals',
        'market_size': 'Growing opportunity'
    }


def get_related_niches(sub_niche: str, limit: int = 8) -> list:
    """
    Get related sub-niches from the same category
    """
    for category, niches in TRENDING_NICHES_2025_2027.items():
        if sub_niche in niches:
            related = [key for key in niches.keys() if key != sub_niche]
            return related[:limit]
    
    return []


def format_trending_bullets(context: dict) -> str:
    """
    Format trending context as bullet points for prompts
    """
    bullets = []
    
    if 'trends_2025' in context:
        bullets.append(f"**2025 Trends**: {', '.join(context['trends_2025'][:4])}")
    
    if 'trends_2027' in context:
        bullets.append(f"**2027 Emerging**: {', '.join(context['trends_2027'][:3])}")
    
    if 'free_tools' in context:
        bullets.append(f"**Free Tools**: {', '.join(context['free_tools'][:5])}")
    
    if 'market_size' in context:
        bullets.append(f"**Market Opportunity**: {context['market_size']}")
    
    return '\n'.join(bullets)
