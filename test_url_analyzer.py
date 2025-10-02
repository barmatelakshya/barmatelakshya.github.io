#!/usr/bin/env python3
"""
Test Script for URL Analyzer
SIH PS1 - Cybersecurity Threat Detector
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from backend.models.url_analyzer import analyze_url, get_analyzer

def test_url_analyzer():
    """Test the URL analyzer with various URLs"""
    print("🔗 Testing Advanced URL Analyzer")
    print("=" * 50)
    
    # Test URLs
    test_urls = [
        # Suspicious URLs
        {
            'url': 'http://192.168.1.100/login.php',
            'description': 'IP address with login page',
            'expected_risk': 'High'
        },
        {
            'url': 'http://bit.ly/suspicious-link',
            'description': 'URL shortener',
            'expected_risk': 'Medium'
        },
        {
            'url': 'http://secure-bank-verify-account-update.suspicious-domain.com/urgent-login',
            'description': 'Suspicious domain with keywords',
            'expected_risk': 'High'
        },
        {
            'url': 'http://paypal-security-update.fake-domain.com/verify?token=aGVsbG93b3JsZA==',
            'description': 'Fake PayPal with Base64',
            'expected_risk': 'High'
        },
        
        # Legitimate URLs
        {
            'url': 'https://amazon.com/orders',
            'description': 'Legitimate Amazon URL',
            'expected_risk': 'Low'
        },
        {
            'url': 'https://github.com/microsoft/vscode',
            'description': 'GitHub repository',
            'expected_risk': 'Low'
        },
        {
            'url': 'https://stackoverflow.com/questions/tagged/python',
            'description': 'Stack Overflow',
            'expected_risk': 'Low'
        }
    ]
    
    print("🧪 Running URL Analysis Tests:")
    print("-" * 40)
    
    for i, test_case in enumerate(test_urls, 1):
        url = test_case['url']
        description = test_case['description']
        expected_risk = test_case['expected_risk']
        
        print(f"\nTest {i}: {description}")
        print(f"URL: {url}")
        
        try:
            result = analyze_url(url)
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                continue
            
            risk_score = result.get('risk_score', 0)
            risk_level = result.get('risk_level', 'Unknown')
            
            print(f"Risk Score: {risk_score:.2f}")
            print(f"Risk Level: {risk_level}")
            print(f"Expected: {expected_risk}")
            
            # Check if result matches expectation
            if ((expected_risk == 'High' and risk_score >= 0.7) or
                (expected_risk == 'Medium' and 0.4 <= risk_score < 0.7) or
                (expected_risk == 'Low' and risk_score < 0.4)):
                print("✅ Result matches expectation")
            else:
                print("⚠️ Result differs from expectation")
            
            # Show key findings
            if result.get('risk_factors'):
                print("Risk Factors:")
                for factor in result['risk_factors'][:3]:  # Show top 3
                    print(f"  • {factor}")
            
            # Show redirections if any
            if result.get('redirections'):
                print(f"Redirections: {len(result['redirections'])} found")
            
            # Show domain age if available
            if result.get('domain_age'):
                print(f"Domain Age: {result['domain_age']}")
            
            print(f"Recommendation: {result.get('recommendation', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print("\n" + "=" * 50)

def interactive_test():
    """Interactive URL testing"""
    print("\n🎯 Interactive URL Testing")
    print("Enter URLs to analyze (or 'quit' to exit):")
    print("-" * 40)
    
    while True:
        try:
            url = input("\n🔗 Enter URL: ").strip()
            
            if url.lower() in ['quit', 'exit', 'q']:
                break
            
            if not url:
                continue
            
            print("🔄 Analyzing URL...")
            result = analyze_url(url)
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                continue
            
            print(f"\n📊 Analysis Results for: {url}")
            print("-" * 60)
            print(f"Domain: {result.get('domain', 'N/A')}")
            print(f"Risk Score: {result.get('risk_score', 0):.2f}")
            print(f"Risk Level: {result.get('risk_level', 'Unknown')}")
            print(f"Confidence: {result.get('confidence', 0):.2f}")
            
            if result.get('domain_age'):
                print(f"Domain Age: {result['domain_age']}")
            
            if result.get('ip_addresses'):
                print(f"IP Addresses: {', '.join(result['ip_addresses'])}")
            
            if result.get('redirections'):
                print(f"Redirections: {len(result['redirections'])} found")
                for i, redirect in enumerate(result['redirections'][:2], 1):
                    print(f"  {i}. {redirect['from']} → {redirect['to']} ({redirect['status']})")
            
            print(f"\n🎯 Recommendation: {result.get('recommendation', 'N/A')}")
            
            if result.get('risk_factors'):
                print(f"\n⚠️ Risk Factors ({len(result['risk_factors'])}):")
                for factor in result['risk_factors']:
                    print(f"  • {factor}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n👋 Goodbye!")

def performance_test():
    """Test analyzer performance"""
    print("\n⚡ Performance Test")
    print("-" * 20)
    
    import time
    
    test_urls = [
        'https://google.com',
        'https://amazon.com',
        'http://bit.ly/test',
        'http://192.168.1.1',
        'https://github.com'
    ]
    
    start_time = time.time()
    
    for url in test_urls:
        try:
            result = analyze_url(url)
            print(f"✅ {url} - Risk: {result.get('risk_score', 0):.2f}")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / len(test_urls)
    
    print(f"\n📊 Performance Results:")
    print(f"Total Time: {total_time:.2f}s")
    print(f"Average per URL: {avg_time:.2f}s")
    print(f"Throughput: {len(test_urls)/total_time:.1f} URLs/second")

if __name__ == "__main__":
    # Run automated tests
    test_url_analyzer()
    
    # Performance test
    performance_test()
    
    # Ask for interactive mode
    try:
        response = input("\n🤔 Run interactive test? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_test()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
