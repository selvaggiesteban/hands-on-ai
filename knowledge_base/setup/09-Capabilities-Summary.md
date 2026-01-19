
---
id: 09-capabilities-summary
title: "Hands-on AI Capabilities Summary"
category: setup
subcategory: 
type: checklist
version: "1.0.0"
last_updated: "2026-01-14"
author: hands-on-ai
status: active
machine_readable: true
---

# Hands-on AI Capabilities Summary

This document provides an explicit overview of the core components and operational parameters of the "Hands-on AI" orchestration engine, as defined by this Knowledge Base.

---

## 1. Technology Stacks

(Refer to `knowledge_base/technologies/` for detailed documentation of each stack)

*   **Frontend**: React (with frameworks like Next.js)
*   **Backend**: Node.js with Express
*   **Database**: PostgreSQL
*   **ORM**: Prisma or Drizzle
*   **Containerization**: Docker
*   **Monorepo Management**: Turborepo with pnpm

---

## 2. Project Scopes (`--scope`)

(Refer to `knowledge_base/setup/07-Rules.md` for detailed rules)

*   **`mvp` (Minimum Viable Product)**
*   **`e2e` (End-to-End Solution)**

---

## 3. Agents (Conceptual & Power Levels)

(Refer to `knowledge_base/setup/05-Methodology.md` for orchestration details and `knowledge_base/technologies/` for specific supported operations)

### Conceptual Agents
1.  **Coder Agent**: Code generation and modification.
2.  **Test & QA Agent**: Quality assurance and testing.
3.  **Security Agent**: Vulnerability identification and mitigation.
4.  **DevOps & Infrastructure Agent**: Build, deployment, and environment management.
5.  **Documentation & Standards Agent**: KB maintenance and style enforcement.

### Power Levels (`--power`)
*   **`p1` (1-3 Agents)**: Low operational intensity.
*   **`p2` (3-5 Agents)**: Moderate operational intensity.
*   **`p3` (5-7 Agents)**: High operational intensity.
*   **`p4` (7-10 Agents)**: Maximum operational intensity.

---

## 4. Skills (Supported Operations)

(Refer to `knowledge_base/technologies/[Technology]/README.md` for technology-specific skills)

*   **Code Generation**: `create-component`, `create-hook`, `create-route`, `add-middleware`, `generate-controller`.
*   **Database Management**: `create-table`, `alter-table`, `create-index`, `run-migration`, `backup-database`.
*   **Testing & QA**: `run-tests`, `check-code-quality`, `identify-performance-bottlenecks`.
*   **Infrastructure & Build**: `build-image`, `run-container`, `orchestrate-with-compose`, `build-app`, `start-server`.
*   **Dependency Management**: `install-dependencies`.

---

## 5. Security Policies

(Refer to `knowledge_base/setup/07-Rules.md` and `knowledge_base/technologies/[Technology]/README.md` `## Dangers / Risks`)

*   Prevention of common web vulnerabilities (XSS, SQLi).
*   Scanning of third-party dependencies.
*   Strict secrets management.
*   Principle of Least Privilege.
*   Use of security-focused tools.

---

## 6. Quality Assurance (QA)

(Refer to `knowledge_base/setup/07-Rules.md` and `knowledge_base/technologies/[Technology]/README.md` `## QA Checklist`)

*   Adherence to code principles (SOLID, SRP).
*   Efficient state management and side effects.
*   Performance checks.
*   Data integrity and normalization.
*   RESTful API conventions.

---

## 7. Token Saving (Efficiency Rules)

(Refer to `knowledge_base/setup/07-Rules.md` for detailed rules)

*   Prompt Caching.
*   Context Management (RAG).
*   Structured Outputs.

---

## 8. Orchestration Rules

(Refer to `knowledge_base/setup/05-Methodology.md` and `knowledge_base/setup/07-Rules.md`)

*   Dual-Hook Analysis (`analysis:init`, `analysis:recalc`).
*   Parameter-Driven Logic (`--scope`, `--power`).
*   KB Schema Enforcement.

---

## 9. Available Templates as Output

(Generated within `C:\Users\Esteban Selvaggi\Desktop\Web Dev Guide\hands-on-ai`)

*   Project Plan.
*   Product Overview.
*   Architectural Decision Records (ADRs).
*   Resumes (conceptual for agent roles).

---

## 10. Available Tools for Operations

(Conceptual tools used by agents to execute `Supported Operations`)

*   File System Tools (`create-file`, `edit-file`, `read-file`).
*   Build & Execution Tools (`install-dependencies`, `run-tests`, `build-app`, `start-server`).
*   Containerization Tools (`build-image`, `run-container`).
*   Database Tools (`run-migration`, `backup-database`).
