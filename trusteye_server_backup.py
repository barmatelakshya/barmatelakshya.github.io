#!/usr/bin/env python3
"""
TrustEye Single Port Server - Fixed Double Opening
"""
import http.server
import socketserver
import webbrowser
import threading
import time
import sys
from pathlib import Path

class TrustEyeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html' or self.path == '/#':
            self.path = '/trusteye_fixed.html'
        super().do_GET()

def open_browser_once():
    """Open browser only once after server starts"""
    time.sleep(2)
    webbrowser.open('http://localhost:8080')
    print("🌐 Browser opened: http://localhost:8080")

def start_server():
    PORT = 8080
    HOST = "127.0.0.1"
    
    # Check if --no-browser flag is passed
    auto_open = '--no-browser' not in sys.argv
    
    print("🚀 Starting TrustEye Server")
    print(f"📱 Access: http://localhost:{PORT}")
    if auto_open:
        print("✨ Opening browser...")
    print("🛑 Press Ctrl+C to stop")
    
    try:
        # Only open browser if not disabled
        if auto_open:
            browser_thread = threading.Thread(target=open_browser_once)
            browser_thread.daemon = True
            browser_thread.start()
        
        with socketserver.TCPServer((HOST, PORT), TrustEyeHandler) as httpd:
            print(f"✅ Server running on localhost:{PORT}")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 TrustEye server stopped!")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    start_server()
