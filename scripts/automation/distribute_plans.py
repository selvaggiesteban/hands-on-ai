import os
import shutil
import re

def get_functional_area_plans(plan_source_dir):
    """Retrieves all markdown plan files from the source directory."""
    return [f for f in os.listdir(plan_source_dir) if f.endswith(".md") and f != "00_MASTER_PLAN.md"]

def generate_master_plan(project_name, plan_dir, plan_files):
    """Generates a master plan aggregating all functional area plans."""
    
    content = [
        f"# Master Execution Plan: {project_name}",
        f"**Generated for Project:** {project_name}",
        "**Status:** ACTIVE",
        "",
        "## 1. Project Overview",
        "This Master Plan serves as the central command document for the project. It aggregates the strategic operational plans of all functional areas, ensuring a unified approach to execution.",
        "It invokes all authorized Agents, mandated Skills, and compliance Checklists.",
        "",
        "## 2. Integrated Functional Areas",
        "The following functional areas are active for this project. Refer to their individual plans for granular details:",
        ""
    ]
    
    # 2. List Linked Functional Areas
    for plan_file in plan_files:
        area_name = os.path.splitext(plan_file)[0].replace('_', ' ').title()
        content.append(f"- **[{area_name}](./{plan_file})")
    
    content.append("")
    content.append("---")
    content.append("## 3. Unified Phased Execution Roadmap")
    content.append("The following roadmap synchronizes the 'Phase 1: Audit' and 'Phase 2: Strategy' actions across all departments.")
    
    content.append("")
    content.append("### Phase 1: Universal Audit & Discovery")
    content.append("**Goal:** Complete system-wide validation using all Auditor Agents.")
    content.append("- [ ] **Execute All Auditor Agents:** Trigger `*` agents in `agents/` to scan the codebase.")
    content.append("- [ ] **Run Mandatory Compliance Checklists:** Verify all assets against `checklist/` standards.")
    
    content.append("")
    content.append("### Phase 2: Architecture & Strategy")
    content.append("**Goal:** Define the technical and creative direction.")
    content.append("- [ ] **Review with Strategic Agents:** Engage `direction_and_strategy` agents.")
    content.append("- [ ] **Skill Gap Analysis:** Verify team possesses all skills listed in `skills/`.")
    
    content.append("")
    content.append("### Phase 3: Implementation")
    content.append("**Goal:** Build and Deploy.")
    content.append("- [ ] **Run Automation Scripts:** Execute setup scripts from `scripts/`.")
    content.append("- [ ] **Agent-Driven Development:** Assign tasks to specific functional agents (e.g., `backend_developer`, `ui_designer`).")
    
    content.append("")
    content.append("### Phase 4: Optimization")
    content.append("**Goal:** Refine and Maintain.")
    content.append("- [ ] **Continuous Compliance:** Re-run all checklists.")
    
    content.append("")
    content.append("---")
    content.append("## 4. Resource Index")
    content.append("### Global Directories")
    content.append("- **Agents:** `../../agents`")
    content.append("- **Skills:** `../../skills`")
    content.append("- **Checklists:** `../../checklist`")
    content.append("- **Scripts:** `../../scripts`")

    master_plan_path = os.path.join(plan_dir, "00_MASTER_PLAN.md")
    with open(master_plan_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    return master_plan_path

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    src_dir = os.path.join(root_dir, "src")
    source_plan_dir = os.path.join(root_dir, "plan")

    if not os.path.exists(src_dir):
        print(f"Source directory {src_dir} does not exist.")
        return

    if not os.path.exists(source_plan_dir):
        print(f"Plan template directory {source_plan_dir} does not exist.")
        return
    
    print(f"Scanning {src_dir} for projects...")
    
    projects = [d for d in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, d))]
    
    if not projects:
        print("No projects found in src/. Add a project folder to 'src/' to generate its plan.")
        return

    for project in projects:
        project_path = os.path.join(src_dir, project)
        target_plan_dir = os.path.join(project_path, "plan")
        
        print(f"Processing Project: {project}")
        
        # 1. Clean existing plan dir in project if it exists
        if os.path.exists(target_plan_dir):
            shutil.rmtree(target_plan_dir)
        
        # 2. Copy the standard plan folder
        shutil.copytree(source_plan_dir, target_plan_dir)
        print(f"  - Copied standard plans to {target_plan_dir}")
        
        # 3. Generate the Master Plan for this specific project
        plan_files = get_functional_area_plans(source_plan_dir)
        master_plan_path = generate_master_plan(project, target_plan_dir, plan_files)
        print(f"  - Generated Master Plan: {master_plan_path}")

if __name__ == "__main__":
    main()
