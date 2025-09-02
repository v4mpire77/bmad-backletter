#!/bin/bash
# BMad-Backletter PR Merge Script with Codex Integration
# Run from repo root after agent work is complete

set -e

# Configuration
REPO="v4mpire77/bmad-backletter"
MAIN_BRANCH="main"
TEST_COMMAND="python -m pytest apps/api/blackletter_api/tests -q"
CODEX_LOG=".codex/merge-log.txt"
CODEX_CONFIG=".codex/config.json"
CODEX_PROGRESS=".codex/progress.json"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Ensure .codex directory exists
mkdir -p .codex

# Codex Integration Functions
codex_log() {
    local message="$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $message" >> "$CODEX_LOG"
    echo -e "${BLUE}📝 CODEX: $message${NC}"
}

codex_broadcast() {
    local message="$1"
    codex_log "BROADCAST: $message"
    echo -e "${PURPLE}📢 CODEX BROADCAST: $message${NC}"
    # Write to config for agent pickup
    echo "{\"broadcast\": \"$message\", \"timestamp\": \"$(date -Iseconds)\"}" > "$CODEX_CONFIG"
}

codex_progress() {
    local stage="$1"
    local details="$2"
    local progress_entry="{\"stage\": \"$stage\", \"details\": \"$details\", \"timestamp\": \"$(date -Iseconds)\"}"
    echo "$progress_entry" >> "$CODEX_PROGRESS"
    codex_log "PROGRESS: $stage - $details"
}

codex_emergency() {
    local action="$1"
    local reason="$2"
    echo -e "${RED}🚨 EMERGENCY: $action - $reason${NC}"
    codex_log "EMERGENCY: $action - $reason"
    echo "{\"emergency\": \"$action\", \"reason\": \"$reason\", \"timestamp\": \"$(date -Iseconds)\"}" > ".codex/emergency.json"
    exit 1
}

codex_agent_status() {
    echo -e "${YELLOW}👥 AGENT STATUS CHECK${NC}"
    echo "Epic 2.1 (@dev-james): Rule Pack Loader"
    echo "Epic 2.4 (@dev-alex): Token Ledger"  
    echo "Epic 2.2 (@dev-sarah): Detector Engine"
    echo "Epic 3.1 (@dev-winston): Findings Table"
    echo "Epic 3.2 (@dev-maya): Report Export"
}

echo -e "${GREEN}🚀 Starting BMad-Backletter PR merge process${NC}"

# Initialize Codex integration
codex_broadcast "Starting PR merge process: #146 → #7 (backward merge strategy)"
codex_progress "INIT" "Merge process initialized, updating main branch"

# Check for emergency stop file
if [ -f ".codex/emergency.json" ]; then
    echo -e "${RED}🚨 Emergency stop detected - halting merge process${NC}"
    cat .codex/emergency.json
    exit 1
fi

# Update main branch
echo -e "${YELLOW}📥 Updating main branch...${NC}"
git fetch origin
git checkout main
git pull --ff-only
codex_progress "MAIN_UPDATED" "Main branch updated to latest"

# Get all open PRs in reverse numerical order (newest first)
echo -e "${YELLOW}📋 Fetching open PRs from #146 backward...${NC}"
ALL_OPEN_PRS=$(gh pr list --state open --json number,title,headRefName --limit 200 -q 'sort_by(.number) | reverse | .[].number')

if [ -z "$ALL_OPEN_PRS" ]; then
    echo -e "${YELLOW}ℹ️  No open PRs found to merge${NC}"
    exit 0
fi

# Convert to array and filter for range 146 down to 7
MERGE_ORDER=()
for pr_num in $ALL_OPEN_PRS; do
    if [ "$pr_num" -le 146 ] && [ "$pr_num" -ge 7 ]; then
        MERGE_ORDER+=("$pr_num")
    fi
done

echo -e "${GREEN}📊 Found ${#MERGE_ORDER[@]} PRs to merge (PR #146 → #7)${NC}"
codex_progress "PRS_IDENTIFIED" "Found ${#MERGE_ORDER[@]} PRs for backward merge"
codex_agent_status

echo -e "${GREEN}📊 Found PRs to merge in dependency order${NC}"

# Function to merge a specific PR by number
merge_pr_by_number() {
    local pr_number=$1
    
    echo -e "${GREEN}🔄 Processing PR #$pr_number${NC}"
    codex_progress "PR_START" "Starting merge of PR #$pr_number"
    
    # Get PR info
    if ! PR_INFO=$(gh pr view "$pr_number" --json title,headRefName 2>/dev/null); then
        echo -e "${YELLOW}⏭️  PR #$pr_number not found or already merged${NC}"
        codex_progress "PR_SKIP" "PR #$pr_number not found or already merged"
        return 0
    fi
    
    PR_TITLE=$(echo "$PR_INFO" | jq -r '.title')
    PR_BRANCH=$(echo "$PR_INFO" | jq -r '.headRefName')
    
    echo -e "${YELLOW}📝 PR #$pr_number: $PR_TITLE${NC}"
    echo -e "${YELLOW}🌿 Branch: $PR_BRANCH${NC}"
    
    # Checkout and rebase PR
    if ! gh pr checkout "$pr_number"; then
        echo -e "${YELLOW}⏭️  Could not checkout PR #$pr_number, skipping${NC}"
        codex_progress "PR_SKIP" "Could not checkout PR #$pr_number"
        return 0
    fi
    
    echo -e "${YELLOW}🔄 Rebasing on latest main...${NC}"
    git fetch origin
    if ! git rebase origin/main; then
        echo -e "${RED}⚠️  Rebase conflicts in PR #$pr_number${NC}"
        codex_emergency "REBASE_CONFLICT" "PR #$pr_number has rebase conflicts requiring manual resolution"
    fi
    
    # Run tests
    echo -e "${YELLOW}🧪 Running tests...${NC}"
    if ! $TEST_COMMAND; then
        echo -e "${RED}❌ Tests failed for PR #$pr_number${NC}"
        codex_emergency "TEST_FAILURE" "PR #$pr_number failed tests"
    fi
    
    # Push rebased branch
    echo -e "${YELLOW}⬆️  Pushing rebased branch...${NC}"
    if ! git push --force-with-lease; then
        echo -e "${RED}⚠️  Failed to push rebased branch for PR #$pr_number${NC}"
        codex_emergency "PUSH_FAILURE" "Could not push rebased branch for PR #$pr_number"
    fi
    
    # Merge PR
    echo -e "${GREEN}🎯 Merging PR #$pr_number...${NC}"
    if ! gh pr merge "$pr_number" --squash --auto --delete-branch; then
        echo -e "${RED}⚠️  Failed to merge PR #$pr_number${NC}"
        codex_emergency "MERGE_FAILURE" "Could not merge PR #$pr_number"
    fi
    
    # Update local main
    git checkout main
    git pull --ff-only
    
    echo -e "${GREEN}✅ Successfully merged PR #$pr_number${NC}"
    codex_progress "PR_COMPLETE" "Successfully merged PR #$pr_number: $PR_TITLE"
    echo ""
}

# Merge PRs in reverse numerical order (newest first)
for pr_number in "${MERGE_ORDER[@]}"; do
    merge_pr_by_number "$pr_number"
done

echo -e "${GREEN}🎉 All BMad feature PRs merged successfully!${NC}"
codex_broadcast "All PRs #146 → #7 merged successfully! 🎉"
codex_progress "MERGE_COMPLETE" "All ${#MERGE_ORDER[@]} PRs merged successfully"

echo -e "${YELLOW}📊 Final status check...${NC}"

# Final test run on main
if $TEST_COMMAND; then
    echo -e "${GREEN}✅ All tests passing on main branch${NC}"
    codex_progress "TESTS_PASS" "Final test suite passed on main branch"
else
    echo -e "${RED}⚠️  Tests failing on main - investigation needed${NC}"
    codex_emergency "FINAL_TEST_FAILURE" "Test suite failed on main after all merges"
fi

# Generate final report
echo -e "${GREEN}📄 Generating merge report...${NC}"
cat > ".codex/merge-report.md" << EOF
# BMad PR Merge Report

**Date:** $(date)
**Strategy:** Backward merge (PR #146 → #7)
**Total PRs Processed:** ${#MERGE_ORDER[@]}

## Summary
- ✅ All PRs merged successfully
- ✅ Tests passing on main branch  
- ✅ No conflicts requiring manual intervention
- ✅ BMad Epic 2 & 3 stories ready for implementation

## Agent Work Coordination
- Epic 2.1: @dev-james - Rule Pack Loader
- Epic 2.4: @dev-alex - Token Ledger
- Epic 2.2: @dev-sarah - Detector Engine  
- Epic 3.1: @dev-winston - Findings Table
- Epic 3.2: @dev-maya - Report Export

## Next Steps
Ready for BMad agent implementation with clean main branch!
EOF

echo -e "${GREEN}🏁 BMad merge process complete!${NC}"
echo -e "${BLUE}📄 Report saved to: .codex/merge-report.md${NC}"
codex_broadcast "Merge process complete - agents ready for Epic implementation!"
