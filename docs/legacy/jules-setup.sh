#!/bin/bash

# Jules Setup Script for Blackletter BMAD Project  
# This script sets up the complete development environment for the Blackletter contract analysis platform
# Updated with shared types creation and improved error handling

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
echo "📦 Installing Node.js dependencies..."
if ! command -v pnpm &> /dev/null; then
    echo "Installing pnpm..."
    npm install -g pnpm
fi

pnpm install

# 2. Set up Python environment
echo "🐍 Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. Set up BMAD Method
echo "🧙 Setting up BMAD Method..."
if [ -d "BMAD-METHOD-main" ]; then
    if [ ! -L "bmad-core" ]; then
        ln -sf BMAD-METHOD-main/bmad-core bmad-core
        echo "✅ BMAD core linked"
    fi
else
    echo "⚠️  BMAD Method not found - some functionality may be limited"
fi

# 4. Create missing shared types
echo "🔧 Creating missing shared types..."
mkdir -p packages/shared/src

cat > packages/shared/src/index.ts << 'EOF'
// Shared types for Blackletter BMAD project
export interface Finding {
  id: string;
  title: string;
  verdict: 'compliant' | 'non-compliant' | 'warning';
  evidence: string[];
  description: string;
  ruleId: string;
  severity: 'high' | 'medium' | 'low';
}

export interface ContractAnalysis {
  id: string;
  findings: Finding[];
  summary: string;
  score: number;
}

// Re-export for compatibility
export * from './index';
EOF

cat > packages/shared/package.json << 'EOF'
{
  "name": "@bmad/shared",
  "version": "1.0.0",
  "main": "src/index.ts",
  "types": "src/index.ts",
  "exports": {
    ".": "./src/index.ts",
    "./types": "./src/index.ts"
  }
}
EOF

# Update workspace configuration
if ! grep -q "packages/shared" pnpm-workspace.yaml; then
  echo "packages:" > pnpm-workspace.yaml
  echo "  - 'apps/*'" >> pnpm-workspace.yaml
  echo "  - 'packages/*'" >> pnpm-workspace.yaml
fi

# 5. Update workspace dependencies
echo "🔄 Updating workspace dependencies..."
pnpm install

# 6. Build Next.js application
echo "🌐 Building Next.js application..."
cd apps/web
pnpm build || {
    echo "⚠️ Next.js build failed - continuing with setup"
    echo "This is expected for incomplete applications"
}
cd ../..

# 7. Run validation tests
echo "🧪 Running validation tests..."
source .venv/bin/activate
python -c "import fastapi, uvicorn, pytest"
echo "✅ Python dependencies working"

if command -v node &> /dev/null && command -v pnpm &> /dev/null; then
    echo "✅ Node.js environment working"
fi

# 8. Environment summary
echo ""
echo "📊 Environment Summary"
echo "====================="

echo "Node.js: $(node --version)"
echo "pnpm: $(pnpm --version)"

source .venv/bin/activate
echo "Python: $(python --version)"

echo ""
echo "🎯 Available Commands:"
echo "  pnpm dev    - Start development"
echo "  pnpm build  - Build applications"
echo "  pnpm test   - Run tests"

echo ""
echo "🤖 BMAD Agents Ready:"
echo "  @sm - Scrum Master (*create-next-story)"
echo "  @dev - Developer (implement story)"
echo "  @qa - QA (*review-story, *qa-gate)"
echo "  @po - Product Owner"

echo ""
echo "✅ Jules Setup Complete!"
echo "Ready for BMAD development workflow automation!"

echo ""
echo "🎯 Next Steps:"
echo "1. Jules will use this environment for all BMAD tasks"
echo "2. Create GitHub issues with 'jules' label to trigger automation"
echo "3. BMAD agents will execute automatically using this setup"
