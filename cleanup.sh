#!/usr/bin/env bash
set -euo pipefail

# This script cleans up the repository by removing bundled dependencies and frameworks
# that should not be in source control.

echo "Starting repository cleanup..."

# --- Step 1: Remove node_modules from Git tracking ---
echo "Removing node_modules from source control..."
if [ -d "node_modules" ]; then
    git rm -r --cached node_modules || true
    echo "Staged removal of node_modules."
else
    echo "node_modules directory not found, skipping."
fi

# --- Step 2: Remove BMAD-METHOD-main from Git tracking ---
echo "Removing bundled BMAD-METHOD-main project..."
if [ -d "BMAD-METHOD-main" ]; then
    git rm -r --cached BMAD-METHOD-main || true
    # Also physically remove the directory after removing from git
    rm -rf BMAD-METHOD-main
    echo "Removed BMAD-METHOD-main project."
else
    echo "BMAD-METHOD-main directory not found, skipping."
fi

# --- Step 3: Update .gitignore ---
echo "Updating .gitignore..."

# Create .gitignore if it doesn't exist
touch .gitignore

# Add node_modules if not already present
grep -qxF 'node_modules/' .gitignore || echo '
# Dependencies
node_modules/' >> .gitignore

# Add BMAD-METHOD-main if not already present
grep -qxF 'BMAD-METHOD-main/' .gitignore || echo '
# Bundled Frameworks
BMAD-METHOD-main/' >> .gitignore

# Deduplicate entries
sort -u .gitignore -o .gitignore

echo ".gitignore updated."

# --- Step 4: Final Instructions ---
echo ""
echo "Cleanup script finished."
echo "Please review the changes with 'git status'."
echo "Then, commit the changes to finalize the cleanup:"
echo 'git add .gitignore cleanup.sh'
echo 'git commit -m "chore: Clean up repository by removing node_modules and BMAD method"'
echo ""
echo "After committing, all developers will need to run 'pnpm install' to regenerate their local dependencies."
echo "To set up the development methodology, run 'npx bmad-method-install'."
