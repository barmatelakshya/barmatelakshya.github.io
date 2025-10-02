#!/usr/bin/env python3
"""
TrustEye System Check & Cleanup
Comprehensive check for all files, glitches, and issues
"""
import os
import json
from pathlib import Path

def check_system():
    print("🔍 TrustEye System Check & Cleanup")
    print("=" * 50)
    
    issues = []
    fixes = []
    
    # Check main files
    main_files = {
        'trusteye_fixed.html': 'Main application (RECOMMENDED)',
        'trusteye_single.py': 'Single port server',
        'start_trusteye.sh': 'Startup script'
    }
    
    print("\n📁 Main Files Check:")
    for file, desc in main_files.items():
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size:,} bytes) - {desc}")
        else:
            print(f"❌ {file} - MISSING")
            issues.append(f"Missing {file}")
    
    # Check duplicate files
    print("\n🗂️ Duplicate Files Check:")
    duplicates = [
        'trusteye_dashboard.html',
        'trusteye_demo.html', 
        'trusteye.html',
        'trusteye_styled.py',
        'trusteye_simple.py',
        'trusteye_online.py',
        'trusteye_working.py'
    ]
    
    for dup in duplicates:
        if os.path.exists(dup):
            print(f"⚠️ {dup} - DUPLICATE (can be removed)")
            fixes.append(f"Remove duplicate: {dup}")
    
    # Check VS Code config
    print("\n⚙️ VS Code Configuration:")
    vscode_files = ['.vscode/launch.json', '.vscode/tasks.json', '.vscode/settings.json']
    for vscode_file in vscode_files:
        if os.path.exists(vscode_file):
            print(f"✅ {vscode_file}")
        else:
            print(f"❌ {vscode_file} - MISSING")
            issues.append(f"Missing VS Code config: {vscode_file}")
    
    # Check permissions
    print("\n🔐 Permissions Check:")
    executable_files = ['start_trusteye.sh', 'trusteye_single.py']
    for exe_file in executable_files:
        if os.path.exists(exe_file):
            if os.access(exe_file, os.X_OK):
                print(f"✅ {exe_file} - Executable")
            else:
                print(f"❌ {exe_file} - NOT Executable")
                issues.append(f"Fix permissions: {exe_file}")
    
    # Check HTML file integrity
    print("\n🌐 HTML File Check:")
    if os.path.exists('trusteye_fixed.html'):
        with open('trusteye_fixed.html', 'r') as f:
            content = f.read()
            
        checks = {
            'Chart.js CDN': 'chart.js' in content,
            'Bootstrap CDN': 'bootstrap' in content,
            'FontAwesome CDN': 'font-awesome' in content,
            'Dashboard section': 'id="dashboard"' in content,
            'Scanner section': 'id="scanner"' in content,
            'JavaScript functions': 'function analyzeThreat' in content,
            'LocalStorage': 'localStorage' in content
        }
        
        for check, passed in checks.items():
            if passed:
                print(f"✅ {check}")
            else:
                print(f"❌ {check} - MISSING")
                issues.append(f"HTML missing: {check}")
    
    # Summary
    print("\n📊 SYSTEM STATUS:")
    print(f"✅ Working files: {len([f for f in main_files.keys() if os.path.exists(f)])}/{len(main_files)}")
    print(f"⚠️ Issues found: {len(issues)}")
    print(f"🔧 Fixes available: {len(fixes)}")
    
    if issues:
        print("\n❌ ISSUES FOUND:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    
    if fixes:
        print("\n🔧 RECOMMENDED FIXES:")
        for i, fix in enumerate(fixes, 1):
            print(f"  {i}. {fix}")
    
    print("\n🎯 RECOMMENDED SETUP:")
    print("1. Use: trusteye_fixed.html (Main app)")
    print("2. Use: trusteye_single.py (Server)")
    print("3. Use: start_trusteye.sh (Startup)")
    print("4. Remove duplicate files")
    
    return len(issues) == 0

if __name__ == "__main__":
    os.chdir('/Users/barmate_lakshya/Documents/SIH_PS1')
    success = check_system()
    
    if success:
        print("\n🎉 SYSTEM CHECK PASSED!")
    else:
        print("\n⚠️ SYSTEM CHECK FOUND ISSUES!")
    
    print("\n🚀 To run TrustEye:")
    print("   ./start_trusteye.sh")
    print("   OR open trusteye_fixed.html directly")
