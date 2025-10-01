"""
URL Parsing Utilities
SIH PS1 - Cybersecurity Threat Detector
"""
import re
from urllib.parse import urlparse, parse_qs
from typing import Dict, List

class URLParser:
    """URL analysis and parsing utilities"""
    
    def __init__(self):
        self.suspicious_domains = [
            'bit.ly', 'tinyurl.com', 'goo.gl', 't.co',
            'ow.ly', 'short.link', 'tiny.cc'
        ]
        
        self.trusted_domains = [
            'google.com', 'amazon.com', 'microsoft.com',
            'apple.com', 'facebook.com', 'twitter.com'
        ]
    
    def parse_url(self, url: str) -> Dict:
        """Parse URL into components"""
        try:
            parsed = urlparse(url)
            return {
                'scheme': parsed.scheme,
                'domain': parsed.netloc,
                'path': parsed.path,
                'params': parse_qs(parsed.query),
                'fragment': parsed.fragment,
                'is_valid': True
            }
        except Exception:
            return {'is_valid': False}
    
    def is_ip_address(self, domain: str) -> bool:
        """Check if domain is an IP address"""
        ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(ip_pattern, domain))
    
    def is_shortened_url(self, domain: str) -> bool:
        """Check if URL uses a shortening service"""
        return any(suspicious in domain.lower() for suspicious in self.suspicious_domains)
    
    def is_trusted_domain(self, domain: str) -> bool:
        """Check if domain is from trusted source"""
        return any(trusted in domain.lower() for trusted in self.trusted_domains)
    
    def count_subdomains(self, domain: str) -> int:
        """Count number of subdomains"""
        return len(domain.split('.')) - 2 if '.' in domain else 0
    
    def has_suspicious_patterns(self, url: str) -> List[str]:
        """Detect suspicious URL patterns"""
        suspicious_patterns = []
        
        # Check for homograph attacks
        if re.search(r'[а-я]', url):  # Cyrillic characters
            suspicious_patterns.append('Cyrillic characters detected')
        
        # Check for excessive hyphens
        if url.count('-') > 3:
            suspicious_patterns.append('Excessive hyphens')
        
        # Check for suspicious keywords
        suspicious_keywords = ['secure', 'verify', 'update', 'login', 'account']
        for keyword in suspicious_keywords:
            if keyword in url.lower():
                suspicious_patterns.append(f'Suspicious keyword: {keyword}')
        
        return suspicious_patterns
    
    def calculate_url_risk(self, url: str) -> Dict:
        """Calculate comprehensive URL risk assessment"""
        parsed = self.parse_url(url)
        
        if not parsed['is_valid']:
            return {'risk_score': 0.0, 'risk_level': 'Unknown', 'issues': ['Invalid URL']}
        
        risk_score = 0.0
        issues = []
        
        domain = parsed['domain']
        
        # IP address instead of domain
        if self.is_ip_address(domain):
            risk_score += 0.4
            issues.append('IP address used instead of domain')
        
        # URL shortening service
        if self.is_shortened_url(domain):
            risk_score += 0.3
            issues.append('URL shortening service detected')
        
        # Trusted domain check
        if self.is_trusted_domain(domain):
            risk_score -= 0.2
            issues.append('Trusted domain detected')
        
        # Too many subdomains
        subdomain_count = self.count_subdomains(domain)
        if subdomain_count > 3:
            risk_score += 0.2
            issues.append(f'Excessive subdomains ({subdomain_count})')
        
        # Suspicious patterns
        patterns = self.has_suspicious_patterns(url)
        if patterns:
            risk_score += len(patterns) * 0.1
            issues.extend(patterns)
        
        # Normalize risk score
        risk_score = max(0.0, min(1.0, risk_score))
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = 'High'
        elif risk_score >= 0.4:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'issues': issues,
            'domain_info': {
                'domain': domain,
                'is_ip': self.is_ip_address(domain),
                'is_shortened': self.is_shortened_url(domain),
                'is_trusted': self.is_trusted_domain(domain),
                'subdomain_count': subdomain_count
            }
        }
