
---
id: 05-methodology
title: "Audit Methodology"
category: setup
subcategory: 
type: checklist
version: "1.0.0"
last_updated: "2026-01-14"
author: hands-on-ai
status: active
machine_readable: true
---

# Audit Methodology

## 7-Step Audit Process

### 1. Read the metadata first
- Understand project context
- Identify client requirements
- Confirm deliverables needed

### 2. Read the original documentation/prompt
- What is promised
- What should exist
- Understand scope and acceptance criteria

### 3. Read the Changelogs if they exist
- Understand the project's change history
- Review version evolution
- Identify breaking changes

### 4. Analyze the code
- Verify if it fulfills what was promised
- Verify if it respects the style: code in English, comments in Spanish
- Check architecture and patterns
- Review implementation quality

### 5. Cross-reference everything with the requirements of the selected technology
- Mark what is met: `[x]`
- Mark what is not met: `[ ]`
- Mark what is doubtful or ambiguous as: `[?] Requires clarification`

### 6. Complete the analysis checklist
- For all applicable technologies
- Use 7 dimensions per technology (see below)
- Document findings and issues

### 7. Identify critical areas for improvement
- Security (OWASP Top 10)
- Architecture
- Testing
- Performance
- Documentation

## 7 Dimensions per Technology

Each technology is evaluated in 7 dimensions for internal audit quality control:

### 1. Scalability
- Ability to grow and handle load
- Horizontal and vertical scaling strategies
- Performance under increasing demand

### 2. Execution Options
- Configuration and environments
- Development vs Production settings
- Deployment options

### 3. Connectivity
- Integrations and communication
- API connections
- External service integration
- Inter-service communication

### 4. Behavior
- Logic, flows, and patterns
- Business logic implementation
- Error handling
- Edge cases

### 5. Dependencies
- Management of libraries and packages
- Version control
- Security vulnerabilities
- Update strategy

### 6. Deliverable
- Project documentation and structure
- Build artifacts
- Deployment packages
- Documentation completeness

### 7. Roles and Responsibilities
- Defines which **role perspective you should adopt** to evaluate each aspect
- Examples: Senior Developer, QA Engineer, Security Analyst, DevOps Engineer, Architect, DBA, etc.

## Important Note on Dimension 7: Role Perspective Switching

This dimension tells you which **role you should impersonate** when reviewing each aspect:

- **Example**: When reviewing "Scalability" in Node.js, you assume the role of "Node.js Senior Developer" with that level of expertise and rigor
- **Example**: When reviewing "Security", you assume the role of "Security Analyst" with deep knowledge of vulnerabilities
- **Example**: When reviewing "Database Dependencies", you assume the role of "DBA" with database optimization expertise

This ensures that each dimension is evaluated with the level of detail and criteria that an expert in that area would use.

âš ï¸ **Important**: It is NOT a real team, it is you (the AI) changing perspective according to the aspect to evaluate.

---

# Hands-on AI Orchestration Engine

This guide serves as the Knowledge Base (KB) for the "Hands-on AI" engine, an orchestrator designed to automate and streamline web development projects.

## `/play` Command Specification

The engine is triggered via the `/play` command in a CLI environment (like Claude Code or Gemini CLI). The command configures and initiates a project plan based on the rules and data within this KB.

### Parameters

#### A) `--scope`
Defines the project's overall goal.
-   **`mvp`**: A Minimum Viable Product, focusing on core functionalities.
-   **`e2e`**: An End-to-End solution, focused on a complete and robust product.

#### B) `--power`
Defines the intensity of the agentic workforce, directly impacting performance and token consumption. It does not define agent roles, only their operational capacity.
-   **`p1`**: 1-3 agents (Low consumption)
-   **`p2`**: 3-5 agents (Moderate consumption)
-   **`p3`**: 5-7 agents (High consumption)
-   **`p4`**: 7-10 agents (Maximum consumption)

## Dual-Hook Analysis Process

The engine uses a two-step analysis process to generate a precise and context-aware project plan.

### 1. `analysis:init` Hook
This hook runs immediately when `/play` is executed, before the user's customization is applied.
-   **Objective**:
    -   Determine the project's current state: `greenfield` (new project) or `brownfield` (existing project).
    -   Detect the technology stack by cross-referencing with the KB.
    -   Generate a default set of development phases based on the `hands-on-ai` templates.

### 2. `analysis:recalc` Hook
This hook runs after the user has selected the `scope` and `power`.
-   **Objective**:
    -   Re-evaluate the default plan against the chosen customization.
    -   Rectify phases, reorder operations, and adjust the level of detail.
    -   Generate the final, updated list of activities to be performed.

