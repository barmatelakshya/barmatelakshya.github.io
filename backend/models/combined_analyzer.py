"""
Combined Threat Analyzer
SIH PS1 - Cybersecurity Threat Detector
"""
import sys
from pathlib import Path
from typing import Dict, Optional, List
import re
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from backend.models.nlp_classifier import predict_phishing
from backend.models.url_analyzer import analyze_url

class CombinedThreatAnalyzer:
    def __init__(self):
        self.weights = {
            'text_weight': 0.6,    # Text analysis weight
            'url_weight': 0.4,     # URL analysis weight
            'combined_bonus': 0.2  # Bonus for multiple threats
        }
    
    def analyze_input(self, text: str = "", url: str = "") -> Dict:
        """
        Combined analysis of text and URL
        
        Args:
            text (str): Email/SMS text content
            url (str): URL to analyze
            
        Returns:
            Dict: Combined threat analysis results
        """
        if not text and not url:
            return {
                'error': 'No text or URL provided',
                'risk_score': 0.0,
                'risk_level': 'Unknown'
            }
        
        results = {
            'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'input_types': [],
            'individual_results': {},
            'combined_score': 0.0,
            'risk_level': 'Low',
            'confidence': 0.0,
            'threat_indicators': [],
            'recommendations': []
        }
        
        text_result = None
        url_result = None
        
        # Analyze text if provided
        if text and text.strip():
            results['input_types'].append('text')
            text_result = predict_phishing(text.strip())
            results['individual_results']['text'] = text_result
            
            # Extract URLs from text for additional analysis
            extracted_urls = self._extract_urls_from_text(text)
            if extracted_urls and not url:
                url = extracted_urls[0]  # Use first extracted URL
                results['extracted_urls'] = extracted_urls
        
        # Analyze URL if provided
        if url and url.strip():
            results['input_types'].append('url')
            url_result = analyze_url(url.strip())
            results['individual_results']['url'] = url_result
        
        # Combine results
        combined_analysis = self._combine_results(text_result, url_result)
        results.update(combined_analysis)
        
        return results
    
    def _extract_urls_from_text(self, text: str) -> List[str]:
        """Extract URLs from text content"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    def _combine_results(self, text_result: Optional[Dict], url_result: Optional[Dict]) -> Dict:
        """Combine text and URL analysis results"""
        combined_score = 0.0
        threat_indicators = []
        recommendations = []
        confidence_scores = []
        
        # Process text results
        if text_result:
            text_score = text_result.get('confidence', 0.0)
            if text_result.get('is_phishing', False):
                text_score = max(text_score, 0.7)  # Minimum score for detected phishing
            
            combined_score += text_score * self.weights['text_weight']
            confidence_scores.append(text_result.get('confidence', 0.0))
            
            if text_result.get('is_phishing', False):
                threat_indicators.append('Phishing text patterns detected')
                recommendations.append('Text contains suspicious phishing indicators')
            
            # Add specific text indicators
            if 'suspicious_keywords' in text_result:
                for keyword in text_result['suspicious_keywords'][:3]:
                    threat_indicators.append(f'Suspicious keyword: {keyword}')
        
        # Process URL results
        if url_result and not url_result.get('error'):
            url_score = url_result.get('risk_score', 0.0)
            combined_score += url_score * self.weights['url_weight']
            confidence_scores.append(url_result.get('confidence', 0.0))
            
            if url_result.get('risk_level') in ['High', 'Medium']:
                threat_indicators.append('Suspicious URL detected')
                recommendations.append(url_result.get('recommendation', 'URL requires caution'))
            
            # Add specific URL indicators
            if 'risk_factors' in url_result:
                for factor in url_result['risk_factors'][:3]:
                    threat_indicators.append(f'URL risk: {factor}')
        
        # Apply combined threat bonus
        if text_result and url_result and not url_result.get('error'):
            if (text_result.get('is_phishing', False) and 
                url_result.get('risk_score', 0) > 0.4):
                combined_score += self.weights['combined_bonus']
                threat_indicators.append('Multiple threat vectors detected')
                recommendations.append('CRITICAL: Both text and URL show suspicious patterns')
        
        # Normalize combined score
        combined_score = min(1.0, max(0.0, combined_score))
        
        # Calculate overall confidence
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        # Determine risk level
        risk_level = self._calculate_risk_level(combined_score)
        
        # Generate final recommendation
        final_recommendation = self._generate_final_recommendation(combined_score, risk_level)
        
        return {
            'combined_score': combined_score,
            'risk_level': risk_level,
            'confidence': overall_confidence,
            'threat_indicators': threat_indicators,
            'recommendations': recommendations,
            'final_recommendation': final_recommendation,
            'is_threat': combined_score > 0.5
        }
    
    def _calculate_risk_level(self, score: float) -> str:
        """Calculate risk level from combined score"""
        if score >= 0.8:
            return 'Critical'
        elif score >= 0.6:
            return 'High'
        elif score >= 0.4:
            return 'Medium'
        elif score >= 0.2:
            return 'Low'
        else:
            return 'Very Low'
    
    def _generate_final_recommendation(self, score: float, risk_level: str) -> str:
        """Generate final recommendation based on risk level"""
        recommendations = {
            'Critical': '🚨 IMMEDIATE ACTION REQUIRED - Do not interact with this content. Report as phishing.',
            'High': '⚠️ HIGH RISK - Avoid interaction. Verify through official channels if legitimate.',
            'Medium': '⚡ CAUTION ADVISED - Exercise extreme caution. Verify authenticity before proceeding.',
            'Low': '✅ GENERALLY SAFE - Content appears legitimate but remain vigilant.',
            'Very Low': '✅ SAFE - No significant threats detected.'
        }
        return recommendations.get(risk_level, 'Analysis complete.')
    
    def batch_analyze(self, inputs: List[Dict]) -> List[Dict]:
        """Analyze multiple inputs at once"""
        results = []
        for input_data in inputs:
            text = input_data.get('text', '')
            url = input_data.get('url', '')
            result = self.analyze_input(text, url)
            results.append(result)
        return results
    
    def get_analyzer_info(self) -> Dict:
        """Get information about the combined analyzer"""
        return {
            'version': '1.0.0',
            'components': ['NLP Classifier', 'URL Analyzer'],
            'weights': self.weights,
            'supported_inputs': ['text', 'url', 'combined'],
            'risk_levels': ['Very Low', 'Low', 'Medium', 'High', 'Critical']
        }

# Global analyzer instance
_combined_analyzer = None

def get_combined_analyzer() -> CombinedThreatAnalyzer:
    """Get or create the global combined analyzer instance"""
    global _combined_analyzer
    if _combined_analyzer is None:
        _combined_analyzer = CombinedThreatAnalyzer()
    return _combined_analyzer

def analyze_input(text: str = "", url: str = "") -> Dict:
    """
    Convenience function for combined threat analysis
    
    Args:
        text (str): Email/SMS text content
        url (str): URL to analyze
        
    Returns:
        Dict: {
            'combined_score': float,           # Final risk score (0.0-1.0)
            'risk_level': str,                # Critical/High/Medium/Low/Very Low
            'confidence': float,              # Analysis confidence (0.0-1.0)
            'is_threat': bool,                # True if threat detected
            'threat_indicators': List[str],   # List of detected threats
            'recommendations': List[str],     # Specific recommendations
            'final_recommendation': str,      # Overall recommendation
            'individual_results': Dict,       # Detailed results from each analyzer
            'input_types': List[str],         # Types of input analyzed
            'analysis_timestamp': str         # When analysis was performed
        }
    """
    analyzer = get_combined_analyzer()
    return analyzer.analyze_input(text, url)
