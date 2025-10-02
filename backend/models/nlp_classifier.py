"""
NLP-Based Phishing Classifier
SIH PS1 - Cybersecurity Threat Detector
"""
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import numpy as np
from typing import Dict, List
import logging

# Suppress warnings
logging.getLogger("transformers").setLevel(logging.ERROR)

class PhishingClassifier:
    def __init__(self, model_name: str = "distilbert-base-uncased"):
        """Initialize the phishing classifier with a pre-trained model"""
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.classifier = None
        self.is_loaded = False
        
        # Phishing keywords for fallback
        self.phishing_keywords = [
            'urgent', 'verify', 'suspended', 'click here', 'winner', 'congratulations',
            'limited time', 'act now', 'expires', 'claim', 'free money', 'lottery',
            'bank account', 'social security', 'password', 'login credentials',
            'update payment', 'confirm identity', 'security alert', 'account locked'
        ]
        
        # Try to load the model
        self._load_model()
    
    def _load_model(self):
        """Load the pre-trained transformer model"""
        try:
            print("🔄 Loading DistilBERT model for phishing detection...")
            
            # Use a sentiment analysis model as base (can be fine-tuned for phishing)
            self.classifier = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                return_all_scores=True
            )
            
            self.is_loaded = True
            print("✅ Model loaded successfully!")
            
        except Exception as e:
            print(f"⚠️ Could not load transformer model: {e}")
            print("📝 Using fallback keyword-based detection")
            self.is_loaded = False
    
    def _keyword_based_prediction(self, text: str) -> Dict:
        """Fallback keyword-based prediction"""
        text_lower = text.lower()
        
        # Count suspicious keywords
        suspicious_count = sum(1 for keyword in self.phishing_keywords if keyword in text_lower)
        
        # Calculate confidence based on keyword density
        words = text.split()
        keyword_density = suspicious_count / len(words) if words else 0
        
        # Determine if phishing
        is_phishing = suspicious_count >= 2 or keyword_density > 0.1
        confidence = min(0.95, 0.5 + (suspicious_count * 0.1) + (keyword_density * 2))
        
        # Found keywords
        found_keywords = [kw for kw in self.phishing_keywords if kw in text_lower]
        
        return {
            'is_phishing': is_phishing,
            'confidence': confidence,
            'method': 'keyword_based',
            'suspicious_keywords': found_keywords[:5],
            'keyword_count': suspicious_count
        }
    
    def _transformer_prediction(self, text: str) -> Dict:
        """Transformer-based prediction"""
        try:
            # Get sentiment scores
            results = self.classifier(text)
            
            # Convert sentiment to phishing probability
            # Negative sentiment often correlates with phishing (urgency, threats)
            negative_score = 0
            positive_score = 0
            
            for result in results[0]:
                if result['label'] == 'NEGATIVE':
                    negative_score = result['score']
                elif result['label'] == 'POSITIVE':
                    positive_score = result['score']
            
            # Heuristic: High negative sentiment + certain keywords = likely phishing
            text_lower = text.lower()
            keyword_boost = sum(0.1 for kw in ['urgent', 'verify', 'click', 'suspended'] if kw in text_lower)
            
            # Calculate phishing probability
            phishing_prob = (negative_score * 0.7) + keyword_boost
            phishing_prob = min(0.95, phishing_prob)
            
            is_phishing = phishing_prob > 0.6
            
            return {
                'is_phishing': is_phishing,
                'confidence': phishing_prob,
                'method': 'transformer',
                'negative_sentiment': negative_score,
                'positive_sentiment': positive_score,
                'model_used': self.model_name
            }
            
        except Exception as e:
            print(f"⚠️ Transformer prediction failed: {e}")
            return self._keyword_based_prediction(text)
    
    def predict_phishing(self, text: str) -> Dict:
        """
        Main prediction function
        
        Args:
            text (str): Email or SMS text to analyze
            
        Returns:
            Dict: Prediction results with confidence scores
        """
        if not text or not text.strip():
            return {
                'is_phishing': False,
                'confidence': 0.0,
                'error': 'Empty text provided'
            }
        
        # Clean text
        text = text.strip()
        
        # Use transformer if available, otherwise fallback to keywords
        if self.is_loaded:
            result = self._transformer_prediction(text)
        else:
            result = self._keyword_based_prediction(text)
        
        # Add common fields
        result.update({
            'text_length': len(text),
            'word_count': len(text.split()),
            'risk_level': self._get_risk_level(result['confidence']),
            'timestamp': self._get_timestamp()
        })
        
        return result
    
    def batch_predict(self, texts: List[str]) -> List[Dict]:
        """Predict multiple texts at once"""
        return [self.predict_phishing(text) for text in texts]
    
    def _get_risk_level(self, confidence: float) -> str:
        """Convert confidence to risk level"""
        if confidence >= 0.8:
            return 'High'
        elif confidence >= 0.6:
            return 'Medium'
        elif confidence >= 0.3:
            return 'Low'
        else:
            return 'Very Low'
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        return {
            'model_name': self.model_name,
            'is_loaded': self.is_loaded,
            'method': 'transformer' if self.is_loaded else 'keyword_based',
            'keywords_count': len(self.phishing_keywords)
        }

# Global classifier instance
_classifier = None

def get_classifier() -> PhishingClassifier:
    """Get or create the global classifier instance"""
    global _classifier
    if _classifier is None:
        _classifier = PhishingClassifier()
    return _classifier

def predict_phishing(text: str) -> Dict:
    """
    Convenience function for phishing prediction
    
    Args:
        text (str): Email or SMS text to analyze
        
    Returns:
        Dict: {
            'is_phishing': bool,
            'confidence': float,
            'risk_level': str,
            'method': str,
            'suspicious_keywords': List[str] (if keyword-based),
            'negative_sentiment': float (if transformer-based),
            'positive_sentiment': float (if transformer-based)
        }
    """
    classifier = get_classifier()
    return classifier.predict_phishing(text)
