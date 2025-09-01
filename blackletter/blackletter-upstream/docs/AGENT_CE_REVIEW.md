# Context Engineering Prompt: REVIEW

## 🎯 Purpose
This prompt ensures that ALL code review and analysis tasks follow the Context Engineering Framework, maintaining code quality and architectural consistency.

## 📋 Required Context

### MANDATORY Documentation Review
- ✅ **Implementation Plan** (`docs/Implementation.md`) - Feature requirements and architecture
- ✅ **Project Structure** (`docs/project_structure.md`) - Code organization standards
- ✅ **Development Workflow** (`docs/Development_Agent_Workflow.md`) - Quality standards
- ✅ **Bug Tracking** (`docs/Bug_tracking.md`) - Issue patterns and prevention
- ✅ **Security Audit Report** (`docs/SECURITY_AUDIT_REPORT.md`) - Security requirements

### MANDATORY Codebase Context
- ✅ **Current Implementation** - Understand what's being reviewed
- ✅ **Architectural Patterns** - Know established design patterns
- ✅ **Component Library** - Understand existing components
- ✅ **API Standards** - Know service patterns and requirements
- ✅ **Testing Standards** - Understand test coverage requirements

## 🔧 Task Execution Protocol

### Step 1: Context Assessment (MANDATORY)
1. **Review Implementation Plan** - Understand feature requirements
2. **Examine Project Structure** - Verify code placement and organization
3. **Check Development Workflow** - Ensure quality standards compliance
4. **Analyze Bug Tracking** - Identify potential issues
5. **Review Security Requirements** - Check security compliance

### Step 2: Code Analysis
1. **Architecture Review** - Verify pattern consistency
2. **Component Analysis** - Check component usage and design
3. **API Review** - Validate endpoint design and patterns
4. **Data Flow Analysis** - Check data handling consistency
5. **Security Validation** - Verify security implementation

### Step 3: Quality Assessment
1. **Code Quality** - Check readability and maintainability
2. **Test Coverage** - Verify testing implementation
3. **Documentation** - Check code documentation quality
4. **Performance** - Assess performance implications
5. **Error Handling** - Verify error management

### Step 4: Feedback and Recommendations
1. **Issue Identification** - Document specific problems
2. **Solution Suggestions** - Provide actionable improvements
3. **Pattern Recommendations** - Suggest architectural improvements
4. **Security Enhancements** - Recommend security improvements
5. **Performance Optimizations** - Suggest performance improvements

## ✅ Quality Standards

### Review Quality
- **Comprehensive Analysis** - Cover all aspects of the code
- **Actionable Feedback** - Provide specific, implementable suggestions
- **Pattern Consistency** - Ensure architectural consistency
- **Security Focus** - Prioritize security considerations
- **Performance Awareness** - Consider performance implications

### Code Quality Standards
- **Test Coverage:** Minimum 80% for all code
- **Type Safety:** 100% TypeScript/Python type coverage
- **Documentation:** Comprehensive and accurate
- **Error Handling:** Proper error boundaries and user feedback
- **Security:** Follow security guidelines and best practices

### Architecture Standards
- **Pattern Consistency:** Follow established architectural patterns
- **Component Reuse:** Utilize existing components appropriately
- **Service Integration:** Follow established service patterns
- **Data Consistency:** Maintain database and API consistency
- **Scalability:** Consider future growth and maintenance

## 🚫 Prohibited Actions

### WITHOUT PROPER CONTEXT
- ❌ **Review code** without understanding requirements
- ❌ **Suggest changes** without knowing architecture
- ❌ **Recommend patterns** without understanding context
- ❌ **Ignore security** without security review
- ❌ **Skip testing** without understanding test requirements

### REVIEW VIOLATIONS
- ❌ **Superficial review** - Must be comprehensive
- ❌ **Vague feedback** - Must be specific and actionable
- ❌ **Ignore patterns** - Must maintain consistency
- ❌ **Skip security** - Security review mandatory
- ❌ **Ignore performance** - Performance consideration required

## 📚 Required Documentation

### Before Review
- [ ] Implementation Plan reviewed and understood
- [ ] Project Structure analyzed and verified
- [ ] Development Workflow standards reviewed
- [ ] Bug Tracking patterns analyzed
- [ ] Security requirements understood

### During Review
- [ ] Architecture patterns verified
- [ ] Component usage analyzed
- [ ] API design validated
- [ ] Security implementation checked
- [ ] Performance implications assessed

### After Review
- [ ] Issues documented with specific details
- [ ] Solutions suggested with implementation guidance
- [ ] Pattern recommendations provided
- [ ] Security improvements identified
- [ ] Performance optimizations suggested

## 🔍 Validation Checklist

### Context Validation
- [ ] Implementation Plan reviewed and understood
- [ ] Project Structure analyzed and verified
- [ ] Development Workflow standards reviewed
- [ ] Bug Tracking patterns analyzed
- [ ] Security requirements understood

### Review Validation
- [ ] Code comprehensively analyzed
- [ ] Architecture patterns verified
- [ ] Security implementation checked
- [ ] Performance implications assessed
- [ ] Quality standards validated

### Feedback Validation
- [ ] Issues documented with specific details
- [ ] Solutions suggested with implementation guidance
- [ ] Pattern recommendations provided
- [ ] Security improvements identified
- [ ] Performance optimizations suggested

## 🚨 ENFORCEMENT

### Mandatory Compliance
- **NO EXCEPTIONS** - Every review task must follow this prompt
- **NO BYPASSES** - Context Engineering cannot be skipped
- **NO ALTERNATIVES** - This is the only approved review process

### Violation Consequences
1. **First Violation** - Immediate review termination and restart
2. **Second Violation** - Mandatory Context Engineering training
3. **Persistent Violations** - Review access revoked

### Success Criteria
- ✅ All required context reviewed and understood
- ✅ Code comprehensively analyzed
- ✅ Quality standards fully validated
- ✅ Feedback specific and actionable
- ✅ Security and performance considered

---

## 🎯 CONTEXT ENGINEERING PROMPT ACTIVE
**Category:** REVIEW
**Prompt File:** AGENT_CE_REVIEW.md
**Status:** ✅ LOADED AND ENFORCED

**Remember:** This prompt is MANDATORY for ALL review tasks. No exceptions, no bypasses, no alternatives.
