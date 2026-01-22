
---
id: 03-deliverables
title: "Deliverable Selection"
category: setup
subcategory: 
type: checklist
version: "1.0.0"
last_updated: "2026-01-14"
author: hands-on-ai
status: active
machine_readable: true
---

# Deliverable Selection

After gathering the analysis metadata, you must ask the user which deliverables they need.

## Ask the User

**Which deliverables do you want to generate at the end of the audit?**

Mark with [x] the deliverables you need:

## Available Deliverables List

### 1. WEBSITE SITEMAP
- Hierarchical site structure
- Keywords per page
- SEO-optimized content
- **When to use**: Web projects with multiple pages, SEO focus

### 2. INTEGRATION GUIDE
- Step-by-step technical instructions
- System requirements
- Configuration by technology
- Main commands
- **When to use**: Projects that will be installed by third parties

### 3. PROGRAMMING AND WEB DEVELOPMENT ANALYSIS
- Complete report with scores by category (Security, Architecture, Testing, etc.)
- Detailed findings by technology
- Prioritized recommendations
- **When to use**: ALWAYS (this is the main deliverable)

### 4. API/INTEGRATION DOCUMENTATION
- Documented endpoints
- Usage examples
- Error codes
- Authentication and permissions
- **When to use**: Projects with REST/GraphQL APIs or external integrations

### 5. CHANGELOG AND VERSION CONTROL
- Change history
- Migration notes
- Breaking changes
- **When to use**: Projects with multiple versions or frequent updates

### 6. SEO ARTICLE (STRICT HTML)
- **Format:** Semantic HTML5 (no CSS)
- **Content:** Fact-based (NO invention allowed)
- **Structure:** 1500+ words, strict paragraph length (100-200w)
- **Linking:** Automatic internal linking based on Sitemap matches + GBP integration
- **When to use:** High-fidelity content strategy requiring technical precision

## Dialogue Example

```
AI: Which deliverables do you want to generate at the end of the audit?

Mark with [x] the ones you need:

[ ] 1. WEBSITE SITEMAP
[ ] 2. INTEGRATION GUIDE
[ ] 3. PROGRAMMING AND WEB DEVELOPMENT ANALYSIS (recommended)
[ ] 4. API/INTEGRATION DOCUMENTATION
[ ] 5. CHANGELOG AND VERSION CONTROL
[ ] 6. BACKLINK PUBLICATION

User:
[x] 3. PROGRAMMING AND WEB DEVELOPMENT ANALYSIS
[x] 4. API/INTEGRATION DOCUMENTATION

AI: Perfect. I will generate:
- Complete technical analysis
- API documentation

Shall we begin with the audit?
```

## Important Notes

**Multiple deliverables can be selected**.

Deliverables will be generated automatically at the end of the audit using the templates from the `knowledge_base/templates/` folder.

## Deliverables vs Internal Tools

âš ï¸ **IMPORTANT**: The following are NOT separate deliverables for the client:

- **Security assessment (OWASP Top 10)**: This is an internal tool. Findings are included in deliverable #3 (Technical analysis) in the "Security: X/10" section

- **Role matrix**: This is for internal audit organization (AI perspective switching). It is NOT delivered to the client.

## Using This File

This file tells you which deliverable options to offer the user before starting the audit.

