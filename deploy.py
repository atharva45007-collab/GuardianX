#!/usr/bin/env python3
"""
GuardianX Deployment Script
Handles deployment to various platforms with proper configuration.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if all deployment requirements are met"""
    print("🔍 Checking deployment requirements...")

    # Check if .env exists and has real keys
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found!")
        return False

    with open(env_file, 'r') as f:
        content = f.read()
        if 'your_' in content and '_here' in content:
            print("⚠️  .env contains placeholder keys!")
            return False

    print("✅ Environment configured")
    return True

def deploy_to_render():
    """Deploy to Render.com"""
    print("🚀 Deploying to Render.com...")

    if not check_requirements():
        print("❌ Fix requirements before deploying")
        return False

    print("📦 Preparing deployment package...")

    # Create deployment directory
    deploy_dir = Path('deploy')
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()

    # Copy necessary files
    files_to_copy = [
        'GuardianX-Backend/app.py',
        'requirements.txt',
        'README.md',
        '.env.example'
    ]

    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy(file, deploy_dir)

    # Create render.yaml for Render deployment
    render_yaml = """
services:
  - type: web
    name: guardianx-backend
    runtime: python3
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: FLASK_ENV
        value: production
      - key: NVIDIA_API_KEY
        sync: false
      - key: HIBP_API_KEY
        sync: false
"""

    with open(deploy_dir / 'render.yaml', 'w') as f:
        f.write(render_yaml)

    print("✅ Deployment package ready in 'deploy/' directory")
    print("📤 Upload the 'deploy/' folder to Render.com")
    return True

def deploy_locally():
    """Run locally for testing"""
    print("🏠 Running locally...")

    if not check_requirements():
        print("❌ Fix requirements before running")
        return False

    # Set environment variable for production mode
    os.environ['FLASK_ENV'] = 'production'

    # Run the app
    try:
        subprocess.run([sys.executable, 'GuardianX-Backend/app.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        return False

    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python deploy.py [local|render]")
        print("  local  - Run locally for testing")
        print("  render - Prepare for Render.com deployment")
        return 1

    command = sys.argv[1].lower()

    if command == 'local':
        return 0 if deploy_locally() else 1
    elif command == 'render':
        return 0 if deploy_to_render() else 1
    else:
        print(f"Unknown command: {command}")
        return 1

if __name__ == "__main__":
    sys.exit(main())