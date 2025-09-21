from typing import Dict, List
import random

class EducationalContent:
    """Provides educational content about misinformation detection"""
    
    def __init__(self):
        self.general_tips = [
            "Check the source: Look for author credentials, publication date, and website reputation",
            "Cross-reference information: Verify claims with multiple reliable sources",
            "Look for evidence: Credible content should cite sources and provide supporting data",
            "Check your emotions: Misinformation often triggers strong emotional responses",
            "Be skeptical of sensational headlines: If it seems too shocking to be true, investigate further",
            "Look for recent updates: Check if information is current and hasn't been debunked",
            "Consider the source's motivation: Ask why this information is being shared",
            "Use fact-checking websites: Consult Snopes, FactCheck.org, or PolitiFact for verification"
        ]
        
        self.text_specific_tips = [
            "Watch for emotional language designed to make you angry or afraid",
            "Be suspicious of articles with ALL CAPS or excessive exclamation points",
            "Look for specific dates, names, and verifiable facts",
            "Check if quotes are properly attributed to real, identifiable people",
            "Be wary of articles that lack author information or publication dates",
            "Notice if the content makes you want to share immediately - that's often intentional",
            "Look for grammatical errors or awkward phrasing that might indicate poor quality",
            "Check if extraordinary claims are supported by extraordinary evidence"
        ]
        
        self.url_specific_tips = [
            "Check the website's 'About' page to understand who runs it",
            "Look at the URL carefully - fake sites often mimic real news sources",
            "See if the website has contact information and editorial policies",
            "Check when the domain was registered - very new sites might be suspicious",
            "Look for other articles on the site - is there a pattern of biased or false content?",
            "See if the website has advertisements that seem questionable or spammy",
            "Check if the site has been flagged by browser security warnings",
            "Look for professional design and layout - legitimate news sites invest in quality"
        ]
        
        self.image_specific_tips = [
            "Use reverse image search to see if the image appears elsewhere online",
            "Look for inconsistencies in lighting, shadows, or image quality",
            "Check if the image matches the context of the story it's used with",
            "Be aware that real photos can be used to illustrate false stories",
            "Look for signs of digital manipulation like blurred edges or color inconsistencies",
            "Check the image metadata if available - when and where was it taken?",
            "Be suspicious of images that seem too perfect or dramatic",
            "Consider whether the image could have been staged or taken out of context"
        ]
        
        self.red_flags = [
            "No author byline or contact information",
            "Emotional, inflammatory language designed to provoke strong reactions",
            "Claims that 'they' don't want you to know something",
            "Requests to share immediately before 'it gets taken down'",
            "Extraordinary claims without credible evidence",
            "Grammar and spelling errors in professional content",
            "Lack of publication date or very recent dates on 'breaking' news",
            "URLs that mimic legitimate news sites but with slight variations",
            "Content that confirms your existing beliefs without challenging them",
            "Appeals to 'common sense' without providing actual evidence"
        ]
        
        self.verification_steps = [
            {
                "step": "Source Verification",
                "description": "Research the publisher, author, and publication to establish credibility",
                "actions": [
                    "Look up the author's credentials and other published work",
                    "Check the website's About page and contact information",
                    "See if the publication has editorial standards and corrections policies",
                    "Research the publication's funding sources and potential biases"
                ]
            },
            {
                "step": "Fact Checking",
                "description": "Verify specific claims and information presented",
                "actions": [
                    "Use established fact-checking websites like Snopes, FactCheck.org, or PolitiFact",
                    "Search for the same information on reputable news sources",
                    "Look for primary sources and original documents",
                    "Check if scientific or statistical claims cite peer-reviewed research"
                ]
            },
            {
                "step": "Cross-Reference",
                "description": "Compare information across multiple independent sources",
                "actions": [
                    "Search for the same story on at least 2-3 different reputable news sites",
                    "Look for expert opinions from relevant professionals",
                    "Check if major news organizations are reporting the same information",
                    "See if the information is being reported consistently across sources"
                ]
            },
            {
                "step": "Context Analysis",
                "description": "Understand the broader context and potential motivations",
                "actions": [
                    "Consider the timing of the information - why is it being shared now?",
                    "Think about who benefits from spreading this information",
                    "Look for what information might be missing or omitted",
                    "Consider alternative explanations for the events described"
                ]
            }
        ]
        
        self.common_manipulation_tactics = [
            {
                "name": "Emotional Manipulation",
                "description": "Using fear, anger, or outrage to bypass critical thinking",
                "examples": ["You won't believe what happened next!", "This will make you furious!", "Shocking truth revealed!"],
                "counter": "Take a moment to calm down before sharing. Ask yourself if you're being manipulated emotionally."
            },
            {
                "name": "False Urgency",
                "description": "Creating artificial time pressure to prevent verification",
                "examples": ["Share before this gets deleted!", "Breaking: Must read now!", "Time-sensitive information!"],
                "counter": "Real news doesn't disappear. Take time to verify before sharing."
            },
            {
                "name": "Cherry-Picking",
                "description": "Selecting only data that supports a predetermined conclusion",
                "examples": ["Studies show... (citing only favorable studies)", "Experts say... (quoting only agreeable experts)"],
                "counter": "Look for comprehensive analysis that considers multiple perspectives and studies."
            },
            {
                "name": "False Dichotomy",
                "description": "Presenting only two options when more exist",
                "examples": ["You're either with us or against us", "The only explanation is...", "It's either X or Y"],
                "counter": "Consider that complex issues usually have multiple perspectives and solutions."
            }
        ]
    
    def get_general_tips(self) -> List[str]:
        """Get general misinformation detection tips"""
        return self.general_tips
    
    def get_tips_for_text(self) -> List[str]:
        """Get tips specific to text content analysis"""
        return self.text_specific_tips
    
    def get_tips_for_urls(self) -> List[str]:
        """Get tips specific to URL/website analysis"""
        return self.url_specific_tips
    
    def get_tips_for_images(self) -> List[str]:
        """Get tips specific to image analysis"""
        return self.image_specific_tips
    
    def get_common_red_flags(self) -> List[str]:
        """Get list of common misinformation red flags"""
        return self.red_flags
    
    def get_verification_steps(self) -> List[Dict]:
        """Get structured verification steps"""
        return self.verification_steps
    
    def get_verification_suggestions(self, content_type: str = "general", risk_score: int = 50) -> List[str]:
        """Get verification suggestions based on content type and risk score"""
        suggestions = []
        
        if risk_score >= 70:
            suggestions.extend([
                "Immediately verify this content before sharing",
                "Check multiple fact-checking websites",
                "Search for the same information on 3+ reputable news sources",
                "Research the source's credibility and potential bias"
            ])
        elif risk_score >= 40:
            suggestions.extend([
                "Verify key claims before sharing",
                "Check at least one fact-checking website",
                "Look for the same story on reputable news sources"
            ])
        elif risk_score >= 20:
            suggestions.extend([
                "Consider verification if sharing widely",
                "Quick fact-check recommended"
            ])
        else:
            suggestions.extend([
                "Standard verification practices apply",
                "Check source if sharing to large audience"
            ])
        
        # Add content-specific suggestions
        if content_type == "text":
            suggestions.append("Look for emotional language that might be manipulative")
            suggestions.append("Check if extraordinary claims have supporting evidence")
        elif content_type == "url":
            suggestions.append("Research the website's reputation and editorial standards")
            suggestions.append("Check the domain registration and contact information")
        elif content_type == "image":
            suggestions.append("Use reverse image search to check if image is used elsewhere")
            suggestions.append("Look for signs of digital manipulation")
        
        return suggestions[:6]  # Return max 6 suggestions
    
    def get_manipulation_tactics(self) -> List[Dict]:
        """Get information about common manipulation tactics"""
        return self.common_manipulation_tactics
    
    def get_random_tip(self) -> str:
        """Get a random educational tip"""
        all_tips = (self.general_tips + self.text_specific_tips + 
                   self.url_specific_tips + self.image_specific_tips)
        return random.choice(all_tips)
    
    def get_content_specific_education(self, content_type: str, risk_score: int) -> Dict:
        """Get educational content tailored to specific content type and risk level"""
        
        education = {
            "risk_level": self._get_risk_level(risk_score),
            "immediate_action": self._get_immediate_action(risk_score),
            "specific_tips": [],
            "verification_priority": self._get_verification_priority(risk_score),
            "additional_resources": self._get_additional_resources()
        }
        
        # Add content-specific tips
        if content_type == "text":
            education["specific_tips"] = self.get_tips_for_text()[:5]
        elif content_type == "url":
            education["specific_tips"] = self.get_tips_for_urls()[:5]
        elif content_type == "image":
            education["specific_tips"] = self.get_tips_for_images()[:5]
        else:
            education["specific_tips"] = self.get_general_tips()[:5]
        
        return education
    
    def _get_risk_level(self, risk_score: int) -> str:
        """Determine risk level description"""
        if risk_score >= 70:
            return "HIGH RISK - This content shows multiple indicators of potential misinformation"
        elif risk_score >= 40:
            return "MODERATE RISK - This content has some concerning elements that warrant verification"
        elif risk_score >= 20:
            return "LOW RISK - Minor concerns detected, but likely legitimate content"
        else:
            return "MINIMAL RISK - Content appears to have good credibility indicators"
    
    def _get_immediate_action(self, risk_score: int) -> str:
        """Get recommended immediate action based on risk score"""
        if risk_score >= 70:
            return "DO NOT SHARE - Verify thoroughly before considering sharing"
        elif risk_score >= 40:
            return "PROCEED WITH CAUTION - Verify key claims before sharing"
        elif risk_score >= 20:
            return "VERIFY IF IMPORTANT - Consider verification if you plan to share"
        else:
            return "GENERALLY SAFE - Standard verification practices recommended"
    
    def _get_verification_priority(self, risk_score: int) -> List[str]:
        """Get prioritized verification steps based on risk level"""
        if risk_score >= 70:
            return [
                "Immediately check multiple fact-checking websites",
                "Search for the same information on 3+ reputable news sources",
                "Research the source's credibility and bias",
                "Look for expert opinions from relevant professionals"
            ]
        elif risk_score >= 40:
            return [
                "Check at least one fact-checking website",
                "Verify with 2+ reputable news sources",
                "Research the publisher's reputation"
            ]
        elif risk_score >= 20:
            return [
                "Quick fact-check if sharing widely",
                "Verify publisher credibility"
            ]
        else:
            return [
                "Standard verification practices",
                "Check source if sharing to large audience"
            ]
    
    def _get_additional_resources(self) -> Dict:
        """Get additional educational resources"""
        return {
            "fact_checkers": [
                {"name": "Snopes", "url": "https://www.snopes.com", "focus": "General fact-checking"},
                {"name": "FactCheck.org", "url": "https://www.factcheck.org", "focus": "Political claims"},
                {"name": "PolitiFact", "url": "https://www.politifact.com", "focus": "Political statements"},
                {"name": "AP Fact Check", "url": "https://apnews.com/hub/ap-fact-check", "focus": "News verification"}
            ],
            "reverse_image_search": [
                {"name": "Google Images", "url": "https://images.google.com", "description": "Upload or paste image URL"},
                {"name": "TinEye", "url": "https://tineye.com", "description": "Reverse image search engine"},
                {"name": "Bing Visual Search", "url": "https://www.bing.com/visualsearch", "description": "Microsoft's image search"}
            ],
            "media_literacy": [
                {"name": "News Literacy Project", "url": "https://newslit.org", "description": "Educational resources"},
                {"name": "MediaWise", "url": "https://www.poynter.org/mediawise/", "description": "Digital media literacy"},
                {"name": "First Draft", "url": "https://firstdraftnews.org", "description": "Verification handbook"}
            ]
        }
