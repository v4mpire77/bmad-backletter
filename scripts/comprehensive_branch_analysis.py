#!/usr/bin/env python3
"""
Comprehensive script to analyze which branches are ahead of main using GitHub API data.
This script identifies branches that have commits not present in main.
"""

import subprocess
import json
import sys
import requests
from typing import List, Dict, Any
from datetime import datetime

# GitHub repository information
GITHUB_OWNER = "v4mpire77"
GITHUB_REPO = "bmad-backletter"
MAIN_BRANCH_SHA = "1d3bf9d5c4815fe89fbb7a07a78efe0a750f611e"

# All branches data from GitHub API
ALL_BRANCHES = [
    {"name":"bmad-merge-plan","commit":{"sha":"18c79d236ceb8349b5531b7c5e07b8de429d2a17"}},
    {"name":"chore/cleanup-story-0-state","commit":{"sha":"f1c76832049aa35c6c13346063b75c3ce0ce3d53"}},
    {"name":"chore/render-blueprint","commit":{"sha":"87fd155a7ca79b545b2e25ca15490d63149c23e7"}},
    {"name":"cleanup-build-files","commit":{"sha":"70a3c4bbbfa33cb0920363fce0c7af7b34e405e8"}},
    {"name":"codespace-legendary-couscous-r4xvr594rv67cw4w","commit":{"sha":"ed699242f8ed04e3c044540c09420f68544490e3"}},
    {"name":"codespace-orange-waddle-x54q9g65946426p5v","commit":{"sha":"4a2f00a5644fb06ac7606404e83bc00231f662c8"}},
    {"name":"codex/act-as-agent-winston-the-architect","commit":{"sha":"412997542bcf6d76808886171a97c153e1f25c6a"}},
    {"name":"codex/add-bmad-scripts-to-package.json","commit":{"sha":"40b9c9402fad544deee392a7297a27aa0d781854"}},
    {"name":"codex/add-bmad-scripts-to-package.json-y39co9","commit":{"sha":"de4f3910b5bddc28bf42ef3145b5dae22462c983"}},
    {"name":"codex/add-codex-integration","commit":{"sha":"0ab05f1c73eaf26c70746a2bce24628735fa9dd8"}},
    {"name":"copilot/fix-5c8bc92a-3fd1-4b8a-84c8-de7f7dfb7d0c","commit":{"sha":"7b6ea0155237e92f161fd54249405fc3bd29720a"}},
    {"name":"copilot/fix-236","commit":{"sha":"4feaec2f7e09134733083d23fa0092aa936f0250"}},
    {"name":"copilot/fix-734d4d9e-74ce-4273-b753-b2eb3dd61016","commit":{"sha":"ce5d8510689650f5fdad64f5a28ef8ad4d9443d1"}},
    {"name":"copilot/fix-769c616d-edaa-4a4e-9db7-85c5bdadeb6b","commit":{"sha":"6578ea320183a7f136077c9f3da304b0109518cc"}},
    {"name":"copilot/fix-d6cc7f7b-05d8-4631-a04c-fb7bc3ddf9d7","commit":{"sha":"95aa58ab3069c6cc1fcb8eedf3241ebc37c0b996"}},
    {"name":"copilot/fix-e9df34de-24a3-45cb-9858-f0ca6c8907ae","commit":{"sha":"ec1f8785148174e575923fa98359fa8161bfdd39"}},
    {"name":"copilot/fix-edd60661-99f0-4b6b-af62-4cf428e17dfb","commit":{"sha":"43d25945b983cc9e402d18ea62eb4a042e5d5357"}},
    {"name":"copilot/fix-f23696e4-ec15-4e56-afa1-aa17d6bfb0f6","commit":{"sha":"1ccbff47adf07360845d512bc7095cd0159428dd"}},
    {"name":"docs/ux-spec","commit":{"sha":"0e0fc2bd40a30b40bb37c958ff4ecab93ed31706"}},
    {"name":"feat/EPIC5-STORY5.1-org-settings","commit":{"sha":"6e351c0c7e984f84d1343cff8dc325cd27903df6"}},
    {"name":"feat/new-landing-page","commit":{"sha":"6b52e4a48de38c572bd8c1ee4358bdb8feaa3bcd"}},
    {"name":"feat/story-1.1-backend","commit":{"sha":"d09f9bfa3fa7788b42ff09c3b5b43abcd9af95a5"}},
    {"name":"feat-a11y-improvements","commit":{"sha":"61ab5d68de64cde126ffed9c8523c613102c6f98"}},
    {"name":"feature/EPIC3-STORY3.3-dashboard-history","commit":{"sha":"f77afcbd9a78d12e5bbd7d934657000e7820850f"}},
    {"name":"feature/EPIC4-STORY4.2-coverage-meter","commit":{"sha":"a51fc08594788721606b106e22fa741f7663bd56"}},
    {"name":"feature/add-render-build-caching","commit":{"sha":"d3a83a9a63081955e480583438ce0fc55bd6fc0f"}},
    {"name":"feature/blackletter-v0-0-mvp","commit":{"sha":"4705f2be688e8599fd54c3ddb7670ac46b9b6311"}},
    {"name":"feature/complete-story-1.3","commit":{"sha":"f3668ae4a6e7798d7a03bfe4507b30f51f83157f"}},
    {"name":"feature/create-story-epic2-story2.5","commit":{"sha":"842109eb425cfedf576192b556b06822377c1dc2"}},
    {"name":"feature/findings-table","commit":{"sha":"ed05c6533f2c906ea221b6977390adeb2ce440c8"}},
    {"name":"feature/new-landing-page","commit":{"sha":"a97272146f552f10e34c10c4abbd47c6499381b8"}},
    {"name":"fix/epic-0-bugs","commit":{"sha":"87a0bb09b517f63c369f3ed70f646419910b22ce"}},
    {"name":"import-blackletter-upstream","commit":{"sha":"c1bb247f7b2a787b18ffa3f0f13fa481755b2faa"}},
    {"name":"jules-optimization-plan","commit":{"sha":"1589d8b08df9a6cde5b821ed722b9e2a920061ff"}},
    {"name":"main","commit":{"sha":"1d3bf9d5c4815fe89fbb7a07a78efe0a750f611e"}},
    {"name":"repo-audit","commit":{"sha":"488c371431752e4323b35c1071411e630d127888"}},
    {"name":"story/EPIC2-STORY2.4-approve","commit":{"sha":"2f9bce01e9c3f1446ad1394509293abcd7240d19"}},
    {"name":"story/create-epic5-story5.2","commit":{"sha":"ff97c7142aa5b6b31c96a9891f4919e02daf97a1"}},
    {"name":"story/create-landing-page-ux-story","commit":{"sha":"1dc71f3a41ac821b1f7721fdf80dede73fd1d43d"}},
    {"name":"story/epic4-story4.1-metrics-wall","commit":{"sha":"db3005e86628feafbccb3f19e3cca3cb24dbe84e"}},
    {"name":"work","commit":{"sha":"ad94b849badc9dfff529ef0aff0c163c397e36c6"}}
]

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

def fetch_branch_if_needed(branch_name: str) -> bool:
    """Fetch a branch from remote if not available locally."""
    try:
        # Try to fetch the specific branch
        run_git_command(['git', 'fetch', 'origin', f'{branch_name}:{branch_name}'])
        return True
    except:
        # If fetch fails, try to fetch the remote ref
        try:
            run_git_command(['git', 'fetch', 'origin', branch_name])
            return True
        except:
            return False

def analyze_branch_against_main(branch_name: str, branch_sha: str) -> Dict[str, Any]:
    """Analyze if a branch is ahead of main using git commands."""
    if branch_name == 'main':
        return None
    
    # Fetch the branch if needed
    fetch_branch_if_needed(branch_name)
    
    try:
        # Check if the branch SHA is the same as main
        if branch_sha == MAIN_BRANCH_SHA:
            return {
                'name': branch_name,
                'sha': branch_sha,
                'ahead': 0,
                'behind': 0,
                'is_ahead': False,
                'status': 'up-to-date'
            }
        
        # Try to get merge-base with main
        try:
            merge_base = run_git_command(['git', 'merge-base', MAIN_BRANCH_SHA, branch_sha])
            
            # If merge-base equals main SHA, then branch is ahead
            if merge_base == MAIN_BRANCH_SHA:
                # Get commit count from main to branch
                ahead_count = run_git_command(['git', 'rev-list', '--count', f'{MAIN_BRANCH_SHA}..{branch_sha}'])
                ahead_count = int(ahead_count) if ahead_count.isdigit() else 0
                
                return {
                    'name': branch_name,
                    'sha': branch_sha,
                    'ahead': ahead_count,
                    'behind': 0,
                    'is_ahead': ahead_count > 0,
                    'status': 'ahead' if ahead_count > 0 else 'up-to-date'
                }
            
            # If merge-base equals branch SHA, then branch is behind
            elif merge_base == branch_sha:
                behind_count = run_git_command(['git', 'rev-list', '--count', f'{branch_sha}..{MAIN_BRANCH_SHA}'])
                behind_count = int(behind_count) if behind_count.isdigit() else 0
                
                return {
                    'name': branch_name,
                    'sha': branch_sha,
                    'ahead': 0,
                    'behind': behind_count,
                    'is_ahead': False,
                    'status': 'behind'
                }
            
            # Branch has diverged
            else:
                ahead_count = run_git_command(['git', 'rev-list', '--count', f'{merge_base}..{branch_sha}'])
                behind_count = run_git_command(['git', 'rev-list', '--count', f'{merge_base}..{MAIN_BRANCH_SHA}'])
                ahead_count = int(ahead_count) if ahead_count.isdigit() else 0
                behind_count = int(behind_count) if behind_count.isdigit() else 0
                
                return {
                    'name': branch_name,
                    'sha': branch_sha,
                    'ahead': ahead_count,
                    'behind': behind_count,
                    'is_ahead': ahead_count > 0,
                    'status': 'diverged'
                }
                
        except:
            # If git operations fail, try simple comparison
            # Assume if SHA is different from main, it might be ahead
            return {
                'name': branch_name,
                'sha': branch_sha,
                'ahead': 1,  # Assume at least 1 commit ahead
                'behind': 0,
                'is_ahead': True,
                'status': 'likely-ahead',
                'note': 'Analysis based on different SHA (detailed git analysis failed)'
            }
            
    except Exception as e:
        return {
            'name': branch_name,
            'sha': branch_sha,
            'ahead': 0,
            'behind': 0,
            'is_ahead': False,
            'status': 'error',
            'error': str(e)
        }

def get_commit_info(branch_name: str, commit_sha: str) -> Dict[str, str]:
    """Get commit information for a branch."""
    try:
        # Try to get commit info using git log
        commit_info = run_git_command([
            'git', 'log', '-1', '--format=%H|%s|%an|%ai', commit_sha
        ])
        
        if commit_info:
            parts = commit_info.split('|')
            return {
                'sha': parts[0] if len(parts) > 0 else commit_sha,
                'message': parts[1] if len(parts) > 1 else '',
                'author': parts[2] if len(parts) > 2 else '',
                'date': parts[3] if len(parts) > 3 else ''
            }
    except:
        pass
    
    # Return basic info if git command fails
    return {
        'sha': commit_sha,
        'message': f'Branch: {branch_name}',
        'author': 'Unknown',
        'date': 'Unknown'
    }

def analyze_all_branches() -> Dict[str, Any]:
    """Analyze all branches from GitHub API data."""
    print("🔍 Analyzing branches ahead of main using comprehensive branch data...")
    print(f"📍 Main branch SHA: {MAIN_BRANCH_SHA}")
    print(f"📊 Total branches to analyze: {len(ALL_BRANCHES)}")
    
    ahead_branches = []
    all_analysis = []
    
    for i, branch_data in enumerate(ALL_BRANCHES):
        branch_name = branch_data['name']
        branch_sha = branch_data['commit']['sha']
        
        print(f"📝 Analyzing {i+1}/{len(ALL_BRANCHES)}: {branch_name}")
        
        analysis = analyze_branch_against_main(branch_name, branch_sha)
        
        if analysis:
            # Add commit info
            commit_info = get_commit_info(branch_name, branch_sha)
            analysis['latest_commit'] = commit_info
            
            all_analysis.append(analysis)
            
            if analysis.get('is_ahead', False):
                ahead_branches.append(analysis)
    
    # Sort ahead branches by number of commits ahead (descending)
    ahead_branches.sort(key=lambda x: x.get('ahead', 0), reverse=True)
    
    return {
        'main_sha': MAIN_BRANCH_SHA,
        'total_branches': len(ALL_BRANCHES),
        'branches_ahead': ahead_branches,
        'ahead_count': len(ahead_branches),
        'all_analysis': all_analysis,
        'analysis_timestamp': datetime.now().isoformat()
    }

def print_results(results: Dict[str, Any]) -> None:
    """Print analysis results in a formatted way."""
    print("\n" + "="*80)
    print("🎯 BRANCHES AHEAD OF MAIN - COMPREHENSIVE ANALYSIS")
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
        print(f"   📊 Status: {branch.get('status', 'unknown')}")
        print(f"   📈 Commits ahead: {branch['ahead']}")
        print(f"   📉 Commits behind: {branch['behind']}")
        print(f"   🔗 SHA: {branch['sha'][:12]}...")
        
        latest = branch.get('latest_commit', {})
        if latest.get('message'):
            print(f"   💬 Latest message: {latest['message']}")
            print(f"   👤 Author: {latest['author']}")
            print(f"   📅 Date: {latest['date']}")
        
        if 'note' in branch:
            print(f"   📝 Note: {branch['note']}")
        
        if 'error' in branch:
            print(f"   ⚠️  Error: {branch['error']}")

def save_results(results: Dict[str, Any]) -> None:
    """Save results to a JSON file."""
    output_file = '/home/runner/work/bmad-backletter/bmad-backletter/comprehensive_branches_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Comprehensive results saved to: {output_file}")

def create_summary_report(results: Dict[str, Any]) -> None:
    """Create a markdown summary report."""
    report_file = '/home/runner/work/bmad-backletter/bmad-backletter/BRANCHES_AHEAD_REPORT.md'
    
    with open(report_file, 'w') as f:
        f.write("# Branches Ahead of Main - Analysis Report\n\n")
        f.write(f"**Analysis Date:** {results['analysis_timestamp']}\n\n")
        f.write(f"**Main Branch SHA:** `{results['main_sha']}`\n\n")
        f.write(f"**Total Branches:** {results['total_branches']}\n\n")
        f.write(f"**Branches Ahead:** {results['ahead_count']}\n\n")
        
        if results['ahead_count'] > 0:
            f.write("## Branches Ahead of Main\n\n")
            
            for i, branch in enumerate(results['branches_ahead'], 1):
                f.write(f"### {i}. `{branch['name']}`\n\n")
                f.write(f"- **Status:** {branch.get('status', 'unknown')}\n")
                f.write(f"- **Commits Ahead:** {branch['ahead']}\n")
                f.write(f"- **Commits Behind:** {branch['behind']}\n")
                f.write(f"- **SHA:** `{branch['sha']}`\n")
                
                latest = branch.get('latest_commit', {})
                if latest.get('message'):
                    f.write(f"- **Latest Commit:** {latest['message']}\n")
                    f.write(f"- **Author:** {latest['author']}\n")
                    f.write(f"- **Date:** {latest['date']}\n")
                
                if 'note' in branch:
                    f.write(f"- **Note:** {branch['note']}\n")
                    
                f.write("\n")
        else:
            f.write("## Result\n\n")
            f.write("✅ All branches are up to date with main!\n\n")
    
    print(f"📄 Summary report saved to: {report_file}")

def main():
    """Main function."""
    try:
        results = analyze_all_branches()
        print_results(results)
        save_results(results)
        create_summary_report(results)
        
        # Return appropriate exit code
        if results['ahead_count'] > 0:
            print(f"\n🎯 Found {results['ahead_count']} branches ahead of main")
            sys.exit(0)  # Success with branches found
        else:
            print("\n✅ All branches are up to date with main")
            sys.exit(0)  # Success with no branches ahead
            
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()