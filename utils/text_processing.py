"""
Text Processing Utilities
SIH PS1 - Cybersecurity Threat Detector
"""
import re
import string
from typing import List, Dict

class TextProcessor:
    """Text cleaning and preprocessing utilities"""
    
    def __init__(self):
        self.phishing_patterns = [
            r'urgent[ly]?',
            r'click\s+here',
            r'verify\s+now',
            r'act\s+now',
            r'limited\s+time',
            r'expires?\s+soon'
        ]
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\!\?\-]', '', text)
        
        return text.lower()
    
    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    def extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    def detect_urgency_words(self, text: str) -> List[str]:
        """Detect urgency-related words"""
        urgency_words = [
            'urgent', 'immediately', 'asap', 'now', 'quick', 'fast',
            'expires', 'deadline', 'limited', 'hurry', 'rush'
        ]
        
        found_words = []
        text_lower = text.lower()
        
        for word in urgency_words:
            if word in text_lower:
                found_words.append(word)
        
        return found_words
    
    def calculate_suspicious_score(self, text: str) -> float:
        """Calculate suspiciousness score based on patterns"""
        text_lower = text.lower()
        score = 0.0
        
        # Check for phishing patterns
        for pattern in self.phishing_patterns:
            if re.search(pattern, text_lower):
                score += 0.2
        
        # Check for urgency words
        urgency_count = len(self.detect_urgency_words(text))
        score += urgency_count * 0.1
        
        # Check for excessive punctuation
        punct_ratio = sum(1 for c in text if c in string.punctuation) / len(text)
        if punct_ratio > 0.1:
            score += 0.15
        
        return min(1.0, score)
    
    def extract_features(self, text: str) -> Dict:
        """Extract comprehensive text features"""
        cleaned_text = self.clean_text(text)
        
        return {
            'text_length': len(text),
            'word_count': len(text.split()),
            'urls': self.extract_urls(text),
            'emails': self.extract_emails(text),
            'urgency_words': self.detect_urgency_words(text),
            'suspicious_score': self.calculate_suspicious_score(text),
            'cleaned_text': cleaned_text
        }
