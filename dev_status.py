#!/usr/bin/env python3
"""
Development Environment Status Checker
"""
import sys
import subprocess
import pkg_resources
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return version.major >= 3 and version.minor >= 8

def check_virtual_env():
    """Check if virtual environment is active"""
    venv_active = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if venv_active:
        print(f"✅ Virtual Environment: {sys.prefix}")
    else:
        print("❌ Virtual Environment: Not activated")
    return venv_active

def check_packages():
    """Check installed packages"""
    required_packages = [
        'flask', 'requests', 'pandas', 'numpy', 
        'nltk', 'textblob', 'beautifulsoup4', 'scikit-learn'
    ]
    
    installed = []
    missing = []
    
    for package in required_packages:
        try:
            pkg_resources.get_distribution(package)
            installed.append(package)
            print(f"✅ {package}")
        except pkg_resources.DistributionNotFound:
            missing.append(package)
            print(f"❌ {package}")
    
    return len(missing) == 0

def check_git_repo():
    """Check Git repository status"""
    git_dir = Path('.git')
    if git_dir.exists():
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            print(f"✅ Git Repository: Initialized")
            if result.stdout.strip():
                print(f"📝 Uncommitted changes: {len(result.stdout.strip().split())}")
            else:
                print("✅ Working directory clean")
            return True
        except:
            print("❌ Git: Command failed")
            return False
    else:
        print("❌ Git Repository: Not initialized")
        return False

def main():
    print("🔍 SIH PS1 Development Environment Status\n")
    
    checks = [
        ("Python Version", check_python_version()),
        ("Virtual Environment", check_virtual_env()),
        ("Required Packages", check_packages()),
        ("Git Repository", check_git_repo())
    ]
    
    print(f"\n📊 Status Summary:")
    passed = sum(1 for _, status in checks if status)
    total = len(checks)
    
    for name, status in checks:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {name}")
    
    print(f"\n🎯 Overall: {passed}/{total} checks passed")
    
    if passed == total:
        print("🚀 Development environment is ready!")
        print("💡 Run: python mvp_app.py")
    else:
        print("⚠️  Please fix the issues above")

if __name__ == "__main__":
    main()
