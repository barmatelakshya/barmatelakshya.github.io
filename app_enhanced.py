from flask import Flask, render_template_string, request, jsonify
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from utils.text_processing import TextProcessor
from utils.url_parser import URLParser
from utils.data_loader import DataLoader

app = Flask(__name__)

# Initialize enhanced utilities
text_processor = TextProcessor()
url_parser = URLParser()
data_loader = DataLoader()

# Load sample data for testing
sample_data = data_loader.load_sample_data()

# HTML Template (same as before)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIH PS1 - Enhanced Cybersecurity Threat Detector</title>
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
        .stats-panel {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-top: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        @media (max-width: 768px) {
            .analyzer-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>🛡️ Enhanced Cybersecurity Threat Detector</h1>
            <p>SIH PS1 - Advanced NLP & URL Analysis with ML Utilities</p>
        </div>
    </div>

    <div class="container">
        <div class="analyzer-grid">
            <div class="analyzer-card">
                <h3>📧 Enhanced Text Analysis</h3>
                <form id="textForm">
                    <textarea id="textInput" placeholder="Paste suspicious email, message, or text content here..."></textarea>
                    <button type="submit" class="analyze-btn" id="textBtn">🔍 Analyze Text</button>
                </form>
                <div id="textResults" class="results"></div>
            </div>

            <div class="analyzer-card">
                <h3>🔗 Advanced URL Analysis</h3>
                <form id="urlForm">
                    <input type="url" id="urlInput" placeholder="Enter suspicious URL here...">
                    <button type="submit" class="analyze-btn" id="urlBtn">🔍 Analyze URL</button>
                </form>
                <div id="urlResults" class="results"></div>
            </div>
        </div>

        <div class="stats-panel">
            <h3>📊 System Statistics</h3>
            <div id="systemStats">Loading statistics...</div>
        </div>
    </div>

    <script>
        // Load system stats on page load
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                const statsDiv = document.getElementById('systemStats');
                statsDiv.innerHTML = `
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
                        <div class="metric">
                            <div class="metric-value">${data.total_samples || 0}</div>
                            <div>Total Samples</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${data.text_samples || 0}</div>
                            <div>Text Samples</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${data.url_samples || 0}</div>
                            <div>URL Samples</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${(data.avg_risk_score * 100).toFixed(1) || 0}%</div>
                            <div>Avg Risk Score</div>
                        </div>
                    </div>
                `;
            });

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
                        <div class="metric-value">${result.features_count || 'N/A'}</div>
                        <div>Features</div>
                    </div>
                </div>
                <div>
                    <strong>Detected Issues:</strong>
                    <div class="keywords">
                        ${(result.detected_keywords || result.detected_issues || result.issues || []).map(item => 
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
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Use enhanced text processing
    features = text_processor.extract_features(text)
    
    # Calculate threat assessment
    is_threat = features['suspicious_score'] > 0.5
    risk_level = 'High' if features['suspicious_score'] > 0.7 else 'Medium' if features['suspicious_score'] > 0.4 else 'Low'
    
    result = {
        'is_threat': is_threat,
        'risk_score': features['suspicious_score'],
        'risk_level': risk_level,
        'confidence': 0.85,
        'detected_keywords': features['urgency_words'],
        'features_count': len(features),
        'urls_found': len(features['urls']),
        'emails_found': len(features['emails'])
    }
    
    return jsonify(result)

@app.route('/api/analyze-url', methods=['POST'])
def analyze_url():
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Use enhanced URL analysis
    risk_info = url_parser.calculate_url_risk(url)
    
    result = {
        'is_threat': risk_info['risk_score'] > 0.4,
        'risk_score': risk_info['risk_score'],
        'risk_level': risk_info['risk_level'],
        'confidence': 0.80,
        'issues': risk_info['issues'],
        'domain_info': risk_info['domain_info']
    }
    
    return jsonify(result)

@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    stats = data_loader.get_data_stats()
    return jsonify(stats)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'message': 'SIH PS1 Enhanced Threat Detector is running!',
        'utilities': ['TextProcessor', 'URLParser', 'DataLoader']
    })

if __name__ == '__main__':
    print("🚀 Starting SIH PS1 Enhanced Cybersecurity Threat Detector...")
    print("📱 Access: http://localhost:4000")
    print("🛠️ Enhanced with ML utilities and data management")
    app.run(debug=True, host='0.0.0.0', port=4000)
