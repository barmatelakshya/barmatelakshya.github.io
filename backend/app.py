from flask import Flask, render_template_string, request, jsonify
import re
import json
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models.threat_detector import ThreatDetector

app = Flask(__name__, 
           template_folder='../frontend/templates',
           static_folder='../frontend/static')

# Initialize detector
detector = ThreatDetector()

# Import dashboard template
from frontend.templates.dashboard import DASHBOARD_TEMPLATE

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    result = detector.analyze_text(text)
    return jsonify(result)

@app.route('/api/analyze-url', methods=['POST'])
def analyze_url():
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    result = detector.analyze_url(url)
    return jsonify(result)

@app.route('/api/status')
def status():
    return jsonify({
        'project': 'SIH PS1 - Cybersecurity Threat Detector',
        'status': 'MVP Ready',
        'features': ['NLP Text Analysis', 'URL Threat Detection', 'Real-time Dashboard'],
        'version': '1.0.0'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
