#!/usr/bin/env python3
"""Test script to verify Gemini API is working"""

import os
import sys
sys.path.append('./backend')

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from backend.modules.gemini_integration import GeminiAnalyzer

def test_gemini():
    print("Testing Gemini API integration...")
    
    # Initialize analyzer
    analyzer = GeminiAnalyzer()
    
    if not analyzer.available:
        print("❌ Gemini API not available")
        return False
    
    print("✅ Gemini API initialized successfully")
    
    # Test text analysis
    test_text = "SHOCKING! This will amaze you!"
    
    try:
        result = analyzer.analyze_text(test_text)
        print(f"✅ Text analysis successful")
        print(f"   Risk Score: {result.get('risk_score', 0)}")
        print(f"   Red Flags: {len(result.get('red_flags', []))}")
        print(f"   AI Confidence: {result.get('ai_confidence', 'unknown')}")
        return True
        
    except Exception as e:
        print(f"❌ Text analysis failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini()
