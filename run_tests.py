#!/usr/bin/env python3
"""
Test Runner for SIH PS1 Cybersecurity Threat Detector
"""
import sys
import subprocess
from pathlib import Path

def run_tests():
    """Run all test suites"""
    print("🧪 Running SIH PS1 Test Suite")
    print("=" * 50)
    
    # Change to project directory
    project_root = Path(__file__).parent
    
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', 
            '-v',
            '--tb=short',
            '--color=yes'
        ], cwd=project_root, capture_output=True, text=True)
        
        print("📊 Test Results:")
        print("-" * 30)
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
            
        return result.returncode == 0
        
    except FileNotFoundError:
        print("❌ pytest not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pytest'])
        return run_tests()
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def run_individual_tests():
    """Run individual test modules"""
    test_modules = [
        'tests/test_nlp_classifier.py',
        'tests/test_url_analyzer.py', 
        'tests/test_combined_analyzer.py',
        'tests/test_integration.py'
    ]
    
    print("🔍 Running Individual Test Modules")
    print("=" * 40)
    
    results = {}
    
    for module in test_modules:
        print(f"\n📋 Testing {module}...")
        
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pytest', 
                module, 
                '-v'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {module} - PASSED")
                results[module] = 'PASSED'
            else:
                print(f"❌ {module} - FAILED")
                results[module] = 'FAILED'
                print(result.stdout[-200:])  # Show last 200 chars
                
        except Exception as e:
            print(f"❌ {module} - ERROR: {e}")
            results[module] = 'ERROR'
    
    print("\n📊 Summary:")
    print("-" * 20)
    for module, status in results.items():
        status_icon = "✅" if status == "PASSED" else "❌"
        print(f"{status_icon} {module}: {status}")
    
    passed = sum(1 for status in results.values() if status == 'PASSED')
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} test modules passed")
    
    return passed == total

if __name__ == "__main__":
    print("🚀 SIH PS1 Test Runner")
    print("Choose test mode:")
    print("1. Run all tests (recommended)")
    print("2. Run individual test modules")
    print("3. Quick smoke test")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            success = run_tests()
        elif choice == "2":
            success = run_individual_tests()
        elif choice == "3":
            print("🔥 Running quick smoke test...")
            # Quick test
            from backend.models.combined_analyzer import analyze_input
            result = analyze_input(text="Test message")
            print(f"✅ Smoke test passed: {result.get('combined_score', 0):.3f}")
            success = True
        else:
            print("Invalid choice. Running all tests...")
            success = run_tests()
        
        if success:
            print("\n🎉 All tests completed successfully!")
            sys.exit(0)
        else:
            print("\n⚠️ Some tests failed. Check output above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n👋 Test run cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test runner error: {e}")
        sys.exit(1)
