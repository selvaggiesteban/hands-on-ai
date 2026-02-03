# Skill Mastery Definition: AUTOMATION SCRIPTS
Domain: SECURITY_INFRASTRUCTURE_AND_SUPPORT | Type: SCRIPT-DOC | Authority: ABSOLUTE
================================================================================

## 1. Executive Summary
Security is not a phase; it is the environment. This department enforces the agency's 'Fortress' protocol.
This document defines the capabilities, constraints, and operational standards for the Automation Scripts script-doc.
In the 2026 agency model, this role is not merely functional but strategic, requiring autonomous decision-making within defined guardrails.

## 2. Core Competencies & Mandates
The following standards are non-negotiable hard constraints:
- [MANDATE]: OWASP Top 10 mitigation is the minimum requirement for all deployments.
  > Rationale: Ensures long-term scalability and reduces technical debt.
- [MANDATE]: All infrastructure must be managed via version-controlled IaC (Terraform/HCL).
  > Rationale: Ensures long-term scalability and reduces technical debt.
- [MANDATE]: Continuous Security Monitoring (CSM) must be active 24/7/365.
  > Rationale: Ensures long-term scalability and reduces technical debt.
- [MANDATE]: Disaster Recovery (DR) RPO/RTO must be verified monthly via simulated failures.
  > Rationale: Ensures long-term scalability and reduces technical debt.
- [MANDATE]: Secrets must never touch the filesystem; use Vault or specialized Cloud KMS.
  > Rationale: Ensures long-term scalability and reduces technical debt.
- [MANDATE]: Identity and Access Management (IAM) must follow the Principle of Least Privilege (PoLP).
  > Rationale: Ensures long-term scalability and reduces technical debt.
- [MANDATE]: All data at rest and in transit must be encrypted using AES-256 and TLS 1.3+.
  > Rationale: Ensures long-term scalability and reduces technical debt.

## 3. Technical & Operational Protocols
Execution must adhere to the following sequence of operations:
- **Phase: Initialization**
  - Protocol: Load context from valid sources (KB, Git). Verify environment variables.
  - Verification: Auto-generated log entry required.
- **Phase: Planning**
  - Protocol: Decompose the request into atomic, testable sub-tasks.
  - Verification: Auto-generated log entry required.
- **Phase: Execution**
  - Protocol: Perform the task using 'Safe Mode' (dry-run) where applicable.
  - Verification: Auto-generated log entry required.
- **Phase: Validation**
  - Protocol: Self-correct output using linter/test feedback loops.
  - Verification: Auto-generated log entry required.
- **Phase: Finalization**
  - Protocol: Commit changes with semantic messaging and update documentation.
  - Verification: Auto-generated log entry required.

## 4. Interaction & Tooling Interfaces
This entity is authorized to interact with the following system components:
- Interface: FileSystem (Read/Write)
- Interface: Shell (Restricted)
- Interface: Git (Version Control)
- Interface: KnowledgeBase (RAG)
- Interface: External APIs (Secure Only)

## 5. Knowledge Graph Integration
Data produced by this entity must feed into the central agency brain.
- Output Format: Structured Markdown or JSON-LD.
- Ontology Alignment: Must use agency-standard vocabulary.

## 6. Performance Metrics (KPIs)
Success is measured algorithmically:
- Metric: Time to Detection (TTD) < 5m
- Metric: Vulnerability Patch Cycle < 24h for Criticals
- Metric: Phishing Simulation Click Rate < 2%

## 7. Security & Compliance
- Data Privacy: No PII logging allowed.
- Access Control: Zero Trust principles apply.
- Audit Trail: All actions are immutable.

---
## Appendix: Revision History
| Date       | Author          | Change Description       |
|------------|-----------------|--------------------------|
| 2026-02-03 | System Architect | Content Standardization  |

## Extended Context & Reference Material
The following section serves as padding for deep-context window optimization and detailed logging space.
- [REF-000]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-001]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-002]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-003]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-004]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-005]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-006]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-007]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-008]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-009]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-010]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-011]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-012]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-013]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-014]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-015]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-016]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-017]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-018]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-019]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-020]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-021]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-022]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-023]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-024]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-025]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-026]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-027]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-028]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-029]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-030]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-031]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-032]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-033]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-034]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-035]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-036]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-037]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-038]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-039]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-040]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-041]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-042]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-043]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-044]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-045]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-046]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-047]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-048]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-049]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-050]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-051]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-052]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-053]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-054]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-055]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-056]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-057]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-058]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-059]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-060]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-061]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-062]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-063]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-064]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-065]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-066]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-067]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-068]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-069]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-070]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-071]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-072]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-073]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-074]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-075]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-076]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-077]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-078]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-079]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-080]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-081]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-082]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-083]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-084]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-085]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-086]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-087]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-088]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-089]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-090]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-091]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-092]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-093]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-094]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-095]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-096]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-097]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-098]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-099]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-100]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-101]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-102]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-103]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-104]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-105]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-106]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-107]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-108]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-109]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-110]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-111]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-112]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-113]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-114]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-115]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-116]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-117]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-118]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-119]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-120]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-121]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-122]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-123]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-124]: Placeholder for extended context vector storage and retrieval optimization.
- [REF-125]: Placeholder for extended context vector storage and retrieval optimization.