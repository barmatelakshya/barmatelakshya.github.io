"""
Threat Detection Models
SIH PS1 - Cybersecurity Threat Detector
"""
import re
from datetime import datetime

class ThreatDetector:
    def __init__(self):
        self.phishing_keywords = [
            'urgent', 'verify', 'suspended', 'click here', 'winner', 'congratulations',
            'limited time', 'act now', 'expires', 'claim', 'free money', 'lottery',
            'bank account', 'social security', 'password', 'login credentials'
        ]
        
    def analyze_text(self, text):
        """NLP-based phishing detection"""
        text_lower = text.lower()
        
        # Keyword analysis
        suspicious_count = sum(1 for keyword in self.phishing_keywords if keyword in text_lower)
        
        # Pattern analysis
        has_urgent_language = any(word in text_lower for word in ['urgent', 'immediate', 'asap'])
        has_financial_terms = any(word in text_lower for word in ['bank', 'account', 'payment', 'money'])
        has_action_words = any(word in text_lower for word in ['click', 'download', 'verify', 'update'])
        
        # Risk calculation
        risk_score = min(0.95, (suspicious_count * 0.15) + 
                        (0.2 if has_urgent_language else 0) +
                        (0.2 if has_financial_terms else 0) +
                        (0.15 if has_action_words else 0))
        
        return {
            'is_threat': risk_score > 0.5,
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'confidence': min(0.95, 0.6 + (suspicious_count * 0.08)),
            'detected_keywords': [kw for kw in self.phishing_keywords if kw in text_lower][:5],
            'analysis_time': datetime.now().strftime('%H:%M:%S')
        }
    
    def analyze_url(self, url):
        """URL threat analysis"""
        suspicious_domains = ['bit.ly', 'tinyurl', 'suspicious-site', 'phishing-test']
        suspicious_patterns = [r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', r'[a-z]+-[a-z]+-[a-z]+\.com']
        
        risk_factors = 0
        detected_issues = []
        
        # Check suspicious domains
        if any(domain in url.lower() for domain in suspicious_domains):
            risk_factors += 0.4
            detected_issues.append('Suspicious domain detected')
            
        # Check IP addresses
        if re.search(r'\d+\.\d+\.\d+\.\d+', url):
            risk_factors += 0.3
            detected_issues.append('IP address instead of domain')
            
        # Check suspicious patterns
        for pattern in suspicious_patterns:
            if re.search(pattern, url.lower()):
                risk_factors += 0.2
                detected_issues.append('Suspicious URL pattern')
                break
        
        risk_score = min(0.95, risk_factors)
        
        return {
            'is_threat': risk_score > 0.4,
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'confidence': 0.85,
            'detected_issues': detected_issues,
            'analysis_time': datetime.now().strftime('%H:%M:%S')
        }
    
    def _get_risk_level(self, score):
        if score >= 0.7: return 'High'
        elif score >= 0.4: return 'Medium'
        else: return 'Low'
