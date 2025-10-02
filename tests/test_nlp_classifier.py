"""
Test Cases for NLP Phishing Classifier
SIH PS1 - Cybersecurity Threat Detector
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from backend.models.nlp_classifier import predict_phishing, get_classifier

class TestNLPClassifier:
    
    def setup_method(self):
        """Setup test fixtures"""
        self.classifier = get_classifier()
    
    def test_phishing_text_detection(self):
        """Test detection of obvious phishing text"""
        phishing_text = "URGENT SECURITY ALERT! Your account will be suspended in 24 hours. Click here immediately to verify your identity."
        
        result = predict_phishing(phishing_text)
        
        assert isinstance(result, dict)
        assert 'is_phishing' in result
        assert 'confidence' in result
        assert 'risk_level' in result
        assert result['confidence'] > 0.5
        assert result['risk_level'] in ['High', 'Medium', 'Low', 'Very Low']
    
    def test_legitimate_text_detection(self):
        """Test detection of legitimate text"""
        legitimate_text = "Thank you for your recent purchase from Amazon. Your order has been shipped and will arrive within 2-3 business days."
        
        result = predict_phishing(legitimate_text)
        
        assert isinstance(result, dict)
        assert 'is_phishing' in result
        assert result['is_phishing'] == False
        assert result['confidence'] >= 0.0
        assert result['risk_level'] in ['High', 'Medium', 'Low', 'Very Low']
    
    def test_empty_text_handling(self):
        """Test handling of empty text"""
        result = predict_phishing("")
        
        assert isinstance(result, dict)
        assert 'error' in result or result['confidence'] == 0.0
    
    def test_suspicious_keywords_detection(self):
        """Test detection of suspicious keywords"""
        test_cases = [
            ("Click here to verify your account", True),
            ("Congratulations! You've won a prize!", True),
            ("Your account will be suspended", True),
            ("Thank you for your order", False),
            ("Meeting scheduled for tomorrow", False)
        ]
        
        for text, should_be_suspicious in test_cases:
            result = predict_phishing(text)
            
            if should_be_suspicious:
                assert result['confidence'] > 0.3, f"Text '{text}' should be suspicious"
            else:
                assert result['confidence'] < 0.7, f"Text '{text}' should not be highly suspicious"
    
    def test_batch_prediction(self):
        """Test batch prediction functionality"""
        texts = [
            "URGENT: Verify your account now!",
            "Thank you for your purchase",
            "Click here to claim your prize!"
        ]
        
        results = self.classifier.batch_predict(texts)
        
        assert len(results) == len(texts)
        for result in results:
            assert isinstance(result, dict)
            assert 'is_phishing' in result
            assert 'confidence' in result
    
    def test_model_info(self):
        """Test model information retrieval"""
        info = self.classifier.get_model_info()
        
        assert isinstance(info, dict)
        assert 'model_name' in info
        assert 'is_loaded' in info
        assert 'method' in info
    
    def test_confidence_scores(self):
        """Test confidence score ranges"""
        high_risk_text = "URGENT! Click here now to verify your suspended account!"
        low_risk_text = "Your order confirmation number is 12345."
        
        high_result = predict_phishing(high_risk_text)
        low_result = predict_phishing(low_risk_text)
        
        assert 0.0 <= high_result['confidence'] <= 1.0
        assert 0.0 <= low_result['confidence'] <= 1.0
        assert high_result['confidence'] > low_result['confidence']
    
    def test_risk_level_consistency(self):
        """Test risk level consistency with confidence scores"""
        test_text = "Your account needs immediate verification!"
        result = predict_phishing(test_text)
        
        confidence = result['confidence']
        risk_level = result['risk_level']
        
        if confidence >= 0.8:
            assert risk_level == 'High'
        elif confidence >= 0.6:
            assert risk_level in ['High', 'Medium']
        elif confidence >= 0.3:
            assert risk_level in ['Medium', 'Low']
        else:
            assert risk_level in ['Low', 'Very Low']
