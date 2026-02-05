# Script: Telemetry Generator

## Purpose
A script designed to scan a project directory, parse its plan and execution history, and generate a comprehensive telemetry report.

## Usage
`./generate-telemetry.sh --project-path <path_to_project>`

## Functional Requirements

### 1. File System Scan
*   Recursively count files and folders in the target directory.
*   Calculate lines of code (LOC) for supported file types (.js, .ts, .php, .py, etc.), adhering to `.gitignore`.

### 2. Plan Parsing
*   Locate the `plan/` directory within the project.
*   Read all `.md` files.
*   Regex match for `- [ ]` (pending) and `- [x]` (completed) tasks.
*   Calculate `total_tasks`, `completed_tasks`, and `progress_percentage`.

### 3. Metric Aggregation
*   Read `logs/execution.log` (or equivalent) to sum `agent_invocations` and `script_executions`.
*   Read `compliance/report.json` (or equivalent) to extract the current `compliance_score`.

### 4. Output Generation
*   **JSON:** Write a structured data object to `project_meta/telemetry.json`.
*   **Console:** Display a summary table with a visual progress bar (e.g., `[#####-----] 50%`).

## Error Handling
*   Gracefully handle missing plan directories or log files (report as 0 or N/A).
*   Validate write permissions for the output directory.
