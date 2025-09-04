#!/bin/bash

# BMad-Backletter Complete Branch Merge Script
# Merges all remote branches into main assuming main is up to date
# Adapted from existing merge scripts for direct git operations

set -e

# Configuration
MAIN_BRANCH="main"
CODEX_LOG=".codex/merge-log.txt"
CODEX_PROGRESS=".codex/progress.json"
MERGE_LOG="/tmp/merge_results.log"

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
echo "=== Branch Merge Process Started: $(date) ===" > "$MERGE_LOG"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] INIT: Starting complete branch merge process" >> "$CODEX_LOG"

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
    
    if git merge "$branch_sha" --no-edit --allow-unrelated-histories -m "Merge branch '$branch_name' into main"; then
        echo -e "${GREEN}✅ Successfully merged $branch_name${NC}"
        echo "SUCCESS: $branch_name" >> "$MERGE_LOG"
        codex_progress "BRANCH_MERGED" "Successfully merged $branch_name"
        
        # Note: We're not deleting remote branches since we don't have write access to most of them
        echo -e "${YELLOW}📝 Note: Remote branch $branch_name not deleted (requires individual permissions)${NC}"
        echo "NOT_DELETED: $branch_name" >> "$MERGE_LOG"
        
        return 0
    else
        echo -e "${RED}❌ Merge conflicts in $branch_name${NC}"
        echo "CONFLICT: $branch_name" >> "$MERGE_LOG"
        
        # Abort the merge
        git merge --abort 2>/dev/null || true
        
        # Try a different strategy - create a merge commit with manual resolution
        echo -e "${YELLOW}🔧 Attempting to resolve conflicts automatically with 'ours' strategy...${NC}"
        
        if git merge "$branch_sha" --strategy-option=ours --allow-unrelated-histories --no-edit -m "Merge branch '$branch_name' with conflict resolution (ours strategy)"; then
            echo -e "${GREEN}✅ Merged $branch_name with automatic conflict resolution${NC}"
            echo "RESOLVED: $branch_name" >> "$MERGE_LOG"
            codex_progress "BRANCH_MERGED_RESOLVED" "Merged $branch_name with conflict resolution"
            return 0
        else
            git merge --abort 2>/dev/null || true
            echo -e "${RED}❌ Unable to automatically resolve conflicts in $branch_name${NC}"
            echo "FAILED: $branch_name" >> "$MERGE_LOG"
            codex_progress "BRANCH_FAILED" "Could not merge $branch_name due to conflicts"
            return 1
        fi
    fi
}

# Main execution
echo -e "${PURPLE}🚀 Starting complete branch merge process...${NC}"
codex_progress "INIT" "Branch merge process initialized"

# Ensure we're on main branch
git checkout "$MAIN_BRANCH"
echo -e "${YELLOW}📥 Ensuring main branch is up to date...${NC}"
git pull --ff-only
codex_progress "MAIN_UPDATED" "Main branch updated to latest"

# Get all remote branches except main
echo -e "${YELLOW}📋 Fetching list of remote branches...${NC}"
git fetch --all

# Get list of all remote branches (excluding main and current working branch) with their SHAs
echo -e "${YELLOW}📋 Fetching list of remote branches...${NC}"

# Get branch data in a more reliable way
REMOTE_BRANCHES=()
BRANCH_SHAS=()

while IFS=$'\t' read -r sha ref; do
    branch_name="${ref#refs/heads/}"
    if [[ "$branch_name" != "$MAIN_BRANCH" ]] && [[ "$branch_name" != "copilot/fix-"* ]]; then
        REMOTE_BRANCHES+=("$branch_name")
        BRANCH_SHAS+=("$sha")
    fi
done < <(git ls-remote --heads origin | grep -v "refs/heads/$MAIN_BRANCH" | grep -v "copilot/fix-" | awk '{print $1 "\t" $2}')

echo -e "${GREEN}📊 Found ${#REMOTE_BRANCHES[@]} branches to merge${NC}"
codex_progress "BRANCHES_IDENTIFIED" "Found ${#REMOTE_BRANCHES[@]} branches for merging"

# Track statistics
TOTAL_BRANCHES=${#REMOTE_BRANCHES[@]}
SUCCESSFUL_MERGES=0
FAILED_MERGES=0

echo -e "${GREEN}📊 Processing $TOTAL_BRANCHES branches...${NC}"

# Process each branch
for i in "${!REMOTE_BRANCHES[@]}"; do
    branch="${REMOTE_BRANCHES[$i]}"
    sha="${BRANCH_SHAS[$i]}"
    
    echo -e "\n${BLUE}===========================================${NC}"
    echo -e "${BLUE}Branch $(($i + 1))/${#REMOTE_BRANCHES[@]}: $branch${NC}"
    echo -e "${BLUE}SHA: ${sha:0:8}...${NC}"
    echo -e "${BLUE}===========================================${NC}"
    
    if merge_branch "$branch" "$sha"; then
        ((SUCCESSFUL_MERGES++))
    else
        ((FAILED_MERGES++))
    fi
    
    # Progress update every 10 branches
    if (( ($i + 1) % 10 == 0 )); then
        echo -e "${PURPLE}📊 Progress: $(($i + 1))/${#REMOTE_BRANCHES[@]} branches processed${NC}"
        echo -e "${GREEN}✅ Successful: $SUCCESSFUL_MERGES${NC}"
        echo -e "${RED}❌ Failed: $FAILED_MERGES${NC}"
        codex_progress "PROGRESS_UPDATE" "Processed $(($i + 1))/${#REMOTE_BRANCHES[@]} - Success: $SUCCESSFUL_MERGES, Failed: $FAILED_MERGES"
    fi
done

# Final summary
echo -e "\n${PURPLE}🎉 Branch merge process completed!${NC}"
echo -e "${GREEN}✅ Successfully merged: $SUCCESSFUL_MERGES branches${NC}"
echo -e "${RED}❌ Failed to merge: $FAILED_MERGES branches${NC}"
echo -e "${BLUE}📊 Total processed: $((SUCCESSFUL_MERGES + FAILED_MERGES))/$TOTAL_BRANCHES branches${NC}"

# Push the final merged state
echo -e "${YELLOW}⬆️  Pushing merged changes to main...${NC}"
if git push origin "$MAIN_BRANCH"; then
    echo -e "${GREEN}✅ Successfully pushed all merged changes to main${NC}"
    codex_progress "PUSH_COMPLETE" "All merged changes pushed to main"
else
    echo -e "${RED}❌ Failed to push merged changes${NC}"
    codex_progress "PUSH_FAILED" "Failed to push merged changes to main"
fi

# Final log entry
echo "=== Branch Merge Process Completed: $(date) ===" >> "$MERGE_LOG"
echo "Total: $TOTAL_BRANCHES, Success: $SUCCESSFUL_MERGES, Failed: $FAILED_MERGES" >> "$MERGE_LOG"

codex_progress "COMPLETE" "Branch merge process completed - Success: $SUCCESSFUL_MERGES, Failed: $FAILED_MERGES"

echo -e "${PURPLE}📋 Detailed log available in: $MERGE_LOG${NC}"
echo -e "${PURPLE}📋 Codex progress in: $CODEX_PROGRESS${NC}"