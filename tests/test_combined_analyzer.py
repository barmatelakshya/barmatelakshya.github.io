"""
Test Cases for Combined Threat Analyzer
SIH PS1 - Cybersecurity Threat Detector
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from backend.models.combined_analyzer import analyze_input, get_combined_analyzer

class TestCombinedAnalyzer:
    
    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = get_combined_analyzer()
    
    def test_text_only_analysis(self):
        """Test analysis with text input only"""
        phishing_text = "URGENT! Your account will be suspended. Click here to verify immediately!"
        
        result = analyze_input(text=phishing_text)
        
        assert isinstance(result, dict)
        assert 'combined_score' in result
        assert 'risk_level' in result
        assert 'input_types' in result
        assert 'text' in result['input_types']
        assert 'individual_results' in result
        assert 'text' in result['individual_results']
    
    def test_url_only_analysis(self):
        """Test analysis with URL input only"""
        suspicious_url = "http://192.168.1.100/urgent-verify/login.php"
        
        result = analyze_input(url=suspicious_url)
        
        assert isinstance(result, dict)
        assert 'combined_score' in result
        assert 'risk_level' in result
        assert 'input_types' in result
        assert 'url' in result['input_types']
        assert 'individual_results' in result
        assert 'url' in result['individual_results']
    
    def test_combined_text_and_url_analysis(self):
        """Test analysis with both text and URL inputs"""
        phishing_text = "Security alert! Verify your account at the link below:"
        suspicious_url = "http://secure-bank-verify.fake-domain.com/login"
        
        result = analyze_input(text=phishing_text, url=suspicious_url)
        
        assert isinstance(result, dict)
        assert 'combined_score' in result
        assert 'risk_level' in result
        assert len(result['input_types']) == 2
        assert 'text' in result['input_types']
        assert 'url' in result['input_types']
        assert 'text' in result['individual_results']
        assert 'url' in result['individual_results']
    
    def test_empty_input_handling(self):
        """Test handling of empty inputs"""
        result = analyze_input(text="", url="")
        
        assert isinstance(result, dict)
        assert 'error' in result
    
    def test_url_extraction_from_text(self):
        """Test automatic URL extraction from text"""
        text_with_url = "Click here to verify: http://suspicious-site.com/verify"
        
        result = analyze_input(text=text_with_url)
        
        assert isinstance(result, dict)
        assert 'combined_score' in result
        # Should analyze both text and extracted URL
        if 'extracted_urls' in result:
            assert len(result['extracted_urls']) > 0
    
    def test_risk_level_calculation(self):
        """Test risk level calculation for different scenarios"""
        test_cases = [
            {
                'text': 'URGENT! Account suspended! Click here now!',
                'url': 'http://192.168.1.1/verify',
                'expected_min_level': 'High'
            },
            {
                'text': 'Your order has been shipped',
                'url': 'https://amazon.com/orders',
                'expected_max_level': 'Low'
            },
            {
                'text': 'Click here to claim prize!',
                'url': '',
                'expected_min_level': 'Medium'
            }
        ]
        
        for case in test_cases:
            result = analyze_input(text=case['text'], url=case['url'])
            
            assert 'risk_level' in result
            assert result['risk_level'] in ['Very Low', 'Low', 'Medium', 'High', 'Critical']
    
    def test_combined_score_calculation(self):
        """Test combined score calculation"""
        # High risk text + high risk URL should give high combined score
        high_risk_text = "URGENT SECURITY ALERT! Verify account immediately!"
        high_risk_url = "http://192.168.1.100/urgent-verify"
        
        result = analyze_input(text=high_risk_text, url=high_risk_url)
        
        assert 'combined_score' in result
        assert 0.0 <= result['combined_score'] <= 1.0
        assert result['combined_score'] > 0.5  # Should be high risk
    
    def test_threat_indicators(self):
        """Test threat indicators detection"""
        suspicious_text = "Click here to verify your suspended account!"
        suspicious_url = "http://bit.ly/account-verify"
        
        result = analyze_input(text=suspicious_text, url=suspicious_url)
        
        assert 'threat_indicators' in result
        assert isinstance(result['threat_indicators'], list)
        assert len(result['threat_indicators']) > 0
    
    def test_recommendations_generation(self):
        """Test recommendations generation"""
        result = analyze_input(text="Urgent security alert!", url="http://suspicious.com")
        
        assert 'recommendations' in result
        assert 'final_recommendation' in result
        assert isinstance(result['recommendations'], list)
        assert isinstance(result['final_recommendation'], str)
    
    def test_confidence_calculation(self):
        """Test confidence score calculation"""
        result = analyze_input(text="Test message", url="https://example.com")
        
        assert 'confidence' in result
        assert 0.0 <= result['confidence'] <= 1.0
    
    def test_batch_analysis(self):
        """Test batch analysis functionality"""
        batch_inputs = [
            {'text': 'URGENT! Verify now!', 'url': ''},
            {'text': '', 'url': 'http://192.168.1.1'},
            {'text': 'Thank you for purchase', 'url': 'https://amazon.com'}
        ]
        
        results = self.analyzer.batch_analyze(batch_inputs)
        
        assert isinstance(results, list)
        assert len(results) == len(batch_inputs)
        
        for result in results:
            assert isinstance(result, dict)
            assert 'combined_score' in result
            assert 'risk_level' in result
    
    def test_analyzer_info(self):
        """Test analyzer information retrieval"""
        info = self.analyzer.get_analyzer_info()
        
        assert isinstance(info, dict)
        assert 'version' in info
        assert 'components' in info
        assert 'weights' in info
        assert 'supported_inputs' in info
    
    def test_is_threat_flag(self):
        """Test is_threat flag consistency"""
        # High risk case
        high_risk_result = analyze_input(
            text="URGENT! Account suspended! Verify now!",
            url="http://192.168.1.1/verify"
        )
        
        # Low risk case
        low_risk_result = analyze_input(
            text="Thank you for your order",
            url="https://amazon.com"
        )
        
        assert 'is_threat' in high_risk_result
        assert 'is_threat' in low_risk_result
        
        # High risk should be flagged as threat
        if high_risk_result['combined_score'] > 0.5:
            assert high_risk_result['is_threat'] == True
        
        # Low risk should not be flagged as threat
        if low_risk_result['combined_score'] <= 0.5:
            assert low_risk_result['is_threat'] == False
    
    def test_timestamp_generation(self):
        """Test timestamp generation in results"""
        result = analyze_input(text="Test message")
        
        assert 'analysis_timestamp' in result
        assert isinstance(result['analysis_timestamp'], str)
        assert len(result['analysis_timestamp']) > 0
