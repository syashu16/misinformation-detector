import requests
import validators
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class URLAnalyzer:
    """Analyzes URLs and their content for misinformation indicators"""
    
    def __init__(self):
        # Known unreliable domains (example list - would need comprehensive database)
        self.suspicious_domains = [
            'fakesite.com', 'notreal.news', 'clickbait.info',
            'conspiracy.org', 'hoax.net'
        ]
        
        # Trusted domains (major news sources)
        self.trusted_domains = [
            'bbc.com', 'reuters.com', 'ap.org', 'npr.org',
            'cnn.com', 'nytimes.com', 'washingtonpost.com',
            'theguardian.com', 'wsj.com', 'bloomberg.com'
        ]
        
        # Suspicious URL patterns
        self.suspicious_patterns = [
            r'\d+\w+\.tk$',  # Suspicious TLD
            r'bit\.ly|tinyurl\.com|t\.co',  # URL shorteners
            r'\d{4,}\.com',  # Domains with many numbers
            r'[0-9]+[a-z]+[0-9]+\.',  # Mixed numbers and letters
        ]
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def analyze(self, url: str) -> Dict:
        """
        Analyze URL for misinformation indicators
        
        Args:
            url: The URL to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Validate URL format
            if not validators.url(url):
                return {'error': 'Invalid URL format'}
            
            # Parse URL components
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            red_flags = []
            risk_score = 0
            
            # Check domain reputation
            domain_score = self._check_domain_reputation(domain, red_flags)
            risk_score += domain_score
            
            # Check URL patterns
            pattern_score = self._check_url_patterns(url, red_flags)
            risk_score += pattern_score
            
            # Fetch and analyze content
            content_analysis = self._fetch_and_analyze_content(url, red_flags)
            risk_score += content_analysis['score']
            
            # Check for HTTPS
            if parsed_url.scheme != 'https':
                red_flags.append("URL uses HTTP instead of HTTPS")
                risk_score += 10
            
            # Normalize risk score
            final_score = min(100, max(0, risk_score))
            
            result = {
                'risk_score': final_score,
                'red_flags': red_flags,
                'domain': domain,
                'scheme': parsed_url.scheme,
                'title': content_analysis.get('title', 'Unknown'),
                'content': content_analysis.get('content', ''),
                'meta_info': content_analysis.get('meta_info', {}),
                'external_links': content_analysis.get('external_links', []),
                'social_signals': content_analysis.get('social_signals', {})
            }
            
            return result
            
        except requests.RequestException as e:
            logger.error(f"Request error analyzing URL {url}: {str(e)}")
            return {'error': f'Failed to fetch URL: {str(e)}'}
        except Exception as e:
            logger.error(f"Error analyzing URL {url}: {str(e)}")
            return {'error': f'Analysis error: {str(e)}'}
    
    def _check_domain_reputation(self, domain: str, red_flags: List[str]) -> int:
        """Check domain against known lists"""
        score = 0
        
        # Remove www. prefix for comparison
        clean_domain = domain.replace('www.', '')
        
        # Check against suspicious domains
        for suspicious in self.suspicious_domains:
            if suspicious in clean_domain:
                red_flags.append(f"Domain '{domain}' flagged as potentially unreliable")
                score += 40
                break
        
        # Check against trusted domains
        is_trusted = False
        for trusted in self.trusted_domains:
            if trusted in clean_domain:
                is_trusted = True
                break
        
        if not is_trusted:
            # Check for common red flags in domain
            if len(clean_domain.split('.')[0]) > 20:  # Very long domain name
                red_flags.append("Unusually long domain name")
                score += 15
            
            if re.search(r'\d{3,}', clean_domain):  # Many numbers in domain
                red_flags.append("Domain contains many numbers")
                score += 10
            
            # Check for suspicious TLDs
            tld = clean_domain.split('.')[-1]
            if tld in ['tk', 'ml', 'ga', 'cf']:
                red_flags.append(f"Suspicious top-level domain: .{tld}")
                score += 20
        
        return score
    
    def _check_url_patterns(self, url: str, red_flags: List[str]) -> int:
        """Check URL for suspicious patterns"""
        score = 0
        
        for pattern in self.suspicious_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                red_flags.append("URL contains suspicious patterns")
                score += 15
                break
        
        # Check URL length
        if len(url) > 200:
            red_flags.append("Unusually long URL")
            score += 10
        
        # Check for excessive parameters
        if url.count('=') > 10:
            red_flags.append("URL has many parameters")
            score += 8
        
        return score
    
    def _fetch_and_analyze_content(self, url: str, red_flags: List[str]) -> Dict:
        """Fetch and analyze page content"""
        try:
            # Set timeout and size limits
            response = self.session.get(url, timeout=10, stream=True)
            
            # Check response size (limit to 5MB)
            content_length = response.headers.get('Content-Length')
            if content_length and int(content_length) > 5 * 1024 * 1024:
                return {'score': 0, 'error': 'Content too large'}
            
            # Get first 5MB of content
            content = b''
            for chunk in response.iter_content(chunk_size=8192):
                content += chunk
                if len(content) > 5 * 1024 * 1024:
                    break
            
            response._content = content
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic information
            title = soup.find('title')
            title_text = title.get_text().strip() if title else 'No title'
            
            # Extract main content
            content_text = self._extract_main_content(soup)
            
            # Extract meta information
            meta_info = self._extract_meta_info(soup)
            
            # Check for content quality indicators
            score = self._analyze_page_content(soup, content_text, red_flags)
            
            # Extract external links
            external_links = self._extract_external_links(soup, url)
            
            # Check for social media signals
            social_signals = self._check_social_signals(soup)
            
            return {
                'score': score,
                'title': title_text,
                'content': content_text[:1000],  # Limit content length
                'meta_info': meta_info,
                'external_links': external_links[:10],  # Limit links
                'social_signals': social_signals
            }
            
        except requests.RequestException as e:
            logger.error(f"Request error fetching content: {str(e)}")
            return {'score': 20, 'error': str(e)}
        except Exception as e:
            logger.error(f"Error analyzing content: {str(e)}")
            return {'score': 10, 'error': str(e)}
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main text content from page"""
        try:
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            # Try to find main content areas
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|article|post|main'))
            
            if main_content:
                text = main_content.get_text()
            else:
                # Fallback to body text
                text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except Exception as e:
            logger.error(f"Error extracting content: {str(e)}")
            return ""
    
    def _extract_meta_info(self, soup: BeautifulSoup) -> Dict:
        """Extract meta information from page"""
        meta_info = {}
        
        try:
            # Extract author
            author = soup.find('meta', {'name': 'author'}) or soup.find('meta', {'property': 'article:author'})
            if author:
                meta_info['author'] = author.get('content', '')
            
            # Extract publication date
            pub_date = soup.find('meta', {'property': 'article:published_time'}) or \
                      soup.find('meta', {'name': 'publish-date'}) or \
                      soup.find('time')
            if pub_date:
                meta_info['published'] = pub_date.get('content') or pub_date.get('datetime', '')
            
            # Extract description
            description = soup.find('meta', {'name': 'description'}) or soup.find('meta', {'property': 'og:description'})
            if description:
                meta_info['description'] = description.get('content', '')
            
            # Extract keywords
            keywords = soup.find('meta', {'name': 'keywords'})
            if keywords:
                meta_info['keywords'] = keywords.get('content', '')
                
        except Exception as e:
            logger.error(f"Error extracting meta info: {str(e)}")
        
        return meta_info
    
    def _analyze_page_content(self, soup: BeautifulSoup, content: str, red_flags: List[str]) -> int:
        """Analyze page content for quality indicators"""
        score = 0
        
        try:
            # Check content length
            if len(content) < 200:
                red_flags.append("Very short article content")
                score += 20
            
            # Check for excessive ads
            ad_indicators = soup.find_all(['iframe', 'ins', 'div'], class_=re.compile(r'ad|advertisement|banner|popup'))
            if len(ad_indicators) > 10:
                red_flags.append("Excessive advertisements detected")
                score += 15
            
            # Check for missing author information
            author_info = soup.find_all(['meta', 'span', 'div'], attrs={'name': re.compile(r'author'), 'class': re.compile(r'author|byline')})
            if not author_info:
                red_flags.append("No author information found")
                score += 12
            
            # Check for missing publication date
            date_info = soup.find_all(['meta', 'time', 'span'], attrs={'name': re.compile(r'date|publish'), 'class': re.compile(r'date|publish|time')})
            if not date_info:
                red_flags.append("No publication date found")
                score += 10
            
            # Check for comment sections (engagement indicator)
            comments = soup.find_all(['div', 'section'], class_=re.compile(r'comment|discuss'))
            if not comments:
                score += 5  # Minor flag, not always available
                
        except Exception as e:
            logger.error(f"Error analyzing page content: {str(e)}")
        
        return score
    
    def _extract_external_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract external links from the page"""
        try:
            external_links = []
            base_domain = urlparse(base_url).netloc
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                parsed = urlparse(full_url)
                
                if parsed.netloc and parsed.netloc != base_domain:
                    external_links.append(full_url)
                    
                if len(external_links) >= 20:  # Limit collection
                    break
            
            return external_links
            
        except Exception as e:
            logger.error(f"Error extracting external links: {str(e)}")
            return []
    
    def _check_social_signals(self, soup: BeautifulSoup) -> Dict:
        """Check for social media sharing buttons and signals"""
        try:
            social_signals = {
                'sharing_buttons': False,
                'social_meta': False,
                'embedded_social': False
            }
            
            # Check for sharing buttons
            sharing_elements = soup.find_all(['a', 'div', 'button'], class_=re.compile(r'share|social|twitter|facebook'))
            if sharing_elements:
                social_signals['sharing_buttons'] = True
            
            # Check for Open Graph meta tags
            og_tags = soup.find_all('meta', property=re.compile(r'^og:'))
            if og_tags:
                social_signals['social_meta'] = True
            
            # Check for embedded social content
            embedded_social = soup.find_all(['iframe', 'blockquote'], class_=re.compile(r'twitter|facebook|instagram'))
            if embedded_social:
                social_signals['embedded_social'] = True
            
            return social_signals
            
        except Exception as e:
            logger.error(f"Error checking social signals: {str(e)}")
            return {}
