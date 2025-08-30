#!/usr/bin/env python3
"""
Story Enhancement Template
Automates the process of making draft stories development-ready according to DoR.

Usage:
    python tools/story_enhancement_template.py docs/stories/X.X-story-name.md
"""

import yaml
import sys
from pathlib import Path
from datetime import datetime

class StoryEnhancer:
    def __init__(self):
        self.template_sections = {
            'tasks_subtasks': self._generate_tasks_template,
            'dev_notes': self._generate_dev_notes_template,
            'dev_agent_record': self._generate_dev_agent_record_template,
            'change_log': self._generate_change_log_template
        }

    def enhance_story(self, story_path):
        """Enhance a draft story to meet Definition of Ready requirements."""
        story_file = Path(story_path)

        if not story_file.exists():
            print(f"❌ Story file not found: {story_path}")
            return False

        print(f"📖 Reading story: {story_file.name}")

        # Read current story content
        with open(story_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse YAML front matter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                front_matter = parts[1]
                body = parts[2]
            else:
                print("❌ Invalid YAML front matter format")
                return False
        else:
            print("❌ No YAML front matter found")
            return False

        try:
            story_data = yaml.safe_load(front_matter)
        except yaml.YAMLError as e:
            print(f"❌ YAML parsing error: {e}")
            return False

        # Check if story needs enhancement
        if story_data.get('status') != 'draft':
            print(f"⚠️  Story status is '{story_data.get('status')}', not 'draft'. Skipping.")
            return False

        print("🔧 Enhancing story structure...")

        # Apply enhancements
        enhanced_data = self._apply_enhancements(story_data)

        # Write enhanced story
        self._write_enhanced_story(story_file, enhanced_data, body)

        print("✅ Story enhanced successfully!"        print(f"📋 Next steps:")
        print(f"   1. Review the enhanced story: {story_file}")
        print(f"   2. Customize the technical specifications")
        print(f"   3. Verify file paths and dependencies")
        print(f"   4. Update status to 'approved' when ready")

        return True

    def _apply_enhancements(self, story_data):
        """Apply all required enhancements to story data."""
        enhanced = story_data.copy()

        # Add missing sections
        for section, generator in self.template_sections.items():
            if section not in enhanced or not enhanced[section]:
                print(f"   ➕ Adding {section} section")
                enhanced[section] = generator(story_data)

        # Ensure dependencies section exists
        if 'dependencies' not in enhanced.get('dev_agent_record', {}):
            enhanced.setdefault('dev_agent_record', {})['dependencies'] = [
                "story: X.X-dependency-name (description)"
            ]

        return enhanced

    def _generate_tasks_template(self, story_data):
        """Generate tasks_subtasks template based on story type."""
        story_title = story_data.get('title', '').lower()

        if 'ui' in story_title or 'frontend' in story_title:
            return """- [ ] **Frontend Implementation**
  - [ ] Create React components following existing patterns
  - [ ] Implement user interactions and state management
  - [ ] Add proper TypeScript types and interfaces
  - [ ] Style components using established design system
- [ ] **API Integration**
  - [ ] Connect to backend APIs with proper error handling
  - [ ] Implement loading states and user feedback
  - [ ] Add optimistic updates where appropriate
- [ ] **Testing**
  - [ ] Write unit tests for components
  - [ ] Add integration tests for user flows
  - [ ] Test accessibility and responsive design
- [ ] **Documentation**
  - [ ] Update component documentation
  - [ ] Add usage examples and props documentation"""

        elif 'api' in story_title or 'backend' in story_title:
            return """- [ ] **Backend Service**
  - [ ] Create service class following dependency injection pattern
  - [ ] Implement core business logic with proper error handling
  - [ ] Add input validation and data sanitization
  - [ ] Integrate with existing services and repositories
- [ ] **API Endpoints**
  - [ ] Create FastAPI router with proper request/response models
  - [ ] Implement authentication and authorization
  - [ ] Add comprehensive error responses
  - [ ] Document API with OpenAPI specifications
- [ ] **Database/Data Layer**
  - [ ] Design data models and schemas
  - [ ] Implement data access layer
  - [ ] Add data validation and constraints
- [ ] **Testing**
  - [ ] Write unit tests for service logic
  - [ ] Add integration tests for API endpoints
  - [ ] Create test fixtures and mock data"""

        else:
            return """- [ ] **Core Implementation**
  - [ ] Implement main functionality following established patterns
  - [ ] Add proper error handling and logging
  - [ ] Integrate with dependent services
- [ ] **Configuration**
  - [ ] Add environment variable configuration
  - [ ] Implement feature flags and toggles
- [ ] **Testing**
  - [ ] Create comprehensive unit tests
  - [ ] Add integration tests for end-to-end flows
  - [ ] Test error scenarios and edge cases"""

    def _generate_dev_notes_template(self, story_data):
        """Generate comprehensive dev_notes template."""
        epic = story_data.get('epic', 'X')
        story_id = story_data.get('id', 'X.X')

        return f"""**General Notes:**
  - Implementation follows established patterns in apps/api/blackletter_api/
  - Use dependency injection and service layer architecture
  - Ensure proper error handling and logging throughout

**Source Tree:**
  - apps/api/blackletter_api/services/{story_id.replace('.', '_')}_service.py
  - apps/api/blackletter_api/tests/unit/test_{story_id.replace('.', '_')}.py
  - apps/api/blackletter_api/tests/integration/test_{story_id.replace('.', '_')}_flow.py

**Technical Specification:**
  - Service interfaces and method signatures
  - Data models and validation schemas
  - External dependencies and library requirements
  - Performance and scalability considerations

**Testing:**
  - Unit tests for core logic and edge cases
  - Integration tests for end-to-end functionality
  - Error scenario testing and validation
  - Test coverage target: ≥80%

**UX Implications:**
  - User experience impact and considerations
  - Error messaging and user feedback
  - Loading states and performance expectations

**Test Data:**
  - Synthetic fixtures: tests/fixtures/{story_id.replace('.', '_')}_test_data.json
  - Mock data for unit tests
  - Edge case scenarios and error conditions"""

    def _generate_dev_agent_record_template(self, story_data):
        """Generate dev_agent_record template."""
        return {
            'proposed_tasks': [
                'backend: Implement core service logic',
                'api: Create necessary API endpoints',
                'tests: Comprehensive test coverage',
                'docs: Update API documentation'
            ],
            'dependencies': [
                'story: X.X-dependency-name (provides required functionality)'
            ],
            'open_decisions': [
                'Technology choices and library selection',
                'API design and data contracts',
                'Error handling strategy'
            ],
            'impl_notes': [
                'Follow existing service patterns in apps/api/blackletter_api/services/',
                'Use dependency injection pattern established in the codebase',
                'Ensure proper logging and monitoring integration',
                'Consider performance implications and optimization opportunities'
            ]
        }

    def _generate_change_log_template(self, story_data):
        """Generate change_log template."""
        return [{
            'date': datetime.now().strftime('%Y-%m-%d'),
            'version': '1.0',
            'description': 'Enhanced story to meet Definition of Ready requirements with detailed tasks, technical specifications, test data, and dependencies',
            'author': 'Story Enhancement Tool'
        }]

    def _write_enhanced_story(self, story_file, enhanced_data, body):
        """Write the enhanced story back to file."""
        # Convert enhanced data back to YAML
        yaml_content = yaml.dump(enhanced_data, default_flow_style=False, sort_keys=False)

        # Write the complete file
        with open(story_file, 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write(yaml_content)
            f.write('---\n')
            f.write(body)


def main():
    if len(sys.argv) != 2:
        print("Usage: python tools/story_enhancement_template.py <story_file>")
        print("Example: python tools/story_enhancement_template.py docs/stories/2.3-weak-language-lexicon.md")
        sys.exit(1)

    story_path = sys.argv[1]
    enhancer = StoryEnhancer()

    success = enhancer.enhance_story(story_path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
