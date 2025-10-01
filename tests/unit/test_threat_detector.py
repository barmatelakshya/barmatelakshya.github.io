"""
Unit Tests for Threat Detector
SIH PS1 - Cybersecurity Threat Detector
"""
import pytest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.models.threat_detector import ThreatDetector

class TestThreatDetector:
    
    def setup_method(self):
        """Setup test fixtures"""
        self.detector = ThreatDetector()
    
    def test_analyze_text_phishing(self):
        """Test phishing text detection"""
        phishing_text = "URGENT: Click here to verify your account immediately!"
        result = self.detector.analyze_text(phishing_text)
        
        assert result['is_threat'] == True
        assert result['risk_score'] > 0.5
        assert result['risk_level'] in ['Medium', 'High']
        assert len(result['detected_keywords']) > 0
    
    def test_analyze_text_safe(self):
        """Test safe text detection"""
        safe_text = "Thank you for your purchase. Your order will arrive soon."
        result = self.detector.analyze_text(safe_text)
        
        assert result['is_threat'] == False
        assert result['risk_score'] < 0.5
        assert result['risk_level'] == 'Low'
    
    def test_analyze_url_suspicious(self):
        """Test suspicious URL detection"""
        suspicious_url = "http://192.168.1.1/login"
        result = self.detector.analyze_url(suspicious_url)
        
        assert result['is_threat'] == True
        assert result['risk_score'] > 0.4
        assert len(result['detected_issues']) > 0
    
    def test_analyze_url_safe(self):
        """Test safe URL detection"""
        safe_url = "https://amazon.com/orders"
        result = self.detector.analyze_url(safe_url)
        
        assert result['is_threat'] == False
        assert result['risk_score'] < 0.4
    
    def test_risk_level_calculation(self):
        """Test risk level calculation"""
        assert self.detector._get_risk_level(0.8) == 'High'
        assert self.detector._get_risk_level(0.5) == 'Medium'
        assert self.detector._get_risk_level(0.2) == 'Low'
