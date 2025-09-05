#!/usr/bin/env bash
set -euo pipefail

# Safe cleanup script for consolidating the repository while keeping a backup.
# Moves redundant directories to _cleanup_backup/ and merges .gitignore files.

BACKUP_DIR="_cleanup_backup"
mkdir -p "$BACKUP_DIR"

########################################
# 1. Archive redundant repositories
########################################
for repo in BMAD-METHOD-main blackletter; do
  if [ -d "$repo" ]; then
    echo "Archiving $repo/"
    mv "$repo" "$BACKUP_DIR/"
  fi
done

########################################
# 2. Consolidate AI configurations
########################################
mkdir -p .ai
for cfg in .bmad-core .bmad-creative-writing .bmad-infrastructure-devops; do
  if [ -d "$cfg" ]; then
    echo "Moving $cfg to .ai/"
    mv "$cfg" .ai/
  fi
done

# Archive old tool-specific configs
for tool in .claude .codex .cursor .crush .gemini .roomodes .qwen \
            .trae .windsurf .clinerules .kilocodemodes .qoder; do
  if [ -d "$tool" ]; then
    echo "Archiving $tool/"
    mv "$tool" "$BACKUP_DIR/"
  fi
done

########################################
# 3. Merge .gitignore files
########################################
if [ -f .gitignore ]; then
  cp .gitignore "$BACKUP_DIR/root.gitignore.bak"
else
  touch .gitignore
fi

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
