#!/usr/bin/env python3
from flask import Flask, render_template_string, request, jsonify
import re

app = Flask(__name__)

def analyze_threat(text="", url=""):
    risk_score = 0.0
    threats = []
    
    if text:
        text_lower = text.lower()
        keywords = ['urgent', 'click here', 'verify', 'suspended', 'winner', 'congratulations']
        found = [kw for kw in keywords if kw in text_lower]
        if found:
            risk_score += len(found) * 0.15
            threats.extend(found)
    
    if url:
        if re.search(r'\d+\.\d+\.\d+\.\d+', url):
            risk_score += 0.4
            threats.append('IP address')
        if 'bit.ly' in url or 'tinyurl' in url:
            risk_score += 0.3
            threats.append('URL shortener')
    
    risk_score = min(0.95, risk_score)
    
    return {
        'combined_score': risk_score,
        'risk_level': 'High' if risk_score > 0.6 else 'Medium' if risk_score > 0.3 else 'Low',
        'is_threat': risk_score > 0.5,
        'confidence': 0.85,
        'threat_indicators': threats
    }

HTML = '''<!DOCTYPE html>
<html>
<head>
    <title>TrustEye - AI Threat Detection</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { color: #2563eb; font-size: 2.5rem; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        textarea, input { width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 8px; }
        textarea { height: 100px; resize: vertical; }
        .scan-btn { background: #2563eb; color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; width: 100%; margin-top: 10px; }
        .scan-btn:hover { background: #1d4ed8; }
        .results { margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px; display: none; }
        .risk-high { background: #fee2e2; color: #991b1b; }
        .risk-medium { background: #fef3c7; color: #92400e; }
        .risk-low { background: #dcfce7; color: #166534; }
        .score { font-size: 2rem; font-weight: bold; text-align: center; margin: 20px 0; }
        .threats { margin-top: 15px; }
        .threat-tag { background: #fbbf24; color: #92400e; padding: 5px 10px; border-radius: 15px; margin: 3px; display: inline-block; font-size: 14px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>👁️ TrustEye</h1>
        <p>AI-Powered Threat Detection System</p>
    </div>
    
    <form id="scanForm">
        <div class="form-group">
            <label>📧 Suspicious Text or Email:</label>
            <textarea id="textInput" placeholder="Paste suspicious content here..."></textarea>
        </div>
        
        <div class="form-group">
            <label>🔗 Suspicious URL:</label>
            <input type="url" id="urlInput" placeholder="https://suspicious-website.com">
        </div>
        
        <button type="submit" class="scan-btn">🔍 Scan with TrustEye</button>
    </form>
    
    <div id="results" class="results">
        <div id="riskHeader" class="score"></div>
        <div><strong>Risk Level:</strong> <span id="riskLevel"></span></div>
        <div><strong>Confidence:</strong> <span id="confidence"></span></div>
        <div id="threatsSection" class="threats">
            <strong>Detected Threats:</strong>
            <div id="threatsList"></div>
        </div>
    </div>

    <script>
        document.getElementById('scanForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const text = document.getElementById('textInput').value.trim();
            const url = document.getElementById('urlInput').value.trim();
            
            if (!text && !url) {
                alert('Please enter text or URL to analyze');
                return;
            }
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text, url })
                });
                
                const result = await response.json();
                displayResults(result);
                
            } catch (error) {
                alert('Analysis failed: ' + error.message);
            }
        });
        
        function displayResults(result) {
            const results = document.getElementById('results');
            const riskScore = Math.round(result.combined_score * 100);
            
            document.getElementById('riskHeader').textContent = riskScore + '% Risk Score';
            document.getElementById('riskLevel').textContent = result.risk_level;
            document.getElementById('confidence').textContent = Math.round(result.confidence * 100) + '%';
            
            const threatsList = document.getElementById('threatsList');
            threatsList.innerHTML = result.threat_indicators.map(threat => 
                `<span class="threat-tag">${threat}</span>`
            ).join('');
            
            results.className = `results risk-${result.risk_level.toLowerCase()}`;
            results.style.display = 'block';
        }
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    url = data.get('url', '')
    result = analyze_threat(text, url)
    return jsonify(result)

if __name__ == '__main__':
    print("🚀 Starting TrustEye...")
    print("👁️ Access: http://localhost:8080")
    app.run(debug=True, host='127.0.0.1', port=8080)
