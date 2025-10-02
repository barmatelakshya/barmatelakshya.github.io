#!/usr/bin/env python3
"""
Test Script for NLP Phishing Classifier
SIH PS1 - Cybersecurity Threat Detector
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from backend.models.nlp_classifier import predict_phishing, get_classifier
import json

def load_test_data():
    """Load test data from JSON file"""
    try:
        with open('data/raw/phishing_dataset.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Test data file not found, using built-in samples")
        return {
            "phishing_samples": [
                {"text": "URGENT: Click here to verify your account now!", "label": "phishing"},
                {"text": "Congratulations! You've won $1000! Claim now!", "label": "phishing"}
            ],
            "legitimate_samples": [
                {"text": "Thank you for your purchase. Your order will arrive soon.", "label": "legitimate"},
                {"text": "Your appointment is confirmed for tomorrow at 2 PM.", "label": "legitimate"}
            ]
        }

def test_classifier():
    """Test the NLP classifier with sample data"""
    print("🧪 Testing NLP Phishing Classifier")
    print("=" * 50)
    
    # Get classifier info
    classifier = get_classifier()
    model_info = classifier.get_model_info()
    
    print(f"📊 Model Info:")
    print(f"  Model: {model_info['model_name']}")
    print(f"  Loaded: {model_info['is_loaded']}")
    print(f"  Method: {model_info['method']}")
    print()
    
    # Load test data
    test_data = load_test_data()
    
    # Test phishing samples
    print("🚨 Testing Phishing Samples:")
    print("-" * 30)
    
    for i, sample in enumerate(test_data['phishing_samples'], 1):
        text = sample['text']
        result = predict_phishing(text)
        
        print(f"Sample {i}: {text[:60]}...")
        print(f"  Prediction: {'✅ PHISHING' if result['is_phishing'] else '❌ SAFE'}")
        print(f"  Confidence: {result['confidence']:.2f}")
        print(f"  Risk Level: {result['risk_level']}")
        print(f"  Method: {result['method']}")
        
        if 'suspicious_keywords' in result:
            print(f"  Keywords: {result['suspicious_keywords']}")
        
        print()
    
    # Test legitimate samples
    print("✅ Testing Legitimate Samples:")
    print("-" * 30)
    
    for i, sample in enumerate(test_data['legitimate_samples'], 1):
        text = sample['text']
        result = predict_phishing(text)
        
        print(f"Sample {i}: {text[:60]}...")
        print(f"  Prediction: {'⚠️ PHISHING' if result['is_phishing'] else '✅ SAFE'}")
        print(f"  Confidence: {result['confidence']:.2f}")
        print(f"  Risk Level: {result['risk_level']}")
        print(f"  Method: {result['method']}")
        print()
    
    # Performance test
    print("⚡ Performance Test:")
    print("-" * 20)
    
    import time
    test_texts = ["This is a test message"] * 10
    
    start_time = time.time()
    results = classifier.batch_predict(test_texts)
    end_time = time.time()
    
    avg_time = (end_time - start_time) / len(test_texts)
    print(f"  Processed {len(test_texts)} texts in {end_time - start_time:.3f}s")
    print(f"  Average time per text: {avg_time * 1000:.1f}ms")
    print(f"  Throughput: {len(test_texts) / (end_time - start_time):.1f} texts/second")

def interactive_test():
    """Interactive testing mode"""
    print("\n🎯 Interactive Testing Mode")
    print("Enter text to analyze (or 'quit' to exit):")
    print("-" * 40)
    
    while True:
        try:
            text = input("\n📝 Enter text: ").strip()
            
            if text.lower() in ['quit', 'exit', 'q']:
                break
            
            if not text:
                continue
            
            result = predict_phishing(text)
            
            print(f"\n📊 Analysis Results:")
            print(f"  Text: {text}")
            print(f"  Prediction: {'🚨 PHISHING DETECTED' if result['is_phishing'] else '✅ APPEARS SAFE'}")
            print(f"  Confidence: {result['confidence']:.2f}")
            print(f"  Risk Level: {result['risk_level']}")
            print(f"  Method: {result['method']}")
            
            if 'suspicious_keywords' in result and result['suspicious_keywords']:
                print(f"  Suspicious Keywords: {', '.join(result['suspicious_keywords'])}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    # Run automated tests
    test_classifier()
    
    # Ask for interactive mode
    try:
        response = input("\n🤔 Run interactive test? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_test()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
