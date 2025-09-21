import os
import json
import time
import logging
from typing import Dict, List, Optional, Tuple
import requests
from datetime import datetime
import hashlib
import numpy as np
from collections import Counter
import re

logger = logging.getLogger(__name__)

class AdvancedAIAnalyzer:
    """
    Sophisticated AI-powered misinformation detection with multiple analysis layers
    """
    
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        
        # Advanced analysis weights
        self.analysis_weights = {
            'semantic_consistency': 0.25,
            'factual_verification': 0.30,
            'source_credibility': 0.20,
            'linguistic_patterns': 0.15,
            'temporal_analysis': 0.10
        }
        
        # Misinformation patterns database
        self.misinformation_patterns = {
            'conspiracy_indicators': [
                'they don\'t want you to know', 'hidden truth', 'mainstream media won\'t tell you',
                'deep state', 'secret agenda', 'cover-up', 'wake up', 'sheeple'
            ],
            'emotional_manipulation': [
                'shocking', 'unbelievable', 'you won\'t believe', 'must see', 'urgent',
                'breaking', 'exclusive', 'leaked', 'exposed', 'revealed'
            ],
            'false_authority': [
                'doctors hate this', 'scientists don\'t want you to know', 'secret study shows',
                'unnamed sources', 'inside sources', 'whistleblower reveals'
            ],
            'urgency_tactics': [
                'share before deleted', 'going viral', 'must share now', 'time sensitive',
                'act now', 'limited time', 'before it\'s too late'
            ]
        }
        
        # Credible source domains
        self.credible_domains = {
            'high_credibility': [
                'reuters.com', 'apnews.com', 'bbc.com', 'npr.org', 'pbs.org',
                'theguardian.com', 'nytimes.com', 'washingtonpost.com', 'wsj.com'
            ],
            'medium_credibility': [
                'cnn.com', 'foxnews.com', 'msnbc.com', 'abc.com', 'cbs.com',
                'nbc.com', 'time.com', 'newsweek.com', 'usatoday.com'
            ],
            'questionable': [
                'infowars.com', 'breitbart.com', 'dailymail.co.uk', 'rt.com',
                'naturalnews.com', 'beforeitsnews.com'
            ]
        }
    
    def analyze_comprehensive(self, content: str, content_type: str = 'text', 
                            url: Optional[str] = None) -> Dict:
        """
        Comprehensive multi-layered analysis of content
        """
        start_time = time.time()
        
        try:
            analysis_results = {
                'content_hash': hashlib.md5(content.encode()).hexdigest()[:16],
                'analysis_timestamp': datetime.now().isoformat(),
                'content_type': content_type,
                'processing_time': 0,
                'confidence_score': 0,
                'risk_assessment': {},
                'detailed_analysis': {},
                'recommendations': []
            }
            
            # Layer 1: Semantic Consistency Analysis
            semantic_analysis = self._analyze_semantic_consistency(content)
            analysis_results['detailed_analysis']['semantic'] = semantic_analysis
            
            # Layer 2: Factual Verification
            factual_analysis = self._verify_factual_claims(content, url)
            analysis_results['detailed_analysis']['factual'] = factual_analysis
            
            # Layer 3: Source Credibility Assessment
            if url:
                source_analysis = self._assess_source_credibility(url)
                analysis_results['detailed_analysis']['source'] = source_analysis
            else:
                source_analysis = {'credibility_score': 50, 'domain_reputation': 'unknown'}
                analysis_results['detailed_analysis']['source'] = source_analysis
            
            # Layer 4: Linguistic Pattern Analysis
            linguistic_analysis = self._analyze_linguistic_patterns(content)
            analysis_results['detailed_analysis']['linguistic'] = linguistic_analysis
            
            # Layer 5: Temporal Analysis
            temporal_analysis = self._analyze_temporal_patterns(content)
            analysis_results['detailed_analysis']['temporal'] = temporal_analysis
            
            # Composite Risk Assessment
            risk_assessment = self._calculate_composite_risk(
                semantic_analysis, factual_analysis, source_analysis,
                linguistic_analysis, temporal_analysis
            )
            analysis_results['risk_assessment'] = risk_assessment
            
            # Generate AI-powered recommendations
            recommendations = self._generate_recommendations(analysis_results)
            analysis_results['recommendations'] = recommendations
            
            # Calculate confidence score
            confidence = self._calculate_confidence_score(analysis_results)
            analysis_results['confidence_score'] = confidence
            
            analysis_results['processing_time'] = round(time.time() - start_time, 3)
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {str(e)}")
            return {
                'error': 'Analysis failed',
                'message': str(e),
                'processing_time': round(time.time() - start_time, 3)
            }
    
    def _analyze_semantic_consistency(self, content: str) -> Dict:
        """Analyze semantic consistency and logical flow"""
        try:
            sentences = content.split('.')
            
            # Analyze logical flow
            logical_inconsistencies = 0
            contradictory_statements = []
            
            # Simple contradiction detection
            positive_claims = []
            negative_claims = []
            
            for sentence in sentences:
                sentence = sentence.strip().lower()
                if 'not' in sentence or 'never' in sentence or 'false' in sentence:
                    negative_claims.append(sentence)
                else:
                    positive_claims.append(sentence)
            
            # Check for semantic coherence
            semantic_score = 100
            
            # Penalty for excessive claims without evidence
            claim_words = ['prove', 'shows', 'demonstrates', 'confirms', 'reveals']
            evidence_words = ['study', 'research', 'data', 'source', 'citation']
            
            claims_count = sum(1 for word in claim_words if word in content.lower())
            evidence_count = sum(1 for word in evidence_words if word in content.lower())
            
            if claims_count > evidence_count * 2:
                semantic_score -= 30
                contradictory_statements.append("Many claims made without sufficient evidence")
            
            # Check for logical fallacies
            fallacies = {
                'false_dichotomy': ['either', 'only two', 'must choose'],
                'ad_hominem': ['stupid', 'idiotic', 'corrupt'],
                'appeal_to_fear': ['dangerous', 'terrifying', 'catastrophic'],
                'bandwagon': ['everyone knows', 'everybody says', 'most people']
            }
            
            detected_fallacies = []
            for fallacy, indicators in fallacies.items():
                for indicator in indicators:
                    if indicator in content.lower():
                        detected_fallacies.append(fallacy)
                        semantic_score -= 15
                        break
            
            return {
                'semantic_score': max(0, semantic_score),
                'logical_inconsistencies': logical_inconsistencies,
                'contradictory_statements': contradictory_statements,
                'detected_fallacies': detected_fallacies,
                'claims_to_evidence_ratio': claims_count / max(evidence_count, 1)
            }
            
        except Exception as e:
            logger.error(f"Error in semantic analysis: {str(e)}")
            return {'semantic_score': 50, 'error': str(e)}
    
    def _verify_factual_claims(self, content: str, url: Optional[str] = None) -> Dict:
        """Verify factual claims using multiple sources"""
        try:
            # Extract potential factual claims
            claims = self._extract_factual_claims(content)
            
            verification_results = {
                'total_claims': len(claims),
                'verified_claims': 0,
                'disputed_claims': 0,
                'unverifiable_claims': 0,
                'fact_check_sources': [],
                'verification_score': 50
            }
            
            # Check against known fact-checking databases
            for claim in claims[:3]:  # Limit to 3 claims for performance
                verification = self._check_claim_against_sources(claim)
                
                if verification['status'] == 'verified':
                    verification_results['verified_claims'] += 1
                elif verification['status'] == 'disputed':
                    verification_results['disputed_claims'] += 1
                else:
                    verification_results['unverifiable_claims'] += 1
                
                verification_results['fact_check_sources'].extend(verification['sources'])
            
            # Calculate verification score
            if verification_results['total_claims'] > 0:
                verified_ratio = verification_results['verified_claims'] / verification_results['total_claims']
                disputed_ratio = verification_results['disputed_claims'] / verification_results['total_claims']
                
                verification_results['verification_score'] = int(
                    (verified_ratio * 100) - (disputed_ratio * 50)
                )
            
            return verification_results
            
        except Exception as e:
            logger.error(f"Error in factual verification: {str(e)}")
            return {'verification_score': 50, 'error': str(e)}
    
    def _extract_factual_claims(self, content: str) -> List[str]:
        """Extract potential factual claims from content"""
        # Simple factual claim extraction
        sentences = content.split('.')
        claims = []
        
        factual_indicators = [
            'study shows', 'research proves', 'data indicates', 'statistics show',
            'according to', 'scientists found', 'experts say', 'reports indicate'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(indicator in sentence.lower() for indicator in factual_indicators):
                claims.append(sentence)
        
        return claims[:5]  # Return max 5 claims
    
    def _check_claim_against_sources(self, claim: str) -> Dict:
        """Check a claim against fact-checking sources"""
        # Simplified fact-checking simulation
        # In a real implementation, this would query actual fact-checking APIs
        
        suspicious_words = ['secret', 'hidden', 'conspiracy', 'cover-up', 'hoax']
        factual_words = ['peer-reviewed', 'published', 'official', 'verified']
        
        if any(word in claim.lower() for word in suspicious_words):
            return {
                'status': 'disputed',
                'confidence': 0.8,
                'sources': ['fact-checker-simulation']
            }
        elif any(word in claim.lower() for word in factual_words):
            return {
                'status': 'verified',
                'confidence': 0.7,
                'sources': ['academic-source-simulation']
            }
        else:
            return {
                'status': 'unverifiable',
                'confidence': 0.5,
                'sources': []
            }
    
    def _assess_source_credibility(self, url: str) -> Dict:
        """Assess the credibility of the source URL"""
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc.lower()
            
            credibility_score = 50
            domain_reputation = 'unknown'
            
            if any(domain.endswith(d) for d in self.credible_domains['high_credibility']):
                credibility_score = 90
                domain_reputation = 'high'
            elif any(domain.endswith(d) for d in self.credible_domains['medium_credibility']):
                credibility_score = 70
                domain_reputation = 'medium'
            elif any(domain.endswith(d) for d in self.credible_domains['questionable']):
                credibility_score = 20
                domain_reputation = 'questionable'
            
            # Additional domain analysis
            domain_age = self._estimate_domain_age(domain)
            has_https = url.startswith('https://')
            
            if domain_age < 1:  # Very new domain
                credibility_score -= 20
            
            if not has_https:
                credibility_score -= 10
            
            return {
                'credibility_score': max(0, min(100, credibility_score)),
                'domain_reputation': domain_reputation,
                'domain': domain,
                'domain_age_estimate': domain_age,
                'has_https': has_https
            }
            
        except Exception as e:
            logger.error(f"Error in source credibility assessment: {str(e)}")
            return {'credibility_score': 50, 'error': str(e)}
    
    def _estimate_domain_age(self, domain: str) -> float:
        """Estimate domain age (simplified simulation)"""
        # This is a simplified estimation
        # In a real implementation, you'd use WHOIS data
        if any(d in domain for d in ['news', 'times', 'post', 'guardian']):
            return 10.0  # Established news sites
        elif len(domain) > 15:
            return 2.0  # Longer domains might be newer
        else:
            return 5.0  # Default estimate
    
    def _analyze_linguistic_patterns(self, content: str) -> Dict:
        """Analyze linguistic patterns for misinformation indicators"""
        try:
            analysis = {
                'pattern_scores': {},
                'detected_patterns': [],
                'linguistic_score': 100
            }
            
            content_lower = content.lower()
            
            # Analyze each pattern category
            for category, patterns in self.misinformation_patterns.items():
                detected = []
                for pattern in patterns:
                    if pattern in content_lower:
                        detected.append(pattern)
                
                if detected:
                    analysis['detected_patterns'].extend(detected)
                    pattern_score = max(0, 100 - len(detected) * 15)
                    analysis['pattern_scores'][category] = pattern_score
                    analysis['linguistic_score'] -= len(detected) * 10
                else:
                    analysis['pattern_scores'][category] = 100
            
            # Additional linguistic analysis
            sentences = content.split('.')
            avg_sentence_length = np.mean([len(s.split()) for s in sentences if s.strip()])
            
            # Very short or very long sentences can indicate poor quality
            if avg_sentence_length < 5 or avg_sentence_length > 40:
                analysis['linguistic_score'] -= 15
            
            # Check for excessive punctuation
            exclamation_ratio = content.count('!') / max(len(content.split()), 1)
            if exclamation_ratio > 0.1:
                analysis['linguistic_score'] -= 20
            
            analysis['linguistic_score'] = max(0, analysis['linguistic_score'])
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in linguistic analysis: {str(e)}")
            return {'linguistic_score': 50, 'error': str(e)}
    
    def _analyze_temporal_patterns(self, content: str) -> Dict:
        """Analyze temporal patterns and urgency indicators"""
        try:
            urgency_indicators = [
                'breaking', 'urgent', 'immediate', 'now', 'today', 'this hour',
                'just in', 'developing', 'alert', 'warning'
            ]
            
            time_references = [
                'yesterday', 'last week', 'recently', 'just happened',
                'moments ago', 'hours ago', 'days ago'
            ]
            
            content_lower = content.lower()
            
            urgency_count = sum(1 for indicator in urgency_indicators if indicator in content_lower)
            time_ref_count = sum(1 for ref in time_references if ref in content_lower)
            
            # Calculate temporal manipulation score
            temporal_score = 100
            
            if urgency_count > 2:
                temporal_score -= urgency_count * 15
            
            if urgency_count > 0 and time_ref_count == 0:
                temporal_score -= 20  # Urgency without time context
            
            return {
                'temporal_score': max(0, temporal_score),
                'urgency_indicators': urgency_count,
                'time_references': time_ref_count,
                'manipulation_risk': 'high' if temporal_score < 50 else 'low'
            }
            
        except Exception as e:
            logger.error(f"Error in temporal analysis: {str(e)}")
            return {'temporal_score': 50, 'error': str(e)}
    
    def _calculate_composite_risk(self, semantic: Dict, factual: Dict, source: Dict,
                                linguistic: Dict, temporal: Dict) -> Dict:
        """Calculate composite risk score from all analysis layers"""
        try:
            # Extract scores with defaults
            scores = {
                'semantic': semantic.get('semantic_score', 50),
                'factual': factual.get('verification_score', 50),
                'source': source.get('credibility_score', 50),
                'linguistic': linguistic.get('linguistic_score', 50),
                'temporal': temporal.get('temporal_score', 50)
            }
            
            # Apply weights
            weighted_score = sum(
                scores[key] * self.analysis_weights.get(f'{key}_consistency' if key == 'semantic'
                                                      else f'{key}_verification' if key == 'factual'
                                                      else f'source_credibility' if key == 'source'
                                                      else f'linguistic_patterns' if key == 'linguistic'
                                                      else 'temporal_analysis')
                for key in scores.keys()
            )
            
            # Convert to risk score (lower score = higher risk)
            risk_score = 100 - weighted_score
            
            # Determine risk level
            if risk_score >= 70:
                risk_level = 'CRITICAL'
                risk_description = 'Multiple strong indicators of misinformation detected'
            elif risk_score >= 50:
                risk_level = 'HIGH'
                risk_description = 'Significant misinformation indicators present'
            elif risk_score >= 30:
                risk_level = 'MODERATE'
                risk_description = 'Some concerning elements detected'
            elif risk_score >= 15:
                risk_level = 'LOW'
                risk_description = 'Minor concerns, generally appears credible'
            else:
                risk_level = 'MINIMAL'
                risk_description = 'Strong credibility indicators, low risk'
            
            return {
                'overall_risk_score': round(risk_score, 1),
                'risk_level': risk_level,
                'risk_description': risk_description,
                'component_scores': scores,
                'weighted_components': {
                    key: round(scores[key] * weight, 2)
                    for key, weight in zip(scores.keys(),
                                         [self.analysis_weights['semantic_consistency'],
                                          self.analysis_weights['factual_verification'],
                                          self.analysis_weights['source_credibility'],
                                          self.analysis_weights['linguistic_patterns'],
                                          self.analysis_weights['temporal_analysis']])
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating composite risk: {str(e)}")
            return {
                'overall_risk_score': 50,
                'risk_level': 'UNKNOWN',
                'error': str(e)
            }
    
    def _generate_recommendations(self, analysis_results: Dict) -> List[Dict]:
        """Generate AI-powered recommendations based on analysis"""
        recommendations = []
        
        risk_score = analysis_results.get('risk_assessment', {}).get('overall_risk_score', 50)
        detailed = analysis_results.get('detailed_analysis', {})
        
        # High-priority recommendations
        if risk_score >= 70:
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'DO NOT SHARE',
                'reason': 'Multiple severe misinformation indicators detected',
                'details': 'This content shows strong signs of being misinformation. Sharing could spread false information.'
            })
        
        # Source-specific recommendations
        source_score = detailed.get('source', {}).get('credibility_score', 50)
        if source_score < 40:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Verify source credibility',
                'reason': 'Source appears unreliable',
                'details': 'Check the publisher\'s reputation, editorial standards, and track record.'
            })
        
        # Factual verification recommendations
        factual_analysis = detailed.get('factual', {})
        if factual_analysis.get('disputed_claims', 0) > 0:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Fact-check specific claims',
                'reason': 'Contains disputed factual claims',
                'details': 'Use multiple fact-checking sources to verify specific claims before believing or sharing.'
            })
        
        # Linguistic pattern recommendations
        linguistic_analysis = detailed.get('linguistic', {})
        if linguistic_analysis.get('linguistic_score', 100) < 60:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Analyze language patterns',
                'reason': 'Suspicious linguistic patterns detected',
                'details': 'Content uses emotional manipulation or conspiracy language patterns.'
            })
        
        # Temporal analysis recommendations
        temporal_analysis = detailed.get('temporal', {})
        if temporal_analysis.get('urgency_indicators', 0) > 2:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Question urgency claims',
                'reason': 'Artificial urgency detected',
                'details': 'Legitimate news rarely requires immediate sharing. Take time to verify.'
            })
        
        return recommendations
    
    def _calculate_confidence_score(self, analysis_results: Dict) -> float:
        """Calculate confidence in the analysis results"""
        try:
            # Base confidence
            confidence = 0.8
            
            # Reduce confidence if there were errors
            for analysis in analysis_results.get('detailed_analysis', {}).values():
                if 'error' in analysis:
                    confidence -= 0.15
            
            # Increase confidence if multiple layers agree
            risk_score = analysis_results.get('risk_assessment', {}).get('overall_risk_score', 50)
            component_scores = analysis_results.get('risk_assessment', {}).get('component_scores', {})
            
            if component_scores:
                score_variance = np.var(list(component_scores.values()))
                if score_variance < 200:  # Low variance means agreement
                    confidence += 0.1
                else:
                    confidence -= 0.1
            
            return round(max(0.3, min(0.95, confidence)), 2)
            
        except Exception:
            return 0.7
