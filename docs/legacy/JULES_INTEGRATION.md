# 🤖 Jules + BMAD Automation Guide

This repository includes a complete automation system that integrates **Jules** (GitHub AI agent) with the **BMAD Method** for streamlined story development, implementation, and review.

## 🚀 Quick Start

### 1. **Create a BMAD Task**
- Go to **Issues** → **New Issue**
- Choose **"BMAD Story Development Task"** template
- Fill in the details (agent, command, context)

### 2. **Trigger Jules**
- Add the `jules` label to your issue
- Jules will automatically comment with BMAD instructions
- Jules will execute the task using the specified BMAD agent

### 3. **Automatic Review**
- Jules tags @codex for code review
- Codex performs comprehensive assessment
- Approved tasks are automatically closed

## 📋 Available BMAD Tasks

| Task Type | Agent | Command | Purpose |
|-----------|--------|---------|---------|
| **Create Story** | `@sm` | `*create-next-story` | Generate new implementation story |
| **Develop Feature** | `@dev` | `implement story` | Execute story tasks and coding |
| **Review Code** | `@qa` | `*review-story` | Comprehensive quality assessment |
| **Risk Assessment** | `@qa` | `*risk` | Identify and mitigate risks |
| **Create Epic** | `@pm` | `*brownfield-create-epic` | Generate new epic from requirements |

## 🏷️ Simple Manual Issue Creation

For quick tasks, create an issue like this:

```markdown
## BMAD Task: Create Landing Page Story

**Agent:** @sm
**Command:** *create-next-story
**Epic/Story:** EPIC1-STORY1.1

**Context:**
Create a story for implementing the landing page with dark theme and gold accents.
Include responsive design, hero section, and social proof components.
```

Then add the `jules` label to trigger automation!

## 🔄 Automation Features

- **Daily Scheduling**: Auto-creates BMAD tasks weekdays at 9 AM UTC
- **Smart Detection**: Recognizes BMAD patterns and provides appropriate context
- **Quality Gates**: Codex reviews ensure high standards
- **Auto-completion**: Approved work is automatically merged and closed
- **Follow-up Tasks**: Generates additional tasks based on review feedback

## 📚 Full Documentation

See [`.github/JULES_BMAD_GUIDE.md`](.github/JULES_BMAD_GUIDE.md) for complete instructions, best practices, and troubleshooting.

## 🧪 Test the Integration

1. Create a new issue using the **"Test Jules + BMAD Integration"** template
2. Add the `jules` label
3. Watch the automation workflow in action!

---

**Remember:** Just add the `jules` label to any BMAD-related issue to trigger the complete automation workflow! 🚀
