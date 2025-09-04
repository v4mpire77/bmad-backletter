#!/bin/bash

# Test version - only processes first 5 branches
# BMad-Backletter Branch Merge Test Script

set -e

# Configuration
MAIN_BRANCH="main"
TEST_LIMIT=5

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🧪 Testing branch merge with first $TEST_LIMIT branches...${NC}"

# Ensure we're on main branch
git checkout "$MAIN_BRANCH"
git pull --ff-only

# Get all remote branches except main and current working branch
git fetch --all
REMOTE_BRANCHES=($(git ls-remote --heads origin | grep -v "refs/heads/$MAIN_BRANCH" | grep -v "copilot/fix-" | awk '{print $2}' | sed 's|refs/heads/||' | head -$TEST_LIMIT))

echo -e "${GREEN}📊 Testing with ${#REMOTE_BRANCHES[@]} branches:${NC}"
for branch in "${REMOTE_BRANCHES[@]}"; do
    echo -e "${BLUE}  - $branch${NC}"
done

read -p "Proceed with test merge? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Test cancelled"
    exit 0
fi

# Test each branch
for branch in "${REMOTE_BRANCHES[@]}"; do
    echo -e "\n${BLUE}Testing merge of: $branch${NC}"
    
    # Skip problematic branch patterns
    if [[ "$branch" == "$MAIN_BRANCH" ]] || [[ "$branch" == "copilot/fix-"* ]]; then
        echo -e "${YELLOW}⏭️  Skipping $branch${NC}"
        continue
    fi
    
    # Fetch and attempt merge
    if git fetch origin "$branch"; then
        if git merge "origin/$branch" --no-edit -m "Test merge: $branch"; then
            echo -e "${GREEN}✅ Successfully merged $branch${NC}"
        else
            echo -e "${RED}❌ Conflicts in $branch, aborting${NC}"
            git merge --abort 2>/dev/null || true
        fi
    else
        echo -e "${RED}❌ Failed to fetch $branch${NC}"
    fi
done

echo -e "\n${PURPLE}🧪 Test completed. Check results above.${NC}"