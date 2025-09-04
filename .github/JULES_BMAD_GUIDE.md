# 🚀 Jules + BMAD Integration Guide

This guide explains how to use Jules (GitHub AI agent) with the BMAD Method for automated story development, implementation, and review.

## 🎯 Quick Start

### 1. **Create a BMAD Task Issue**
Use the BMAD Story Development issue template or create a custom issue:

```markdown
## BMAD Task: Create Landing Page Story

**Task Type:** Create New Story (Scrum Master)
**Epic/Story:** EPIC1-STORY1.1
**BMAD Agent:** @sm
**Command:** *create-next-story

**Context:**
Create a comprehensive story for implementing the landing page component with:
- Dark theme with gold accents (#c9a961)
- Responsive design for all devices
- Hero section with call-to-action buttons
- Social proof and trust indicators
- Smooth animations and floating gradients

**Acceptance Criteria:**
- [ ] Story follows BMAD template format
- [ ] All acceptance criteria are clearly defined
- [ ] Technical context is sufficient for implementation
- [ ] Integration approach is documented
- [ ] Testing requirements are specified
```

### 2. **Tag Jules for Execution**
Add the `jules` label to the issue:
1. Click the gear icon next to "Labels" on the issue
2. Add the label `jules` (case insensitive)
3. Jules will automatically comment and start working

### 3. **Jules Executes BMAD Workflow**
Jules will:
- Load the specified BMAD agent (@sm, @dev, @qa)
- Execute the requested command (*create-next-story, *review-story, etc.)
- Follow BMAD best practices
- Update story files in `docs/stories/`
- Provide completion summary and link to PR

### 4. **Automatic Codex Review**
After Jules completes the task:
- Jules tags @codex in the completion comment
- Codex performs code review and quality assessment
- If approved, changes are automatically merged (for low-risk changes)

## 🔧 BMAD Task Types

### **Story Creation Tasks**

#### Create New Story (Scrum Master)
```yaml
Agent: @sm
Command: *create-next-story
Purpose: Create implementation-ready story from epic requirements
Output: docs/stories/EPIC-STORY.md
```

#### Create Brownfield Story (Scrum Master)
```yaml
Agent: @sm  
Command: *brownfield-create-story
Purpose: Create story for existing codebase modifications
Output: docs/stories/EPIC-STORY.md
```

### **Development Tasks**

#### Implement Story (Developer)
```yaml
Agent: @dev
Command: implement story {story-name}
Purpose: Execute all tasks and subtasks in approved story
Output: Code changes + updated story file
```

### **Quality Assurance Tasks**

#### Review Story (QA/Test Architect)
```yaml
Agent: @qa
Command: *review-story {story-name}
Purpose: Comprehensive code review and quality assessment
Output: QA Results section + gate file
```

#### Risk Assessment (QA)
```yaml
Agent: @qa
Command: *risk {story-name}
Purpose: Identify potential risks and mitigation strategies
Output: docs/qa/assessments/{epic}.{story}-risk-{date}.md
```

#### Test Design (QA)
```yaml
Agent: @qa
Command: *design {story-name}
Purpose: Create comprehensive test strategy
Output: docs/qa/assessments/{epic}.{story}-test-design-{date}.md
```

### **Project Management Tasks**

#### Create Epic (Product Manager)
```yaml
Agent: @pm
Command: *brownfield-create-epic
Purpose: Create new epic from project requirements
Output: docs/epics/EPIC-NAME.md
```

#### Shard Documentation (BMAD Master)
```yaml
Agent: @bmad-master
Command: *shard-doc {document}
Purpose: Break down large documents into manageable pieces
Output: Sharded documents in appropriate directories
```

## 📋 Issue Templates

### Using the BMAD Story Development Template

1. Go to **Issues** → **New Issue**
2. Select **"BMAD Story Development Task"**
3. Fill out the form:
   - **Task Type:** Select from dropdown
   - **Epic/Story Name:** e.g., EPIC1-STORY1.1
   - **Context:** Detailed requirements
   - **Priority:** High/Medium/Low
   - **Automation Options:** Check desired features

### Manual Issue Creation

```markdown
## BMAD Task: [Task Title]

**Agent:** @[agent-name]
**Command:** [command]
**Epic/Story:** [epic-story-name]

**Context:**
[Detailed description of what needs to be done]

**Automation:**
- [x] Auto-trigger Codex review after completion
- [ ] Create follow-up tasks if dependencies found

**Additional Notes:**
[Any special instructions or constraints]
```

## 🔄 Automation Workflows

### Daily BMAD Scheduler
Automatically creates BMAD tasks every weekday at 9 AM UTC:
- Creates 3 random tasks from the BMAD task queue
- Avoids duplicate issues
- Provides weekly summaries on Mondays

### Jules → Codex Integration
When Jules completes a task:
1. Jules comments with completion summary
2. Jules tags @codex for review
3. Workflow automatically triggers Codex review
4. Codex provides detailed assessment
5. Low-risk approved changes are auto-merged

### Auto-completion
When Codex approves work:
- Issue is labeled as 'completed' and 'automated'
- Issue is automatically closed
- Completion summary is posted

## 🎯 Best Practices

### For Story Creation
- Provide clear context and requirements
- Reference existing epics and architecture docs
- Specify integration points and constraints
- Include testing requirements

### For Development Tasks
- Ensure story is approved before implementation
- Provide specific implementation guidance
- Reference coding standards and patterns
- Include performance and security considerations

### For QA Tasks
- Specify focus areas for review
- Include risk tolerance level
- Mention specific testing requirements
- Reference quality gates and standards

## 📂 File Organization

BMAD automation creates and updates files in structured locations:

```
docs/
├── stories/           # User stories
│   ├── EPIC1-STORY1.1.md
│   └── EPIC2-STORY2.1.md
├── epics/            # Epic definitions
│   ├── EPIC1-LANDING.md
│   └── EPIC2-AUTH.md
├── qa/               # QA assessments
│   ├── assessments/
│   └── gates/
├── prd/              # Sharded PRD sections
└── architecture/     # Sharded architecture docs
```

## 🚨 Troubleshooting

### Jules Not Responding
1. Verify the `jules` label is applied
2. Check that Jules app has repo access
3. Ensure issue has sufficient context
4. Try removing and re-adding the label

### BMAD Agent Errors
1. Verify agent name is correct (@sm, @dev, @qa)
2. Check command syntax (*create-next-story, etc.)
3. Ensure required files exist (epics, architecture)
4. Review BMAD documentation for requirements

### Codex Review Issues
1. Check that @codex was properly tagged
2. Verify automation workflow is enabled
3. Review workflow permissions
4. Check for rate limiting issues

## 🔧 Configuration

### Environment Setup
Ensure your repository has:
- Jules GitHub app installed and authorized
- BMAD Method integrated
- Proper file structure (docs/, etc.)
- Workflow permissions enabled

### Workflow Customization
Edit `.github/workflows/bmad-jules-automation.yml` to:
- Modify automation triggers
- Adjust review criteria
- Change notification settings
- Update auto-merge conditions

## 📊 Monitoring

### Task Statistics
The daily scheduler provides weekly summaries with:
- Total BMAD tasks created
- Open vs. completed tasks
- In-progress task count
- Automation health status

### Success Metrics
Monitor these indicators:
- Task completion rate
- Time from creation to completion
- Code review approval rate
- Auto-merge success rate

---

## 🚀 Quick Reference

| Need | Action |
|------|--------|
| Create Story | New issue → BMAD template → Select "Create New Story" → Add `jules` label |
| Implement Feature | New issue → Manual creation → @dev + implement story → Add `jules` label |
| Review Code | New issue → Manual creation → @qa + *review-story → Add `jules` label |
| Risk Assessment | New issue → Manual creation → @qa + *risk → Add `jules` label |

**Remember:** Always add the `jules` label to trigger automation! 🏷️
