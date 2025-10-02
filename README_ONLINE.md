# 👁️ TrustEye - Online Deployment

## 🚀 Quick Start

### Method 1: One-Click Start
```bash
./start_trusteye.sh
```

### Method 2: Manual Start
```bash
python3 trusteye_online.py
```

## 🌐 Access URLs

- **Local**: http://localhost:8080
- **Network**: http://0.0.0.0:8080
- **Mobile**: http://[YOUR_IP]:8080

## ✅ Features Online

### 🔍 Scanner
- AI-powered phishing detection
- URL threat analysis
- Real-time risk scoring
- Multiple sample inputs

### 📊 Dashboard
- Scan statistics
- Risk level distribution charts
- Threat detection analytics
- Time-based trends

### 🎯 Demo System
- Random phishing samples
- Suspicious URL examples
- One-click demo scans
- Interactive examples

## 📱 Mobile Access

1. Find your computer's IP address:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

2. Access from mobile:
   ```
   http://[YOUR_IP]:8080
   ```

## 🛑 Stop Server

- Press `Ctrl+C` in terminal
- Or kill process: `pkill -f trusteye_online.py`

## 🔧 Troubleshooting

### Port Already in Use
```bash
lsof -ti:8080 | xargs kill -9
```

### Permission Denied
```bash
chmod +x start_trusteye.sh
chmod +x trusteye_online.py
```

## 📂 File Structure
```
SIH_PS1/
├── trusteye_dashboard.html    # Main application
├── trusteye_online.py         # Online server
├── start_trusteye.sh          # Startup script
└── README_ONLINE.md           # This file
```

## 🎉 Success!

TrustEye is now running online and accessible from any device on your network!

**Built for Smart India Hackathon 2025** 🇮🇳
