import re
import string
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class TextAnalyzer:
    """Analyzes text content for potential misinformation indicators"""
    
    def __init__(self):
        # Emotional manipulation keywords
        self.emotional_keywords = [
            'shocking', 'unbelievable', 'you won\'t believe', 'doctors hate',
            'secret', 'hidden truth', 'they don\'t want you to know',
            'urgent', 'breaking', 'exclusive', 'leaked', 'exposed',
            'miracle', 'amazing', 'incredible', 'stunning',
            'destroy', 'devastating', 'terrifying', 'outrageous'
        ]
        
        # Clickbait patterns
        self.clickbait_patterns = [
            r'\d+\s+(things|ways|reasons|secrets)',
            r'you won\'t believe',
            r'this will (shock|amaze|surprise) you',
            r'what happened next',
            r'the answer will (shock|surprise) you',
            r'number \d+ will',
            r'wait until you see'
        ]
        
        # Unreliable source indicators
        self.unreliable_indicators = [
            'anonymous sources', 'sources say', 'reportedly',
            'allegedly', 'rumored', 'claims without evidence',
            'my friend told me', 'i heard that', 'word on the street'
        ]
        
        # Certainty words (overconfident language)
        self.certainty_words = [
            'definitely', 'absolutely', 'certainly', 'without doubt',
            'guaranteed', 'proven fact', 'undeniable', 'obvious',
            'clearly', 'obviously', 'everyone knows'
        ]
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze text for misinformation indicators
        
        Args:
            text: The text content to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            text_lower = text.lower()
            
            # Initialize analysis results
            red_flags = []
            risk_score = 0
            
            # Check for emotional manipulation
            emotional_score = self._check_emotional_manipulation(text_lower, red_flags)
            risk_score += emotional_score
            
            # Check for clickbait patterns
            clickbait_score = self._check_clickbait_patterns(text_lower, red_flags)
            risk_score += clickbait_score
            
            # Check for unreliable source indicators
            source_score = self._check_source_reliability(text_lower, red_flags)
            risk_score += source_score
            
            # Check language certainty
            certainty_score = self._check_certainty_language(text_lower, red_flags)
            risk_score += certainty_score
            
            # Sentiment analysis
            sentiment_score = self._analyze_sentiment(text, red_flags)
            risk_score += sentiment_score
            
            # Grammar and spelling check
            grammar_score = self._check_grammar_quality(text, red_flags)
            risk_score += grammar_score
            
            # Length and structure analysis
            structure_score = self._analyze_structure(text, red_flags)
            risk_score += structure_score
            
            # Normalize risk score to 0-100
            final_score = min(100, max(0, risk_score))
            
            return {
                'risk_score': final_score,
                'red_flags': red_flags,
                'details': {
                    'emotional_manipulation': emotional_score,
                    'clickbait_patterns': clickbait_score,
                    'source_reliability': source_score,
                    'certainty_language': certainty_score,
                    'sentiment': sentiment_score,
                    'grammar_quality': grammar_score,
                    'structure': structure_score
                },
                'word_count': len(text.split()),
                'sentiment': self._get_sentiment_details(text)
            }
            
        except Exception as e:
            logger.error(f"Error in text analysis: {str(e)}")
            return {
                'risk_score': 0,
                'red_flags': ['Error occurred during analysis'],
                'details': {},
                'word_count': 0,
                'sentiment': {}
            }
    
    def _check_emotional_manipulation(self, text: str, red_flags: List[str]) -> int:
        """Check for emotional manipulation keywords"""
        score = 0
        found_keywords = []
        
        for keyword in self.emotional_keywords:
            if keyword in text:
                found_keywords.append(keyword)
                score += 10
        
        if found_keywords:
            red_flags.append(f"Emotional manipulation detected: {', '.join(found_keywords[:3])}")
        
        return min(score, 30)  # Cap at 30 points
    
    def _check_clickbait_patterns(self, text: str, red_flags: List[str]) -> int:
        """Check for clickbait patterns"""
        score = 0
        found_patterns = []
        
        for pattern in self.clickbait_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found_patterns.append(pattern)
                score += 15
        
        if found_patterns:
            red_flags.append(f"Clickbait patterns detected: {len(found_patterns)} patterns found")
        
        return min(score, 30)  # Cap at 30 points
    
    def _check_source_reliability(self, text: str, red_flags: List[str]) -> int:
        """Check for unreliable source indicators"""
        score = 0
        found_indicators = []
        
        for indicator in self.unreliable_indicators:
            if indicator in text:
                found_indicators.append(indicator)
                score += 12
        
        if found_indicators:
            red_flags.append(f"Unreliable source indicators: {', '.join(found_indicators[:2])}")
        
        return min(score, 25)  # Cap at 25 points
    
    def _check_certainty_language(self, text: str, red_flags: List[str]) -> int:
        """Check for overconfident language"""
        score = 0
        found_words = []
        
        for word in self.certainty_words:
            if word in text:
                found_words.append(word)
                score += 8
        
        if found_words:
            red_flags.append(f"Overconfident language detected: {', '.join(found_words[:3])}")
        
        return min(score, 20)  # Cap at 20 points
    
    def _analyze_sentiment(self, text: str, red_flags: List[str]) -> int:
        """Analyze sentiment for extreme polarization using keyword-based approach"""
        try:
            text_lower = text.lower()
            
            # Positive sentiment words
            positive_words = ['amazing', 'fantastic', 'incredible', 'wonderful', 'excellent', 'perfect']
            # Negative sentiment words
            negative_words = ['terrible', 'awful', 'horrible', 'disgusting', 'hate', 'worst', 'destroy']
            
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            
            total_sentiment = pos_count + neg_count
            words_count = len(text.split())
            
            if words_count > 0 and total_sentiment > words_count * 0.15:  # More than 15% sentiment words
                red_flags.append("High emotional content detected")
                return 15
            elif words_count > 0 and total_sentiment > words_count * 0.1:  # More than 10% sentiment words
                red_flags.append("Moderate emotional content detected")
                return 8
                
            return 0
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return 0
    
    def _check_grammar_quality(self, text: str, red_flags: List[str]) -> int:
        """Check grammar and spelling quality"""
        try:
            # Count obvious spelling errors (basic check)
            words = text.split()
            if len(words) < 5:
                return 0
            
            # Count words with numbers mixed in (often spam)
            mixed_words = sum(1 for word in words if any(c.isdigit() for c in word) and any(c.isalpha() for c in word))
            
            # Count excessive punctuation
            punct_count = sum(1 for c in text if c in '!?')
            
            score = 0
            if mixed_words > len(words) * 0.1:  # More than 10% mixed words
                red_flags.append("Unusual word patterns detected")
                score += 10
            
            if punct_count > len(words) * 0.3:  # Excessive punctuation
                red_flags.append("Excessive punctuation detected")
                score += 10
            
            return score
            
        except Exception as e:
            logger.error(f"Error in grammar check: {str(e)}")
            return 0
    
    def _analyze_structure(self, text: str, red_flags: List[str]) -> int:
        """Analyze text structure for suspicious patterns"""
        score = 0
        
        # Check for very short content
        if len(text.split()) < 10:
            red_flags.append("Very short content")
            score += 10
        
        # Check for excessive capitalization
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        if caps_ratio > 0.3:
            red_flags.append("Excessive capitalization")
            score += 15
        
        # Check for repetitive content
        words = text.lower().split()
        if len(words) > 10:
            unique_words = set(words)
            repetition_ratio = 1 - (len(unique_words) / len(words))
            if repetition_ratio > 0.7:
                red_flags.append("Highly repetitive content")
                score += 12
        
        return score
    
    def _get_sentiment_details(self, text: str) -> Dict:
        """Get detailed sentiment analysis using keyword-based approach"""
        try:
            text_lower = text.lower()
            
            # Simple keyword-based sentiment
            positive_words = ['good', 'great', 'amazing', 'fantastic', 'excellent', 'wonderful', 'love', 'like']
            negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'worst', 'horrible']
            
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            
            total_words = len(text.split())
            if total_words == 0:
                return {'polarity': 0, 'subjectivity': 0, 'interpretation': 'No content'}
            
            # Calculate polarity (-1 to 1)
            polarity = (pos_count - neg_count) / max(total_words, 1)
            polarity = max(-1, min(1, polarity * 10))  # Scale and clamp
            
            # Calculate subjectivity (0 to 1)
            subjective_words = pos_count + neg_count
            subjectivity = min(1, subjective_words / max(total_words, 1) * 5)
            
            return {
                'polarity': round(polarity, 3),
                'subjectivity': round(subjectivity, 3),
                'interpretation': self._interpret_sentiment(polarity, subjectivity)
            }
            
        except Exception as e:
            logger.error(f"Error getting sentiment details: {str(e)}")
            return {'polarity': 0, 'subjectivity': 0, 'interpretation': 'Unknown'}
    
    def _interpret_sentiment(self, polarity: float, subjectivity: float) -> str:
        """Interpret sentiment scores"""
        if abs(polarity) > 0.8:
            sentiment_type = "extremely positive" if polarity > 0 else "extremely negative"
        elif abs(polarity) > 0.5:
            sentiment_type = "strongly positive" if polarity > 0 else "strongly negative"
        elif abs(polarity) > 0.2:
            sentiment_type = "moderately positive" if polarity > 0 else "moderately negative"
        else:
            sentiment_type = "neutral"
        
        objectivity = "highly subjective" if subjectivity > 0.8 else \
                     "moderately subjective" if subjectivity > 0.5 else \
                     "relatively objective"
        
        return f"{sentiment_type}, {objectivity}"
