"""
Indian Misinformation Pattern Detector
Specialized patterns for Indian context
"""
import re
from typing import Dict, List

class IndianMisinfoDetector:
    """Detects misinformation patterns specific to Indian context"""
    
    def __init__(self):
        # Common Indian misinformation patterns
        self.whatsapp_patterns = [
            r'good morning.*forward.*10 people',
            r'share.*this.*message.*luck',
            r'govt.*scheme.*apply.*immediately',
            r'bank.*account.*blocked.*click'
        ]
        
        # COVID-19 specific myths common in India
        self.covid_myths = [
            'cow urine', 'gaumutra', 'home remedy cures covid',
            'ayurveda prevents corona', 'turmeric immunity',
            'hot water kills virus', 'garlic prevents covid'
        ]
        
        # Political misinformation patterns
        self.political_patterns = [
            'survey shows.*%.*votes',
            'exit poll predicts',
            'leaked video shows',
            'whatsapp university'
        ]
        
        # Financial scam patterns
        self.financial_scams = [
            'earn.*lakhs.*from home',
            'government giving.*money',
            'lottery winner.*claim prize',
            'investment returns.*%.*guaranteed'
        ]
    
    def analyze_indian_context(self, text: str) -> Dict:
        """Analyze text for Indian misinformation patterns"""
        text_lower = text.lower()
        risk_factors = []
        india_score = 0
        
        # Check WhatsApp-style patterns
        for pattern in self.whatsapp_patterns:
            if re.search(pattern, text_lower):
                risk_factors.append("WhatsApp-style viral message pattern")
                india_score += 25
        
        # Check COVID myths
        for myth in self.covid_myths:
            if myth in text_lower:
                risk_factors.append(f"COVID-19 misinformation: {myth}")
                india_score += 30
        
        # Check political patterns
        for pattern in self.political_patterns:
            if re.search(pattern, text_lower):
                risk_factors.append("Political misinformation pattern")
                india_score += 20
        
        # Check financial scams
        for scam in self.financial_scams:
            if re.search(scam, text_lower):
                risk_factors.append("Financial scam pattern")
                india_score += 35
        
        return {
            'india_specific_risk': min(100, india_score),
            'regional_patterns': risk_factors,
            'context': 'indian_misinformation'
        }
