---
id: 11-permanent-rules
title: "Permanent Rules - System Memory"
category: setup
type: rules
version: "1.0.0"
last_updated: "2026-01-19"
author: hands-on-ai
status: active
machine_readable: true
source: "Rules Check.txt"
---

# Permanent Rules - System Memory

These rules must be enforced by the orchestrator in all operations.

---

## 1. Spec-Driven Development Protocol

### 1.1 Planning is Mandatory
- **NEVER** start coding without a plan
- Activate **Plan Mode** before any implementation
- Generate detailed implementation plan
- Ask clarifying questions before executing

### 1.2 Context Initialization
- Execute `/init` or `initialize` on existing repositories
- Generate memory file (claude.md, gemini.md, codex.md)
- Create `product-overview.md` or `architecture.md` for new projects

### 1.3 Plan Approval
- Do NOT approve execution until plan includes:
  - Files to be affected
  - Interfaces needed
  - Potential side effects

---

## 2. Code and Syntax Rules

### 2.1 TypeScript Rules
- **NEVER** use `any` type
- Define explicit interfaces for all components
- Use strict mode

### 2.2 Next.js Rules
- Do NOT use Server Actions for complex backend logic
- Use dedicated API Routes instead
- Use `use server` only for direct queries from server components

### 2.3 Style Rules
- Use Tailwind CSS for styling
- Ensure dark mode support by default
- Mobile-responsive design mandatory

### 2.4 Language Rules
- Code must be in **English**
- Comments must be in **Spanish**

---

## 3. Architecture Rules

### 3.1 Clean Architecture
- Separate business logic (Use Cases)
- Separate data access (Repositories/Services)
- Separate UI (Components)
- **NEVER** mix database logic in React components

### 3.2 Agent Autonomy
- Auto-invoke specific skills when tasks are detected
- Do NOT wait for user instruction for skill activation

---

## 4. Security Protocols

### 4.1 Secrets Management
- **NEVER** include API Keys in client code
- Use environment variables (`.env`)
- Access secrets only from server

### 4.2 Verification Before Completion
- Run `build` command before marking task complete
- Run `test` command to confirm no regressions
- Validate no syntax errors

### 4.3 Input Validation
- Sanitize all user inputs
- Use parameterized queries for SQL
- Implement rate limiting

---

## 5. Documentation Standards

### 5.1 Stack Documentation
Each technology stack README.md must include:
1. `# Name`
2. `## Overview`
3. `## Supported Operations`
4. `## QA Checklist`
5. `## Dangers/Risks`
6. `## Examples`

Plus additional aspects:
- Escalabilidad
- Opciones de ejecuciÃ³n
- Conectividad
- Comportamiento
- Dependencias
- Entregables
- Roles

---

## 6. Migration Protocol (WordPress/Elementor)

Strict order for migrations:
1. Import images (quick start package)
2. Export/Import Elementor templates (JSON)
3. Elementor customization and site settings
4. Plugin configuration
5. Import WooCommerce catalog
6. Import/Export Blog posts
7. Connect dynamic post templates

---

## 7. Assistant Behavior

### 7.1 Missing Information
- If critical information is missing, **ASK** the user
- **NEVER** assume values or hallucinate data

### 7.2 Review Mode
- When review is requested, act as "Brutal Critic"
- Aggressively search for:
  - Logic flaws
  - Security issues
  - Redundancy

### 7.3 Error Handling
- If something is unclear in documentation, mark as `Requires attention`
- Do NOT invent solutions

---

## 8. New Paradigm: Autonomous Recursive Development

### 8.1 Principles
- Describe outcomes instead of writing code
- Use AI to optimize AI tools
- Minimize human intervention
- Enable self-repair and self-expansion

### 8.2 Implementation
- Tools optimize themselves
- Closed loop development
- Software that:
  - Repairs itself
  - Expands itself
  - Protects itself

### 8.3 Local Execution
- Environment: Windows 10, CPU local, local disk
- No cloud dependency for core operations
- Cache all possible data locally

---

## 9. Multi-Model Processing Rules

### 9.1 Code Generation Trigger
- When the orchestrator detects a code generation request, **MUST** offer the user the option to invoke "Multi-Model Processing"
- Keywords that trigger this: genera, crea, escribe, implementa, cÃ³digo, function, class, componente, api, endpoint, script

### 9.2 Multi-Model Processing Mode
When activated, the system must:
1. Execute prompt in **parallel** to all available providers (OpenAI, Anthropic, Gemini)
2. Apply **equitative rotation (round-robin)** for single requests
3. Perform **intelligent merge** based on quality criteria
4. Invoke **Board of Directors** (one model evaluates others' responses)
5. Auto-select best response based on Hands On AI criteria

### 9.3 Response Selection Criteria
- Technical correctness
- Code completeness
- Compliance with permanent rules (no `any`, clean architecture, etc.)
- Cost efficiency
- Response latency

### 9.4 Output Handling
- Always write generated code directly to local files
- Validate code against contract before writing
- Never push to GitHub automatically

### 9.5 Configurable Limits
- Maximum requests per day (configurable)
- Maximum tokens per day (configurable)
- Maximum cost per day in USD (configurable)

---

## 10. Enforcement

The orchestrator must:
1. Load these rules at startup
2. Validate against rules before any operation
3. Block operations that violate rules
4. Log all rule violations
5. Suggest corrections for violations
6. Offer multi-model processing for code generation requests

