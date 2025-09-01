# BMAD Advanced Elicitation Guidelines for Agent Workflow

This document provides detailed guidelines for implementing BMAD Advanced Elicitation Techniques within the Blackletter Systems agent workflow. These techniques enable deeper exploration of ideas and enhanced content quality through structured elicitation methods.

## Overview

Advanced elicitation provides optional reflective and brainstorming actions to enhance content quality by enabling deeper exploration of ideas through structured elicitation techniques. These methods support iterative refinement through multiple analytical perspectives.

## When to Apply Advanced Elicitation

Agents MUST apply advanced elicitation techniques in the following scenarios:

1. **After Drafting Significant Sections**: When completing substantial portions of code, documentation, or design
2. **Before Finalizing Complex Components**: Prior to marking complex features as complete
3. **When Stakeholder Input is Valuable**: When working on features that would benefit from diverse perspectives
4. **During Problem-Solving**: When encountering challenging design or implementation decisions

## Core Elicitation Methods

### Always Include Core Methods (3-4 methods)

1. **Expand or Contract for Audience**: Adjust content detail level for different stakeholder groups
2. **Critique and Refine**: Identify weaknesses and suggest improvements
3. **Identify Potential Risks**: Surface possible issues or failure points
4. **Assess Alignment with Goals**: Verify content supports stated objectives

### Context-Specific Methods (4-5 methods)

#### Technical Content
- **Tree of Thoughts**: Explore multiple reasoning paths for complex problems
- **ReWOO**: Reasoning with working memory for complex logic
- **Meta-Prompting**: Self-reflection on the prompting process

#### User-Facing Content
- **Agile Team Perspective**: Evaluate from developer, tester, and product owner viewpoints
- **Stakeholder Roundtable**: Consider perspectives of various business stakeholders

#### Creative Content
- **Innovation Tournament**: Generate and evaluate multiple creative alternatives
- **Escape Room Challenge**: Think through constraints and creative problem-solving

#### Strategic Content
- **Red Team vs Blue Team**: Debate content from opposing viewpoints
- **Hindsight Reflection**: Evaluate decisions as if made in the future

### Closure Method
- **Proceed / No Further Actions**: Option 9 to continue without further elicitation

## Implementation Process

### 1. Intelligent Method Selection

Before presenting options, agents must analyze:

- **Content Type**: Technical specs, user stories, architecture, requirements, etc.
- **Complexity Level**: Simple, moderate, or complex content
- **Stakeholder Needs**: Who will use this information
- **Risk Level**: High-impact decisions vs routine items
- **Creative Potential**: Opportunities for innovation or alternatives

### 2. Section Context and Review

When invoked after outputting a section:

1. **Provide Context Summary**: Give a brief 1-2 sentence summary of what the user should look for in the section just presented
2. **Explain Visual Elements**: If the section contains diagrams, explain them briefly before offering elicitation options
3. **Clarify Scope Options**: If the section contains multiple distinct items, inform the user they can apply elicitation actions to:
   - The entire section as a whole
   - Individual items within the section (specify which item when selecting an action)

### 3. Present Elicitation Options

**Review Request Process:**

- Ask the user to review the drafted section
- In the SAME message, inform them they can suggest direct changes OR select an elicitation method
- Present 9 intelligently selected methods (0-8) plus "Proceed" (9)
- Keep descriptions short - just the method name
- Await simple numeric selection

**Action List Presentation Format:**

```
**Advanced Elicitation Options**
Choose a number (0-8) or 9 to proceed:

0. [Method Name]
1. [Method Name]
2. [Method Name]
3. [Method Name]
4. [Method Name]
5. [Method Name]
6. [Method Name]
7. [Method Name]
8. [Method Name]
9. Proceed / No Further Actions
```

### 4. Method Execution Framework

**Execution Process:**

1. **Retrieve Method**: Access the specific elicitation method from the elicitation-methods data file
2. **Apply Context**: Execute the method from your current role's perspective
3. **Provide Results**: Deliver insights, critiques, or alternatives relevant to the content
4. **Re-offer Choice**: Present the same 9 options again until user selects 9 or gives direct feedback

**Execution Guidelines:**

- **Be Concise**: Focus on actionable insights, not lengthy explanations
- **Stay Relevant**: Tie all elicitation back to the specific content being analyzed
- **Identify Personas**: For multi-persona methods, clearly identify which viewpoint is speaking
- **Maintain Flow**: Keep the process moving efficiently

## Integration with Context Engineering Workflow

Advanced elicitation techniques should be integrated into the existing Context Engineering Workflow as follows:

### During Code Implementation
- After drafting significant functions or classes
- Before finalizing complex algorithms
- When making architectural decisions

### During Documentation
- After completing major sections of documentation
- Before finalizing requirements or specifications
- When describing complex processes or workflows

### During Design
- After creating initial UI/UX designs
- Before finalizing system architecture decisions
- When planning integration approaches

## Best Practices

1. **Timing**: Apply advanced elicitation at natural breakpoints in work, not continuously
2. **Selection**: Choose methods that match the content type and stakeholder needs
3. **Conciseness**: Provide focused, actionable feedback rather than lengthy analysis
4. **Relevance**: Always tie elicitation results back to the specific content being reviewed
5. **Efficiency**: Don't force elicitation on every small task; reserve for significant work

## Example Implementation

### Good Implementation

```
I've drafted the user authentication service. Before proceeding, here are advanced elicitation options:

**Advanced Elicitation Options**
Choose a number (0-8) or 9 to proceed:

0. Critique and Refine
1. Identify Potential Risks
2. Assess Alignment with Goals
3. Tree of Thoughts
4. ReWOO
5. Red Team vs Blue Team
6. Agile Team Perspective
7. Stakeholder Roundtable
8. Innovation Tournament
9. Proceed / No Further Actions

Please review the drafted section and either suggest changes directly or select an elicitation method to explore further.
```

### Poor Implementation

```
Here's my code. Do you think it's good?
```

## Quality Standards

When applying advanced elicitation techniques, ensure:

- **Appropriate Timing**: Only apply to substantial work, not minor changes
- **Method Relevance**: Select methods that match the content and context
- **Actionable Insights**: Provide concrete suggestions, not abstract criticism
- **Workflow Integration**: Follow the established presentation and execution framework
- **Documentation**: Record key insights gained through elicitation for knowledge transfer

## Troubleshooting

### Common Issues

1. **Overuse of Elicitation**: Applying techniques to every small task
   - Solution: Reserve for substantial work with complexity or strategic importance

2. **Irrelevant Method Selection**: Choosing methods that don't match content type
   - Solution: Carefully analyze content type and stakeholder needs before selection

3. **Lengthy Responses**: Providing overly detailed analysis during elicitation
   - Solution: Focus on key insights and actionable recommendations

4. **Ignoring Direct Feedback**: Continuing to offer elicitation after receiving direct input
   - Solution: Apply direct feedback and only offer elicitation when explicitly requested

## Related Documentation

- [AGENT_CONTEXT_ENGINEERING_WORKFLOW.md](AGENT_CONTEXT_ENGINEERING_WORKFLOW.md)
- [BMAD-METHOD Documentation](../BMAD-METHOD-main/)

## Conclusion

BMAD Advanced Elicitation Techniques enhance the quality and robustness of agent outputs by providing structured approaches for deeper exploration of ideas. When properly integrated into the workflow, these techniques lead to better solutions, reduced risks, and increased stakeholder satisfaction.
