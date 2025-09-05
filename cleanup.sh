#!/usr/bin/env bash
set -euo pipefail

# Safe cleanup script for consolidating the repository while keeping a backup.
# Moves redundant directories to _cleanup_backup/ and merges .gitignore files.

BACKUP_DIR="_cleanup_backup"
mkdir -p "$BACKUP_DIR"

# Ensure .gitignore exists and back it up
if [ -f .gitignore ]; then
  cp .gitignore "$BACKUP_DIR/root.gitignore.bak"
else
  touch .gitignore
fi

ignore_and_untrack() {
  local dir="$1"
  if git ls-files "$dir" | grep -q .; then
    git rm -r --cached "$dir"
    echo "Removed $dir from Git index"
  fi
  if ! grep -Fxq "$dir/" .gitignore; then
    echo "$dir/" >> .gitignore
    echo "Added $dir/ to .gitignore"
  fi
}

# Ignore backup directory
ignore_and_untrack "$BACKUP_DIR"

########################################
# 1. Archive redundant repositories
########################################
for repo in BMAD-METHOD-main blackletter; do
  if [ -d "$repo" ] && [ ! -d "$BACKUP_DIR/$repo" ]; then
    echo "Archiving $repo/ to $BACKUP_DIR/"
    mv "$repo" "$BACKUP_DIR/"
    ignore_and_untrack "$repo"
  fi
done

########################################
# 2. Consolidate AI configurations
########################################
mkdir -p .ai
ignore_and_untrack ".ai"
for cfg in .bmad-core .bmad-creative-writing .bmad-infrastructure-devops; do
  if [ -d "$cfg" ] && [ ! -d ".ai/$cfg" ]; then
    echo "Moving $cfg to .ai/"
    mv "$cfg" .ai/
    ignore_and_untrack "$cfg"
  fi
done

# Archive old tool-specific configs
for tool in .claude .codex .cursor .crush .gemini .roomodes .qwen \
            .trae .windsurf .clinerules .kilocodemodes .qoder; do
  if [ -d "$tool" ]; then
    echo "Archiving $tool/ to $BACKUP_DIR/"
    mv "$tool" "$BACKUP_DIR/"
    ignore_and_untrack "$tool"
  fi
done

########################################
# 3. Merge .gitignore files
########################################
for src in "$BACKUP_DIR"/BMAD-METHOD-main/.gitignore \
           "$BACKUP_DIR"/blackletter/.gitignore \
           "$BACKUP_DIR"/blackletter/blackletter-upstream/.gitignore; do
  if [ -f "$src" ]; then
    echo -e "\n# Merged from ${src#$BACKUP_DIR/}" >> .gitignore
    cat "$src" >> .gitignore
  fi
done

# Deduplicate and sort .gitignore entries
sort -u .gitignore -o .gitignore

echo "Cleanup completed. Review $BACKUP_DIR before committing."