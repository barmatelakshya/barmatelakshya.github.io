# 🚀 VS Code Setup Guide

## Quick Start in VS Code

### 1. Open Project
```bash
code /Users/barmate_lakshya/Documents/SIH_PS1
```

### 2. Select Python Interpreter
- Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
- Type "Python: Select Interpreter"
- Choose: `./venv/bin/python`

### 3. Run Applications

#### Option A: Using Debug Panel (F5)
1. Press `F5` or go to Run & Debug panel
2. Select configuration:
   - **🤖 NLP Phishing Detector** → http://localhost:8080
   - **🔗 URL Analyzer** → http://localhost:8080
   - **🧪 Test NLP Classifier** → Run tests
   - **🧪 Test URL Analyzer** → Run tests

#### Option B: Using Tasks (Cmd+Shift+P)
1. Press `Cmd+Shift+P`
2. Type "Tasks: Run Task"
3. Choose:
   - **🚀 Start NLP App**
   - **🔗 Start URL Analyzer**
   - **🧪 Run Tests**
   - **📦 Install Dependencies**

#### Option C: Using Terminal
1. Open VS Code terminal (`Ctrl+` `)
2. Run commands:
```bash
# Activate environment
source venv/bin/activate

# Run NLP app
python app_nlp.py

# Run URL analyzer
python app_url_analyzer.py

# Run tests
python test_nlp_classifier.py
```

## 🛠️ VS Code Extensions (Recommended)

Install these extensions for better development:

1. **Python** (Microsoft) - Python support
2. **Pylance** (Microsoft) - Python language server
3. **Python Docstring Generator** - Auto docstrings
4. **GitLens** - Git integration
5. **Thunder Client** - API testing
6. **Live Server** - HTML preview

## 🔧 Keyboard Shortcuts

| Action | Shortcut | Description |
|--------|----------|-------------|
| `F5` | Debug/Run | Start debugging |
| `Ctrl+F5` | Run | Run without debugging |
| `Cmd+Shift+P` | Command Palette | Access all commands |
| `Ctrl+` ` | Terminal | Open integrated terminal |
| `Cmd+Shift+E` | Explorer | File explorer |
| `Cmd+Shift+D` | Debug | Debug panel |

## 📁 Project Structure in VS Code

```
SIH_PS1/
├── 📂 .vscode/              # VS Code configuration
│   ├── launch.json         # Debug configurations
│   ├── settings.json       # Workspace settings
│   └── tasks.json          # Task definitions
├── 📂 backend/
│   └── 📂 models/
│       ├── nlp_classifier.py    # NLP model
│       └── url_analyzer.py      # URL analyzer
├── 📄 app_nlp.py           # NLP web app
├── 📄 app_url_analyzer.py  # URL analyzer app
├── 📄 test_nlp_classifier.py    # NLP tests
└── 📄 test_url_analyzer.py     # URL tests
```

## 🎯 Quick Actions

### Start Development
1. Open project in VS Code
2. Press `F5`
3. Select "🤖 NLP Phishing Detector"
4. App opens at http://localhost:8080

### Debug Code
1. Set breakpoints (click left margin)
2. Press `F5`
3. Use debug controls (step, continue, etc.)

### Run Tests
1. Press `Cmd+Shift+P`
2. Type "Tasks: Run Task"
3. Select "🧪 Run Tests"

Ready to develop in VS Code! 🎉
