#!/bin/bash

# Jules Setup Script for Blackletter BMAD Project
# This script sets up the complete development environment for the Blackletter contract analysis platform

set -e  # Exit on any error

echo "🚀 Jules Environment Setup for Blackletter BMAD Project"
echo "========================================================="

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Not in project root directory"
    echo "Expected files: package.json, requirements.txt"
    exit 1
fi

echo "✅ Project root verified"

# 1. Install Node.js dependencies (pnpm workspace)
echo ""
echo "📦 Installing Node.js dependencies with pnpm..."
if ! command -v pnpm &> /dev/null; then
    echo "Installing pnpm..."
    npm install -g pnpm
fi

# Install all workspace dependencies
pnpm install

echo "✅ Node.js dependencies installed"

# 2. Set up Python environment
echo ""
echo "🐍 Setting up Python environment..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment and install dependencies
source .venv/bin/activate
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Python environment configured"

# 3. Install BMAD Method dependencies
echo ""
echo "🧙 Setting up BMAD Method..."

# Copy BMAD core files to accessible location
if [ -d "BMAD-METHOD-main" ]; then
    echo "BMAD Method files found"
    # Ensure bmad-core is accessible
    if [ ! -L "bmad-core" ] && [ -d "BMAD-METHOD-main/bmad-core" ]; then
        ln -sf BMAD-METHOD-main/bmad-core bmad-core
        echo "✅ BMAD core linked"
    fi
else
    echo "⚠️  BMAD Method not found - some functionality may be limited"
fi

# 4. Build Next.js application
echo ""
echo "🌐 Building Next.js web application..."
cd apps/web
pnpm build
cd ../..

echo "✅ Web application built"

# 5. Run tests to validate setup
echo ""
echo "🧪 Running validation tests..."

# Run Python tests
echo "Testing Python backend..."
source .venv/bin/activate
python -m pytest -xvs || echo "⚠️  Some Python tests failed - continuing..."

# Run Node.js tests
echo "Testing Node.js components..."
pnpm test || echo "⚠️  Some Node.js tests failed - continuing..."

# 6. Validate BMAD agents
echo ""
echo "🤖 Validating BMAD agents..."

if [ -f "bmad-core/agents/sm.md" ]; then
    echo "✅ Scrum Master agent available"
fi

if [ -f "bmad-core/agents/dev.md" ]; then
    echo "✅ Developer agent available"
fi

if [ -f "bmad-core/agents/qa.md" ]; then
    echo "✅ QA agent available"
fi

if [ -f "bmad-core/agents/po.md" ]; then
    echo "✅ Product Owner agent available"
fi

# 7. Environment summary
echo ""
echo "📊 Environment Summary"
echo "====================="

echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"
echo "pnpm version: $(pnpm --version)"

source .venv/bin/activate
echo "Python version: $(python --version)"
echo "pip version: $(pip --version)"

echo ""
echo "🎯 Available Commands:"
echo "  pnpm dev          - Start development servers"
echo "  pnpm build        - Build all applications"
echo "  pnpm test         - Run all tests"
echo "  pnpm lint         - Run linters"
echo ""
echo "🤖 BMAD Commands (for agents):"
echo "  @sm *create-next-story     - Create user stories"
echo "  @dev implement story       - Implement features"
echo "  @qa *review-story          - Review stories"
echo "  @qa *qa-gate              - Run quality gates"
echo ""
echo "🚀 Jules Setup Complete!"
echo "Ready for BMAD development workflow automation!"
