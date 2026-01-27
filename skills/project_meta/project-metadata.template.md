---
name: project-metadata.template
description: Use when [describe the use case for this skill].
---

# Project Metadata

## Required Fields

At the beginning of each audit, you must ask for the following data (labels):

- **Project name**: {{project_name}}
- **Client name**: {{client_name}}
- **Analysis date**: {{activity_date}}
- **Manager's full name**: {{responsible_person}}
- **Manager's email**: {{responsible_email}}
- **Reason for analysis**: {{audit_reason}}
- **Technology**: {{technology}}
- **Auditor role**: {{auditor_role}}
  - Options: Senior Developer / QA Engineer / Technical Auditor / DevOps Engineer / Software Architect / Security Analyst / DBA / AI Engineer / Business Analyst
- **Changelog file and version control**: {{changelog_file}}

## Mandatory File Naming

This data must **mandatorily** appear in a changelog file in markdown format that you must name as:

**"Programming and Web Development Analysis {{YYYY-MM-DD -- HH-mm}}.md"**

## Metadata Template

```markdown
## Analysis metadata

- Project : {{project_name}}
- Client : {{client_name}}
- Date : {{activity_date}}
- Responsible : {{responsible_person}}
- Reason : {{audit_reason}}
- Technology : {{technology}}
```
