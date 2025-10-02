"""
Test Cases for URL Analyzer
SIH PS1 - Cybersecurity Threat Detector
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from backend.models.url_analyzer import analyze_url, get_analyzer

class TestURLAnalyzer:
    
    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = get_analyzer()
    
    def test_ip_address_detection(self):
        """Test detection of IP addresses in URLs"""
        ip_url = "http://192.168.1.100/login.php"
        
        result = analyze_url(ip_url)
        
        assert isinstance(result, dict)
        assert 'risk_score' in result
        assert 'risk_factors' in result
        assert result['risk_score'] > 0.3
        assert any('IP address' in factor for factor in result['risk_factors'])
    
    def test_url_shortener_detection(self):
        """Test detection of URL shortening services"""
        short_url = "http://bit.ly/suspicious-link"
        
        result = analyze_url(short_url)
        
        assert isinstance(result, dict)
        assert result['risk_score'] > 0.2
        assert any('shortening' in factor.lower() for factor in result['risk_factors'])
    
    def test_legitimate_url_analysis(self):
        """Test analysis of legitimate URLs"""
        legitimate_urls = [
            "https://amazon.com/orders",
            "https://github.com/microsoft/vscode",
            "https://stackoverflow.com/questions"
        ]
        
        for url in legitimate_urls:
            result = analyze_url(url)
            
            assert isinstance(result, dict)
            assert 'risk_score' in result
            assert result['risk_score'] < 0.5  # Should be low risk
    
    def test_suspicious_domain_patterns(self):
        """Test detection of suspicious domain patterns"""
        suspicious_urls = [
            "http://secure-bank-verify.fake-domain.com/urgent",
            "http://paypal-security-update.suspicious.com/login",
            "http://amazon-account-verify.malicious.org/update"
        ]
        
        for url in suspicious_urls:
            result = analyze_url(url)
            
            assert isinstance(result, dict)
            assert result['risk_score'] > 0.1
            assert len(result['risk_factors']) > 0
    
    def test_empty_url_handling(self):
        """Test handling of empty URLs"""
        result = analyze_url("")
        
        assert isinstance(result, dict)
        assert 'error' in result or result['risk_score'] == 0.0
    
    def test_invalid_url_handling(self):
        """Test handling of invalid URLs"""
        invalid_urls = [
            "not-a-url",
            "htp://invalid-protocol.com",
            "://missing-protocol.com"
        ]
        
        for url in invalid_urls:
            result = analyze_url(url)
            
            assert isinstance(result, dict)
            # Should either handle gracefully or return error
            assert 'error' in result or 'risk_score' in result
    
    def test_redirection_analysis(self):
        """Test redirection chain analysis"""
        # Note: This test might be slow due to network requests
        test_url = "https://httpbin.org/redirect/2"
        
        result = analyze_url(test_url)
        
        assert isinstance(result, dict)
        assert 'redirections' in result or 'risk_factors' in result
    
    def test_risk_level_calculation(self):
        """Test risk level calculation consistency"""
        test_cases = [
            ("http://192.168.1.1/login", "High"),
            ("http://bit.ly/test", "Medium"),
            ("https://amazon.com", "Low")
        ]
        
        for url, expected_min_level in test_cases:
            result = analyze_url(url)
            
            assert 'risk_level' in result
            assert result['risk_level'] in ['Very Low', 'Low', 'Medium', 'High']
    
    def test_confidence_scores(self):
        """Test confidence score ranges"""
        test_url = "http://suspicious-domain.com/login"
        result = analyze_url(test_url)
        
        assert 'confidence' in result
        assert 0.0 <= result['confidence'] <= 1.0
    
    def test_domain_age_check(self):
        """Test domain age checking functionality"""
        # Test with a well-known domain
        result = analyze_url("https://google.com")
        
        assert isinstance(result, dict)
        # Domain age might be available or not depending on WHOIS
        if 'domain_age' in result:
            assert isinstance(result['domain_age'], str)
    
    def test_suspicious_file_extensions(self):
        """Test detection of suspicious file extensions"""
        suspicious_urls = [
            "http://example.com/download.exe",
            "http://example.com/file.scr",
            "http://example.com/script.bat"
        ]
        
        for url in suspicious_urls:
            result = analyze_url(url)
            
            assert isinstance(result, dict)
            assert result['risk_score'] > 0.2
    
    def test_long_url_detection(self):
        """Test detection of unusually long URLs"""
        long_url = "http://example.com/" + "a" * 200 + "/login"
        
        result = analyze_url(long_url)
        
        assert isinstance(result, dict)
        assert result['risk_score'] > 0.0
