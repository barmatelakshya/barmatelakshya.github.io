#!/usr/bin/env python3
"""
Test Script for Combined Threat Analyzer
SIH PS1 - Cybersecurity Threat Detector
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from backend.models.combined_analyzer import analyze_input, get_combined_analyzer

def test_combined_analyzer():
    """Test the combined threat analyzer"""
    print("🔥 Testing Combined Threat Analyzer")
    print("=" * 50)
    
    # Get analyzer info
    analyzer = get_combined_analyzer()
    info = analyzer.get_analyzer_info()
    
    print(f"📊 Analyzer Info:")
    print(f"  Version: {info['version']}")
    print(f"  Components: {', '.join(info['components'])}")
    print(f"  Weights: Text={info['weights']['text_weight']}, URL={info['weights']['url_weight']}")
    print()
    
    # Test cases
    test_cases = [
        {
            'name': 'High Risk: Phishing Text + Suspicious URL',
            'text': 'URGENT SECURITY ALERT! Your account will be suspended in 24 hours. Click here to verify: http://secure-bank-verify.fake-domain.com/urgent-login',
            'url': 'http://secure-bank-verify.fake-domain.com/urgent-login',
            'expected_risk': 'Critical/High'
        },
        {
            'name': 'Medium Risk: Phishing Text Only',
            'text': 'Congratulations! You have won $1,000,000 in our lottery! Click to claim your prize now!',
            'url': '',
            'expected_risk': 'Medium/High'
        },
        {
            'name': 'Medium Risk: Suspicious URL Only',
            'text': '',
            'url': 'http://192.168.1.100/login.php?redirect=bank-verify',
            'expected_risk': 'Medium/High'
        },
        {
            'name': 'Low Risk: Safe Text + Safe URL',
            'text': 'Thank you for your Amazon purchase. Your order will arrive soon.',
            'url': 'https://amazon.com/orders',
            'expected_risk': 'Low'
        },
        {
            'name': 'Text with Embedded URL',
            'text': 'Your PayPal account needs verification. Please visit http://bit.ly/paypal-verify to update your information.',
            'url': '',
            'expected_risk': 'Medium/High'
        },
        {
            'name': 'Empty Input',
            'text': '',
            'url': '',
            'expected_risk': 'Error'
        }
    ]
    
    print("🧪 Running Combined Analysis Tests:")
    print("-" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        name = test_case['name']
        text = test_case['text']
        url = test_case['url']
        expected = test_case['expected_risk']
        
        print(f"\nTest {i}: {name}")
        print(f"Text: {text[:60]}{'...' if len(text) > 60 else ''}")
        print(f"URL: {url}")
        print(f"Expected: {expected}")
        
        try:
            result = analyze_input(text, url)
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                continue
            
            combined_score = result.get('combined_score', 0)
            risk_level = result.get('risk_level', 'Unknown')
            confidence = result.get('confidence', 0)
            is_threat = result.get('is_threat', False)
            
            print(f"📊 Results:")
            print(f"  Combined Score: {combined_score:.3f}")
            print(f"  Risk Level: {risk_level}")
            print(f"  Confidence: {confidence:.3f}")
            print(f"  Threat Detected: {'Yes' if is_threat else 'No'}")
            
            # Show input types analyzed
            input_types = result.get('input_types', [])
            print(f"  Analyzed: {', '.join(input_types)}")
            
            # Show individual scores
            individual = result.get('individual_results', {})
            if 'text' in individual:
                text_conf = individual['text'].get('confidence', 0)
                print(f"  Text Score: {text_conf:.3f}")
            if 'url' in individual:
                url_score = individual['url'].get('risk_score', 0)
                print(f"  URL Score: {url_score:.3f}")
            
            # Show top threat indicators
            indicators = result.get('threat_indicators', [])
            if indicators:
                print(f"  Top Threats: {', '.join(indicators[:2])}")
            
            # Show final recommendation
            final_rec = result.get('final_recommendation', '')
            print(f"  Recommendation: {final_rec}")
            
            # Check if result matches expectation
            if expected == 'Error':
                print("✅ Error handling works correctly")
            elif 'Critical' in expected and risk_level == 'Critical':
                print("✅ Critical risk detected correctly")
            elif 'High' in expected and risk_level in ['High', 'Critical']:
                print("✅ High risk detected correctly")
            elif 'Medium' in expected and risk_level in ['Medium', 'High']:
                print("✅ Medium risk detected correctly")
            elif 'Low' in expected and risk_level in ['Low', 'Very Low']:
                print("✅ Low risk detected correctly")
            else:
                print(f"⚠️ Result ({risk_level}) differs from expected ({expected})")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print("\n" + "=" * 50)

def test_batch_analysis():
    """Test batch analysis functionality"""
    print("\n📦 Testing Batch Analysis")
    print("-" * 30)
    
    batch_inputs = [
        {'text': 'URGENT: Verify your account now!', 'url': ''},
        {'text': '', 'url': 'http://192.168.1.1/login'},
        {'text': 'Thank you for your purchase', 'url': 'https://amazon.com'},
        {'text': 'Click here to claim prize!', 'url': 'http://bit.ly/prize'}
    ]
    
    analyzer = get_combined_analyzer()
    results = analyzer.batch_analyze(batch_inputs)
    
    print(f"Processed {len(results)} inputs:")
    for i, result in enumerate(results, 1):
        score = result.get('combined_score', 0)
        risk = result.get('risk_level', 'Unknown')
        print(f"  {i}. Score: {score:.3f}, Risk: {risk}")

def performance_test():
    """Test analyzer performance"""
    print("\n⚡ Performance Test")
    print("-" * 20)
    
    import time
    
    test_inputs = [
        ('Urgent security alert!', 'http://suspicious.com'),
        ('Thank you for purchase', 'https://amazon.com'),
        ('Click here now!', 'http://bit.ly/test'),
        ('Your order shipped', 'https://fedex.com'),
        ('Account suspended!', 'http://192.168.1.1')
    ]
    
    start_time = time.time()
    
    for text, url in test_inputs:
        result = analyze_input(text, url)
        score = result.get('combined_score', 0)
        print(f"✅ {text[:20]}... + {url[:20]}... → {score:.3f}")
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / len(test_inputs)
    
    print(f"\n📊 Performance Results:")
    print(f"Total Time: {total_time:.2f}s")
    print(f"Average per Analysis: {avg_time:.2f}s")
    print(f"Throughput: {len(test_inputs)/total_time:.1f} analyses/second")

def interactive_test():
    """Interactive testing mode"""
    print("\n🎯 Interactive Combined Analysis")
    print("Enter text and/or URL to analyze (or 'quit' to exit):")
    print("-" * 50)
    
    while True:
        try:
            print("\n📝 Enter content to analyze:")
            text = input("Text (or press Enter to skip): ").strip()
            url = input("URL (or press Enter to skip): ").strip()
            
            if not text and not url:
                response = input("No input provided. Quit? (y/n): ").strip().lower()
                if response in ['y', 'yes', 'quit', 'q']:
                    break
                continue
            
            print("\n🔄 Analyzing combined input...")
            result = analyze_input(text, url)
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                continue
            
            print(f"\n🎯 Combined Analysis Results:")
            print("-" * 40)
            print(f"Combined Score: {result.get('combined_score', 0):.3f}")
            print(f"Risk Level: {result.get('risk_level', 'Unknown')}")
            print(f"Threat Detected: {'Yes' if result.get('is_threat') else 'No'}")
            print(f"Confidence: {result.get('confidence', 0):.3f}")
            
            # Show analyzed components
            input_types = result.get('input_types', [])
            print(f"Analyzed Components: {', '.join(input_types)}")
            
            # Show threat indicators
            indicators = result.get('threat_indicators', [])
            if indicators:
                print(f"\n⚠️ Threat Indicators:")
                for indicator in indicators:
                    print(f"  • {indicator}")
            
            # Show final recommendation
            final_rec = result.get('final_recommendation', '')
            print(f"\n🎯 Final Recommendation:")
            print(f"  {final_rec}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    # Run automated tests
    test_combined_analyzer()
    
    # Batch analysis test
    test_batch_analysis()
    
    # Performance test
    performance_test()
    
    # Ask for interactive mode
    try:
        response = input("\n🤔 Run interactive test? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_test()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
