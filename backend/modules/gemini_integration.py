import google.generativeai as genai
import os
from typing import Dict, List
import logging
import json
import base64
from PIL import Image

logger = logging.getLogger(__name__)

class GeminiAnalyzer:
    """Integrates with Google's Gemini AI for advanced content analysis"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                # Use the correct model names for Gemini
                self.model = genai.GenerativeModel('gemini-1.5-flash')  # Faster, free tier friendly
                self.available = True
                logger.info("Gemini AI integration initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing Gemini: {str(e)}")
                self.available = False
        else:
            self.available = False
            logger.warning("Gemini API key not found. AI analysis will be limited.")
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze text content using Gemini AI
        
        Args:
            text: The text content to analyze
            
        Returns:
            Dictionary containing AI analysis results
        """
        if not self.available:
            return self._get_fallback_analysis()
        
        try:
            # Limit text length to avoid quota issues
            if len(text) > 1000:
                text = text[:1000] + "..."
            
            prompt = self._create_simple_text_prompt(text)
            
            # Add safety settings to avoid blocking
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
            
            response = self.model.generate_content(
                prompt,
                safety_settings=safety_settings,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=500,
                )
            )
            
            if response.text:
                # Simple parsing instead of complex JSON
                return self._parse_simple_response(response.text)
            else:
                logger.warning("Empty response from Gemini AI")
                return self._get_fallback_analysis()
                
        except Exception as e:
            logger.error(f"Error in Gemini text analysis: {str(e)}")
            return self._get_fallback_analysis()
    
    def analyze_image(self, image_path: str) -> Dict:
        """
        Analyze image content using Gemini AI
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing AI analysis results
        """
        if not self.available:
            return self._get_fallback_analysis()
        
        try:
            # Load and prepare image
            image = Image.open(image_path)
            
            # Simple image analysis prompt
            prompt = """
Analyze this image for potential manipulation or misleading content. 
Rate manipulation risk 0-100 and list any concerns.

Look for: digital manipulation, inconsistent lighting/shadows, misleading context, deepfakes.

Response format:
Risk Score: [0-100]
Issues: [list problems found]
Explanation: [brief explanation]
"""
            
            response = self.model.generate_content([prompt, image])
            
            if response.text:
                analysis = self._parse_simple_response(response.text)
                return analysis
            else:
                logger.warning("Empty response from Gemini Vision")
                return self._get_fallback_analysis()
                
        except Exception as e:
            logger.error(f"Error in Gemini image analysis: {str(e)}")
            return self._get_fallback_analysis()
    
    def _create_simple_text_prompt(self, text: str) -> str:
        """Create a simple, reliable prompt for text analysis"""
        return f"""
Analyze this text for misinformation indicators. Rate the risk from 0-100 and explain why.

Text: "{text}"

Please respond with:
Risk Score: [0-100]
Main Issues: [list up to 3 key problems]
Explanation: [brief explanation]
Verification: [suggest 1-2 verification steps]

Focus on: emotional manipulation, unsupported claims, suspicious language patterns, or misleading information.
"""

    def _parse_simple_response(self, response_text: str) -> Dict:
        """Parse simple AI response format"""
        try:
            # Extract risk score
            risk_score = 0
            if "Risk Score:" in response_text or "risk score" in response_text.lower():
                import re
                score_match = re.search(r'(?:Risk Score:|risk score:?)\s*(\d+)', response_text, re.IGNORECASE)
                if score_match:
                    risk_score = min(100, max(0, int(score_match.group(1))))
            
            # Extract issues/red flags
            red_flags = []
            if "Main Issues:" in response_text or "issues:" in response_text.lower():
                # Try to extract issues section
                issues_start = response_text.lower().find("issues:")
                if issues_start != -1:
                    issues_section = response_text[issues_start:issues_start+200]
                    # Look for bullet points or listed items
                    lines = issues_section.split('\n')
                    for line in lines[1:4]:  # Take up to 3 lines after "Issues:"
                        if line.strip() and not line.lower().startswith('explanation'):
                            red_flags.append(line.strip(' -•*'))
            
            # Extract explanation
            explanation = "AI analysis completed"
            if "Explanation:" in response_text:
                exp_start = response_text.find("Explanation:")
                if exp_start != -1:
                    exp_section = response_text[exp_start+12:exp_start+300]
                    exp_end = exp_section.find("Verification:")
                    if exp_end != -1:
                        explanation = exp_section[:exp_end].strip()
                    else:
                        explanation = exp_section.strip()
            
            # Extract verification steps
            verification_steps = []
            if "Verification:" in response_text:
                ver_start = response_text.find("Verification:")
                if ver_start != -1:
                    ver_section = response_text[ver_start+13:ver_start+200]
                    lines = ver_section.split('\n')
                    for line in lines[:3]:  # Take up to 3 lines
                        if line.strip():
                            verification_steps.append(line.strip(' -•*'))
            
            return {
                'risk_score': risk_score,
                'red_flags': red_flags if red_flags else ["AI detected potential concerns"],
                'explanation': explanation,
                'verification_steps': verification_steps if verification_steps else ["Verify with trusted sources"],
                'ai_confidence': 'high' if risk_score > 0 else 'medium'
            }
            
        except Exception as e:
            logger.error(f"Error parsing simple response: {str(e)}")
            # Return the raw response with basic parsing
            return {
                'risk_score': 30,  # Moderate score when unsure
                'red_flags': ["Unable to parse AI response completely"],
                'explanation': response_text[:200] + "..." if len(response_text) > 200 else response_text,
                'verification_steps': ["Manually verify information"],
                'ai_confidence': 'low'
            }
    def _get_fallback_analysis(self) -> Dict:
        """Provide fallback analysis when AI is unavailable"""
        return {
            'risk_score': 0,
            'red_flags': [],
            'explanation': 'AI analysis unavailable. Using rule-based analysis instead.',
            'verification_steps': [
                'Manually verify information with trusted sources',
                'Check for author credentials and publication date'
            ],
            'ai_confidence': 'unavailable'
        }
    
    def get_analysis_explanation(self, content_type: str, analysis_results: Dict) -> str:
        """Generate human-readable explanation of analysis results"""
        if not self.available:
            return "AI-powered analysis is currently unavailable. Please use manual verification methods."
        
        try:
            risk_score = analysis_results.get('risk_score', 0)
            red_flags = analysis_results.get('red_flags', [])
            
            if risk_score >= 70:
                risk_level = "HIGH RISK"
                color = "red"
            elif risk_score >= 40:
                risk_level = "MODERATE RISK"
                color = "orange"
            elif risk_score >= 20:
                risk_level = "LOW RISK"
                color = "yellow"
            else:
                risk_level = "MINIMAL RISK"
                color = "green"
            
            explanation = f"**{risk_level}** (Score: {risk_score}/100)\n\n"
            
            if red_flags:
                explanation += "**Key Concerns:**\n"
                for flag in red_flags[:5]:  # Limit to top 5 flags
                    explanation += f"• {flag}\n"
                explanation += "\n"
            
            explanation += analysis_results.get('explanation', '')
            
            verification_steps = analysis_results.get('verification_steps', [])
            if verification_steps:
                explanation += "\n\n**Recommended Verification Steps:**\n"
                for step in verification_steps[:3]:  # Limit to top 3 steps
                    explanation += f"• {step}\n"
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            return "Error generating analysis explanation."
