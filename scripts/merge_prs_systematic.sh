#!/bin/bash

# BMad PR Merge Script - Systematic conflict resolution and merging
# Handles rebasing and merging PRs in priority order

set -e

echo "🚀 Starting systematic PR merge process..."

# Function to attempt merge with automatic conflict resolution
merge_pr() {
    local pr_num=$1
    local pr_title=$2
    
    echo "📋 Processing PR #$pr_num: $pr_title"
    
    # Get PR details
    local branch=$(gh pr view $pr_num --json headRefName | jq -r '.headRefName')
    local mergeable=$(gh pr view $pr_num --json mergeable | jq -r '.mergeable')
    
    echo "   Branch: $branch"
    echo "   Mergeable: $mergeable"
    
    if [[ "$mergeable" == "MERGEABLE" ]]; then
        echo "   ✅ Merging directly..."
        if gh pr merge $pr_num --merge --delete-branch; then
            echo "   ✅ PR #$pr_num merged successfully"
            return 0
        else
            echo "   ❌ Direct merge failed"
            return 1
        fi
    else
        echo "   🔄 Attempting rebase and merge..."
        
        # Fetch and rebase
        git fetch origin $branch
        git checkout $branch
        
        if git rebase main; then
            echo "   ✅ Rebase successful, pushing..."
            git push --force-with-lease origin $branch
            
            # Try merge again
            if gh pr merge $pr_num --merge --delete-branch; then
                echo "   ✅ PR #$pr_num merged after rebase"
                git checkout main
                return 0
            else
                echo "   ❌ Merge failed after rebase"
                git checkout main
                return 1
            fi
        else
            echo "   ❌ Rebase failed - manual intervention needed"
            git rebase --abort 2>/dev/null || true
            git checkout main
            return 1
        fi
    fi
}

# Phase 1: Documentation and low-risk changes
echo "🔵 Phase 1: Documentation and Low-Risk Changes"
low_risk_prs=(7 29 33 42 72 73)

for pr in "${low_risk_prs[@]}"; do
    if merge_pr $pr "$(gh pr view $pr --json title | jq -r '.title')"; then
        echo "✅ Phase 1 PR #$pr completed"
    else
        echo "⚠️  Phase 1 PR #$pr needs manual review"
    fi
    echo "---"
done

echo "🔵 Phase 1 Complete"
echo "📊 Remaining PRs: $(gh pr list --state open | wc -l)"
