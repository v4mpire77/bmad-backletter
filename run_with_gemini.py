#!/usr/bin/env python3
"""
CLI script to run the Blackletter API with Gemini AI integration
"""

import os
import sys
import subprocess
from pathlib import Path


def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'google-generativeai',
        'pydantic-settings'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
            ])
            print("✅ Packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run: pip install -r requirements.txt")
            return False

    return True


def check_env_file():
    """Check if .env file exists and has Gemini configuration"""
    env_file = Path('.env')

    if not env_file.exists():
        print("⚠️  .env file not found!")
        print("📝 Creating .env file with default configuration...")
        create_env_file()
        print("✅ .env file created!")
        print("🔑 Please add your Gemini API key to the .env file")
        return False

    # Check if Gemini API key is configured
    with open(env_file, 'r') as f:
        content = f.read()

    if 'your_gemini_api_key_here' in content:
        print("⚠️  Gemini API key not configured!")
        print("🔑 Please set your GEMINI_API_KEY in the .env file")
        print("   Get your key from: https://makersuite.google.com/app/apikey")
        return False

    return True


def create_env_file():
    """Create .env file with default configuration"""
    env_content = """# Database Configuration
DATABASE_URL=sqlite:///./blackletter.db

# CORS Configuration
CORS_ORIGINS=*

# Gemini AI Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=2048
GEMINI_TEMPERATURE=0.7

# Logging Configuration
LOG_LEVEL=INFO

# Security Configuration
SECRET_KEY=your-secret-key-change-this-in-production
"""

    with open('.env', 'w') as f:
        f.write(env_content)


def run_api():
    """Run the FastAPI server"""
    print("🚀 Starting Blackletter API with Gemini AI integration...")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    print()

    try:
        # Change to API directory
        api_dir = Path('apps/api')
        if api_dir.exists():
            os.chdir(api_dir)

        # Run uvicorn
        subprocess.run([
            sys.executable, '-m', 'uvicorn',
            'blackletter_api.main:app',
            '--reload',
            '--host', '0.0.0.0',
            '--port', '8000'
        ])

    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

    return True


def main():
    """Main CLI function"""
    print("🤖 Blackletter API with Gemini AI Integration")
    print("=" * 50)

    # Check requirements
    if not check_requirements():
        return 1

    # Check environment configuration
    if not check_env_file():
        print("\n💡 To continue:")
        print("1. Get your Gemini API key from: https://makersuite.google.com/app/apikey")
        print("2. Add it to the .env file: GEMINI_API_KEY=your_actual_key_here")
        print("3. Run this script again")
        return 1

    # Run the API
    success = run_api()

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
