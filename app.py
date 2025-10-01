from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# HTML Template for new project
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIH PS1 - New Project</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .container {
            text-align: center;
            background: rgba(255,255,255,0.1);
            padding: 60px 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        h1 { font-size: 3rem; margin-bottom: 20px; }
        p { font-size: 1.2rem; opacity: 0.9; margin-bottom: 30px; }
        .status { 
            background: rgba(39,174,96,0.2);
            padding: 15px 30px;
            border-radius: 25px;
            display: inline-block;
            border: 2px solid rgba(39,174,96,0.5);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 SIH PS1 Project</h1>
        <p>New Smart India Hackathon Project Started</p>
        <div class="status">
            ✅ Project Initialized Successfully
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def status():
    return jsonify({
        'project': 'SIH PS1',
        'status': 'initialized',
        'message': 'New project ready for development'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
