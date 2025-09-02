# Comprehensive PR Conflict Resolution Guide

This guide provides a complete workflow for resolving merge conflicts and managing pull requests in the bmad-backletter repository.

## Quick Start

### 1. Resolve All Conflicts Automatically
```bash
# Run comprehensive conflict resolution
./scripts/resolve_all_conflicts.sh

# Or with PowerShell (Windows)
./blackletter/blackletter-upstream/resolve_conflicts.ps1 -Strategy smart
```

### 2. Process All Open PRs
```bash
# Process ready-to-merge PRs first
./scripts/enhanced_pr_manager.sh process ready-first

# Process conflicted PRs first
./scripts/enhanced_pr_manager.sh process conflicts-first

# Process all PRs
./scripts/enhanced_pr_manager.sh process all
```

### 3. Get PR Status
```bash
# List all open PRs
./scripts/enhanced_pr_manager.sh list all

# List only conflicted PRs
./scripts/enhanced_pr_manager.sh list conflicted

# List ready-to-merge PRs
./scripts/enhanced_pr_manager.sh list ready
```

## Available Scripts

### 1. `scripts/resolve_all_conflicts.sh`
Comprehensive Bash script for automated conflict resolution.

**Features:**
- Automatic backup creation
- File-type specific conflict resolution strategies
- Router import merging for Python files
- Package.json dependency merging
- Requirements.txt intelligent merging
- Documentation conflict resolution (prefers HEAD)
- Configuration file handling

**Usage:**
```bash
./scripts/resolve_all_conflicts.sh
```

### 2. `scripts/enhanced_pr_manager.sh`
Advanced PR management with conflict resolution integration.

**Features:**
- GitHub CLI integration
- Multiple processing strategies
- Automated rebase and merge
- Progress tracking and logging
- Comprehensive reporting

**Usage:**
```bash
# Process PRs with different strategies
./scripts/enhanced_pr_manager.sh process ready-first
./scripts/enhanced_pr_manager.sh process conflicts-first
./scripts/enhanced_pr_manager.sh process all

# List PRs with filters
./scripts/enhanced_pr_manager.sh list all
./scripts/enhanced_pr_manager.sh list ready
./scripts/enhanced_pr_manager.sh list conflicted

# Generate reports
./scripts/enhanced_pr_manager.sh report

# Get help
./scripts/enhanced_pr_manager.sh help
```

### 3. `blackletter/blackletter-upstream/resolve_conflicts.ps1`
Enhanced PowerShell script for Windows environments.

**Features:**
- Multiple resolution strategies (smart, head, merge, manual)
- Dry-run mode for testing
- Verbose output
- File-type specific handling
- Comprehensive backup system
- Detailed reporting

**Usage:**
```powershell
# Smart resolution (recommended)
./resolve_conflicts.ps1 -Strategy smart

# Dry run to preview changes
./resolve_conflicts.ps1 -Strategy smart -DryRun

# Verbose output
./resolve_conflicts.ps1 -Strategy smart -Verbose

# Use HEAD version only
./resolve_conflicts.ps1 -Strategy head
```

### 4. `scripts/merge_prs_systematic.sh`
Systematic PR merging with priority-based processing.

**Features:**
- Phase-based merging (low-risk first)
- Automatic rebase handling
- Test validation
- Branch cleanup

**Usage:**
```bash
./scripts/merge_prs_systematic.sh
```

## Conflict Resolution Strategies

### 1. Smart Resolution (Default)
Intelligently resolves conflicts based on file type:

- **Python files**: Merges router imports, prefers HEAD for other conflicts
- **package.json**: Prefers HEAD version with conflict logging
- **requirements.txt**: Merges dependencies intelligently
- **Documentation (.md, .txt)**: Prefers HEAD version
- **Configuration files (.yml, .yaml, .json)**: Prefers HEAD version
- **Other files**: Prefers HEAD version

### 2. HEAD Resolution
Always prefers the HEAD (current branch) version.

### 3. Merge Resolution
Attempts to merge both versions (implementation varies by file type).

### 4. Manual Resolution
Leaves conflicts for manual resolution.

## Common Conflict Patterns

### Router Import Conflicts (FastAPI)
```python
# Before resolution
<<<<<<< HEAD
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
=======
app.include_router(auth.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
>>>>>>> feature-branch

# After resolution
app.include_router(auth.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(users.router, prefix="/api")
```

### Requirements.txt Conflicts
```text
# Before resolution
<<<<<<< HEAD
fastapi==0.68.0
uvicorn==0.15.0
=======
fastapi==0.68.0
pydantic==1.8.2
>>>>>>> feature-branch

# After resolution
fastapi==0.68.0
pydantic==1.8.2
uvicorn==0.15.0
```

## Workflow Integration

### Emergency Recovery
If the merge process encounters an emergency state:

1. Check the emergency file:
   ```bash
   cat .codex/emergency.json
   ```

2. Clear the emergency state:
   ```bash
   ./scripts/resolve_all_conflicts.sh
   ```

3. Resume processing:
   ```bash
   ./scripts/enhanced_pr_manager.sh process ready-first
   ```

### Backup and Recovery
All scripts create automatic backups:

- **Bash scripts**: `.codex/backups/backup_YYYYMMDD_HHMMSS`
- **PowerShell script**: `.codex/backups/YYYYMMDD_HHMMSS/`

To restore from backup:
```bash
# List available backups
ls .codex/backups/

# Restore from git stash (Bash scripts)
git stash list
git stash apply stash@{0}

# Manual file restoration (PowerShell backups)
cp .codex/backups/YYYYMMDD_HHMMSS/filename.ext ./original/path/
```

## Monitoring and Logging

### Log Files
- **Conflict resolution**: `.codex/conflict-resolution-log.txt`
- **PR management**: `.codex/pr-manager-log.txt`
- **Legacy merge log**: `.codex/merge-log.txt`

### Progress Tracking
- **PR progress**: `.codex/pr-progress.json`
- **Emergency state**: `.codex/emergency.json`

### Reports
- **Conflict resolution**: `.codex/conflict-resolution-report.txt`
- **PR summary**: `.codex/pr-resolution-report.md`

## Best Practices

### Before Running Scripts
1. Ensure clean working directory:
   ```bash
   git status
   git stash  # if needed
   ```

2. Update main branch:
   ```bash
   git checkout main
   git pull origin main
   ```

3. Authenticate with GitHub CLI:
   ```bash
   gh auth status
   gh auth login  # if needed
   ```

### During Processing
1. Monitor output for errors or warnings
2. Check progress files in `.codex/` directory
3. Review generated reports

### After Processing
1. Verify repository state:
   ```bash
   git status
   ./scripts/resolve_all_conflicts.sh  # Should report no conflicts
   ```

2. Run tests:
   ```bash
   python -m pytest apps/api/blackletter_api/tests -q
   ```

3. Review generated reports:
   ```bash
   cat .codex/pr-resolution-report.md
   ```

## Troubleshooting

### Common Issues

#### "GitHub CLI not authenticated"
```bash
gh auth login
```

#### "Conflict resolver not found"
```bash
chmod +x ./scripts/resolve_all_conflicts.sh
chmod +x ./scripts/enhanced_pr_manager.sh
```

#### "Python module not found"
```bash
pip install -r requirements.txt
# or
pip install pytest
```

#### "Permission denied"
```bash
chmod +x ./scripts/*.sh
```

### Emergency Procedures

#### Repository in inconsistent state
```bash
# Save current work
git stash

# Reset to known good state
git checkout main
git reset --hard origin/main

# Clear emergency state
rm -f .codex/emergency.json

# Restart process
./scripts/enhanced_pr_manager.sh process ready-first
```

#### Too many conflicts to resolve automatically
```bash
# Use manual strategy
./blackletter/blackletter-upstream/resolve_conflicts.ps1 -Strategy manual

# Or process one PR at a time
gh pr list --state open
gh pr checkout PR_NUMBER
# Resolve manually
git add .
git rebase --continue
```

## Integration with Development Workflow

### For Developers
1. Create feature branch
2. Make changes
3. Create PR
4. Wait for automated processing or request manual merge

### For Maintainers
1. Run daily conflict resolution:
   ```bash
   ./scripts/enhanced_pr_manager.sh process ready-first
   ```

2. Weekly comprehensive cleanup:
   ```bash
   ./scripts/enhanced_pr_manager.sh process all
   ./scripts/enhanced_pr_manager.sh report
   ```

3. Monitor emergency states and failed merges

### For CI/CD Integration
```yaml
# Example GitHub Actions workflow
name: Auto-merge PRs
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  
jobs:
  auto-merge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup GitHub CLI
        run: |
          echo "${{ secrets.GITHUB_TOKEN }}" | gh auth login --with-token
      - name: Process ready PRs
        run: |
          ./scripts/enhanced_pr_manager.sh process ready-first
```

---

**Note**: Always test conflict resolution scripts in a safe environment before using in production. The scripts are designed to be conservative and create backups, but manual verification is recommended for critical changes.