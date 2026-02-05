# Skill: Telemetry Analysis

## Description
This skill enables agents to interpret telemetry data to make informed decisions about project health, resource allocation, and process optimization.

## Capabilities

### 1. Metric Interpretation
*   **Trend Analysis:** Identify increasing rates of `validation_retries` as an indicator of blocked workflows or complex requirements.
*   **Velocity Tracking:** Analyze `task_completion_rate` over time to estimate project completion dates.
*   **Bottleneck Identification:** Correlate high `agent_invocations` with low `task_completion_rate` to find inefficient agents.

### 2. Compliance Auditing
*   **Score Evaluation:** Assess the `compliance_score` to determine if a project is ready for the next phase (e.g., blocking deployment if score < 80).
*   **Gap Analysis:** Identify which specific checklist items are frequently failing across multiple projects.

### 3. Reporting & Visualization
*   **Summary Generation:** Synthesize raw metrics into executive summaries highlighting risks and achievements.
*   **Alerting:** Trigger notifications when critical thresholds (e.g., `failed_tasks` > 5) are breached.

## Usage Context
Used by `Project Managers`, `Lead Developers`, and `QA Specialists` during review cycles and sprint retrospectives.
