#!/usr/bin/env python3
"""
Complete Flask App with Combined Threat Analyzer
SIH PS1 - Cybersecurity Threat Detector
"""
from flask import Flask, render_template_string, request, jsonify
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from backend.models.combined_analyzer import analyze_input, get_combined_analyzer

app = Flask(__name__)

# Initialize combined analyzer
analyzer = get_combined_analyzer()

# Complete HTML Template
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
            padding: 30px 0;
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .header h1 { font-size: 2.8rem; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 1.2rem; margin-bottom: 15px; }
        .features {
            background: rgba(255,255,255,0.2);
            padding: 15px 25px;
            border-radius: 25px;
            display: inline-block;
            font-size: 0.95rem;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        .analyzer-card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .analyzer-card h3 { 
            color: #667eea; 
            margin-bottom: 30px; 
            font-size: 2rem; 
            text-align: center;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .input-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        .input-group h4 { 
            color: #333; 
            margin-bottom: 15px; 
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        textarea, .url-input {
            width: 100%;
            padding: 20px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            font-size: 16px;
            margin-bottom: 15px;
            transition: all 0.3s;
        }
        textarea {
            min-height: 120px;
            resize: vertical;
            font-family: inherit;
        }
        .url-input {
            font-family: 'Courier New', monospace;
        }
        textarea:focus, .url-input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }
        .samples {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }
        .sample-btn {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 8px 12px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.3s;
        }
        .sample-btn:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        .analyze-btn {
            width: 100%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 20px;
            border-radius: 15px;
            font-size: 20px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
            margin-top: 20px;
        }
        .analyze-btn:hover { transform: translateY(-3px); }
        .analyze-btn:disabled { opacity: 0.7; cursor: not-allowed; transform: none; }
        .results {
            margin-top: 30px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 20px;
            display: none;
        }
        .result-header {
            text-align: center;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 25px;
            font-weight: 600;
            font-size: 1.4rem;
        }
        .critical { background: #dc3545; color: white; }
        .high { background: #fd7e14; color: white; }
        .medium { background: #ffc107; color: #212529; }
        .low { background: #28a745; color: white; }
        .very-low { background: #6c757d; color: white; }
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }
        .metric {
            text-align: center;
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .metric-value { 
            font-size: 2.2rem; 
            font-weight: bold; 
            color: #667eea; 
            margin-bottom: 8px; 
        }
        .metric-label { font-size: 1rem; color: #666; }
        .details {
            background: white;
            padding: 25px;
            border-radius: 15px;
            margin-top: 20px;
        }
        .details h4 { color: #333; margin-bottom: 15px; font-size: 1.2rem; }
        .threat-indicators {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }
        .threat-indicator {
            background: #fff3cd;
            color: #856404;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            border-left: 4px solid #ffc107;
        }
        .recommendation {
            background: #e8f5e8;
            border: 2px solid #28a745;
            padding: 20px;
            border-radius: 15px;
            margin-top: 20px;
            font-weight: 600;
            text-align: center;
            font-size: 1.1rem;
        }
        .recommendation.critical {
            background: #f8d7da;
            border-color: #dc3545;
            color: #721c24;
        }
        .recommendation.high {
            background: #fff3cd;
            border-color: #fd7e14;
            color: #856404;
        }
        .recommendation.medium {
            background: #fff3cd;
            border-color: #ffc107;
            color: #856404;
        }
        .individual-results {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }
        .individual-result {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }
        @media (max-width: 768px) {
            .input-section { grid-template-columns: 1fr; }
            .individual-results { grid-template-columns: 1fr; }
            .metrics { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>👁️ TrustEye</h1>
            <p>SIH PS1 - Advanced Combined NLP & URL Analysis</p>
            <div class="features">
                🤖 AI Text Analysis • 🔗 URL Security • 🔥 Combined Intelligence • ⚡ Real-time Detection
            </div>
        </div>
    </div>

    <div class="container">
        <div class="analyzer-card">
            <h3>👁️ TrustEye Intelligence</h3>
            
            <form id="analyzeForm">
                <div class="input-section">
                    <div class="input-group">
                        <h4>📧 Text Analysis</h4>
                        <div class="samples">
                            <button type="button" class="sample-btn" onclick="loadTextSample(1)">🚨 Phishing</button>
                            <button type="button" class="sample-btn" onclick="loadTextSample(2)">💰 Lottery</button>
                            <button type="button" class="sample-btn" onclick="loadTextSample(3)">✅ Safe</button>
                        </div>
                        <textarea id="textInput" placeholder="Paste email content, SMS message, or any suspicious text here..."></textarea>
                    </div>
                    
                    <div class="input-group">
                        <h4>🔗 URL Analysis</h4>
                        <div class="samples">
                            <button type="button" class="sample-btn" onclick="loadUrlSample(1)">🚨 IP Address</button>
                            <button type="button" class="sample-btn" onclick="loadUrlSample(2)">🔗 Shortener</button>
                            <button type="button" class="sample-btn" onclick="loadUrlSample(3)">✅ Safe</button>
                        </div>
                        <input type="url" id="urlInput" class="url-input" placeholder="Enter suspicious URL here (optional)...">
                    </div>
                </div>
                
                <button type="submit" class="analyze-btn" id="analyzeBtn">
                    👁️ Analyze with TrustEye
                </button>
            </form>
            
            <div id="results" class="results"></div>
        </div>
    </div>

    <script>
        const textSamples = {
            1: "URGENT SECURITY ALERT! Your account will be suspended in 24 hours due to suspicious activity. Click here immediately to verify your identity and avoid account closure.",
            2: "Congratulations! You've won $1,000,000 in our international lottery! Claim your prize now by clicking this link and providing your bank details.",
            3: "Thank you for your recent purchase from Amazon. Your order has been shipped and will arrive within 2-3 business days."
        };

        const urlSamples = {
            1: "http://192.168.1.100/urgent-bank-verify/login.php",
            2: "http://bit.ly/urgent-security-update",
            3: "https://amazon.com/your-orders"
        };

        function loadTextSample(id) {
            document.getElementById('textInput').value = textSamples[id];
        }

        function loadUrlSample(id) {
            document.getElementById('urlInput').value = urlSamples[id];
        }

        document.getElementById('analyzeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const text = document.getElementById('textInput').value.trim();
            const url = document.getElementById('urlInput').value.trim();
            
            if (!text && !url) {
                alert('Please enter text and/or URL to analyze');
                return;
            }

            const resultsDiv = document.getElementById('results');
            const analyzeBtn = document.getElementById('analyzeBtn');
            
            // Show loading state
            analyzeBtn.disabled = true;
            analyzeBtn.textContent = '🔄 TrustEye Analyzing...';
            resultsDiv.style.display = 'none';

            try {
                const response = await fetch('/api/analyze-combined', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text, url: url })
                });
                
                const result = await response.json();
                
                if (result.error) {
                    alert('Analysis failed: ' + result.error);
                    return;
                }
                
                displayResults(result, resultsDiv);
                
            } catch (error) {
                alert('Analysis failed: ' + error.message);
            } finally {
                analyzeBtn.disabled = false;
                analyzeBtn.textContent = '👁️ Analyze with TrustEye';
            }
        });

        function displayResults(result, container) {
            const combinedScore = Math.round(result.combined_score * 100);
            const riskLevel = result.risk_level.toLowerCase().replace(' ', '-');
            const confidence = Math.round(result.confidence * 100);
            
            let headerClass, headerText;
            switch(result.risk_level) {
                case 'Critical':
                    headerClass = 'critical';
                    headerText = '🚨 CRITICAL THREAT DETECTED';
                    break;
                case 'High':
                    headerClass = 'high';
                    headerText = '⚠️ HIGH RISK DETECTED';
                    break;
                case 'Medium':
                    headerClass = 'medium';
                    headerText = '⚡ MEDIUM RISK DETECTED';
                    break;
                case 'Low':
                    headerClass = 'low';
                    headerText = '✅ LOW RISK DETECTED';
                    break;
                default:
                    headerClass = 'very-low';
                    headerText = '✅ VERY LOW RISK';
            }
            
            // Threat indicators
            let indicatorsHtml = '';
            if (result.threat_indicators && result.threat_indicators.length > 0) {
                indicatorsHtml = `
                    <div class="details">
                        <h4>⚠️ Threat Indicators (${result.threat_indicators.length})</h4>
                        <div class="threat-indicators">
                            ${result.threat_indicators.map(indicator => 
                                `<span class="threat-indicator">${indicator}</span>`
                            ).join('')}
                        </div>
                    </div>
                `;
            }
            
            // Individual results
            let individualHtml = '';
            const individual = result.individual_results || {};
            if (Object.keys(individual).length > 0) {
                individualHtml = '<div class="individual-results">';
                
                if (individual.text) {
                    const textConf = Math.round(individual.text.confidence * 100);
                    individualHtml += `
                        <div class="individual-result">
                            <h4>📧 Text Analysis</h4>
                            <p><strong>Confidence:</strong> ${textConf}%</p>
                            <p><strong>Phishing:</strong> ${individual.text.is_phishing ? 'Yes' : 'No'}</p>
                            <p><strong>Method:</strong> ${individual.text.method}</p>
                        </div>
                    `;
                }
                
                if (individual.url && !individual.url.error) {
                    const urlScore = Math.round(individual.url.risk_score * 100);
                    individualHtml += `
                        <div class="individual-result">
                            <h4>🔗 URL Analysis</h4>
                            <p><strong>Risk Score:</strong> ${urlScore}%</p>
                            <p><strong>Risk Level:</strong> ${individual.url.risk_level}</p>
                            <p><strong>Domain:</strong> ${individual.url.domain || 'N/A'}</p>
                        </div>
                    `;
                }
                
                individualHtml += '</div>';
            }
            
            container.innerHTML = `
                <div class="result-header ${headerClass}">${headerText}</div>
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">${combinedScore}%</div>
                        <div class="metric-label">Combined Score</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${result.risk_level}</div>
                        <div class="metric-label">Risk Level</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${confidence}%</div>
                        <div class="metric-label">Confidence</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${result.input_types.join(' + ')}</div>
                        <div class="metric-label">Analysis Type</div>
                    </div>
                </div>
                ${indicatorsHtml}
                ${individualHtml}
                <div class="recommendation ${riskLevel}">
                    🎯 ${result.final_recommendation}
                </div>
            `;
            
            container.style.display = 'block';
        }
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/analyze-combined', methods=['POST'])
def analyze_combined():
    """Combined analysis endpoint"""
    data = request.get_json()
    text = data.get('text', '').strip()
    url = data.get('url', '').strip()
    
    if not text and not url:
        return jsonify({'error': 'No text or URL provided'}), 400
    
    # Perform combined analysis
    result = analyze_input(text, url)
    
    return jsonify(result)

@app.route('/api/analyzer-info')
def analyzer_info():
    """Get analyzer information"""
    return jsonify(analyzer.get_analyzer_info())

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'TrustEye Threat Detector is running!',
        'components': ['NLP Classifier', 'URL Analyzer', 'Combined Intelligence'],
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 Starting TrustEye - AI Threat Detection System...")
    print("👁️ Features: Combined NLP + URL analysis with intelligent scoring")
    print("📱 Access: http://localhost:8080")
    print("✨ Ready for comprehensive threat detection!")
    
    app.run(debug=True, host='127.0.0.1', port=8080)
