#!/bin/bash

# Conflict Resolution Validation Script
# Tests the conflict resolution tools with synthetic conflicts

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

TEST_DIR="/tmp/conflict-resolution-test"
ORIGINAL_DIR=$(pwd)

echo -e "${GREEN}🧪 Starting conflict resolution validation${NC}"

# Create test directory
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Initialize git repo
git init
git config user.email "test@example.com"
git config user.name "Test User"

# Create synthetic conflict files
create_test_files() {
    echo -e "${YELLOW}📝 Creating test files with synthetic conflicts${NC}"
    
    # Python router conflict
    cat > main.py << 'EOF'
from fastapi import FastAPI
app = FastAPI()

<<<<<<< HEAD
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
=======
app.include_router(auth.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
>>>>>>> feature-branch

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

    # Requirements.txt conflict
    cat > requirements.txt << 'EOF'
fastapi==0.68.0
<<<<<<< HEAD
uvicorn==0.15.0
pytest==6.2.4
=======
pydantic==1.8.2
requests==2.25.1
>>>>>>> feature-branch
sqlalchemy==1.4.0
EOF

    # Documentation conflict
    cat > README.md << 'EOF'
# Test Project

This is a test project for conflict resolution.

<<<<<<< HEAD
## Installation

pip install -r requirements.txt

## Usage

Run the application with:
python main.py
=======
## Setup

1. Install dependencies
2. Configure environment
3. Run tests

## Development

Use pytest for testing.
>>>>>>> feature-branch

## License

MIT License
EOF

    # JSON conflict
    cat > package.json << 'EOF'
{
  "name": "test-project",
  "version": "1.0.0",
<<<<<<< HEAD
  "scripts": {
    "start": "node index.js",
    "test": "jest"
  },
=======
  "scripts": {
    "start": "node server.js",
    "build": "webpack"
  },
>>>>>>> feature-branch
  "dependencies": {
    "express": "^4.17.1"
  }
}
EOF

    echo -e "${GREEN}✅ Test files created${NC}"
}

# Test conflict detection
test_conflict_detection() {
    echo -e "${YELLOW}🔍 Testing conflict detection${NC}"
    
    local conflict_count=$(find . -type f \( -name "*.py" -o -name "*.txt" -o -name "*.md" -o -name "*.json" \) -exec grep -l "<<<<<<< \|=======\|>>>>>>> " {} \; | wc -l)
    
    if [ "$conflict_count" -eq 4 ]; then
        echo -e "${GREEN}✅ Conflict detection working - found $conflict_count conflicted files${NC}"
        return 0
    else
        echo -e "${RED}❌ Conflict detection failed - expected 4, found $conflict_count${NC}"
        return 1
    fi
}

# Test bash conflict resolver
test_bash_resolver() {
    echo -e "${YELLOW}🔧 Testing Bash conflict resolver${NC}"
    
    # Copy the resolver script
    cp "$ORIGINAL_DIR/scripts/resolve_all_conflicts.sh" ./
    chmod +x ./resolve_all_conflicts.sh
    
    # Run resolver
    if ./resolve_all_conflicts.sh; then
        echo -e "${GREEN}✅ Bash resolver completed${NC}"
        
        # Check if conflicts are resolved
        local remaining_conflicts=$(find . -type f \( -name "*.py" -o -name "*.txt" -o -name "*.md" -o -name "*.json" \) -exec grep -l "<<<<<<< \|=======\|>>>>>>> " {} \; | wc -l)
        
        if [ "$remaining_conflicts" -eq 0 ]; then
            echo -e "${GREEN}✅ All conflicts resolved by Bash script${NC}"
            return 0
        else
            echo -e "${RED}❌ $remaining_conflicts conflicts remain after Bash resolution${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ Bash resolver failed${NC}"
        return 1
    fi
}

# Test PowerShell resolver (if available)
test_powershell_resolver() {
    echo -e "${YELLOW}🔧 Testing PowerShell conflict resolver${NC}"
    
    if ! command -v pwsh >/dev/null 2>&1; then
        echo -e "${YELLOW}⏭️ PowerShell not available, skipping${NC}"
        return 0
    fi
    
    # Recreate conflicts for PowerShell test
    create_test_files
    
    # Copy the PowerShell script
    cp "$ORIGINAL_DIR/blackletter/blackletter-upstream/resolve_conflicts.ps1" ./
    
    # Run PowerShell resolver
    if pwsh -File ./resolve_conflicts.ps1 -Strategy smart; then
        echo -e "${GREEN}✅ PowerShell resolver completed${NC}"
        
        # Check if conflicts are resolved
        local remaining_conflicts=$(find . -type f \( -name "*.py" -o -name "*.txt" -o -name "*.md" -o -name "*.json" \) -exec grep -l "<<<<<<< \|=======\|>>>>>>> " {} \; | wc -l)
        
        if [ "$remaining_conflicts" -eq 0 ]; then
            echo -e "${GREEN}✅ All conflicts resolved by PowerShell script${NC}"
            return 0
        else
            echo -e "${RED}❌ $remaining_conflicts conflicts remain after PowerShell resolution${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ PowerShell resolver failed${NC}"
        return 1
    fi
}

# Validate resolution quality
validate_resolution_quality() {
    echo -e "${YELLOW}📊 Validating resolution quality${NC}"
    
    # Check Python file
    if grep -q "app.include_router(auth.router" main.py && 
       grep -q "app.include_router(users.router" main.py &&
       grep -q "app.include_router(reports.router" main.py; then
        echo -e "${GREEN}✅ Python router merging worked correctly${NC}"
    else
        echo -e "${RED}❌ Python router merging failed${NC}"
        echo "Content of main.py:"
        cat main.py
        return 1
    fi
    
    # Check requirements.txt
    if grep -q "fastapi==0.68.0" requirements.txt &&
       grep -q "uvicorn==0.15.0" requirements.txt &&
       grep -q "pydantic==1.8.2" requirements.txt; then
        echo -e "${GREEN}✅ Requirements merging worked correctly${NC}"
    else
        echo -e "${RED}❌ Requirements merging failed${NC}"
        echo "Content of requirements.txt:"
        cat requirements.txt
        return 1
    fi
    
    # Check that files are valid
    python3 -m py_compile main.py 2>/dev/null && echo -e "${GREEN}✅ Python syntax valid${NC}" || echo -e "${RED}❌ Python syntax invalid${NC}"
    
    python3 -c "import json; json.load(open('package.json'))" 2>/dev/null && echo -e "${GREEN}✅ JSON syntax valid${NC}" || echo -e "${RED}❌ JSON syntax invalid${NC}"
    
    return 0
}

# Run tests
main() {
    local test_results=()
    
    create_test_files
    
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Test conflict detection
    if test_conflict_detection; then
        test_results+=("PASS: Conflict detection")
    else
        test_results+=("FAIL: Conflict detection")
    fi
    
    # Test Bash resolver
    if test_bash_resolver; then
        test_results+=("PASS: Bash resolver")
        validate_resolution_quality && test_results+=("PASS: Resolution quality") || test_results+=("FAIL: Resolution quality")
    else
        test_results+=("FAIL: Bash resolver")
    fi
    
    # Test PowerShell resolver (if available)
    if test_powershell_resolver; then
        test_results+=("PASS: PowerShell resolver")
    else
        test_results+=("FAIL: PowerShell resolver")
    fi
    
    # Print results
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}📊 Test Results:${NC}"
    
    local passed=0
    local total=0
    
    for result in "${test_results[@]}"; do
        ((total++))
        if [[ "$result" == PASS:* ]]; then
            ((passed++))
            echo -e "${GREEN}✅ $result${NC}"
        else
            echo -e "${RED}❌ $result${NC}"
        fi
    done
    
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}📈 Summary: $passed/$total tests passed${NC}"
    
    # Cleanup
    cd "$ORIGINAL_DIR"
    rm -rf "$TEST_DIR"
    
    if [ "$passed" -eq "$total" ]; then
        echo -e "${GREEN}🎉 All tests passed! Conflict resolution tools are working correctly.${NC}"
        return 0
    else
        echo -e "${RED}❌ Some tests failed. Please review the conflict resolution tools.${NC}"
        return 1
    fi
}

# Execute main function
main "$@"