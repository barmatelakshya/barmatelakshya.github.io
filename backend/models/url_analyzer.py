"""
Advanced URL Analyzer
SIH PS1 - Cybersecurity Threat Detector
"""
import requests
import re
import base64
import socket
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
import dns.resolver
from typing import Dict, List, Optional
import time

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False
    print("⚠️ python-whois not available, domain age checking disabled")

class URLAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Suspicious patterns
        self.suspicious_domains = [
            'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 
            'short.link', 'tiny.cc', 'is.gd', 'buff.ly'
        ]
        
        self.trusted_domains = [
            'google.com', 'amazon.com', 'microsoft.com', 'apple.com',
            'facebook.com', 'twitter.com', 'linkedin.com', 'github.com',
            'stackoverflow.com', 'wikipedia.org'
        ]
        
        self.suspicious_keywords = [
            'secure', 'verify', 'update', 'login', 'account', 'bank',
            'paypal', 'amazon', 'microsoft', 'apple', 'google'
        ]
    
    def analyze_url(self, url: str) -> Dict:
        """
        Comprehensive URL analysis
        
        Args:
            url (str): URL to analyze
            
        Returns:
            Dict: Analysis results with risk assessment
        """
        if not url or not url.strip():
            return {'error': 'Empty URL provided', 'risk_score': 0.0}
        
        url = url.strip()
        
        # Parse URL
        try:
            parsed = urlparse(url)
            if not parsed.scheme:
                url = 'http://' + url
                parsed = urlparse(url)
        except Exception as e:
            return {'error': f'Invalid URL: {e}', 'risk_score': 0.0}
        
        analysis_results = {
            'url': url,
            'domain': parsed.netloc,
            'risk_score': 0.0,
            'risk_factors': [],
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Run all analysis checks
        self._check_suspicious_patterns(url, parsed, analysis_results)
        self._check_redirection_chains(url, analysis_results)
        self._check_domain_age(parsed.netloc, analysis_results)
        self._check_dns_records(parsed.netloc, analysis_results)
        
        # Calculate final risk assessment
        self._calculate_risk_assessment(analysis_results)
        
        return analysis_results
    
    def _check_suspicious_patterns(self, url: str, parsed, results: Dict):
        """Check for suspicious URL patterns"""
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        query = parsed.query.lower()
        
        # IP address instead of domain
        if re.match(r'^\d+\.\d+\.\d+\.\d+', domain):
            results['risk_score'] += 0.4
            results['risk_factors'].append('IP address used instead of domain')
        
        # URL shortening services
        if any(short_domain in domain for short_domain in self.suspicious_domains):
            results['risk_score'] += 0.3
            results['risk_factors'].append('URL shortening service detected')
        
        # Trusted domain check (reduces risk)
        if any(trusted in domain for trusted in self.trusted_domains):
            results['risk_score'] -= 0.2
            results['risk_factors'].append('Trusted domain detected')
        
        # Excessive subdomains
        subdomain_count = len(domain.split('.')) - 2
        if subdomain_count > 3:
            results['risk_score'] += 0.2
            results['risk_factors'].append(f'Excessive subdomains ({subdomain_count})')
        
        # Suspicious keywords in domain
        for keyword in self.suspicious_keywords:
            if keyword in domain and not any(trusted in domain for trusted in self.trusted_domains):
                results['risk_score'] += 0.15
                results['risk_factors'].append(f'Suspicious keyword in domain: {keyword}')
                break
        
        # Long domain name
        if len(domain) > 50:
            results['risk_score'] += 0.1
            results['risk_factors'].append('Unusually long domain name')
        
        # Excessive hyphens
        if domain.count('-') > 3:
            results['risk_score'] += 0.1
            results['risk_factors'].append('Excessive hyphens in domain')
        
        # Base64 encoding in URL
        try:
            if any(len(part) > 20 and self._is_base64(part) for part in [path, query]):
                results['risk_score'] += 0.2
                results['risk_factors'].append('Base64 encoding detected')
        except:
            pass
        
        # Suspicious file extensions
        suspicious_extensions = ['.exe', '.scr', '.bat', '.com', '.pif', '.vbs']
        if any(ext in path for ext in suspicious_extensions):
            results['risk_score'] += 0.3
            results['risk_factors'].append('Suspicious file extension')
        
        # URL length
        if len(url) > 200:
            results['risk_score'] += 0.1
            results['risk_factors'].append('Unusually long URL')
    
    def _check_redirection_chains(self, url: str, results: Dict):
        """Check for redirection chains"""
        try:
            redirections = []
            current_url = url
            max_redirects = 10
            
            for i in range(max_redirects):
                response = self.session.head(current_url, allow_redirects=False, timeout=5)
                
                if response.status_code in [301, 302, 303, 307, 308]:
                    redirect_url = response.headers.get('Location', '')
                    if redirect_url:
                        redirections.append({
                            'from': current_url,
                            'to': redirect_url,
                            'status': response.status_code
                        })
                        current_url = redirect_url
                    else:
                        break
                else:
                    break
            
            results['redirections'] = redirections
            redirect_count = len(redirections)
            
            if redirect_count > 0:
                results['risk_factors'].append(f'Redirection chain detected ({redirect_count} redirects)')
                
                # Multiple redirections increase risk
                if redirect_count > 3:
                    results['risk_score'] += 0.3
                elif redirect_count > 1:
                    results['risk_score'] += 0.15
                else:
                    results['risk_score'] += 0.05
                
                # Check if redirections go through suspicious domains
                for redirect in redirections:
                    redirect_domain = urlparse(redirect['to']).netloc.lower()
                    if any(suspicious in redirect_domain for suspicious in self.suspicious_domains):
                        results['risk_score'] += 0.2
                        results['risk_factors'].append('Redirection through suspicious domain')
                        break
            
        except requests.RequestException as e:
            results['risk_factors'].append(f'Could not check redirections: {str(e)[:50]}')
        except Exception as e:
            results['risk_factors'].append(f'Redirection check failed: {str(e)[:50]}')
    
    def _check_domain_age(self, domain: str, results: Dict):
        """Check domain age using WHOIS"""
        if not WHOIS_AVAILABLE:
            results['domain_age'] = 'Unknown (WHOIS not available)'
            return
        
        try:
            # Clean domain (remove port, subdomain for main domain check)
            clean_domain = domain.split(':')[0]
            domain_parts = clean_domain.split('.')
            if len(domain_parts) > 2:
                # Get main domain (last two parts)
                clean_domain = '.'.join(domain_parts[-2:])
            
            w = whois.whois(clean_domain)
            
            if w.creation_date:
                creation_date = w.creation_date
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]
                
                if creation_date:
                    age_days = (datetime.now() - creation_date).days
                    results['domain_age'] = f'{age_days} days'
                    
                    # Very new domains are suspicious
                    if age_days < 30:
                        results['risk_score'] += 0.3
                        results['risk_factors'].append(f'Very new domain ({age_days} days old)')
                    elif age_days < 90:
                        results['risk_score'] += 0.15
                        results['risk_factors'].append(f'Recently created domain ({age_days} days old)')
                    
                    # Very old domains are generally trustworthy
                    if age_days > 365 * 5:  # 5 years
                        results['risk_score'] -= 0.1
                        results['risk_factors'].append('Well-established domain (5+ years)')
                else:
                    results['domain_age'] = 'Unknown'
            else:
                results['domain_age'] = 'Unknown'
                
        except Exception as e:
            results['domain_age'] = f'Check failed: {str(e)[:50]}'
    
    def _check_dns_records(self, domain: str, results: Dict):
        """Check DNS records for suspicious patterns"""
        try:
            # Clean domain
            clean_domain = domain.split(':')[0]
            
            # Check A records
            try:
                a_records = dns.resolver.resolve(clean_domain, 'A')
                ip_addresses = [str(record) for record in a_records]
                results['ip_addresses'] = ip_addresses
                
                # Check for suspicious IP ranges
                for ip in ip_addresses:
                    if self._is_suspicious_ip(ip):
                        results['risk_score'] += 0.2
                        results['risk_factors'].append(f'Suspicious IP address: {ip}')
                        
            except dns.resolver.NXDOMAIN:
                results['risk_score'] += 0.4
                results['risk_factors'].append('Domain does not exist (NXDOMAIN)')
            except dns.resolver.NoAnswer:
                results['risk_factors'].append('No A records found')
            except Exception:
                pass
            
            # Check MX records (legitimate domains usually have email)
            try:
                mx_records = dns.resolver.resolve(clean_domain, 'MX')
                results['has_mx_records'] = True
            except:
                results['has_mx_records'] = False
                results['risk_score'] += 0.05
                results['risk_factors'].append('No email records (MX) found')
                
        except Exception as e:
            results['risk_factors'].append(f'DNS check failed: {str(e)[:50]}')
    
    def _is_base64(self, s: str) -> bool:
        """Check if string is base64 encoded"""
        try:
            if len(s) % 4 != 0:
                return False
            base64.b64decode(s, validate=True)
            return True
        except:
            return False
    
    def _is_suspicious_ip(self, ip: str) -> bool:
        """Check if IP address is in suspicious ranges"""
        try:
            parts = [int(x) for x in ip.split('.')]
            
            # Private IP ranges (suspicious for public websites)
            if (parts[0] == 10 or 
                (parts[0] == 172 and 16 <= parts[1] <= 31) or
                (parts[0] == 192 and parts[1] == 168)):
                return True
                
            # Localhost
            if parts[0] == 127:
                return True
                
            return False
        except:
            return False
    
    def _calculate_risk_assessment(self, results: Dict):
        """Calculate final risk assessment"""
        risk_score = max(0.0, min(1.0, results['risk_score']))
        results['risk_score'] = risk_score
        
        # Determine risk level
        if risk_score >= 0.7:
            results['risk_level'] = 'High'
            results['recommendation'] = 'DO NOT VISIT - High risk of malicious content'
        elif risk_score >= 0.4:
            results['risk_level'] = 'Medium'
            results['recommendation'] = 'CAUTION - Potentially suspicious, verify before visiting'
        elif risk_score >= 0.2:
            results['risk_level'] = 'Low'
            results['recommendation'] = 'Generally safe, but remain cautious'
        else:
            results['risk_level'] = 'Very Low'
            results['recommendation'] = 'Appears safe to visit'
        
        # Calculate confidence based on number of checks performed
        checks_performed = len([f for f in results['risk_factors'] if not f.startswith('Could not') and not f.startswith('Check failed')])
        results['confidence'] = min(0.95, 0.6 + (checks_performed * 0.05))

# Global analyzer instance
_analyzer = None

def get_analyzer() -> URLAnalyzer:
    """Get or create the global analyzer instance"""
    global _analyzer
    if _analyzer is None:
        _analyzer = URLAnalyzer()
    return _analyzer

def analyze_url(url: str) -> Dict:
    """
    Convenience function for URL analysis
    
    Args:
        url (str): URL to analyze
        
    Returns:
        Dict: {
            'url': str,
            'domain': str,
            'risk_score': float,
            'risk_level': str,
            'risk_factors': List[str],
            'redirections': List[Dict],
            'domain_age': str,
            'ip_addresses': List[str],
            'recommendation': str,
            'confidence': float
        }
    """
    analyzer = get_analyzer()
    return analyzer.analyze_url(url)
