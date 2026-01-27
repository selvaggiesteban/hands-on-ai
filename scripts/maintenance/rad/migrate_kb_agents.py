
import os
import shutil

DOMAIN_SOURCE = "knowledge_base/agents/domain"
AUTOMATION_SOURCE = "knowledge_base/agents/automation"
DOMAIN_TARGET = "agents/Domain_Experts"
AUTOMATION_TARGET = "agents/Automation"

def migrate_agents(source_dir, target_dir, category_name):
    print(f"Migrating agents from {source_dir} to {target_dir}...")
    
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return

    for agent_name in os.listdir(source_dir):
        agent_path = os.path.join(source_dir, agent_name)
        
        if os.path.isdir(agent_path):
            md_file = os.path.join(agent_path, "agent.md")
            
            if os.path.exists(md_file):
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check if frontmatter exists
                if not content.strip().startswith("---"):
                    print(f"Adding frontmatter to {agent_name}...")
                    new_content = f"""---
name: "{agent_name}"
type: "kb-{category_name}-{agent_name}"
description: "Expert agent for {agent_name} domain."
capabilities:
  - read
  - write
tools:
  - read_file
  - write_file
---
# System Prompt

{content}
"""
                else:
                    new_content = content
                
                target_file = os.path.join(target_dir, f"{agent_name}.md")
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(new_content)
                
                print(f"Migrated {agent_name} to {target_file}")
            else:
                print(f"Warning: No agent.md found in {agent_path}")

def main():
    migrate_agents(DOMAIN_SOURCE, DOMAIN_TARGET, "domain")
    migrate_agents(AUTOMATION_SOURCE, AUTOMATION_TARGET, "automation")
    print("KB Agent migration complete.")

if __name__ == "__main__":
    main()
