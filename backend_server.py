#!/usr/bin/env python3
"""
TrustEye Backend API Server
Flask backend with CORS support for frontend integration
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

class TrustEyeEngine:
    def __init__(self):
        self.phishing_keywords = [
            'urgent', 'verify', 'suspended', 'click here', 'winner', 
            'congratulations', 'limited time', 'act now', 'expires', 
            'claim', 'free money', 'lottery', 'bank account', 
            'social security', 'password', 'login credentials',
            'update payment', 'confirm identity', 'security alert'
        ]
        
        self.suspicious_domains = [
            'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly',
            'short.link', 'tiny.cc', 'is.gd'
        ]
    
    def analyze_text(self, text):
        """Analyze text for phishing patterns"""
        if not text:
            return {'score': 0.0, 'indicators': []}
        
        text_lower = text.lower()
        found_keywords = [kw for kw in self.phishing_keywords if kw in text_lower]
        
        # Calculate scores
        keyword_score = min(0.7, len(found_keywords) * 0.12)
        urgency_score = 0.2 if any(word in text_lower for word in ['urgent', 'immediate', 'now']) else 0
        financial_score = 0.15 if any(word in text_lower for word in ['bank', 'account', 'payment']) else 0
        
        total_score = min(0.95, keyword_score + urgency_score + financial_score)
        
        return {
            'score': total_score,
            'indicators': found_keywords[:5]  # Limit to 5 indicators
        }
    
    def analyze_url(self, url):
        """Analyze URL for suspicious patterns"""
        if not url:
            return {'score': 0.0, 'indicators': []}
        
        indicators = []
        score = 0.0
        
        # IP address check
        if re.search(r'\d+\.\d+\.\d+\.\d+', url):
            score += 0.4
            indicators.append('IP address detected')
        
        # URL shortener check
        if any(domain in url.lower() for domain in self.suspicious_domains):
            score += 0.3
            indicators.append('URL shortener')
        
        # Suspicious keywords in URL
        if any(keyword in url.lower() for keyword in ['secure', 'verify', 'update', 'login']):
            score += 0.15
            indicators.append('Suspicious URL keywords')
        
        # Long URL
        if len(url) > 100:
            score += 0.1
            indicators.append('Unusually long URL')
        
        # Excessive hyphens
        if url.count('-') > 3:
            score += 0.1
            indicators.append('Excessive hyphens')
        
        return {
            'score': min(0.95, score),
            'indicators': indicators
        }
    
    def combine_analysis(self, text_result, url_result):
        """Combine text and URL analysis"""
        # Weighted combination
        text_weight = 0.6
        url_weight = 0.4
        
        combined_score = (text_result['score'] * text_weight) + (url_result['score'] * url_weight)
        
        # Bonus for multiple threats
        if text_result['score'] > 0.5 and url_result['score'] > 0.3:
            combined_score += 0.15
        
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

# Initialize engine
engine = TrustEyeEngine()

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Main analysis endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        text = data.get('text', '').strip()
        url = data.get('url', '').strip()
        
        if not text and not url:
            return jsonify({'error': 'Either text or URL must be provided'}), 400
        
        # Perform analysis
        text_result = engine.analyze_text(text)
        url_result = engine.analyze_url(url)
        combined_result = engine.combine_analysis(text_result, url_result)
        
        return jsonify(combined_result)
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'TrustEye API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/info', methods=['GET'])
def info():
    """API information"""
    return jsonify({
        'service': 'TrustEye Backend API',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/analyze': 'Analyze text and/or URL for threats',
            'GET /api/health': 'Health check',
            'GET /api/info': 'API information'
        }
    })

# Serve frontend files
@app.route('/')
def serve_frontend():
    """Serve the main frontend page"""
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static frontend files"""
    return send_from_directory('frontend', filename)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting TrustEye Backend Server...")
    print("📡 API Endpoints:")
    print("  POST /api/analyze - Main threat analysis")
    print("  GET /api/health - Health check")
    print("  GET /api/info - API information")
    print("🌐 Frontend: http://localhost:5000")
    print("📱 API Base: http://localhost:5000/api")
    print("✨ Ready for connections!")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
