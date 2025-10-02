#!/usr/bin/env python3
"""
Test Backend API Connection
"""
import requests
import json
import time

API_BASE = "http://localhost:5000/api"

def test_connection():
    """Test basic API connection"""
    print("🔍 Testing Backend Connection...")
    
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is running: {data['service']} v{data['version']}")
            return True
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def test_analyze_endpoint():
    """Test the main analyze endpoint"""
    print("\n🔍 Testing /api/analyze endpoint...")
    
    test_cases = [
        {
            "name": "Phishing Text",
            "data": {
                "text": "URGENT! Your account will be suspended. Click here to verify now!",
                "url": ""
            }
        },
        {
            "name": "Suspicious URL",
            "data": {
                "text": "",
                "url": "http://192.168.1.100/login.php"
            }
        },
        {
            "name": "Combined Threat",
            "data": {
                "text": "Security alert! Verify at link below:",
                "url": "http://bit.ly/urgent-verify"
            }
        },
        {
            "name": "Safe Content",
            "data": {
                "text": "Thank you for your Amazon purchase",
                "url": "https://amazon.com"
            }
        }
    ]
    
    for case in test_cases:
        print(f"\n📋 Testing: {case['name']}")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{API_BASE}/analyze", 
                json=case['data'],
                timeout=10
            )
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success ({(end_time - start_time)*1000:.0f}ms)")
                print(f"   Risk Score: {result['combined_score']:.3f}")
                print(f"   Risk Level: {result['risk_level']}")
                print(f"   Is Threat: {result['is_threat']}")
                if result['threat_indicators']:
                    print(f"   Indicators: {', '.join(result['threat_indicators'][:3])}")
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")

def test_frontend_serving():
    """Test if frontend is being served"""
    print("\n🔍 Testing Frontend Serving...")
    
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200 and 'TrustEye' in response.text:
            print("✅ Frontend is being served correctly")
            return True
        else:
            print(f"❌ Frontend serving failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def test_cors():
    """Test CORS headers"""
    print("\n🔍 Testing CORS Configuration...")
    
    try:
        response = requests.options(f"{API_BASE}/analyze")
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
        }
        
        if cors_headers['Access-Control-Allow-Origin']:
            print("✅ CORS is configured")
            print(f"   Origin: {cors_headers['Access-Control-Allow-Origin']}")
        else:
            print("⚠️ CORS headers not found")
            
    except Exception as e:
        print(f"❌ CORS test failed: {e}")

def main():
    print("🧪 TrustEye Backend Connection Test")
    print("=" * 40)
    
    # Test connection first
    if not test_connection():
        print("\n❌ Backend is not running!")
        print("💡 Start it with: python backend_server.py")
        return
    
    # Run all tests
    test_analyze_endpoint()
    test_frontend_serving()
    test_cors()
    
    print("\n✅ Backend connection tests completed!")
    print("🌐 Access TrustEye at: http://localhost:5000")

if __name__ == "__main__":
    main()
