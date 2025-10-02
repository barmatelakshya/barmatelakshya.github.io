#!/usr/bin/env python3
"""
TrustEye Backend API
SIH PS1 - Cybersecurity Threat Detector
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

class TrustEyeDetector:
    def __init__(self):
        self.phishing_keywords = [
            'urgent', 'verify', 'suspended', 'click here', 'winner', 
            'congratulations', 'limited time', 'act now', 'expires', 
            'claim', 'free money', 'lottery', 'bank account', 
            'social security', 'password', 'login credentials'
        ]
        
        self.suspicious_domains = [
            'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly'
        ]
    
    def analyze_text(self, text):
        """Analyze text for phishing indicators"""
        if not text:
            return {'score': 0.0, 'indicators': []}
        
        text_lower = text.lower()
        found_keywords = [kw for kw in self.phishing_keywords if kw in text_lower]
        
        # Calculate text risk score
        keyword_score = min(0.8, len(found_keywords) * 0.15)
        
        # Check for urgency patterns
        urgency_patterns = ['urgent', 'immediate', 'asap', 'now', 'quickly']
        urgency_score = 0.2 if any(pattern in text_lower for pattern in urgency_patterns) else 0
        
        # Check for financial terms
        financial_terms = ['bank', 'account', 'payment', 'money', 'credit card']
        financial_score = 0.15 if any(term in text_lower for term in financial_terms) else 0
        
        total_score = min(0.95, keyword_score + urgency_score + financial_score)
        
        return {
            'score': total_score,
            'indicators': found_keywords,
            'has_urgency': urgency_score > 0,
            'has_financial': financial_score > 0
        }
    
    def analyze_url(self, url):
        """Analyze URL for suspicious patterns"""
        if not url:
            return {'score': 0.0, 'indicators': []}
        
        indicators = []
        score = 0.0
        
        # Check for IP address
        if re.search(r'\d+\.\d+\.\d+\.\d+', url):
            score += 0.4
            indicators.append('IP address detected')
        
        # Check for URL shorteners
        if any(domain in url.lower() for domain in self.suspicious_domains):
            score += 0.3
            indicators.append('URL shortener detected')
        
        # Check for suspicious keywords in URL
        suspicious_url_keywords = ['secure', 'verify', 'update', 'login', 'account']
        for keyword in suspicious_url_keywords:
            if keyword in url.lower():
                score += 0.1
                indicators.append(f'Suspicious keyword: {keyword}')
                break
        
        # Check for long URLs
        if len(url) > 100:
            score += 0.1
            indicators.append('Unusually long URL')
        
        # Check for excessive hyphens
        if url.count('-') > 3:
            score += 0.1
            indicators.append('Excessive hyphens')
        
        return {
            'score': min(0.95, score),
            'indicators': indicators
        }
    
    def combine_scores(self, text_result, url_result):
        """Combine text and URL analysis scores"""
        text_weight = 0.6
        url_weight = 0.4
        
        # Calculate weighted score
        combined_score = (text_result['score'] * text_weight) + (url_result['score'] * url_weight)
        
        # Apply bonus for multiple threat vectors
        if text_result['score'] > 0.5 and url_result['score'] > 0.3:
            combined_score += 0.15  # Bonus for multiple threats
        
        combined_score = min(0.95, combined_score)
        
        # Determine risk level
        if combined_score >= 0.8:
            risk_level = 'Critical'
        elif combined_score >= 0.6:
            risk_level = 'High'
        elif combined_score >= 0.4:
            risk_level = 'Medium'
        elif combined_score >= 0.2:
            risk_level = 'Low'
        else:
            risk_level = 'Very Low'
        
        # Combine indicators
        all_indicators = text_result['indicators'] + url_result['indicators']
        
        return {
            'combined_score': combined_score,
            'risk_level': risk_level,
            'is_threat': combined_score > 0.5,
            'confidence': 0.85,
            'text_score': text_result['score'],
            'url_score': url_result['score'],
            'threat_indicators': all_indicators,
            'analysis_timestamp': datetime.now().isoformat()
        }

# Initialize detector
detector = TrustEyeDetector()

@app.route('/api/analyze', methods=['POST'])
def analyze_threat():
    """
    Main API endpoint for threat analysis
    
    Request Body:
    {
        "text": "optional text content",
        "url": "optional URL to analyze"
    }
    
    Response:
    {
        "combined_score": 0.75,
        "risk_level": "High",
        "is_threat": true,
        "confidence": 0.85,
        "text_score": 0.8,
        "url_score": 0.6,
        "threat_indicators": ["urgent", "verify", "IP address detected"],
        "analysis_timestamp": "2025-10-02T09:55:00"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        text = data.get('text', '').strip()
        url = data.get('url', '').strip()
        
        if not text and not url:
            return jsonify({'error': 'Either text or URL must be provided'}), 400
        
        # Analyze text and URL
        text_result = detector.analyze_text(text)
        url_result = detector.analyze_url(url)
        
        # Combine results
        combined_result = detector.combine_scores(text_result, url_result)
        
        return jsonify(combined_result)
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    """
    Batch analysis endpoint
    
    Request Body:
    {
        "items": [
            {"text": "text1", "url": "url1"},
            {"text": "text2", "url": "url2"}
        ]
    }
    """
    try:
        data = request.get_json()
        items = data.get('items', [])
        
        if not items:
            return jsonify({'error': 'No items provided'}), 400
        
        results = []
        for item in items:
            text = item.get('text', '').strip()
            url = item.get('url', '').strip()
            
            if text or url:
                text_result = detector.analyze_text(text)
                url_result = detector.analyze_url(url)
                combined_result = detector.combine_scores(text_result, url_result)
                results.append(combined_result)
        
        return jsonify({'results': results, 'count': len(results)})
        
    except Exception as e:
        return jsonify({'error': f'Batch analysis failed: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'TrustEye API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/info', methods=['GET'])
def api_info():
    """API information endpoint"""
    return jsonify({
        'service': 'TrustEye Backend API',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/analyze': 'Analyze text and/or URL for threats',
            'POST /api/batch-analyze': 'Batch analysis of multiple items',
            'GET /api/health': 'Health check',
            'GET /api/info': 'API information'
        },
        'features': [
            'Text phishing detection',
            'URL threat analysis',
            'Combined risk scoring',
            'Batch processing'
        ]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting TrustEye Backend API...")
    print("📡 API Endpoints:")
    print("  POST /api/analyze - Main threat analysis")
    print("  POST /api/batch-analyze - Batch processing")
    print("  GET /api/health - Health check")
    print("  GET /api/info - API information")
    print("🌐 Access: http://localhost:5000")
    print("✨ Ready to detect threats!")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
