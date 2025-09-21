"""
Demo content for hackathon presentation
Real Indian misinformation examples for testing
"""

DEMO_MISINFORMATION_EXAMPLES = {
    "covid_myth": {
        "text": "URGENT: Govt doctors don't want you to know! Drinking hot water with turmeric and cow urine 3 times daily COMPLETELY prevents COVID-19! Big pharma hiding this truth! Share with 10 friends immediately for protection! 🙏",
        "expected_risk": 85,
        "category": "Health Misinformation"
    },
    
    "whatsapp_forward": {
        "text": "Good morning! 🌅 Reliance Jio is giving FREE 1TB data to first 1000 people who forward this message to 20 contacts. Offer valid till tonight only! Don't miss this golden opportunity! Forward now! 📱💯",
        "expected_risk": 90,
        "category": "WhatsApp Scam"
    },
    
    "political_deepfake": {
        "text": "LEAKED VIDEO: Opposition leader caught taking Rs 500 crore bribe! Media hiding this scandal! Watch before it gets deleted! Share everywhere! This will change election results! 🔥🔥",
        "expected_risk": 95,
        "category": "Political Misinformation"
    },
    
    "financial_scam": {
        "text": "🎉 CONGRATULATIONS! You have won Rs 25 LAKH in Modi Government's Digital India Lottery! Claim your prize by clicking this link and providing Aadhaar details. Limited time offer! 💰",
        "expected_risk": 100,
        "category": "Financial Fraud"
    },
    
    "fake_news": {
        "text": "BREAKING: Scientists at IIT Delhi discover new element that can solve India's energy crisis! This revolutionary finding will make petrol price Rs 5 per liter! Government trying to suppress this news!",
        "expected_risk": 75,
        "category": "Fake Scientific Claims"
    },
    
    "reliable_content": {
        "text": "According to a peer-reviewed study published in The Lancet by researchers at AIIMS Delhi, the new COVID-19 variant shows 15% increased transmissibility. The study, conducted over 6 months with 10,000 participants, suggests continued mask usage in crowded areas. Full paper available at doi.org/example",
        "expected_risk": 10,
        "category": "Credible Information"
    }
}

REGIONAL_EDUCATIONAL_CONTENT = {
    "hindi_tips": [
        "संदिग्ध संदेशों को तुरंत शेयर न करें",
        "स्रोत की विश्वसनीयता जांचें",
        "तथ्य-जांच वेबसाइटों का उपयोग करें",
        "भावनात्मक भाषा से सावधान रहें"
    ],
    
    "whatsapp_awareness": [
        "WhatsApp forwards are often unverified",
        "Check sender credibility before believing",
        "Don't forward without fact-checking",
        "Be skeptical of 'urgent' messages"
    ],
    
    "indian_fact_checkers": [
        "Alt News (altnews.in)",
        "Boom Live (boomlive.in)", 
        "The Quint WebQoof",
        "India Today Fact Check"
    ]
}
