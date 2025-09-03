#!/usr/bin/env python3
"""
Script to analyze which branches are ahead of main branch.
This script identifies branches that have commits not present in main.
"""

import subprocess
import json
import sys
from typing import List, Dict, Any
from datetime import datetime

def run_git_command(command: List[str]) -> str:
    """Run a git command and return the output."""
    try:
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True,
            cwd='/home/runner/work/bmad-backletter/bmad-backletter'
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {' '.join(command)}")
        print(f"Error: {e.stderr}")
        return ""

def get_main_commit_sha() -> str:
    """Get the current commit SHA of main branch."""
    return run_git_command(['git', 'rev-parse', 'main'])

def get_all_remote_branches() -> List[Dict[str, str]]:
    """Get all remote branches with their commit SHAs."""
    # Fetch all remote branches
    run_git_command(['git', 'fetch', '--all'])
    
    # Get list of remote branches with commit SHAs
    output = run_git_command(['git', 'for-each-ref', '--format=%(refname:short) %(objectname)', 'refs/remotes/origin'])
    
    branches = []
    for line in output.split('\n'):
        if line.strip():
            parts = line.strip().split(' ')
            if len(parts) >= 2:
                branch_name = parts[0].replace('origin/', '')
                commit_sha = parts[1]
                if branch_name != 'HEAD':  # Skip HEAD reference
                    branches.append({
                        'name': branch_name,
                        'sha': commit_sha
                    })
    
    return branches

def is_branch_ahead_of_main(branch_name: str, main_sha: str) -> Dict[str, Any]:
    """Check if a branch is ahead of main and return analysis."""
    try:
        # Get the merge-base between branch and main
        merge_base = run_git_command(['git', 'merge-base', f'origin/{branch_name}', 'main'])
        
        # Get commit count from merge-base to branch
        ahead_count = run_git_command(['git', 'rev-list', '--count', f'{merge_base}..origin/{branch_name}'])
        ahead_count = int(ahead_count) if ahead_count.isdigit() else 0
        
        # Get commit count from merge-base to main 
        behind_count = run_git_command(['git', 'rev-list', '--count', f'{merge_base}..main'])
        behind_count = int(behind_count) if behind_count.isdigit() else 0
        
        # Get latest commit info for the branch
        commit_info = run_git_command([
            'git', 'log', '-1', '--format=%H|%s|%an|%ai', f'origin/{branch_name}'
        ])
        
        commit_parts = commit_info.split('|') if commit_info else ['', '', '', '']
        
        return {
            'name': branch_name,
            'ahead': ahead_count,
            'behind': behind_count,
            'is_ahead': ahead_count > 0,
            'latest_commit': {
                'sha': commit_parts[0],
                'message': commit_parts[1],
                'author': commit_parts[2],
                'date': commit_parts[3]
            }
        }
    except Exception as e:
        print(f"Error analyzing branch {branch_name}: {e}")
        return {
            'name': branch_name,
            'ahead': 0,
            'behind': 0,
            'is_ahead': False,
            'error': str(e)
        }

def analyze_branches() -> Dict[str, Any]:
    """Analyze all branches and find those ahead of main."""
    print("🔍 Analyzing branches ahead of main...")
    
    # Get main commit SHA
    main_sha = get_main_commit_sha()
    print(f"📍 Main branch is at commit: {main_sha}")
    
    # Get all remote branches
    all_branches = get_all_remote_branches()
    print(f"📊 Found {len(all_branches)} total branches")
    
    # Analyze each branch
    ahead_branches = []
    all_analysis = []
    
    for i, branch_info in enumerate(all_branches):
        branch_name = branch_info['name']
        
        # Skip main branch
        if branch_name == 'main':
            continue
            
        print(f"📝 Analyzing {i+1}/{len(all_branches)}: {branch_name}")
        
        analysis = is_branch_ahead_of_main(branch_name, main_sha)
        all_analysis.append(analysis)
        
        if analysis.get('is_ahead', False):
            ahead_branches.append(analysis)
    
    # Sort ahead branches by number of commits ahead (descending)
    ahead_branches.sort(key=lambda x: x.get('ahead', 0), reverse=True)
    
    return {
        'main_sha': main_sha,
        'total_branches': len(all_branches),
        'branches_ahead': ahead_branches,
        'ahead_count': len(ahead_branches),
        'analysis_timestamp': datetime.now().isoformat()
    }

def print_results(results: Dict[str, Any]) -> None:
    """Print analysis results in a formatted way."""
    print("\n" + "="*80)
    print("🎯 BRANCHES AHEAD OF MAIN - ANALYSIS RESULTS")
    print("="*80)
    
    print(f"📍 Main branch SHA: {results['main_sha']}")
    print(f"📊 Total branches analyzed: {results['total_branches']}")
    print(f"🚀 Branches ahead of main: {results['ahead_count']}")
    print(f"⏰ Analysis timestamp: {results['analysis_timestamp']}")
    
    if results['ahead_count'] == 0:
        print("\n✅ No branches are ahead of main!")
        return
    
    print(f"\n📋 BRANCHES AHEAD OF MAIN ({results['ahead_count']} total):")
    print("-" * 80)
    
    for i, branch in enumerate(results['branches_ahead'], 1):
        print(f"\n{i}. 🌿 {branch['name']}")
        print(f"   📈 Commits ahead: {branch['ahead']}")
        print(f"   📉 Commits behind: {branch['behind']}")
        
        latest = branch.get('latest_commit', {})
        if latest.get('sha'):
            print(f"   📝 Latest commit: {latest['sha'][:8]}...")
            print(f"   💬 Message: {latest['message']}")
            print(f"   👤 Author: {latest['author']}")
            print(f"   📅 Date: {latest['date']}")
        
        if 'error' in branch:
            print(f"   ⚠️  Error: {branch['error']}")

def save_results(results: Dict[str, Any]) -> None:
    """Save results to a JSON file."""
    output_file = '/home/runner/work/bmad-backletter/bmad-backletter/branches_ahead_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to: {output_file}")

def main():
    """Main function."""
    try:
        results = analyze_branches()
        print_results(results)
        save_results(results)
        
        # Return appropriate exit code
        if results['ahead_count'] > 0:
            print(f"\n🎯 Found {results['ahead_count']} branches ahead of main")
            sys.exit(0)  # Success with branches found
        else:
            print("\n✅ All branches are up to date with main")
            sys.exit(0)  # Success with no branches ahead
            
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()