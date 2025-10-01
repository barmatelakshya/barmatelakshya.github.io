from flask import Flask, render_template_string, request, jsonify
import re
import json
from datetime import datetime

app = Flask(__name__)

# MVP Core Features Implementation
class ThreatDetector:
    def __init__(self):
        self.phishing_keywords = [
            'urgent', 'verify', 'suspended', 'click here', 'winner', 'congratulations',
            'limited time', 'act now', 'expires', 'claim', 'free money', 'lottery',
            'bank account', 'social security', 'password', 'login credentials'
        ]
        
    def analyze_text(self, text):
        """NLP-based phishing detection"""
        text_lower = text.lower()
        
        # Keyword analysis
        suspicious_count = sum(1 for keyword in self.phishing_keywords if keyword in text_lower)
        
        # Pattern analysis
        has_urgent_language = any(word in text_lower for word in ['urgent', 'immediate', 'asap'])
        has_financial_terms = any(word in text_lower for word in ['bank', 'account', 'payment', 'money'])
        has_action_words = any(word in text_lower for word in ['click', 'download', 'verify', 'update'])
        
        # Risk calculation
        risk_score = min(0.95, (suspicious_count * 0.15) + 
                        (0.2 if has_urgent_language else 0) +
                        (0.2 if has_financial_terms else 0) +
                        (0.15 if has_action_words else 0))
        
        return {
            'is_threat': risk_score > 0.5,
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'confidence': min(0.95, 0.6 + (suspicious_count * 0.08)),
            'detected_keywords': [kw for kw in self.phishing_keywords if kw in text_lower][:5],
            'analysis_time': datetime.now().strftime('%H:%M:%S')
        }
    
    def analyze_url(self, url):
        """URL threat analysis"""
        suspicious_domains = ['bit.ly', 'tinyurl', 'suspicious-site', 'phishing-test']
        suspicious_patterns = [r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', r'[a-z]+-[a-z]+-[a-z]+\.com']
        
        risk_factors = 0
        detected_issues = []
        
        # Check suspicious domains
        if any(domain in url.lower() for domain in suspicious_domains):
            risk_factors += 0.4
            detected_issues.append('Suspicious domain detected')
            
        # Check IP addresses
        if re.search(r'\d+\.\d+\.\d+\.\d+', url):
            risk_factors += 0.3
            detected_issues.append('IP address instead of domain')
            
        # Check suspicious patterns
        for pattern in suspicious_patterns:
            if re.search(pattern, url.lower()):
                risk_factors += 0.2
                detected_issues.append('Suspicious URL pattern')
                break
        
        risk_score = min(0.95, risk_factors)
        
        return {
            'is_threat': risk_score > 0.4,
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'confidence': 0.85,
            'detected_issues': detected_issues,
            'analysis_time': datetime.now().strftime('%H:%M:%S')
        }
    
    def _get_risk_level(self, score):
        if score >= 0.7: return 'High'
        elif score >= 0.4: return 'Medium'
        else: return 'Low'

# Initialize detector
detector = ThreatDetector()

# MVP Dashboard Template
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIH PS1 - Cybersecurity Threat Detector</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            color: #333;
        }
        .header {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 20px 0;
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .header p { opacity: 0.9; }
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
        .analyzer-card h3 {
            color: #2a5298;
            margin-bottom: 20px;
            font-size: 1.5rem;
        }
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
            background: linear-gradient(135deg, #2a5298, #1e3c72);
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
        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #2a5298;
        }
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
            <!-- Text Analyzer -->
            <div class="analyzer-card">
                <h3>📧 Text Threat Analysis</h3>
                <form id="textForm">
                    <textarea id="textInput" placeholder="Paste suspicious email, message, or text content here..."></textarea>
                    <button type="submit" class="analyze-btn" id="textBtn">🔍 Analyze Text</button>
                </form>
                <div id="textResults" class="results"></div>
            </div>

            <!-- URL Analyzer -->
            <div class="analyzer-card">
                <h3>🔗 URL Threat Analysis</h3>
                <form id="urlForm">
                    <input type="url" id="urlInput" placeholder="Enter suspicious URL here...">
                    <button type="submit" class="analyze-btn" id="urlBtn">🔍 Analyze URL</button>
                </form>
                <div id="urlResults" class="results"></div>
            </div>
        </div>
    </div>

    <script>
        // Text Analysis
        document.getElementById('textForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = document.getElementById('textInput').value.trim();
            if (!text) return alert('Please enter text to analyze');
            
            await analyzeContent('/api/analyze-text', { text }, 'textResults', 'textBtn');
        });

        // URL Analysis
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
                        <div class="metric-value">${result.analysis_time}</div>
                        <div>Analyzed</div>
                    </div>
                </div>
                <div>
                    <strong>Detected Issues:</strong>
                    <div class="keywords">
                        ${(result.detected_keywords || result.detected_issues || []).map(item => 
                            `<span class="keyword">${item}</span>`
                        ).join('')}
                    </div>
                </div>
            `;
            
            container.style.display = 'block';
        }
    </script>
</body>
</html>
'''

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
