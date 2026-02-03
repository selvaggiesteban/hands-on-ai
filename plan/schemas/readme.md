---
name: readme
description: Use when [describe the use case for this skill].
---

# JSON Schemas for Project Metadata

This directory contains formal JSON schemas to validate the structure and types of the project's core configuration files. Enforcing these schemas ensures that all machine-readable metadata is consistent, correct, and reliable, which is critical for automated tools and AI agents that interact with the project.

## Why Use Schemas?

1.  **Reliability**: Guarantees that config files have the expected structure, preventing runtime errors from malformed data.
2.  **Consistency**: Enforces naming conventions and data types across the project.
3.  **Machine Readability**: Provides a formal contract for AI agents and scripts, allowing them to parse and interact with the configuration files confidently.
4.  **Validation**: Enables automated CI/CD checks to fail builds if a configuration change introduces an invalid structure.
5.  **Documentation**: Acts as formal, machine-checked documentation for the structure of the configuration files.

## Available Schemas

-   **`rag-config.schema.json`**: Validates `project_meta/ai-context/rag-config.json`.
    -   Defines the structure for the Retrieval-Augmented Generation (RAG) system, including vector store providers, embedding models, chunking strategies, and indexing rules.

-   **`plan.schema.json`**: Validates `project_meta/planning/plan.json`.
    -   Defines the structure for the architecture and development plan, including metadata, quality gates, security policies, and technical implementation details.

-   **`prompt-library.schema.json`**: Validates `project_meta/ai-context/prompt-library.json`.
    -   Defines the structure for the AI prompt templates, including system roles, task definitions, constraints, and examples.

-   **`threat-model.schema.json`**: Validates `project_meta/security/threat-model.yaml`.
    -   Defines the structure for the security threat model, including STRIDE analysis, OWASP Top 10 mapping, and security controls.

## Usage

These schemas can be used with any standard JSON schema validation tool (e.g., `jsonschema` in Python, `ajv` in JavaScript) to check the validity of the corresponding configuration files. A validation script is available at `tools/validate_project.py`.