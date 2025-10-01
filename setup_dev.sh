#!/bin/bash

echo "🚀 Setting up SIH PS1 Development Environment..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "🔄 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create project structure
echo "📁 Creating project structure..."
mkdir -p {src,tests,static,templates,data,docs}

# Create .env file
echo "🔐 Creating environment file..."
cat > .env << EOF
FLASK_APP=mvp_app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
PORT=5000
EOF

# Create .gitignore
echo "🚫 Creating .gitignore..."
cat > .gitignore << EOF
# Virtual Environment
venv/
env/
.env

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
.pytest_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Data
data/*.csv
data/*.json
!data/sample_data.json
EOF

echo "✅ Development environment setup complete!"
echo "🎯 Next steps:"
echo "   1. source venv/bin/activate"
echo "   2. python mvp_app.py"
echo "   3. Open http://localhost:5000"
