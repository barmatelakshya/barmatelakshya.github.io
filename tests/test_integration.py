"""
Integration Test Cases
SIH PS1 - Cybersecurity Threat Detector
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from backend.models.combined_analyzer import analyze_input

class TestIntegration:
    
    def test_end_to_end_phishing_detection(self):
        """Test complete phishing detection workflow"""
        phishing_email = """
        URGENT SECURITY ALERT!
        
        Your account will be suspended in 24 hours due to suspicious activity.
        Click here immediately to verify your identity: http://secure-bank-verify.fake-domain.com/urgent-login
        
        Failure to verify will result in permanent account closure.
        """
        
        result = analyze_input(text=phishing_email)
        
        # Should detect high risk
        assert result['combined_score'] > 0.6
        assert result['risk_level'] in ['High', 'Critical']
        assert result['is_threat'] == True
        assert len(result['threat_indicators']) > 0
    
    def test_legitimate_content_detection(self):
        """Test detection of legitimate content"""
        legitimate_email = """
        Thank you for your recent purchase from Amazon.
        
        Your order #123456789 has been shipped and will arrive within 2-3 business days.
        You can track your package at: https://amazon.com/your-orders
        
        Thank you for choosing Amazon.
        """
        
        result = analyze_input(text=legitimate_email)
        
        # Should detect low risk
        assert result['combined_score'] < 0.4
        assert result['risk_level'] in ['Low', 'Very Low']
        assert result['is_threat'] == False
    
    def test_mixed_risk_scenarios(self):
        """Test various mixed risk scenarios"""
        test_cases = [
            {
                'name': 'Suspicious text + safe URL',
                'text': 'Click here to claim your prize!',
                'url': 'https://amazon.com',
                'expected_risk': 'Medium'
            },
            {
                'name': 'Safe text + suspicious URL',
                'text': 'Please visit our website',
                'url': 'http://192.168.1.100/login',
                'expected_risk': 'Medium'
            },
            {
                'name': 'Both suspicious',
                'text': 'URGENT! Verify account now!',
                'url': 'http://bit.ly/urgent-verify',
                'expected_risk': 'High'
            }
        ]
        
        for case in test_cases:
            result = analyze_input(text=case['text'], url=case['url'])
            
            assert 'combined_score' in result
            assert 'risk_level' in result
            assert result['risk_level'] in ['Very Low', 'Low', 'Medium', 'High', 'Critical']
    
    def test_performance_benchmarks(self):
        """Test performance benchmarks"""
        import time
        
        test_input = "URGENT: Your account needs verification!"
        
        start_time = time.time()
        result = analyze_input(text=test_input)
        end_time = time.time()
        
        analysis_time = end_time - start_time
        
        # Should complete within reasonable time
        assert analysis_time < 10.0  # 10 seconds max
        assert isinstance(result, dict)
        assert 'combined_score' in result
