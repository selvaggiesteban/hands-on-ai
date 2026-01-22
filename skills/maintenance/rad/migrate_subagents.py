import os
import re
import yaml
import glob
from dataclasses import dataclass, asdict
import json

@dataclass
class SubagentDef:
    name: str
    type_enum: str
    description: str
    tools: list
    system_prompt: str
    category: str
    metadata: dict  # Nuevo campo para preservar todo el YAML

def parse_markdown_agent(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract frontmatter
        match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None
            
        frontmatter = yaml.safe_load(match.group(1))
        body = content[match.end():].strip()
        
        # Clean up tools
        tools_raw = frontmatter.get('tools', '')
        if isinstance(tools_raw, str):
            tools = [t.strip().lower() for t in tools_raw.split(',')]
        else:
            tools = []
            
        # Create enum-friendly name
        name = frontmatter.get('name', os.path.basename(file_path).replace('.md', ''))
        enum_name = name.upper().replace('-', '_')
        
        # Get category from path
        category = os.path.basename(os.path.dirname(file_path))
        
        return SubagentDef(
            name=name,
            type_enum=enum_name,
            description=frontmatter.get('description', ''),
            tools=tools,
            system_prompt=body,
            category=category,
            metadata=frontmatter # Guardamos todo el YAML aquí
        )
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def generate_python_module(agents):
    lines = [
        '"""',
        'Imported Subagents - Auto-generated from external providers',
        '"""',
        '',
        'from enum import Enum',
        'from dataclasses import dataclass',
        'from typing import List',
        '',
        '@dataclass',
        'class SubagentConfig:',
        '    type: str',
        '    description: str',
        '    capabilities: List[str]',
        '    tool_permissions: List[str]',
        '    system_prompt: str',
        '    metadata: dict = None',
        '',
        'class ImportedSubagentType(Enum):'
    ]
    
    # Enum definitions
    for agent in agents:
        lines.append(f'    {agent.type_enum} = "{agent.name}"')
        
    lines.append('')
    lines.append('IMPORTED_SUBAGENTS = {')
    
    # Agent definitions
    for agent in agents:
        # Escape quotes in prompt
        safe_prompt = agent.system_prompt.replace('"""', '\"\"\"')
        
        lines.append(f'    ImportedSubagentType.{agent.type_enum}: SubagentConfig(')
        lines.append(f'        type="{agent.name}",')
        lines.append(f'        description="{agent.description}",')
        lines.append(f'        capabilities={json.dumps(agent.tools)},')
        lines.append(f'        tool_permissions={json.dumps(agent.tools)},')
        lines.append('        system_prompt=r"""' + safe_prompt + '""",')
        lines.append(f'        metadata={json.dumps(agent.metadata, indent=4)}')
        lines.append('    ),')
        
    lines.append('}')
    
    return "\n".join(lines)

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../external/providers/anthropic/awesome-claude-code-subagents/categories'))
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../agents/imported_subagents.py'))
    
    print(f"Scanning {root_dir}...")
    
    files = glob.glob(os.path.join(root_dir, "**/*.md"), recursive=True)
    agents = []
    
    for f in files:
        if "README.md" in f: continue
        agent = parse_markdown_agent(f)
        if agent:
            agents.append(agent)
            print(f"Parsed: {agent.name}")
            
    content = generate_python_module(agents)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"\nSuccessfully generated {output_path} with {len(agents)} agents.")

if __name__ == "__main__":
    main()