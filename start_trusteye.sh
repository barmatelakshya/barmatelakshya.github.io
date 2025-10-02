#!/bin/bash
echo "🚀 Starting TrustEye - AI Threat Detection System"
echo "================================================"

# Kill any existing servers to prevent conflicts
pkill -f "trusteye" 2>/dev/null
pkill -f "python.*trusteye" 2>/dev/null
sleep 1

# Start TrustEye server (will auto-open browser once)
cd "$(dirname "$0")"
python3 trusteye_single.py &

echo "✅ TrustEye starting on port 8080"
echo "📱 Access: http://localhost:8080"
echo "🌐 Browser will open automatically"
echo "🛑 Press Ctrl+C to stop"

# Keep script running
wait
