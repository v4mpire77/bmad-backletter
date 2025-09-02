#!/bin/bash

# Test the new parsing logic
set -e

echo "Testing branch parsing logic..."

MAIN_BRANCH="main"
REMOTE_BRANCHES=()
BRANCH_SHAS=()

while IFS=$'\t' read -r sha ref; do
    branch_name="${ref#refs/heads/}"
    if [[ "$branch_name" != "$MAIN_BRANCH" ]] && [[ "$branch_name" != "copilot/fix-"* ]]; then
        REMOTE_BRANCHES+=("$branch_name")
        BRANCH_SHAS+=("$sha")
    fi
done < <(git ls-remote --heads origin | grep -v "refs/heads/$MAIN_BRANCH" | grep -v "copilot/fix-" | awk '{print $1 "\t" $2}' | head -5)

echo "Found ${#REMOTE_BRANCHES[@]} branches:"
for i in "${!REMOTE_BRANCHES[@]}"; do
    echo "  $((i+1)). ${REMOTE_BRANCHES[$i]} (${BRANCH_SHAS[$i]:0:8})"
done