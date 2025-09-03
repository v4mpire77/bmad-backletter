#!/usr/bin/env python3
"""
Quick summary script to answer: "What branches are ahead of main?"
"""

import json

def load_analysis():
    """Load the comprehensive analysis results."""
    try:
        with open('/home/runner/work/bmad-backletter/bmad-backletter/comprehensive_branches_analysis.json', 'r') as f:
            return json.load(f)
    except:
        return None

def print_summary():
    """Print a concise summary of branches ahead of main."""
    data = load_analysis()
    if not data:
        print("❌ No analysis data found. Run the comprehensive analysis first.")
        return
    
    print("🎯 BRANCHES AHEAD OF MAIN - QUICK SUMMARY")
    print("=" * 60)
    print(f"📊 Total branches analyzed: {data['total_branches']}")
    print(f"🚀 Branches ahead of main: {data['ahead_count']}")
    print(f"📍 Main branch SHA: {data['main_sha'][:12]}...")
    
    if data['ahead_count'] == 0:
        print("\n✅ All branches are up to date with main!")
        return
    
    # Group by status
    ahead_branches = data['branches_ahead']
    
    # Count by status
    status_counts = {}
    for branch in ahead_branches:
        status = branch.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print(f"\n📈 Branch Status Distribution:")
    for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {status}: {count} branches")
    
    # Top 10 branches with most commits ahead
    print(f"\n🔝 TOP 10 BRANCHES AHEAD:")
    print("-" * 60)
    
    top_branches = sorted(ahead_branches, key=lambda x: x.get('ahead', 0), reverse=True)[:10]
    
    for i, branch in enumerate(top_branches, 1):
        name = branch['name']
        ahead = branch['ahead']
        status = branch.get('status', 'unknown')
        sha = branch['sha'][:8]
        
        # Truncate long branch names
        if len(name) > 35:
            name = name[:32] + "..."
        
        print(f"{i:2}. {name:<38} | {ahead:3} commits | {status} | {sha}")
    
    # Category breakdown
    print(f"\n📋 BRANCH CATEGORIES:")
    print("-" * 60)
    
    categories = {
        'copilot/': [],
        'codex/': [],
        'feature/': [],
        'feat/': [],
        'story/': [],
        'fix/': [],
        'chore/': [],
        'docs/': [],
        'other': []
    }
    
    for branch in ahead_branches:
        name = branch['name']
        categorized = False
        
        for prefix, branches_list in categories.items():
            if prefix != 'other' and name.startswith(prefix):
                branches_list.append(branch)
                categorized = True
                break
        
        if not categorized:
            categories['other'].append(branch)
    
    for category, branches_list in categories.items():
        if branches_list:
            total_commits = sum(b.get('ahead', 0) for b in branches_list)
            print(f"   • {category:<12} {len(branches_list):2} branches ({total_commits:4} total commits)")
    
    print(f"\n💡 Use the full report at BRANCHES_AHEAD_REPORT.md for detailed analysis")

if __name__ == "__main__":
    print_summary()