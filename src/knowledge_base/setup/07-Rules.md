
---
id: 07-rules
title: "Working Rules"
category: setup
subcategory: 
type: checklist
version: "1.0.0"
last_updated: "2026-01-14"
author: hands-on-ai
status: active
machine_readable: true
---

# Working Rules

## CRITICAL: No Automatic Code Modification

**IMPORTANT**: You must await manual confirmation from the responsible web developer before editing the source code.

This is an **AUDIT TOOL**, not an auto-fix tool.

## Final Reminder for the Model

- Do not modify the code or provide an automatically rewritten version.
- Do not execute the code or assume you can do so.
- Work solely based on: Analysis Metadata, Original Documentation/Prompt, and Provided Code, including Technology-specific Requirement Lists.
- Return only the report in the described format.

## Rules for Applying Code Edits (when authorized)

When authorized to apply code changes, you must strictly comply with the following rules:

### 1. Code Language
Develop **code in English** and **comments in Spanish**.

### 2. Dependency Management
Ask **before** integrating internal or external dependencies.
- Mention what they are
- Explain why they are needed

### 3. Change Documentation
Explain **after development** everything about:
- The structure of the modified plugin/module
- The most important folders and files
- The changes made and their impact

### 4. Limited Scope
Do not develop requirements that are **not presented** in:
- The original documentation
- The analysis checklist

### 5. Prior Approval
**Always ask before** integrating or applying changes automatically.

### 6. Partial Deliveries
If you have doubts during implementation:
- Make a partial delivery
- Ask before proceeding

---

# `/play` Command Rules

These rules govern the behavior of the "Hands-on AI" orchestrator based on the parameters selected by the user. The engine uses these rules to interpret the Knowledge Base (KB).

## 1. Scope Rules (`--scope`)

-   **`--scope=mvp`**:
    -   The orchestrator will only execute `Supported Operations` from the KB that are tagged as `core` or `essential`.
    -   The `QA Checklist` will be executed using a `light` profile, focusing only on critical checks.
    -   Documentation generation will be minimal.

-   **`--scope=e2e`**:
    -   All `Supported Operations` defined in the KB are eligible for execution.
    -   The `QA Checklist` will be executed in `full` mode, running all checks.
    -   Comprehensive documentation, including API specs and usage examples, will be generated.

## 2. Power Rules (`--power`)

-   **`--power=p1` (1-3 Agents)**:
    -   Imposes a low token budget.
    -   Code analysis is limited to a single level of dependency depth.
    -   Agents will prefer to use file summaries instead of reading entire files.

-   **`--power=p2` (3-5 Agents)**:
    -   Imposes a moderate token budget.
    -   Analysis can go up to two levels of dependency depth.

-   **`--power=p3` (5-7 Agents)**:
    -   Imposes a high token budget.
    -   Allows for more in-depth code refactoring and optimization tasks.

-   **`--power=p4` (7-10 Agents)**:
    -   Imposes a very high token budget.
    -   Enables full dependency tree analysis.
    -   The `Dangers / Risks` section of the KB is analyzed with maximum scrutiny to identify potential issues proactively.

## 3. Agent Operating Rules

-   **Token Management**:
    -   **Prompt Caching**: Stable parts of prompts (system instructions, tool definitions) will be cached to reduce costs.
    -   **Context Management**: Agents will use RAG (Retrieval-Augmented Generation) and file summaries to keep the context window focused and efficient.
-   **Hook Management**:
    -   The orchestration engine uses a system of hooks (pre/post execution) to ensure quality, enforce policies, and manage the agent lifecycle. All operations are subject to these hooks.

