#!/usr/bin/env python3
from flask import Flask, render_template_string, request, jsonify
import re
from datetime import datetime

app = Flask(__name__)

# Simple threat detection
def analyze_text_threat(text):
    keywords = ['urgent', 'click here', 'verify', 'suspended', 'winner', 'congratulations', 'act now', 'expires', 'claim', 'free money']
    text_lower = text.lower()
    
    suspicious_count = sum(1 for keyword in keywords if keyword in text_lower)
    risk_score = min(0.95, suspicious_count * 0.2)
    
    return {
        'is_threat': risk_score > 0.4,
        'risk_score': risk_score,
        'risk_level': 'High' if risk_score > 0.7 else 'Medium' if risk_score > 0.4 else 'Low',
        'confidence': 0.85,
        'detected_keywords': [kw for kw in keywords if kw in text_lower][:5]
    }

def analyze_url_threat(url):
    risk_factors = 0
    issues = []
    
    # IP address check
    if re.search(r'\d+\.\d+\.\d+\.\d+', url):
        risk_factors += 0.4
        issues.append('IP address detected')
    
    # Suspicious domains
    if any(domain in url.lower() for domain in ['bit.ly', 'tinyurl', 'suspicious']):
        risk_factors += 0.3
        issues.append('Suspicious domain')
    
    return {
        'is_threat': risk_factors > 0.3,
        'risk_score': min(0.95, risk_factors),
        'risk_level': 'High' if risk_factors > 0.6 else 'Medium' if risk_factors > 0.3 else 'Low',
        'confidence': 0.80,
        'issues': issues
    }

# Complete HTML page
HTML_PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIH PS1 - Cybersecurity Threat Detector</title>
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
            padding: 30px 0;
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        .analyzer-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        .analyzer-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .analyzer-card h3 { color: #667eea; margin-bottom: 20px; font-size: 1.5rem; }
        textarea, input[type="url"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 15px;
            resize: vertical;
        }
        textarea { min-height: 120px; }
        .analyze-btn {
            width: 100%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .analyze-btn:hover { transform: translateY(-2px); }
        .analyze-btn:disabled { opacity: 0.7; cursor: not-allowed; }
        .results {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            display: none;
        }
        .result-header {
            text-align: center;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-weight: 600;
        }
        .safe { background: #d4edda; color: #155724; }
        .warning { background: #fff3cd; color: #856404; }
        .danger { background: #f8d7da; color: #721c24; }
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }
        .metric {
            text-align: center;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .metric-value { font-size: 1.5rem; font-weight: bold; color: #667eea; }
        .keywords {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }
        .keyword {
            background: #fff3cd;
            color: #856404;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 14px;
        }
        .samples {
            margin-bottom: 15px;
        }
        .sample-btn {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 8px 15px;
            margin: 5px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        .sample-btn:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        @media (max-width: 768px) {
            .analyzer-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>🛡️ Cybersecurity Threat Detector</h1>
            <p>SIH PS1 - Advanced NLP & URL Analysis System</p>
        </div>
    </div>

    <div class="container">
        <div class="analyzer-grid">
            <div class="analyzer-card">
                <h3>📧 Text Threat Analysis</h3>
                <div class="samples">
                    <button class="sample-btn" onclick="loadTextSample(1)">🚨 Phishing Email</button>
                    <button class="sample-btn" onclick="loadTextSample(2)">✅ Safe Email</button>
                </div>
                <form id="textForm">
                    <textarea id="textInput" placeholder="Paste suspicious email, message, or text content here..."></textarea>
                    <button type="submit" class="analyze-btn" id="textBtn">🔍 Analyze Text</button>
                </form>
                <div id="textResults" class="results"></div>
            </div>

            <div class="analyzer-card">
                <h3>🔗 URL Threat Analysis</h3>
                <div class="samples">
                    <button class="sample-btn" onclick="loadUrlSample(1)">🚨 Suspicious URL</button>
                    <button class="sample-btn" onclick="loadUrlSample(2)">✅ Safe URL</button>
                </div>
                <form id="urlForm">
                    <input type="url" id="urlInput" placeholder="Enter suspicious URL here...">
                    <button type="submit" class="analyze-btn" id="urlBtn">🔍 Analyze URL</button>
                </form>
                <div id="urlResults" class="results"></div>
            </div>
        </div>
    </div>

    <script>
        const textSamples = {
            1: "URGENT SECURITY ALERT! Your account will be suspended in 24 hours due to suspicious activity. Click here immediately to verify your identity and avoid account closure.",
            2: "Thank you for your recent purchase from Amazon. Your order has been shipped and will arrive within 2-3 business days. Track your package using the link in your account."
        };

        const urlSamples = {
            1: "http://192.168.1.100/urgent-bank-verify/login.php",
            2: "https://amazon.com/your-orders"
        };

        function loadTextSample(id) {
            document.getElementById('textInput').value = textSamples[id];
        }

        function loadUrlSample(id) {
            document.getElementById('urlInput').value = urlSamples[id];
        }

        document.getElementById('textForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = document.getElementById('textInput').value.trim();
            if (!text) return alert('Please enter text to analyze');
            await analyzeContent('/api/analyze-text', { text }, 'textResults', 'textBtn');
        });

        document.getElementById('urlForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const url = document.getElementById('urlInput').value.trim();
            if (!url) return alert('Please enter URL to analyze');
            await analyzeContent('/api/analyze-url', { url }, 'urlResults', 'urlBtn');
        });

        async function analyzeContent(endpoint, data, resultsId, btnId) {
            const resultsDiv = document.getElementById(resultsId);
            const btn = document.getElementById(btnId);
            
            btn.disabled = true;
            btn.textContent = '🔄 Analyzing...';
            resultsDiv.style.display = 'none';

            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                displayResults(result, resultsDiv);
                
            } catch (error) {
                alert('Analysis failed: ' + error.message);
            } finally {
                btn.disabled = false;
                btn.textContent = btn.id === 'textBtn' ? '🔍 Analyze Text' : '🔍 Analyze URL';
            }
        }

        function displayResults(result, container) {
            const riskScore = Math.round(result.risk_score * 100);
            const headerClass = result.is_threat ? 'danger' : (riskScore > 30 ? 'warning' : 'safe');
            const headerText = result.is_threat ? '⚠️ THREAT DETECTED' : (riskScore > 30 ? '⚡ SUSPICIOUS' : '✅ SAFE');
            
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
                    <div class="metric">
                        <div class="metric-value">${new Date().toLocaleTimeString()}</div>
                        <div>Analyzed</div>
                    </div>
                </div>
                <div>
                    <strong>Detected Issues:</strong>
                    <div class="keywords">
                        ${(result.detected_keywords || result.issues || []).map(item => 
                            `<span class="keyword">${item}</span>`
                        ).join('') || '<span class="keyword">None detected</span>'}
                    </div>
                </div>
            `;
            
            container.style.display = 'block';
        }
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    result = analyze_text_threat(text)
    return jsonify(result)

@app.route('/api/analyze-url', methods=['POST'])
def analyze_url():
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    result = analyze_url_threat(url)
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'SIH PS1 Threat Detector is running!'})

if __name__ == '__main__':
    print("🚀 Starting SIH PS1 Cybersecurity Threat Detector...")
    print("📱 Access: http://localhost:8080")
    print("✅ Single localhost application ready!")
    app.run(debug=True, host='127.0.0.1', port=8080)
