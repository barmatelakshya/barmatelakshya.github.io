#!/usr/bin/env python3
"""
TrustEye API Test Script
"""
import requests
import json
import time

API_BASE = "http://localhost:5000/api"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing Health Endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_single_analysis():
    """Test single threat analysis"""
    print("\n🔍 Testing Single Analysis...")
    
    test_cases = [
        {
            "name": "Phishing Text + Suspicious URL",
            "data": {
                "text": "URGENT! Your account will be suspended. Click here to verify: http://secure-bank.fake-domain.com",
                "url": "http://192.168.1.100/verify"
            }
        },
        {
            "name": "Safe Text + Safe URL",
            "data": {
                "text": "Thank you for your Amazon purchase",
                "url": "https://amazon.com/orders"
            }
        },
        {
            "name": "Text Only",
            "data": {
                "text": "Congratulations! You've won $1000! Click to claim!"
            }
        },
        {
            "name": "URL Only",
            "data": {
                "url": "http://bit.ly/suspicious-link"
            }
        }
    ]
    
    for case in test_cases:
        print(f"\n📋 Test: {case['name']}")
        try:
            response = requests.post(f"{API_BASE}/analyze", json=case['data'])
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success")
                print(f"  Combined Score: {result['combined_score']:.3f}")
                print(f"  Risk Level: {result['risk_level']}")
                print(f"  Is Threat: {result['is_threat']}")
                print(f"  Indicators: {result['threat_indicators'][:3]}")
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"  Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")

def test_batch_analysis():
    """Test batch analysis"""
    print("\n🔍 Testing Batch Analysis...")
    
    batch_data = {
        "items": [
            {"text": "URGENT! Verify now!", "url": ""},
            {"text": "", "url": "http://192.168.1.1/login"},
            {"text": "Thank you for purchase", "url": "https://amazon.com"},
            {"text": "Click here to claim prize!", "url": "http://bit.ly/prize"}
        ]
    }
    
    try:
        response = requests.post(f"{API_BASE}/batch-analyze", json=batch_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Batch analysis successful")
            print(f"  Processed: {result['count']} items")
            
            for i, item_result in enumerate(result['results'], 1):
                print(f"  Item {i}: Score={item_result['combined_score']:.3f}, Risk={item_result['risk_level']}")
        else:
            print(f"❌ Batch analysis failed: {response.status_code}")
            print(f"  Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Batch request failed: {e}")

def test_error_handling():
    """Test error handling"""
    print("\n🔍 Testing Error Handling...")
    
    # Test empty request
    try:
        response = requests.post(f"{API_BASE}/analyze", json={})
        print(f"Empty request: {response.status_code} - {response.json().get('error', 'No error')}")
    except Exception as e:
        print(f"❌ Empty request test failed: {e}")
    
    # Test invalid endpoint
    try:
        response = requests.get(f"{API_BASE}/invalid")
        print(f"Invalid endpoint: {response.status_code} - {response.json().get('error', 'No error')}")
    except Exception as e:
        print(f"❌ Invalid endpoint test failed: {e}")

def test_performance():
    """Test API performance"""
    print("\n🔍 Testing Performance...")
    
    test_data = {
        "text": "URGENT security alert! Verify your account now!",
        "url": "http://suspicious-domain.com/verify"
    }
    
    times = []
    for i in range(5):
        start_time = time.time()
        try:
            response = requests.post(f"{API_BASE}/analyze", json=test_data)
            end_time = time.time()
            
            if response.status_code == 200:
                times.append(end_time - start_time)
                print(f"  Request {i+1}: {(end_time - start_time)*1000:.1f}ms")
            else:
                print(f"  Request {i+1}: Failed")
                
        except Exception as e:
            print(f"  Request {i+1}: Error - {e}")
    
    if times:
        avg_time = sum(times) / len(times)
        print(f"📊 Average response time: {avg_time*1000:.1f}ms")
        print(f"📊 Throughput: {1/avg_time:.1f} requests/second")

def main():
    print("🧪 TrustEye API Test Suite")
    print("=" * 40)
    
    # Test health first
    if not test_health():
        print("❌ API is not running. Start with: python trusteye_api.py")
        return
    
    # Run all tests
    test_single_analysis()
    test_batch_analysis()
    test_error_handling()
    test_performance()
    
    print("\n✅ All API tests completed!")

if __name__ == "__main__":
    main()
