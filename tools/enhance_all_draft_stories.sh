#!/bin/bash
# Batch enhance all draft stories to meet Definition of Ready requirements
# Usage: ./tools/enhance_all_draft_stories.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
STORY_DIR="$PROJECT_ROOT/docs/stories"

echo "🔍 Finding all draft stories in $STORY_DIR..."

# Find all draft stories
DRAFT_STORIES=$(grep -l "status: draft" "$STORY_DIR"/*.md || true)

if [ -z "$DRAFT_STORIES" ]; then
    echo "✅ No draft stories found. All stories are ready!"
    exit 0
fi

echo "📋 Found draft stories:"
echo "$DRAFT_STORIES" | sed 's|.*/||' | sed 's|^|  - |'

echo ""
echo "🚀 Enhancing draft stories..."

for story in $DRAFT_STORIES; do
    echo "🔧 Processing: $(basename "$story")"

    if [ -f "$SCRIPT_DIR/story_enhancement_template.py" ]; then
        python "$SCRIPT_DIR/story_enhancement_template.py" "$story"
    else
        echo "❌ Enhancement script not found: $SCRIPT_DIR/story_enhancement_template.py"
        exit 1
    fi

    echo "✅ Enhanced: $(basename "$story")"
    echo ""
done

echo "🎉 All draft stories have been enhanced!"
echo ""
echo "📝 Next steps:"
echo "  1. Review each enhanced story for accuracy"
echo "  2. Customize technical specifications as needed"
echo "  3. Verify file paths and dependencies are correct"
echo "  4. Update story status to 'approved' when ready for development"
