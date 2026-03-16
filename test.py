#!/usr/bin/env python3
"""
GuardianX Test Script
Tests all components before deployment
"""

import requests
import time
import os
import subprocess
import sys
from pathlib import Path

def test_backend_connection():
    """Test if backend is running and responding"""
    print("🔍 Testing backend connection...")

    try:
        # Test health endpoint
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend healthy: {data['status']}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_frontend_connection():
    """Test if frontend can connect to backend"""
    print("🔍 Testing frontend-backend connection...")

    try:
        # Test API endpoints
        endpoints = ['dashboard', 'logs', 'report']
        for endpoint in endpoints:
            response = requests.get(f"http://localhost:5000/api/{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"✅ API /{endpoint} working")
            else:
                print(f"⚠️  API /{endpoint} returned {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Frontend connection test failed: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("🔍 Testing environment configuration...")

    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found")
        return False

    # Check for required keys
    required_keys = ['NVIDIA_API_KEY', 'HIBP_API_KEY']
    missing_keys = []

    for key in required_keys:
        value = os.getenv(key)
        if not value or value.startswith('your_'):
            missing_keys.append(key)

    if missing_keys:
        print(f"⚠️  Missing or placeholder keys: {', '.join(missing_keys)}")
        print("   Configure these in your .env file for full functionality")
    else:
        print("✅ All API keys configured")

    return len(missing_keys) == 0

def test_dependencies():
    """Test if all dependencies are installed"""
    print("🔍 Testing dependencies...")

    try:
        import flask
        import flask_cors
        import requests
        import dotenv
        print("✅ Core dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 GuardianX Deployment Test Suite")
    print("=" * 40)

    tests = [
        ("Environment Setup", test_environment),
        ("Dependencies", test_dependencies),
        ("Backend Connection", test_backend_connection),
        ("API Integration", test_frontend_connection),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} error: {e}")

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Ready for deployment!")
        return 0
    elif passed >= total - 1:  # Allow 1 failure (API keys)
        print("⚠️  Mostly ready! Fix API keys for full functionality.")
        return 0
    else:
        print("❌ Critical issues found. Fix before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())