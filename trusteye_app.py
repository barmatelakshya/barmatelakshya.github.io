#!/usr/bin/env python3
from flask import Flask, render_template_string, request, jsonify
import re
from datetime import datetime

app = Flask(__name__)

def analyze_threat(text="", url=""):
    """Simple threat analysis"""
    risk_score = 0.0
    threats = []
    
    # Text analysis
    if text:
        text_lower = text.lower()
        phishing_words = ['urgent', 'click here', 'verify', 'suspended', 'winner', 'congratulations', 'act now']
        found_words = [word for word in phishing_words if word in text_lower]
        
        if found_words:
            risk_score += len(found_words) * 0.15
            threats.extend(found_words)
    
    # URL analysis
    if url:
        if re.search(r'\d+\.\d+\.\d+\.\d+', url):
            risk_score += 0.4
            threats.append('IP address detected')
        if any(domain in url.lower() for domain in ['bit.ly', 'tinyurl']):
            risk_score += 0.3
            threats.append('URL shortener detected')
    
    risk_score = min(0.95, risk_score)
    
    if risk_score >= 0.7:
        risk_level = 'High'
    elif risk_score >= 0.4:
        risk_level = 'Medium'
    else:
        risk_level = 'Low'
    
    return {
        'risk_score': risk_score,
        'risk_level': risk_level,
        'is_threat': risk_score > 0.5,
        'threats': threats,
        'confidence': 0.85
    }

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrustEye - AI Threat Detection</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .header {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 40px 0;
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .header h1 { font-size: 3rem; margin-bottom: 15px; }
        .header p { opacity: 0.9; font-size: 1.2rem; }
        .container { max-width: 800px; margin: 0 auto; padding: 0 20px; }
        .analyzer-card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .input-group { margin-bottom: 25px; }
        .input-group h4 { color: #333; margin-bottom: 15px; font-size: 1.2rem; }
        textarea, input[type="url"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 16px;
            margin-bottom: 15px;
        }
        textarea { min-height: 100px; resize: vertical; }
        .analyze-btn {
            width: 100%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 18px;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .analyze-btn:hover { transform: translateY(-2px); }
        .analyze-btn:disabled { opacity: 0.7; cursor: not-allowed; }
        .results {
            margin-top: 30px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 15px;
            display: none;
        }
        .result-header {
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-weight: 600;
            font-size: 1.2rem;
        }
        .high { background: #f8d7da; color: #721c24; }
        .medium { background: #fff3cd; color: #856404; }
        .low { background: #d4edda; color: #155724; }
        .metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        .metric {
            text-align: center;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .metric-value { font-size: 1.8rem; font-weight: bold; color: #667eea; }
        .threats {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 15px;
        }
        .threat-item {
            background: #fff3cd;
            color: #856404;
            padding: 8px 15px;
            margin: 5px;
            border-radius: 15px;
            display: inline-block;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>👁️ TrustEye</h1>
            <p>AI-Powered Threat Detection System</p>
        </div>
    </div>

    <div class="container">
        <div class="analyzer-card">
            <form id="analyzeForm">
                <div class="input-group">
                    <h4>📧 Text Analysis</h4>
                    <textarea id="textInput" placeholder="Paste suspicious email or message here..."></textarea>
                </div>
                
                <div class="input-group">
                    <h4>🔗 URL Analysis</h4>
                    <input type="url" id="urlInput" placeholder="Enter suspicious URL here...">
                </div>
                
                <button type="submit" class="analyze-btn" id="analyzeBtn">
                    👁️ Analyze with TrustEye
                </button>
            </form>
            
            <div id="results" class="results"></div>
        </div>
    </div>

    <script>
        document.getElementById('analyzeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const text = document.getElementById('textInput').value.trim();
            const url = document.getElementById('urlInput').value.trim();
            
            if (!text && !url) {
                alert('Please enter text or URL to analyze');
                return;
            }

            const resultsDiv = document.getElementById('results');
            const analyzeBtn = document.getElementById('analyzeBtn');
            
            analyzeBtn.disabled = true;
            analyzeBtn.textContent = '🔄 TrustEye Analyzing...';
            resultsDiv.style.display = 'none';

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text, url: url })
                });
                
                const result = await response.json();
                displayResults(result, resultsDiv);
                
            } catch (error) {
                alert('Analysis failed: ' + error.message);
            } finally {
                analyzeBtn.disabled = false;
                analyzeBtn.textContent = '👁️ Analyze with TrustEye';
            }
        });

        function displayResults(result, container) {
            const riskScore = Math.round(result.risk_score * 100);
            const riskLevel = result.risk_level.toLowerCase();
            
            let headerText, headerClass;
            if (result.is_threat) {
                headerText = '⚠️ THREAT DETECTED';
                headerClass = riskLevel === 'high' ? 'high' : 'medium';
            } else {
                headerText = '✅ APPEARS SAFE';
                headerClass = 'low';
            }
            
            container.innerHTML = `
                <div class="result-header ${headerClass}">${headerText}</div>
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">${riskScore}%</div>
                        <div>Risk Score</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${result.risk_level}</div>
                        <div>Risk Level</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${Math.round(result.confidence * 100)}%</div>
                        <div>Confidence</div>
                    </div>
                </div>
                ${result.threats.length > 0 ? `
                    <div class="threats">
                        <h4>Detected Threats:</h4>
                        ${result.threats.map(threat => `<span class="threat-item">${threat}</span>`).join('')}
                    </div>
                ` : ''}
            `;
            
            container.style.display = 'block';
        }
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    url = data.get('url', '')
    
    result = analyze_threat(text, url)
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'TrustEye is running!'})

if __name__ == '__main__':
    print("🚀 Starting TrustEye - AI Threat Detection System...")
    print("👁️ Access: http://localhost:8080")
    app.run(debug=True, host='127.0.0.1', port=8080)
