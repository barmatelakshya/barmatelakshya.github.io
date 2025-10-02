#!/usr/bin/env python3
"""
Enhanced Flask App with NLP Phishing Classifier
SIH PS1 - Cybersecurity Threat Detector
"""
from flask import Flask, render_template_string, request, jsonify
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from backend.models.nlp_classifier import predict_phishing, get_classifier

app = Flask(__name__)

# Initialize classifier
classifier = get_classifier()

# HTML Template with enhanced features
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIH PS1 - NLP Phishing Detector</title>
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
        .model-info {
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 20px;
            display: inline-block;
            margin-top: 10px;
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
            gap: 15px;
            margin-bottom: 25px;
        }
        .sample-group h4 { color: #333; margin-bottom: 10px; font-size: 1rem; }
        .sample-btn {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 10px 15px;
            margin: 5px 0;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
            text-align: left;
            width: 100%;
        }
        .sample-btn:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        .phishing-sample { border-left: 4px solid #dc3545; }
        .safe-sample { border-left: 4px solid #28a745; }
        textarea {
            width: 100%;
            padding: 20px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            font-size: 16px;
            margin-bottom: 20px;
            resize: vertical;
            min-height: 150px;
            font-family: inherit;
        }
        textarea:focus {
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
        .keywords {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }
        .keyword {
            background: #fff3cd;
            color: #856404;
            padding: 6px 12px;
            border-radius: 15px;
            font-size: 14px;
            font-weight: 500;
        }
        .method-badge {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
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
            <h1>🤖 NLP Phishing Detector</h1>
            <p>SIH PS1 - Advanced Transformer-Based Threat Detection</p>
            <div class="model-info" id="modelInfo">Loading model info...</div>
        </div>
    </div>

    <div class="container">
        <div class="analyzer-card">
            <h3>📧 AI-Powered Text Analysis</h3>
            
            <div class="samples">
                <div class="sample-group">
                    <h4>🚨 Phishing Examples</h4>
                    <button class="sample-btn phishing-sample" onclick="loadSample(1)">
                        URGENT: Account suspended! Verify now...
                    </button>
                    <button class="sample-btn phishing-sample" onclick="loadSample(2)">
                        Congratulations! You've won $1,000,000...
                    </button>
                    <button class="sample-btn phishing-sample" onclick="loadSample(3)">
                        Security Alert: Unknown login detected...
                    </button>
                </div>
                
                <div class="sample-group">
                    <h4>✅ Legitimate Examples</h4>
                    <button class="sample-btn safe-sample" onclick="loadSample(4)">
                        Thank you for your Amazon purchase...
                    </button>
                    <button class="sample-btn safe-sample" onclick="loadSample(5)">
                        Your appointment is confirmed for...
                    </button>
                    <button class="sample-btn safe-sample" onclick="loadSample(6)">
                        Monthly bank statement available...
                    </button>
                </div>
            </div>
            
            <form id="analyzeForm">
                <textarea id="textInput" placeholder="Paste email content, SMS message, or any suspicious text here for AI analysis..."></textarea>
                <button type="submit" class="analyze-btn" id="analyzeBtn">
                    🔍 Analyze with AI
                </button>
            </form>
            
            <div id="results" class="results"></div>
        </div>
    </div>

    <script>
        const samples = {
            1: "URGENT SECURITY ALERT! Your account will be suspended in 24 hours due to suspicious activity. Click here immediately to verify your identity and avoid account closure.",
            2: "Congratulations! You've won $1,000,000 in our international lottery! Claim your prize now by clicking this link and providing your bank details.",
            3: "Security Alert: We detected a login attempt from an unknown device in Russia. If this wasn't you, click here to secure your account immediately.",
            4: "Thank you for your recent purchase from Amazon. Your order #123456789 has been shipped and will arrive within 2-3 business days. Track your package in your account.",
            5: "Your appointment with Dr. Smith is confirmed for tomorrow at 2:00 PM. Please arrive 15 minutes early for check-in. Call us if you need to reschedule.",
            6: "Your monthly bank statement is now available. You can view it by logging into your online banking account or visiting any of our branch locations."
        };

        // Load model info
        fetch('/api/model-info')
            .then(response => response.json())
            .then(data => {
                const modelInfo = document.getElementById('modelInfo');
                modelInfo.innerHTML = `
                    <span class="method-badge">${data.method}</span>
                    ${data.is_loaded ? '🤖 Transformer Model' : '📝 Keyword-Based'} • 
                    ${data.keywords_count} Keywords
                `;
            });

        function loadSample(id) {
            document.getElementById('textInput').value = samples[id];
        }

        document.getElementById('analyzeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const text = document.getElementById('textInput').value.trim();
            if (!text) {
                alert('Please enter text to analyze');
                return;
            }

            const resultsDiv = document.getElementById('results');
            const analyzeBtn = document.getElementById('analyzeBtn');
            
            // Show loading state
            analyzeBtn.disabled = true;
            analyzeBtn.textContent = '🔄 Analyzing with AI...';
            resultsDiv.style.display = 'none';

            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                
                const result = await response.json();
                displayResults(result, resultsDiv);
                
            } catch (error) {
                alert('Analysis failed: ' + error.message);
            } finally {
                analyzeBtn.disabled = false;
                analyzeBtn.textContent = '🔍 Analyze with AI';
            }
        });

        function displayResults(result, container) {
            const confidence = Math.round(result.confidence * 100);
            const headerClass = result.is_phishing ? 'danger' : (confidence > 30 ? 'warning' : 'safe');
            const headerText = result.is_phishing ? '🚨 PHISHING DETECTED' : (confidence > 30 ? '⚡ SUSPICIOUS CONTENT' : '✅ APPEARS SAFE');
            
            let detailsHtml = '';
            
            if (result.method === 'transformer') {
                detailsHtml = `
                    <div class="details">
                        <h4>🤖 AI Analysis Details</h4>
                        <p><strong>Negative Sentiment:</strong> ${Math.round(result.negative_sentiment * 100)}%</p>
                        <p><strong>Positive Sentiment:</strong> ${Math.round(result.positive_sentiment * 100)}%</p>
                        <p><strong>Model:</strong> ${result.model_used}</p>
                    </div>
                `;
            } else {
                detailsHtml = `
                    <div class="details">
                        <h4>📝 Keyword Analysis</h4>
                        <p><strong>Suspicious Keywords Found:</strong></p>
                        <div class="keywords">
                            ${result.suspicious_keywords.map(keyword => 
                                `<span class="keyword">${keyword}</span>`
                            ).join('')}
                        </div>
                        <p style="margin-top: 10px;"><strong>Keyword Count:</strong> ${result.keyword_count}</p>
                    </div>
                `;
            }
            
            container.innerHTML = `
                <div class="result-header ${headerClass}">${headerText}</div>
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">${confidence}%</div>
                        <div class="metric-label">Confidence</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${result.risk_level}</div>
                        <div class="metric-label">Risk Level</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${result.word_count}</div>
                        <div class="metric-label">Words</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${result.method === 'transformer' ? '🤖' : '📝'}</div>
                        <div class="metric-label">Method</div>
                    </div>
                </div>
                ${detailsHtml}
            `;
            
            container.style.display = 'block';
        }
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Get prediction from NLP classifier
    result = predict_phishing(text)
    
    return jsonify(result)

@app.route('/api/model-info')
def model_info():
    """Get model information"""
    return jsonify(classifier.get_model_info())

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'NLP Phishing Detector is running!',
        'model_loaded': classifier.is_loaded
    })

if __name__ == '__main__':
    print("🚀 Starting SIH PS1 NLP Phishing Detector...")
    print("🤖 Loading AI models...")
    print("📱 Access: http://localhost:8080")
    print("✨ Features: Transformer-based detection with fallback")
    
    app.run(debug=True, host='127.0.0.1', port=8080)
