import os
import re
import yaml
import json
import shutil
import glob
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class SkillDef:
    name: str
    description: str
    instructions: str
    triggers: List[str]
    owners: List[str] = field(default_factory=list)
    source: str = ""
    is_executable: bool = False
    path: str = ""

AGENT_KEYWORD_MAP = {
    "frontend": ["frontend-developer", "ui-designer", "react-specialist", "nextjs-developer", "vue-expert"],
    "backend": ["backend-developer", "python-pro", "golang-pro", "api-designer", "microservices-architect"],
    "security": ["security-engineer", "security-auditor", "penetration-tester"],
    "data": ["data-scientist", "data-engineer", "ml-engineer", "database-administrator"],
    "doc": ["documentation-engineer", "technical-writer", "product-manager"],
    "debug": ["debugger", "error-detective", "qa-expert"],
    "plan": ["project-manager", "scrum-master", "architect-reviewer", "multi-agent-coordinator"],
    "code": ["fullstack-developer", "typescript-pro", "javascript-pro", "rust-engineer"],
}

def get_owners_by_text(text, agent_list):
    owners = []
    text_lower = text.lower()
    for kw, agents in AGENT_KEYWORD_MAP.items():
        if kw in text_lower:
            owners.extend(agents)
    return list(set(owners))

def parse_skill_folder(folder_path, source_name):
    skill_file = os.path.join(folder_path, "SKILL.md")
    if not os.path.exists(skill_file):
        skill_file = os.path.join(folder_path, "README.md")
    if not os.path.exists(skill_file):
        return None
    try:
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
        name = os.path.basename(folder_path)
        description = ""
        instructions = content
        match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1))
                if frontmatter:
                    description = frontmatter.get('description', '')
                    instructions = content[match.end():].strip()
            except: pass
        else:
            lines = [l for l in content.split('\n') if l.strip() and not l.startswith('#')]
            if lines: description = lines[0]
        triggers = [name.replace('-', ' ')]
        words = re.findall(r'\w+', name + " " + description)
        triggers.extend([w.lower() for w in words if len(w) > 4])
        triggers = list(set(triggers))
        has_code = any(len(glob.glob(os.path.join(folder_path, f"*.{ext}"))) > 0 for ext in ['py', 'js', 'sh'])
        return SkillDef(name=name, description=description, instructions=instructions, triggers=triggers, source=source_name, is_executable=has_code, path=folder_path)
    except Exception as e:
        print(f"Error parsing skill at {folder_path}: {e}")
        return None

def main():
    sources = {"anthropic": "../../external/providers/anthropic/skills/skills", "superpowers": "../../external/providers/anthropic/superpowers/skills"}
    output_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '../skills/imported'))
    registry_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../skills/imported_skills.py'))
    all_skills = []
    for source_name, rel_path in sources.items():
        source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), rel_path))
        if not os.path.exists(source_dir): continue
        folders = [f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))]
        for f in folders:
            folder_path = os.path.join(source_dir, f)
            skill = parse_skill_folder(folder_path, source_name)
            if skill:
                target_name = skill.name
                if any(s.name == target_name for s in all_skills):
                    target_name = f"{skill.name}_{source_name}"
                    skill.name = target_name
                skill.owners = get_owners_by_text(skill.name + " " + skill.description, [])
                if not skill.owners: skill.owners = ["multi-agent-coordinator", "fullstack-developer"]
                dest_path = os.path.join(output_base, target_name)
                os.makedirs(dest_path, exist_ok=True)
                for item in os.listdir(folder_path):
                    s = os.path.join(folder_path, item)
                    d = os.path.join(dest_path, item)
                    if os.path.isfile(s): shutil.copy2(s, d)
                    elif os.path.isdir(s) and item not in ['.git', 'node_modules', '__pycache__']: shutil.copytree(s, d, dirs_exist_ok=True)
                skill.path = f"tools/skills/imported/{target_name}"
                all_skills.append(skill)
                print(f"Migrated Skill: {skill.name} ({source_name})")
    lines = ['"""Imported Skills Registry"""', 'from dataclasses import dataclass', 'from typing import List, Dict', '', '@dataclass', 'class SkillConfig:', '    name: str', '    description: str', '    instructions: str', '    triggers: List[str]', '    owners: List[str]', '    source: str', '    is_executable: bool', '    path: str', '', 'IMPORTED_SKILLS: Dict[str, SkillConfig] = {']
    for s in all_skills:
        safe_instructions = s.instructions.replace('"""', '\"\"\"')
        lines.append('    "' + s.name + '": SkillConfig(')
        lines.append('        name="' + s.name + '",')
        lines.append('        description=' + json.dumps(s.description) + ',')
        lines.append('        instructions=r"""' + safe_instructions + '""",')
        lines.append('        triggers=' + json.dumps(s.triggers) + ',')
        lines.append('        owners=' + json.dumps(s.owners) + ',')
        lines.append('        source="' + s.source + '",')
        lines.append('        is_executable=' + str(s.is_executable) + ',')
        lines.append('        path="' + s.path + '"')
        lines.append('    ),')
    lines.append('}')
    with open(registry_path, 'w', encoding='utf-8') as f: f.write("\n".join(lines))
    print(f"\nSuccessfully generated {registry_path} with {len(all_skills)} skills.")

if __name__ == "__main__": main()
