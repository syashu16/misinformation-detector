import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import hashlib
import re

logger = logging.getLogger(__name__)

class RealTimeFactChecker:
    """
    Real-time fact-checking integration with multiple sources
    """
    
    def __init__(self):
        self.fact_check_sources = {
            'snopes': {
                'enabled': True,
                'weight': 0.3,
                'api_base': 'https://www.snopes.com/api/v1/',
                'rate_limit': 100  # requests per hour
            },
            'politifact': {
                'enabled': True,
                'weight': 0.25,
                'api_base': 'https://www.politifact.com/api/v/2/',
                'rate_limit': 50
            },
            'factcheck_org': {
                'enabled': True,
                'weight': 0.25,
                'api_base': 'https://www.factcheck.org/api/',
                'rate_limit': 30
            },
            'google_fact_check': {
                'enabled': True,
                'weight': 0.2,
                'api_base': 'https://factchecktools.googleapis.com/v1alpha1/claims:search',
                'rate_limit': 1000
            }
        }
        
        self.cache = {}
        self.cache_expiry = timedelta(hours=24)
        
        # Claim extraction patterns
        self.claim_patterns = [
            r'(?:according to|study shows|research proves|data indicates|scientists found|experts say|reports indicate|statistics show)\s+(.+?)(?:\.|,|;)',
            r'(?:it is|this is|that is)\s+(proven|confirmed|verified|established)\s+(?:that\s+)?(.+?)(?:\.|,|;)',
            r'(?:the fact is|the truth is|it\'s a fact that)\s+(.+?)(?:\.|,|;)',
            r'(\d+%?\s+of\s+.+?)(?:\.|,|;)',
            r'(evidence shows|research indicates|studies demonstrate)\s+(.+?)(?:\.|,|;)'
        ]
        
        # Suspicious claim indicators
        self.suspicious_indicators = [
            'secret study', 'hidden research', 'they don\'t want you to know',
            'suppressed evidence', 'cover-up', 'conspiracy', 'fake news',
            'hoax', 'propaganda', 'mainstream media lies'
        ]
    
    async def check_claims_comprehensive(self, content: str, content_type: str = 'text') -> Dict:
        """
        Comprehensive fact-checking across multiple sources
        """
        start_time = time.time()
        
        try:
            # Extract claims from content
            extracted_claims = self.extract_claims(content)
            
            if not extracted_claims:
                return {
                    'total_claims': 0,
                    'fact_check_results': {},
                    'overall_credibility': 50,
                    'processing_time': round(time.time() - start_time, 3)
                }
            
            # Check claims against multiple sources
            fact_check_results = await self.verify_claims_parallel(extracted_claims)
            
            # Calculate overall credibility
            overall_credibility = self.calculate_overall_credibility(fact_check_results)
            
            # Generate recommendations
            recommendations = self.generate_fact_check_recommendations(fact_check_results)
            
            return {
                'total_claims': len(extracted_claims),
                'extracted_claims': extracted_claims[:5],  # Limit for display
                'fact_check_results': fact_check_results,
                'overall_credibility': overall_credibility,
                'source_breakdown': self.get_source_breakdown(fact_check_results),
                'recommendations': recommendations,
                'suspicious_indicators': self.detect_suspicious_indicators(content),
                'processing_time': round(time.time() - start_time, 3)
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive fact-checking: {str(e)}")
            return {
                'error': 'Fact-checking failed',
                'message': str(e),
                'processing_time': round(time.time() - start_time, 3)
            }
    
    def extract_claims(self, content: str) -> List[str]:
        """Extract factual claims from content using pattern matching"""
        claims = []
        
        # Clean content
        content = re.sub(r'\s+', ' ', content.strip())
        
        # Extract claims using patterns
        for pattern in self.claim_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                claim = match.group(1) if match.lastindex >= 1 else match.group(0)
                claim = claim.strip()
                
                # Filter out very short or very long claims
                if 10 <= len(claim) <= 200:
                    claims.append(claim)
        
        # Also extract sentences with strong factual indicators
        sentences = content.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if any(indicator in sentence.lower() for indicator in 
                   ['percent', '%', 'million', 'billion', 'study', 'research', 'data']):
                if 15 <= len(sentence) <= 250:
                    claims.append(sentence)
        
        # Remove duplicates and return top claims
        unique_claims = list(dict.fromkeys(claims))
        return unique_claims[:10]  # Limit to 10 claims
    
    async def verify_claims_parallel(self, claims: List[str]) -> Dict:
        """Verify claims across multiple fact-checking sources in parallel"""
        results = {}
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            tasks = []
            
            for i, claim in enumerate(claims[:5]):  # Limit to 5 claims for performance
                claim_hash = hashlib.md5(claim.encode()).hexdigest()
                
                # Check cache first
                if claim_hash in self.cache:
                    cache_entry = self.cache[claim_hash]
                    if datetime.now() - cache_entry['timestamp'] < self.cache_expiry:
                        results[f'claim_{i+1}'] = cache_entry['result']
                        continue
                
                # Create verification tasks for each source
                for source_name, source_config in self.fact_check_sources.items():
                    if source_config['enabled']:
                        task = self.verify_claim_with_source(session, claim, source_name, source_config)
                        tasks.append((f'claim_{i+1}', claim, source_name, task))
            
            # Execute all tasks
            if tasks:
                task_results = await asyncio.gather(*[task[3] for task in tasks], return_exceptions=True)
                
                # Process results
                for (claim_id, claim_text, source_name, _), result in zip(tasks, task_results):
                    if claim_id not in results:
                        results[claim_id] = {
                            'claim_text': claim_text,
                            'source_results': {},
                            'consensus': 'unknown'
                        }
                    
                    if not isinstance(result, Exception):
                        results[claim_id]['source_results'][source_name] = result
                    else:
                        logger.warning(f"Error checking {claim_id} with {source_name}: {result}")
        
        # Calculate consensus for each claim
        for claim_id, claim_data in results.items():
            claim_data['consensus'] = self.calculate_claim_consensus(claim_data['source_results'])
        
        return results
    
    async def verify_claim_with_source(self, session: aiohttp.ClientSession, 
                                     claim: str, source_name: str, source_config: Dict) -> Dict:
        """Verify a single claim with a specific fact-checking source"""
        try:
            # Simulate fact-checking API calls (replace with real API calls)
            if source_name == 'google_fact_check':
                return await self.check_google_fact_check(session, claim)
            elif source_name == 'snopes':
                return await self.check_snopes(session, claim)
            elif source_name == 'politifact':
                return await self.check_politifact(session, claim)
            elif source_name == 'factcheck_org':
                return await self.check_factcheck_org(session, claim)
            else:
                return {'status': 'unknown', 'confidence': 0.5, 'details': 'Source not implemented'}
                
        except Exception as e:
            logger.error(f"Error checking claim with {source_name}: {str(e)}")
            return {'status': 'error', 'confidence': 0.0, 'details': str(e)}
    
    async def check_google_fact_check(self, session: aiohttp.ClientSession, claim: str) -> Dict:
        """Check claim using Google Fact Check Tools API (simulated)"""
        # This is a simulation - replace with actual API call
        await asyncio.sleep(0.5)  # Simulate API delay
        
        # Simulate response based on claim content
        suspicious_words = ['secret', 'hidden', 'conspiracy', 'hoax', 'fake']
        credible_words = ['study', 'research', 'university', 'peer-reviewed']
        
        if any(word in claim.lower() for word in suspicious_words):
            return {
                'status': 'false',
                'confidence': 0.8,
                'details': 'Claim contains suspicious language patterns',
                'source_url': 'https://factchecktools.googleapis.com/simulated'
            }
        elif any(word in claim.lower() for word in credible_words):
            return {
                'status': 'partially_true',
                'confidence': 0.7,
                'details': 'Claim references legitimate research',
                'source_url': 'https://factchecktools.googleapis.com/simulated'
            }
        else:
            return {
                'status': 'unknown',
                'confidence': 0.5,
                'details': 'Insufficient information to verify',
                'source_url': 'https://factchecktools.googleapis.com/simulated'
            }
    
    async def check_snopes(self, session: aiohttp.ClientSession, claim: str) -> Dict:
        """Check claim using Snopes (simulated)"""
        await asyncio.sleep(0.3)
        
        # Simulate Snopes-style fact-checking
        if 'breaking' in claim.lower() or 'urgent' in claim.lower():
            return {
                'status': 'mixture',
                'confidence': 0.6,
                'details': 'Urgent claims often contain mixed or exaggerated information',
                'source_url': 'https://snopes.com/simulated'
            }
        else:
            return {
                'status': 'unproven',
                'confidence': 0.5,
                'details': 'No definitive evidence found',
                'source_url': 'https://snopes.com/simulated'
            }
    
    async def check_politifact(self, session: aiohttp.ClientSession, claim: str) -> Dict:
        """Check claim using PolitiFact (simulated)"""
        await asyncio.sleep(0.4)
        
        political_keywords = ['government', 'politician', 'election', 'vote', 'policy']
        
        if any(word in claim.lower() for word in political_keywords):
            return {
                'status': 'half_true',
                'confidence': 0.7,
                'details': 'Political claims often contain partial truths',
                'source_url': 'https://politifact.com/simulated'
            }
        else:
            return {
                'status': 'unknown',
                'confidence': 0.4,
                'details': 'Outside PolitiFact scope',
                'source_url': 'https://politifact.com/simulated'
            }
    
    async def check_factcheck_org(self, session: aiohttp.ClientSession, claim: str) -> Dict:
        """Check claim using FactCheck.org (simulated)"""
        await asyncio.sleep(0.6)
        
        # Simulate FactCheck.org response
        if len(claim) > 100:
            return {
                'status': 'needs_context',
                'confidence': 0.6,
                'details': 'Complex claims require additional context',
                'source_url': 'https://factcheck.org/simulated'
            }
        else:
            return {
                'status': 'unknown',
                'confidence': 0.5,
                'details': 'No matching fact-checks found',
                'source_url': 'https://factcheck.org/simulated'
            }
    
    def calculate_claim_consensus(self, source_results: Dict) -> str:
        """Calculate consensus across multiple fact-checking sources"""
        if not source_results:
            return 'unknown'
        
        # Weight the results based on source credibility
        weighted_scores = {
            'true': 0,
            'false': 0,
            'partially_true': 0,
            'mixture': 0,
            'unknown': 0
        }
        
        total_weight = 0
        
        for source_name, result in source_results.items():
            if source_name in self.fact_check_sources:
                weight = self.fact_check_sources[source_name]['weight']
                status = result.get('status', 'unknown')
                confidence = result.get('confidence', 0.5)
                
                # Normalize status names
                normalized_status = self.normalize_status(status)
                if normalized_status in weighted_scores:
                    weighted_scores[normalized_status] += weight * confidence
                    total_weight += weight
        
        if total_weight == 0:
            return 'unknown'
        
        # Find the status with highest weighted score
        max_score = max(weighted_scores.values())
        consensus = [status for status, score in weighted_scores.items() if score == max_score][0]
        
        return consensus
    
    def normalize_status(self, status: str) -> str:
        """Normalize different fact-checking status names"""
        status_lower = status.lower()
        
        if status_lower in ['true', 'correct', 'accurate', 'verified']:
            return 'true'
        elif status_lower in ['false', 'incorrect', 'inaccurate', 'debunked', 'hoax']:
            return 'false'
        elif status_lower in ['partially_true', 'half_true', 'mostly_true', 'partly_true']:
            return 'partially_true'
        elif status_lower in ['mixture', 'mixed', 'complex', 'needs_context']:
            return 'mixture'
        else:
            return 'unknown'
    
    def calculate_overall_credibility(self, fact_check_results: Dict) -> int:
        """Calculate overall credibility score from fact-check results"""
        if not fact_check_results:
            return 50
        
        total_score = 0
        total_claims = len(fact_check_results)
        
        for claim_data in fact_check_results.values():
            consensus = claim_data.get('consensus', 'unknown')
            
            if consensus == 'true':
                total_score += 90
            elif consensus == 'partially_true':
                total_score += 70
            elif consensus == 'mixture':
                total_score += 50
            elif consensus == 'false':
                total_score += 10
            else:  # unknown
                total_score += 50
        
        return int(total_score / total_claims) if total_claims > 0 else 50
    
    def get_source_breakdown(self, fact_check_results: Dict) -> Dict:
        """Get breakdown of results by source"""
        source_breakdown = {}
        
        for claim_data in fact_check_results.values():
            for source_name, result in claim_data.get('source_results', {}).items():
                if source_name not in source_breakdown:
                    source_breakdown[source_name] = {
                        'checks_performed': 0,
                        'avg_confidence': 0,
                        'status_distribution': {}
                    }
                
                source_breakdown[source_name]['checks_performed'] += 1
                confidence = result.get('confidence', 0.5)
                source_breakdown[source_name]['avg_confidence'] += confidence
                
                status = result.get('status', 'unknown')
                if status not in source_breakdown[source_name]['status_distribution']:
                    source_breakdown[source_name]['status_distribution'][status] = 0
                source_breakdown[source_name]['status_distribution'][status] += 1
        
        # Calculate averages
        for source_data in source_breakdown.values():
            if source_data['checks_performed'] > 0:
                source_data['avg_confidence'] /= source_data['checks_performed']
                source_data['avg_confidence'] = round(source_data['avg_confidence'], 2)
        
        return source_breakdown
    
    def generate_fact_check_recommendations(self, fact_check_results: Dict) -> List[Dict]:
        """Generate recommendations based on fact-checking results"""
        recommendations = []
        
        false_claims = sum(1 for claim_data in fact_check_results.values() 
                          if claim_data.get('consensus') == 'false')
        
        if false_claims > 0:
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'VERIFY IMMEDIATELY',
                'reason': f'{false_claims} claims flagged as false',
                'details': 'Multiple fact-checkers have disputed key claims in this content'
            })
        
        mixture_claims = sum(1 for claim_data in fact_check_results.values() 
                           if claim_data.get('consensus') == 'mixture')
        
        if mixture_claims > 0:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'SEEK ADDITIONAL CONTEXT',
                'reason': f'{mixture_claims} claims need context',
                'details': 'Some claims contain partial truths that may be misleading without context'
            })
        
        unknown_claims = sum(1 for claim_data in fact_check_results.values() 
                           if claim_data.get('consensus') == 'unknown')
        
        if unknown_claims > len(fact_check_results) * 0.7:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'INDEPENDENT VERIFICATION NEEDED',
                'reason': 'Many claims could not be verified',
                'details': 'Consider seeking primary sources or expert opinions'
            })
        
        return recommendations
    
    def detect_suspicious_indicators(self, content: str) -> List[str]:
        """Detect suspicious indicators in content"""
        detected = []
        content_lower = content.lower()
        
        for indicator in self.suspicious_indicators:
            if indicator in content_lower:
                detected.append(indicator)
        
        return detected
