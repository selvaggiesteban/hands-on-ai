# Checklist: Telemetry System Validation

## Overview
This checklist ensures that the Telemetry System is correctly implemented and producing accurate, reliable data for all projects.

## Validation Criteria

### 1. Data Integrity
- [ ] **Invocation Tracking:** Verify that agent and script counters increment correctly after execution.
- [ ] **Volumetrics Accuracy:** Confirm that reported file/folder counts match the actual filesystem.
- [ ] **LOC Calculation:** Ensure lines of code are counted correctly, excluding ignored directories (e.g., `node_modules`, `vendor`).

### 2. Progress Calculation
- [ ] **Task Parsing:** Verify that the system correctly identifies all `- [ ]` and `- [x]` items in plan documents.
- [ ] **Percentage Formula:** Confirm that `(Completed / Total) * 100` is calculated accurately.
- [ ] **Status Updates:** Ensure that modifying a task to `[x]` is immediately reflected in the progress score.

### 3. Compliance Scoring
- [ ] **Checklist Mapping:** Verify that all relevant checklists are being included in the score.
- [ ] **Scoring Logic:** Confirm that the 0-100 score accurately reflects the ratio of passed validation gates.

### 4. Reporting & Output
- [ ] **Format Compliance:** Ensure reports are generated in the required JSON/YAML format.
- [ ] **Project Isolation:** Verify that metrics for one project do not bleed into another.
- [ ] **Error Handling:** Confirm that the system records `failed_tasks` and `validation_retries` without crashing.
