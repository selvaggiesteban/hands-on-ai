# Hands-on AI Agency Framework (2026 Edition)

![Status](https://img.shields.io/badge/Status-Operational-green) ![Version](https://img.shields.io/badge/Version-2026.1.0-blue) ![Compliance](https://img.shields.io/badge/Compliance-Absolute_Truths-red)

## 📖 Executive Summary

This repository houses the **Hands-on AI Agency Framework**, a hyper-structured operating system for a futuristic digital agency. It is built on the principle of **"Architecture as a Service"**, where every functional area—from SEO to Backend Development—is governed by autonomous Agents, rigorous Checklists, and standardized Skills.

**Primary Goal:** To provide a standardized, scalable, and automated environment for deploying high-performance digital projects using AI-human collaboration.

---

## 📂 Directory Map (Machine Readable)

The filesystem is organized into **17 Functional Areas** across four primary pillars:

| Directory        | Purpose                                                                                                       | Count       | Format               |
| :--------------- | :------------------------------------------------------------------------------------------------------------ | :---------- | :------------------- |
| **`agents/`**    | **Intelligence Layer.** Defines personas, capabilities, and strict mandates for AI agents.                    | 17 Areas    | Markdown (`.md`)     |
| **`checklist/`** | **Quality Assurance Layer.** Passive validation gates that MUST be passed before any deliverable is approved. | 17 Areas    | Markdown (`.md`)     |
| **`models/`**    | **Provider Layer.** Configuration and persona definitions for specific AI models (LLMs).                      | 3 Providers | Markdown (`.md`)     |
| **`skills/`**    | **Capability Layer.** Detailed technical guides and reference materials required for execution.               | 17 Areas    | Markdown (`.md`)     |
| **`scripts/`**   | **Automation Layer.** Code and documentation for executing tasks within each domain.                          | 17 Areas    | Mixed (`.py`, `.md`) |
| **`plan/`**      | **Strategy Layer.** Strategic Operational Plans connecting the resources above into roadmaps.                 | 17 Docs     | Markdown (`.md`)     |
| **`src/`**       | **Project Workspace.** Container for individual client projects (e.g., `src/client-alpha`).                   | -           | Project Folders      |

---

## 🏗️ Functional Areas (The 17 Pillars)

The framework is divided into 17 functional areas, each containing specialized agents, checklists, and skills. Some areas include sub-specialties for deeper expertise (e.g., `advanced_content_and_ai` includes `nlp_engineer` and `prompt_engineer`).

1.  **`advanced_content_and_ai`**: NLP Engineering, Prompt Engineering, AI Marketing.
2.  **`automation`**: Internal system automation, KB generation, and project scaffolding.
3.  **`automation_tooling`**: Specialized infrastructure for agent orchestration and DX.
4.  **`core`**: Foundational agency logic (Planning, Orchestration, Review).
5.  **`creative_and_design`**: UI/UX, Mobile Design, Creative Direction.
6.  **`crm_and_automation`**: Customer Relationship Management workflows.
7.  **`direction_and_strategy`**: Product Management, Project Leadership.
8.  **`marketing_and_media`**: General marketing campaigns and media buying.
9.  **`multimedia_production`**: Video, Audio, and Rich Media assets.
10. **`sales_and_growth`**: Business Development and Sales pipelines.
11. **`security_infrastructure_and_support`**: DevOps, InfoSec, IT Support.
12. **`seo_and_content`**: Search Generative Experience (SGE), Technical SEO.
13. **`social_media`**: Community management and social growth.
14. **`strategy_and_analytics`**: Data Analysis, User Research.
15. **`talent_and_administration`**: HR, Recruiting, Ops Admin.
16. **`user_experience`**: Deep UX Research and usability testing.
17. **`web_development_and_technology`**: Full-stack engineering (Node, Python, React).

---

## ⚡ Quick Start: Project Initialization

To start a new client project using this framework:

### 1. Create the Project Folder

```bash
mkdir src/my-new-project
```

### 2. Distribute Strategic Plans

Run the automation script to inject the intelligence framework into your new project.

```bash
python scripts/automation/distribute_plans.py
```

> **What happens?** This duplicates the `plan/` folder into `src/my-new-project/plan/` and generates a `00_MASTER_PLAN.md` that orchestrates all 17 areas specific to this project.

### 3. Execution

Navigate to `src/my-new-project/plan/00_MASTER_PLAN.md` and follow the **Phased Execution Roadmap**:

1.  **Phase 1:** Audit (Run Checklists)
2.  **Phase 2:** Strategy (Consult Agents)
3.  **Phase 3:** Build (Execute Scripts)
4.  **Phase 4:** Optimize (Review Skills)

---

## 🤖 System Maintenance & Updates

### Regenerating Content Standards

If the "Absolute Truths 2026" (Global Standards) change, run these scripts to propagate updates to all Agents and Skills documents:

```bash
# Propagate knowledge base updates
python scripts/automation/generate_expert_content.py

# Upgrade existing content with new standards
python scripts/automation/upgrade_content.py
```

### Syncing Checklists

To ensure the `checklist/` directory remains a perfect mirror of the agent structure:

```bash
python scripts/automation/generate_checklist_structure.py
```

---

## 📜 The "Absolute Truths 2026" (Engineering Standards)

All agents and checklists strictly enforce the following mandates:

- **Architecture:** CLEAN Architecture & SOLID Principles are non-negotiable.
- **Security:** Zero Trust Architecture (ZTA) by default. OWASP Top 10 mitigation.
- **AI Operations:** Human-in-the-Loop (HITL) for all generative tasks.
- **Data:** 3rd Normal Form for relational DBs; JSON-LD for Structured Data.
- **Code:** 100% Type Safety (TypeScript/Python Type Hints).

---

> **Note for LLMs:** When analyzing this repository, prioritize `plan/` documents for strategy and `checklist/` documents for validation constraints. Treat `agents/` as persona definitions.

**Maintained by:** Esteban Selvaggi
