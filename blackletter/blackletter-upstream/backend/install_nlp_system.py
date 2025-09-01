#!/usr/bin/env python3
"""
NLP System Installation Script
Automates the installation and setup of the NLP system.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_step(step, description):
    """Print a step with description"""
    print(f"\n{step}. {description}")

def run_command(command, description, check=True):
    """Run a command and handle errors"""
    print(f"   Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error: {e}")
        if e.stderr:
            print(f"   Error output: {e.stderr.strip()}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print_step("1", "Checking Python version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"   ❌ Python {version.major}.{version.minor} is not supported.")
        print("   Please install Python 3.8 or higher.")
        return False
    
    print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_pip():
    """Check if pip is available"""
    print_step("2", "Checking pip availability")
    
    if shutil.which("pip") is None:
        print("   ❌ pip is not found. Please install pip first.")
        return False
    
    print("   ✅ pip is available")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print_step("3", "Installing Python dependencies")
    
    # Check if requirements.txt exists
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("   ❌ requirements.txt not found in current directory")
        return False
    
    # Install dependencies
    success = run_command("pip install -r requirements.txt", "Installing dependencies from requirements.txt")
    
    if success:
        print("   ✅ Dependencies installed successfully")
    else:
        print("   ❌ Failed to install dependencies")
    
    return success

def download_spacy_model():
    """Download spaCy model"""
    print_step("4", "Downloading spaCy model")
    
    success = run_command("python -m spacy download en_core_web_sm", "Downloading spaCy English model")
    
    if success:
        print("   ✅ spaCy model downloaded successfully")
    else:
        print("   ⚠️  spaCy model download failed (will be downloaded on first use)")
    
    return success

def download_nltk_data():
    """Download NLTK data"""
    print_step("5", "Downloading NLTK data")
    
    nltk_script = """
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)
print("NLTK data downloaded successfully")
"""
    
    try:
        result = subprocess.run([sys.executable, "-c", nltk_script], 
                              capture_output=True, text=True, check=True)
        print("   ✅ NLTK data downloaded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️  NLTK data download failed: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print_step("6", "Testing imports")
    
    test_script = """
try:
    import torch
    import transformers
    import spacy
    import nltk
    import pandas
    import numpy
    import sklearn
    import sentence_transformers
    print("✅ All core dependencies imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)
"""
    
    try:
        result = subprocess.run([sys.executable, "-c", test_script], 
                              capture_output=True, text=True, check=True)
        print("   ✅ All dependencies imported successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Import test failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False

def test_nlp_engine():
    """Test NLP engine initialization"""
    print_step("7", "Testing NLP engine initialization")
    
    test_script = """
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

try:
    from app.core.nlp_engine import NLPEngine
    nlp = NLPEngine()
    print(f"✅ NLP Engine initialized successfully on device: {nlp.device}")
except Exception as e:
    print(f"❌ NLP Engine initialization failed: {e}")
    exit(1)
"""
    
    try:
        result = subprocess.run([sys.executable, "-c", test_script], 
                              capture_output=True, text=True, check=True)
        print("   ✅ NLP Engine initialized successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ NLP Engine test failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False

def create_directories():
    """Create necessary directories"""
    print_step("8", "Creating necessary directories")
    
    directories = [
        "models",
        "corpus_data",
        "corpus_data/raw",
        "corpus_data/processed",
        "corpus_data/metadata",
        "corpus_data/uploads"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created directory: {directory}")
    
    return True

def run_quick_test():
    """Run a quick functionality test"""
    print_step("9", "Running quick functionality test")
    
    test_script = """
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

try:
    from app.core.nlp_engine import NLPEngine
    
    # Initialize engine
    nlp = NLPEngine()
    
    # Test basic functionality
    test_text = "Natural Language Processing is amazing!"
    
    # Sentiment analysis
    sentiment = nlp.analyze_sentiment(test_text)
    print(f"✅ Sentiment analysis: {sentiment}")
    
    # Keyword extraction
    keywords = nlp.extract_keywords(test_text)
    print(f"✅ Keyword extraction: {len(keywords)} keywords found")
    
    # Readability analysis
    readability = nlp.analyze_readability(test_text)
    print(f"✅ Readability analysis: {readability['flesch_reading_ease']:.1f}")
    
    print("✅ All basic functionality tests passed")
    
except Exception as e:
    print(f"❌ Functionality test failed: {e}")
    exit(1)
"""
    
    try:
        result = subprocess.run([sys.executable, "-c", test_script], 
                              capture_output=True, text=True, check=True)
        print("   ✅ Functionality test passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Functionality test failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print_step("10", "Installation complete!")
    
    print("\n🎉 NLP System installation completed successfully!")
    print("\nNext steps:")
    print("1. Run the quick start demo:")
    print("   python quick_start_nlp.py")
    print("\n2. Try the command line interface:")
    print("   python scripts/nlp_cli.py demo")
    print("\n3. Start the API server:")
    print("   uvicorn main:app --reload")
    print("   Then visit: http://localhost:8000/docs")
    print("\n4. Run tests:")
    print("   python tests/test_nlp_system.py")
    print("\n5. Read documentation:")
    print("   NLP_SYSTEM_README.md")
    print("\n6. Collect your first corpus:")
    print("   python scripts/nlp_cli.py corpus collect --sources news wikipedia --query 'artificial intelligence'")

def main():
    """Main installation function"""
    print_header("NLP System Installation")
    
    print("This script will install and configure the NLP system.")
    print("Make sure you have Python 3.8+ and pip installed.")
    
    # Check if running in the correct directory
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found. Please run this script from the backend directory.")
        return 1
    
    input("\nPress Enter to continue with installation...")
    
    # Run installation steps
    steps = [
        check_python_version,
        check_pip,
        install_dependencies,
        download_spacy_model,
        download_nltk_data,
        test_imports,
        test_nlp_engine,
        create_directories,
        run_quick_test
    ]
    
    failed_steps = []
    
    for step_func in steps:
        if not step_func():
            failed_steps.append(step_func.__name__)
    
    if failed_steps:
        print(f"\n❌ Installation failed at steps: {', '.join(failed_steps)}")
        print("Please check the errors above and try again.")
        return 1
    
    show_next_steps()
    return 0

if __name__ == "__main__":
    exit(main())
