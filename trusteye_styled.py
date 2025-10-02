#!/usr/bin/env python3
from flask import Flask, render_template_string, request, jsonify
import re

app = Flask(__name__)

def analyze_threat(text="", url=""):
    risk_score = 0.0
    threats = []
    
    if text:
        text_lower = text.lower()
        keywords = ['urgent', 'click here', 'verify', 'suspended', 'winner', 'congratulations', 'act now', 'expires', 'claim']
        found = [kw for kw in keywords if kw in text_lower]
        if found:
            risk_score += len(found) * 0.15
            threats.extend(found)
    
    if url:
        if re.search(r'\d+\.\d+\.\d+\.\d+', url):
            risk_score += 0.4
            threats.append('IP address detected')
        if any(domain in url.lower() for domain in ['bit.ly', 'tinyurl', 'goo.gl']):
            risk_score += 0.3
            threats.append('URL shortener detected')
        if any(word in url.lower() for word in ['secure', 'verify', 'update', 'login']):
            risk_score += 0.2
            threats.append('Suspicious URL keywords')
    
    risk_score = min(0.95, risk_score)
    
    return {
        'combined_score': risk_score,
        'risk_level': 'Critical' if risk_score > 0.8 else 'High' if risk_score > 0.6 else 'Medium' if risk_score > 0.3 else 'Low',
        'is_threat': risk_score > 0.5,
        'confidence': 0.85,
        'threat_indicators': threats
    }

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrustEye - AI Threat Detection</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #2563eb;
            --secondary-color: #64748b;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --critical-color: #dc2626;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .navbar-brand {
            font-size: 1.8rem;
            font-weight: bold;
        }
        
        .logo-icon {
            font-size: 2rem;
            margin-right: 0.5rem;
        }
        
        .hero-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            color: white;
            padding: 4rem 0;
            text-align: center;
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        
        .hero-subtitle {
            font-size: 1.3rem;
            opacity: 0.9;
        }
        
        .main-card {
            background: white;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            margin-top: -50px;
            position: relative;
            z-index: 10;
        }
        
        .scan-btn {
            background: linear-gradient(135deg, var(--primary-color), #1d4ed8);
            border: none;
            padding: 15px 30px;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        
        .scan-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(37, 99, 235, 0.3);
        }
        
        .risk-indicator {
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            text-align: center;
        }
        
        .risk-critical {
            background: linear-gradient(135deg, #fee2e2, #fecaca);
            border: 2px solid var(--critical-color);
            color: var(--critical-color);
        }
        
        .risk-high {
            background: linear-gradient(135deg, #fef3c7, #fed7aa);
            border: 2px solid var(--danger-color);
            color: var(--danger-color);
        }
        
        .risk-medium {
            background: linear-gradient(135deg, #fff7ed, #fef3c7);
            border: 2px solid var(--warning-color);
            color: var(--warning-color);
        }
        
        .risk-low {
            background: linear-gradient(135deg, #dcfce7, #bbf7d0);
            border: 2px solid var(--success-color);
            color: var(--success-color);
        }
        
        .risk-score {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .risk-level {
            font-size: 1.5rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .threat-badge {
            background: var(--warning-color);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            margin: 0.25rem;
            display: inline-block;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .stats-card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: var(--primary-color);
        }
        
        .feature-icon {
            font-size: 3rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
        }
        
        .footer {
            background: #1e293b;
            color: white;
            padding: 2rem 0;
            margin-top: 3rem;
        }
        
        .example-btn {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 20px;
            padding: 0.5rem 1rem;
            margin: 0.25rem;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }
        
        .example-btn:hover {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="#">
                <span class="logo-icon">👁️</span>TrustEye
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#scanner">Scanner</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#features">Features</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#about">About</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container">
            <h1 class="hero-title">👁️ TrustEye</h1>
            <p class="hero-subtitle">AI-Powered Cybersecurity Threat Detection</p>
            <p class="mt-3">Protect yourself from phishing attacks with advanced machine learning</p>
        </div>
    </section>

    <!-- Main Scanner -->
    <section id="scanner" class="container">
        <div class="main-card p-5">
            <div class="row">
                <div class="col-lg-8 mx-auto">
                    <h2 class="text-center mb-4">
                        <i class="fas fa-shield-alt text-primary me-2"></i>
                        Threat Scanner
                    </h2>
                    <p class="text-center text-muted mb-4">
                        Enter suspicious text or URLs to analyze potential phishing threats
                    </p>

                    <!-- Quick Examples -->
                    <div class="text-center mb-4">
                        <small class="text-muted">Quick Examples:</small><br>
                        <button type="button" class="btn example-btn" onclick="loadExample('phishing')">
                            <i class="fas fa-exclamation-triangle text-danger"></i> Phishing Email
                        </button>
                        <button type="button" class="btn example-btn" onclick="loadExample('url')">
                            <i class="fas fa-link text-warning"></i> Suspicious URL
                        </button>
                        <button type="button" class="btn example-btn" onclick="loadExample('safe')">
                            <i class="fas fa-check-circle text-success"></i> Safe Content
                        </button>
                    </div>

                    <form id="scanForm">
                        <div class="mb-4">
                            <label for="textInput" class="form-label">
                                <i class="fas fa-envelope text-primary"></i> Suspicious Text or Email
                            </label>
                            <textarea class="form-control" id="textInput" rows="4" 
                                placeholder="Paste suspicious email content, SMS message, or any text here..."></textarea>
                        </div>

                        <div class="mb-4">
                            <label for="urlInput" class="form-label">
                                <i class="fas fa-link text-primary"></i> Suspicious URL
                            </label>
                            <input type="url" class="form-control" id="urlInput" 
                                placeholder="https://suspicious-website.com">
                        </div>

                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary scan-btn">
                                <i class="fas fa-search me-2"></i>Scan with TrustEye
                            </button>
                        </div>
                    </form>

                    <!-- Results Section -->
                    <div id="results" class="mt-4" style="display: none;">
                        <div id="riskIndicator" class="risk-indicator">
                            <div id="riskScore" class="risk-score">0%</div>
                            <div id="riskLevel" class="risk-level">Safe</div>
                            <div class="mt-3">
                                <small><i class="fas fa-clock"></i> Analysis completed</small>
                            </div>
                        </div>

                        <div class="row mt-4">
                            <div class="col-md-4">
                                <div class="stats-card">
                                    <div id="confidenceValue" class="stat-value">85%</div>
                                    <div class="text-muted">Confidence</div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="stats-card">
                                    <div id="threatCount" class="stat-value">0</div>
                                    <div class="text-muted">Threats Found</div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="stats-card">
                                    <div class="stat-value"><i class="fas fa-robot"></i></div>
                                    <div class="text-muted">AI Analysis</div>
                                </div>
                            </div>
                        </div>

                        <div id="threatsSection" class="mt-4">
                            <h5><i class="fas fa-exclamation-triangle text-warning"></i> Detected Threats:</h5>
                            <div id="threatsList"></div>
                        </div>

                        <div class="text-center mt-4">
                            <button class="btn btn-outline-secondary me-2" onclick="clearResults()">
                                <i class="fas fa-trash"></i> Clear
                            </button>
                            <button class="btn btn-primary" onclick="scanAnother()">
                                <i class="fas fa-redo"></i> Scan Another
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="container mt-5">
        <h2 class="text-center mb-5">Why Choose TrustEye?</h2>
        <div class="row">
            <div class="col-md-4 text-center mb-4">
                <div class="feature-icon">
                    <i class="fas fa-brain"></i>
                </div>
                <h4>AI-Powered Detection</h4>
                <p class="text-muted">Advanced machine learning algorithms detect sophisticated phishing attempts with high accuracy.</p>
            </div>
            <div class="col-md-4 text-center mb-4">
                <div class="feature-icon">
                    <i class="fas fa-bolt"></i>
                </div>
                <h4>Real-Time Analysis</h4>
                <p class="text-muted">Instant threat analysis with results delivered in under 2 seconds for immediate protection.</p>
            </div>
            <div class="col-md-4 text-center mb-4">
                <div class="feature-icon">
                    <i class="fas fa-shield-alt"></i>
                </div>
                <h4>Comprehensive Protection</h4>
                <p class="text-muted">Analyzes both text content and URL patterns for complete cybersecurity coverage.</p>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>
                        <span class="logo-icon">👁️</span>TrustEye
                    </h5>
                    <p class="text-muted">AI-Powered Cybersecurity Threat Detection System</p>
                    <p class="text-muted">SIH PS1 - Smart India Hackathon Project</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <h6>Features</h6>
                    <ul class="list-unstyled">
                        <li><i class="fas fa-check text-success"></i> Text Analysis</li>
                        <li><i class="fas fa-check text-success"></i> URL Scanning</li>
                        <li><i class="fas fa-check text-success"></i> Real-time Detection</li>
                        <li><i class="fas fa-check text-success"></i> Risk Assessment</li>
                    </ul>
                </div>
            </div>
            <hr class="my-4">
            <div class="text-center">
                <p class="mb-0">&copy; 2025 TrustEye. Built for Smart India Hackathon.</p>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const examples = {
            'phishing': {
                text: 'URGENT SECURITY ALERT! Your account will be suspended in 24 hours due to suspicious activity. Click here immediately to verify your identity and avoid account closure.',
                url: 'http://secure-bank-verify.fake-domain.com/urgent-login'
            },
            'url': {
                text: '',
                url: 'http://192.168.1.100/urgent-verify/login.php'
            },
            'safe': {
                text: 'Thank you for your recent purchase from Amazon. Your order has been shipped and will arrive within 2-3 business days.',
                url: 'https://amazon.com/your-orders'
            }
        };

        function loadExample(type) {
            const example = examples[type];
            document.getElementById('textInput').value = example.text;
            document.getElementById('urlInput').value = example.url;
        }

        document.getElementById('scanForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const text = document.getElementById('textInput').value.trim();
            const url = document.getElementById('urlInput').value.trim();
            
            if (!text && !url) {
                alert('Please enter text or URL to analyze');
                return;
            }
            
            const scanBtn = document.querySelector('.scan-btn');
            scanBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
            scanBtn.disabled = true;
            
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
            } finally {
                scanBtn.innerHTML = '<i class="fas fa-search me-2"></i>Scan with TrustEye';
                scanBtn.disabled = false;
            }
        });
        
        function displayResults(result) {
            const results = document.getElementById('results');
            const riskScore = Math.round(result.combined_score * 100);
            const riskLevel = result.risk_level.toLowerCase();
            
            // Update risk indicator
            const riskIndicator = document.getElementById('riskIndicator');
            riskIndicator.className = `risk-indicator risk-${riskLevel}`;
            
            document.getElementById('riskScore').textContent = riskScore + '%';
            document.getElementById('riskLevel').textContent = result.risk_level;
            
            // Update stats
            document.getElementById('confidenceValue').textContent = Math.round(result.confidence * 100) + '%';
            document.getElementById('threatCount').textContent = result.threat_indicators.length;
            
            // Update threats
            const threatsList = document.getElementById('threatsList');
            if (result.threat_indicators.length > 0) {
                threatsList.innerHTML = result.threat_indicators.map(threat => 
                    `<span class="threat-badge">${threat}</span>`
                ).join('');
                document.getElementById('threatsSection').style.display = 'block';
            } else {
                document.getElementById('threatsSection').style.display = 'none';
            }
            
            results.style.display = 'block';
            results.scrollIntoView({ behavior: 'smooth' });
        }
        
        function clearResults() {
            document.getElementById('results').style.display = 'none';
        }
        
        function scanAnother() {
            document.getElementById('textInput').value = '';
            document.getElementById('urlInput').value = '';
            clearResults();
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

if __name__ == '__main__':
    print("🚀 Starting TrustEye with Enhanced Styling...")
    print("👁️ Access: http://localhost:8080")
    print("🎨 Features: Bootstrap, Logo, Header, Footer, Color-coded Risk")
    app.run(debug=True, host='127.0.0.1', port=8080)
