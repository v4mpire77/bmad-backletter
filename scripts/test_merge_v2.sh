#!/bin/bash

# Test version - only processes first 3 branches with the new logic
# BMad-Backletter Branch Merge Test Script

set -e

# Configuration
MAIN_BRANCH="main"
CODEX_LOG=".codex/merge-log.txt"
CODEX_PROGRESS=".codex/progress.json"
MERGE_LOG="/tmp/merge_test_results.log"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Ensure .codex directory exists
mkdir -p .codex

# Initialize logs
echo "=== Test Branch Merge Process Started: $(date) ===" > "$MERGE_LOG"

# Codex Integration Functions
codex_log() {
    local message="$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $message" >> "$CODEX_LOG"
    echo -e "${BLUE}📝 CODEX: $message${NC}"
}

codex_progress() {
    local stage="$1"
    local details="$2"
    local progress_entry="{\"stage\": \"$stage\", \"details\": \"$details\", \"timestamp\": \"$(date -Iseconds)\"}"
    echo "$progress_entry" >> "$CODEX_PROGRESS"
    codex_log "PROGRESS: $stage - $details"
}

# Function to attempt merging a branch
merge_branch() {
    local branch_name="$1"
    local branch_sha="$2"
    
    echo -e "${GREEN}🔄 Processing branch: $branch_name${NC}"
    echo "Processing: $branch_name" >> "$MERGE_LOG"
    
    # Skip if it's the main branch or current working branch
    if [[ "$branch_name" == "$MAIN_BRANCH" ]] || [[ "$branch_name" == "copilot/fix-"* ]]; then
        echo -e "${YELLOW}⏭️  Skipping $branch_name (main branch or current working branch)${NC}"
        echo "SKIPPED: $branch_name (main/current)" >> "$MERGE_LOG"
        return 0
    fi
    
    # Attempt to merge the branch directly using the SHA
    echo -e "${YELLOW}🔀 Attempting to merge $branch_name (${branch_sha:0:8}) into main...${NC}"
    
    if git merge "$branch_sha" --no-edit --allow-unrelated-histories -m "Test merge: $branch_name"; then
        echo -e "${GREEN}✅ Successfully merged $branch_name${NC}"
        echo "SUCCESS: $branch_name" >> "$MERGE_LOG"
        return 0
    else
        echo -e "${RED}❌ Merge conflicts in $branch_name${NC}"
        echo "CONFLICT: $branch_name" >> "$MERGE_LOG"
        
        # Abort the merge
        git merge --abort 2>/dev/null || true
        
        # Try a different strategy - create a merge commit with manual resolution
        echo -e "${YELLOW}🔧 Attempting to resolve conflicts automatically with 'ours' strategy...${NC}"
        
        if git merge "$branch_sha" --strategy-option=ours --allow-unrelated-histories --no-edit -m "Test merge: $branch_name (ours strategy)"; then
            echo -e "${GREEN}✅ Merged $branch_name with automatic conflict resolution${NC}"
            echo "RESOLVED: $branch_name" >> "$MERGE_LOG"
            return 0
        else
            git merge --abort 2>/dev/null || true
            echo -e "${RED}❌ Unable to automatically resolve conflicts in $branch_name${NC}"
            echo "FAILED: $branch_name" >> "$MERGE_LOG"
            return 1
        fi
    fi
}

echo -e "${PURPLE}🧪 Testing branch merge with first 3 branches...${NC}"

# Ensure we're on main branch
git checkout "$MAIN_BRANCH"

# Get list of remote branches with their SHAs (first 3 only)
REMOTE_BRANCHES=()
BRANCH_SHAS=()

while IFS=$'\t' read -r sha ref; do
    branch_name="${ref#refs/heads/}"
    if [[ "$branch_name" != "$MAIN_BRANCH" ]] && [[ "$branch_name" != "copilot/fix-"* ]]; then
        REMOTE_BRANCHES+=("$branch_name")
        BRANCH_SHAS+=("$sha")
    fi
done < <(git ls-remote --heads origin | grep -v "refs/heads/$MAIN_BRANCH" | grep -v "copilot/fix-" | awk '{print $1 "\t" $2}' | head -3)

echo -e "${GREEN}📊 Testing with ${#REMOTE_BRANCHES[@]} branches:${NC}"
for i in "${!REMOTE_BRANCHES[@]}"; do
    echo -e "${BLUE}  $((i+1)). ${REMOTE_BRANCHES[$i]} (${BRANCH_SHAS[$i]:0:8})${NC}"
done

read -p "Proceed with test merge? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Test cancelled"
    exit 0
fi

# Track statistics
SUCCESSFUL_MERGES=0
FAILED_MERGES=0

# Process each branch
for i in "${!REMOTE_BRANCHES[@]}"; do
    branch="${REMOTE_BRANCHES[$i]}"
    sha="${BRANCH_SHAS[$i]}"
    
    echo -e "\n${BLUE}===========================================${NC}"
    echo -e "${BLUE}Branch $((i+1))/${#REMOTE_BRANCHES[@]}: $branch${NC}"
    echo -e "${BLUE}SHA: ${sha:0:8}...${NC}"
    echo -e "${BLUE}===========================================${NC}"
    
    if merge_branch "$branch" "$sha"; then
        ((SUCCESSFUL_MERGES++))
    else
        ((FAILED_MERGES++))
    fi
done

echo -e "\n${PURPLE}🧪 Test completed!${NC}"
echo -e "${GREEN}✅ Successfully merged: $SUCCESSFUL_MERGES branches${NC}"
echo -e "${RED}❌ Failed to merge: $FAILED_MERGES branches${NC}"

echo "=== Test Merge Process Completed: $(date) ===" >> "$MERGE_LOG"
echo "Test Results - Success: $SUCCESSFUL_MERGES, Failed: $FAILED_MERGES" >> "$MERGE_LOG"