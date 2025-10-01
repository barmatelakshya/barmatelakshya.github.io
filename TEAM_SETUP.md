# 👥 Team Development Setup

## Quick Setup for Team Members

### 1. Clone Repository
```bash
git clone https://github.com/barmate-lakshya/sih-ps1-threat-detector.git
cd sih-ps1-threat-detector
```

### 2. Setup Environment (One Command)
```bash
./setup_dev.sh
```

### 3. Activate & Run
```bash
source venv/bin/activate
python mvp_app.py
```

### 4. Check Status
```bash
python dev_status.py
```

## 🔄 Daily Workflow

### Start Development
```bash
cd sih-ps1-threat-detector
source venv/bin/activate
git pull origin main
python mvp_app.py
```

### Commit Changes
```bash
git add .
git commit -m "Add: feature description"
git push origin main
```

## 🛠️ Environment Details

**✅ Ready Components:**
- Python 3.13 virtual environment
- Flask web framework
- NLP libraries (NLTK, TextBlob)
- Data processing (Pandas, NumPy)
- Web scraping (BeautifulSoup, Requests)
- Machine learning (Scikit-learn)
- Testing framework (Pytest)

**📱 Access Points:**
- **Web App**: http://localhost:5000
- **API Status**: http://localhost:5000/api/status

**🎯 Project Structure:**
```
sih-ps1-threat-detector/
├── mvp_app.py          # Main application
├── requirements.txt    # Dependencies
├── setup_dev.sh       # Environment setup
├── dev_status.py      # Status checker
├── src/               # Source code
├── tests/             # Test files
├── static/            # Frontend assets
└── templates/         # HTML templates
```

Ready for team collaboration! 🚀
