
---
id: 01-overview
title: "Web Development Guide - Overview"
category: setup
subcategory: 
type: checklist
version: "1.0.0"
last_updated: "2026-01-14"
author: hands-on-ai
status: active
machine_readable: true
---

# Web Development Guide - Overview

## 1. Objective

- Verify the **consistency between code, original documentation/prompt, and language/technology requirements** to detect **improvements**, **pending items**, and **inconsistencies**, and record edits in an **analysis in actionable checklist format**, which will be manually applied later.

## 2. Customization Rules

### 2.1. Environment and Access
- Do not assume access to environments, databases, or external services.

### 2.2. Code Standards
- The **code** must always be in **English**.
- The **comments** must always be in **Spanish**.

### 2.3. Editing Restrictions
- You must not edit or execute code automatically.
- If something **is not clear in the documentation**, mark it as:
  - `Requires attention` in the checklist, rather than inventing a solution.

### 2.4. Final Reminders
- Do not modify the code or provide an automatically rewritten version.
- Do not execute the code or assume you can do so.
- Work solely based on: Analysis Metadata, Original Documentation/Prompt, and Provided Code, including Technology-specific Requirement Lists.
- Return only the report in the described format.

## 3. Writing Style

When generating documentation, reports, or any written content:

- **Use simple language**: Write simply with short sentences. Example: "I need help with this matter."
- **Avoid typical AI-generated phrases**: Do not use clichés like "dive into," "unlock your potential," etc.
  - Avoid: "Let's dive into this game-changing solution."
  - Instead, use: "Here's how it works."
- **Be direct and concise**: Get to the point; eliminate unnecessary words. Example: "We should meet tomorrow."
- **Maintain a natural tone**: Write as you normally speak; it's okay to start sentences with "and" or "but." Example: "And that's why it's important."
- **Avoid commercial language**: Do not use advertising or promotional words.
  - Avoid: "This revolutionary product will transform your life."
  - Instead, use: "This product can help you."
- **Be realistic**: Be sincere; do not force kindness. Example: "I don't think that's the best idea."
- **Simplify grammar**: Don't stress about perfect grammar; it's fine not to capitalize "i" if that's your style. Example: "I guess we can try."
- **Avoid wordiness**: Avoid unnecessary adjectives and adverbs. Example: "We finished the task."
- **Focus on clarity**: Make your message easy to understand. Example: "Please send the file by Monday."

---

## 4. Knowledge Base (KB) Document Schema

To ensure this guide can be reliably parsed by the "Hands-on AI" orchestration engine, all documents, particularly those in the `knowledge_base/technologies` section, must adhere to a strict schema. Each document must be under 200 lines and contain the following mandatory headings in this exact order.

### 4.1. `## Stack / Tags`
A machine-readable list of associated technologies and concepts.
-   **Example**: `[Node.js, Express, API, Backend, JavaScript]`

### 4.2. `## Supported Operations`
A list of actions the orchestrator can perform related to this technology.
-   **Example**: `[create-route, add-middleware, generate-controller, run-tests]`

### 4.3. `## QA Checklist`
A list of quality assurance checks to be performed for this technology.
-   **Example**: `- Route follows RESTful principles. - Middleware handles errors gracefully. - Controller logic is separated from business logic.`

### 4.4. `## Dangers / Risks`
A list of potential issues, security vulnerabilities, or anti-patterns.
-   **Example**: `- Risk of SQL injection if inputs are not sanitized. - Middleware order can cause security issues. - Lack of rate limiting can lead to DoS attacks.`
