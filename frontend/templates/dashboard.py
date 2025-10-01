"""
Dashboard HTML Template
SIH PS1 - Cybersecurity Threat Detector
"""

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

    <script src="../static/js/dashboard.js"></script>
</body>
</html>
'''
