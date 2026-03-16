#!/usr/bin/env python3
"""
GuardianX Security Audit Script
Checks for common security issues and configuration problems.
"""

import os
import sys
from pathlib import Path

def check_env_security():
    """Check .env file security"""
    print("🔍 Checking environment security...")

    env_file = Path('.env')
    env_example = Path('.env.example')

    if not env_file.exists():
        print("❌ .env file not found!")
        return False

    if not env_example.exists():
        print("❌ .env.example file not found!")
        return False

    # Check if .env is in .gitignore
    gitignore = Path('.gitignore')
    if gitignore.exists():
        with open(gitignore, 'r') as f:
            if '.env' not in f.read():
                print("⚠️  .env not found in .gitignore!")
            else:
                print("✅ .env properly ignored in .gitignore")

    # Check for placeholder values
    with open(env_file, 'r') as f:
        content = f.read()
        if 'your_' in content and '_here' in content:
            print("⚠️  Placeholder API keys detected in .env")
        else:
            print("✅ No placeholder keys found")

    return True

def check_dependencies():
    """Check for security-related dependencies"""
    print("\n🔍 Checking dependencies...")

    try:
        import flask
        import flask_cors
        import requests
        import python_dotenv
        print("✅ Core dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

    return True

def check_database_security():
    """Check database file permissions"""
    print("\n🔍 Checking database security...")

    db_file = Path('guardianx.db')
    if db_file.exists():
        # Check if database is readable by others (basic check)
        import stat
        st = db_file.stat()
        if st.st_mode & stat.S_IRGRP or st.st_mode & stat.S_IROTH:
            print("⚠️  Database file is readable by group/others")
        else:
            print("✅ Database file has appropriate permissions")
    else:
        print("ℹ️  Database not yet created")

    return True

def main():
    """Run all security checks"""
    print("🛡️  GuardianX Security Audit")
    print("=" * 40)

    checks = [
        check_env_security,
        check_dependencies,
        check_database_security
    ]

    passed = 0
    for check in checks:
        try:
            if check():
                passed += 1
        except Exception as e:
            print(f"❌ Error during check: {e}")

    print(f"\n📊 Audit Results: {passed}/{len(checks)} checks passed")

    if passed == len(checks):
        print("🎉 All security checks passed!")
        return 0
    else:
        print("⚠️  Some security issues found. Please address them before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())