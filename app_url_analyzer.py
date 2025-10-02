#!/usr/bin/env python3
"""
Flask App with Advanced URL Analyzer
SIH PS1 - Cybersecurity Threat Detector
"""
from flask import Flask, render_template_string, request, jsonify
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from backend.models.url_analyzer import analyze_url, get_analyzer

app = Flask(__name__)

# Initialize analyzer
analyzer = get_analyzer()

# HTML Template
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIH PS1 - Advanced URL Analyzer</title>
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
        .header p { opacity: 0.9; font-size: 1.1rem; }
        .features {
            background: rgba(255,255,255,0.2);
            padding: 15px 25px;
            border-radius: 25px;
            display: inline-block;
            margin-top: 15px;
            font-size: 0.9rem;
        }
        .container { max-width: 1000px; margin: 0 auto; padding: 0 20px; }
        .analyzer-card {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .analyzer-card h3 { color: #667eea; margin-bottom: 25px; font-size: 1.8rem; text-align: center; }
        .samples {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }
        .sample-group h4 { color: #333; margin-bottom: 15px; font-size: 1.1rem; }
        .sample-btn {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 12px 15px;
            margin: 8px 0;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
            text-align: left;
            width: 100%;
            word-break: break-all;
        }
        .sample-btn:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        .suspicious-sample { border-left: 4px solid #dc3545; }
        .safe-sample { border-left: 4px solid #28a745; }
        .url-input {
            width: 100%;
            padding: 20px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            font-size: 16px;
            margin-bottom: 20px;
            font-family: 'Courier New', monospace;
        }
        .url-input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }
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
        .analyze-btn:disabled { opacity: 0.7; cursor: not-allowed; transform: none; }
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
            border-radius: 12px;
            margin-bottom: 20px;
            font-weight: 600;
            font-size: 1.2rem;
        }
        .safe { background: #d4edda; color: #155724; }
        .warning { background: #fff3cd; color: #856404; }
        .danger { background: #f8d7da; color: #721c24; }
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .metric {
            text-align: center;
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .metric-value { font-size: 1.8rem; font-weight: bold; color: #667eea; margin-bottom: 5px; }
        .metric-label { font-size: 0.9rem; color: #666; }
        .details {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin-top: 15px;
        }
        .details h4 { color: #333; margin-bottom: 15px; }
        .risk-factors {
            list-style: none;
            padding: 0;
        }
        .risk-factors li {
            background: #fff3cd;
            color: #856404;
            padding: 8px 15px;
            margin: 5px 0;
            border-radius: 8px;
            border-left: 4px solid #ffc107;
        }
        .redirections {
            background: #e7f3ff;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        .redirect-item {
            font-family: 'Courier New', monospace;
            font-size: 14px;
            margin: 5px 0;
            word-break: break-all;
        }
        .recommendation {
            background: #e8f5e8;
            border: 2px solid #28a745;
            padding: 15px;
            border-radius: 12px;
            margin-top: 15px;
            font-weight: 600;
            text-align: center;
        }
        .recommendation.warning {
            background: #fff3cd;
            border-color: #ffc107;
            color: #856404;
        }
        .recommendation.danger {
            background: #f8d7da;
            border-color: #dc3545;
            color: #721c24;
        }
        @media (max-width: 768px) {
            .samples { grid-template-columns: 1fr; }
            .metrics { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>🔗 Advanced URL Analyzer</h1>
            <p>SIH PS1 - Comprehensive URL Security Analysis</p>
            <div class="features">
                🔄 Redirection Chains • 📅 Domain Age • 🌐 DNS Records • 🔍 Pattern Analysis
            </div>
        </div>
    </div>

    <div class="container">
        <div class="analyzer-card">
            <h3>🛡️ URL Security Analysis</h3>
            
            <div class="samples">
                <div class="sample-group">
                    <h4>🚨 Suspicious URLs</h4>
                    <button class="sample-btn suspicious-sample" onclick="loadSample(1)">
                        http://192.168.1.100/login.php
                    </button>
                    <button class="sample-btn suspicious-sample" onclick="loadSample(2)">
                        http://bit.ly/suspicious-link
                    </button>
                    <button class="sample-btn suspicious-sample" onclick="loadSample(3)">
                        http://secure-bank-verify.fake-domain.com/urgent
                    </button>
                </div>
                
                <div class="sample-group">
                    <h4>✅ Legitimate URLs</h4>
                    <button class="sample-btn safe-sample" onclick="loadSample(4)">
                        https://amazon.com/orders
                    </button>
                    <button class="sample-btn safe-sample" onclick="loadSample(5)">
                        https://github.com/microsoft/vscode
                    </button>
                    <button class="sample-btn safe-sample" onclick="loadSample(6)">
                        https://stackoverflow.com/questions
                    </button>
                </div>
            </div>
            
            <form id="analyzeForm">
                <input type="url" id="urlInput" class="url-input" placeholder="Enter URL to analyze (e.g., https://example.com)">
                <button type="submit" class="analyze-btn" id="analyzeBtn">
                    🔍 Analyze URL Security
                </button>
            </form>
            
            <div id="results" class="results"></div>
        </div>
    </div>

    <script>
        const samples = {
            1: "http://192.168.1.100/login.php",
            2: "http://bit.ly/suspicious-link",
            3: "http://secure-bank-verify.fake-domain.com/urgent-update",
            4: "https://amazon.com/orders",
            5: "https://github.com/microsoft/vscode",
            6: "https://stackoverflow.com/questions/tagged/python"
        };

        function loadSample(id) {
            document.getElementById('urlInput').value = samples[id];
        }

        document.getElementById('analyzeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const url = document.getElementById('urlInput').value.trim();
            if (!url) {
                alert('Please enter a URL to analyze');
                return;
            }

            const resultsDiv = document.getElementById('results');
            const analyzeBtn = document.getElementById('analyzeBtn');
            
            // Show loading state
            analyzeBtn.disabled = true;
            analyzeBtn.textContent = '🔄 Analyzing URL...';
            resultsDiv.style.display = 'none';

            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url })
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
                analyzeBtn.textContent = '🔍 Analyze URL Security';
            }
        });

        function displayResults(result, container) {
            const riskScore = Math.round(result.risk_score * 100);
            const riskLevel = result.risk_level;
            
            let headerClass, headerText;
            if (riskLevel === 'High') {
                headerClass = 'danger';
                headerText = '🚨 HIGH RISK DETECTED';
            } else if (riskLevel === 'Medium') {
                headerClass = 'warning';
                headerText = '⚠️ MEDIUM RISK DETECTED';
            } else {
                headerClass = 'safe';
                headerText = '✅ LOW RISK DETECTED';
            }
            
            let detailsHtml = '';
            
            // Risk factors
            if (result.risk_factors && result.risk_factors.length > 0) {
                detailsHtml += `
                    <div class="details">
                        <h4>⚠️ Risk Factors (${result.risk_factors.length})</h4>
                        <ul class="risk-factors">
                            ${result.risk_factors.map(factor => `<li>${factor}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }
            
            // Redirections
            if (result.redirections && result.redirections.length > 0) {
                detailsHtml += `
                    <div class="details">
                        <h4>🔄 Redirection Chain (${result.redirections.length} redirects)</h4>
                        <div class="redirections">
                            ${result.redirections.map((redirect, i) => 
                                `<div class="redirect-item">${i + 1}. ${redirect.from} → ${redirect.to} (${redirect.status})</div>`
                            ).join('')}
                        </div>
                    </div>
                `;
            }
            
            // Additional info
            let additionalInfo = '';
            if (result.domain_age) {
                additionalInfo += `<p><strong>Domain Age:</strong> ${result.domain_age}</p>`;
            }
            if (result.ip_addresses) {
                additionalInfo += `<p><strong>IP Addresses:</strong> ${result.ip_addresses.join(', ')}</p>`;
            }
            if (result.has_mx_records !== undefined) {
                additionalInfo += `<p><strong>Email Records:</strong> ${result.has_mx_records ? 'Yes' : 'No'}</p>`;
            }
            
            if (additionalInfo) {
                detailsHtml += `
                    <div class="details">
                        <h4>ℹ️ Additional Information</h4>
                        ${additionalInfo}
                    </div>
                `;
            }
            
            // Recommendation
            let recClass = 'safe';
            if (riskLevel === 'High') recClass = 'danger';
            else if (riskLevel === 'Medium') recClass = 'warning';
            
            container.innerHTML = `
                <div class="result-header ${headerClass}">${headerText}</div>
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">${riskScore}%</div>
                        <div class="metric-label">Risk Score</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${result.risk_level}</div>
                        <div class="metric-label">Risk Level</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${Math.round(result.confidence * 100)}%</div>
                        <div class="metric-label">Confidence</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${result.domain || 'N/A'}</div>
                        <div class="metric-label">Domain</div>
                    </div>
                </div>
                ${detailsHtml}
                <div class="recommendation ${recClass}">
                    🎯 ${result.recommendation || 'Analysis complete'}
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

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Main URL analysis endpoint"""
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Analyze URL
    result = analyze_url(url)
    
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Advanced URL Analyzer is running!',
        'features': ['Redirection Analysis', 'Domain Age Check', 'DNS Analysis', 'Pattern Detection']
    })

if __name__ == '__main__':
    print("🚀 Starting SIH PS1 Advanced URL Analyzer...")
    print("🔗 Features: Redirection chains, Domain age, DNS records, Pattern analysis")
    print("📱 Access: http://localhost:8080")
    
    app.run(debug=True, host='127.0.0.1', port=8080)
