# 🐙 GitHub Repository Setup

## Quick Setup Commands

### 1. Initialize Git Repository
```bash
cd /Users/barmate_lakshya/Documents/SIH_PS1
git init
git add .
git commit -m "Initial commit: SIH PS1 Cybersecurity Threat Detector"
```

### 2. Create GitHub Repository
1. Go to [GitHub.com](https://github.com)
2. Click "New Repository"
3. Name: `sih-ps1-threat-detector`
4. Description: `SIH 2025 - Advanced Cybersecurity Threat Detection System`
5. Keep it Public (for hackathon visibility)
6. Don't initialize with README (we have one)

### 3. Connect Local to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/sih-ps1-threat-detector.git
git branch -M main
git push -u origin main
```

### 4. Team Collaboration Setup
```bash
# Clone for team members
git clone https://github.com/YOUR_USERNAME/sih-ps1-threat-detector.git
cd sih-ps1-threat-detector

# Setup development environment
./setup_dev.sh

# Start development
source venv/bin/activate
python mvp_app.py
```

## 🔄 Development Workflow

### Daily Workflow
```bash
# Pull latest changes
git pull origin main

# Create feature branch
git checkout -b feature/new-feature

# Make changes, then commit
git add .
git commit -m "Add: new feature description"

# Push to GitHub
git push origin feature/new-feature

# Create Pull Request on GitHub
```

### Branch Strategy
- `main` - Production ready code
- `develop` - Integration branch
- `feature/feature-name` - Individual features
- `hotfix/issue-name` - Quick fixes

## 👥 Team Access
Add team members as collaborators:
1. Go to repository Settings
2. Manage access → Invite a collaborator
3. Add team member GitHub usernames

## 📋 Repository Structure
```
sih-ps1-threat-detector/
├── README.md
├── requirements.txt
├── setup_dev.sh
├── mvp_app.py
├── .env.example
├── .gitignore
├── src/
├── tests/
├── static/
├── templates/
├── data/
└── docs/
```

Ready for team collaboration! 🚀
