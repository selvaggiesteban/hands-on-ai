import os
import re
import json

def extract_agents_from_py(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex to find Agent definitions
    # Agent(name="...", instructions="...", ...)
    agents = []
    
    # Find patterns like: name="FAQ Agent", instructions="""..."""
    matches = re.finditer(r'Agent[\w]*\(\s*name=["\\](.*?)["\\],"instructions"=(["\\]{1,3})(.*?)\2', content, re.DOTALL)
    
    for match in matches:
        agents.append({
            "name": match.group(1),
            "instructions": match.group(3).strip()
        })
    
    return agents

def main():
    examples_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../external/providers/openai/openai-agents-python/examples'))
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../agents/imported_subagents.py'))
    
    print(f"Scanning {examples_dir} for OpenAI agents...")
    
    all_found = []
    for root, dirs, files in os.walk(examples_dir):
        for f in files:
            if f.endswith('.py'):
                found = extract_agents_from_py(os.path.join(root, f))
                for a in found:
                    a['source'] = f"openai-examples/{os.path.basename(root)}"
                    all_found.append(a)
                    print(f"Found OpenAI Agent: {a['name']}")

    if not all_found:
        print("No agents found with regex.")
        return

    # Append to imported_subagents.py
    with open(output_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the IMPORTED_SUBAGENTS dictionary
    # It ends with '}'
    # We want to insert before the last '}'
    
    new_entries = []
    for a in all_found:
        enum_name = a['name'].upper().replace(' ', '_').replace('-', '_')
        entry = '    ImportedSubagentType.' + enum_name + ': SubagentConfig(\n'
        entry += '        type="' + a['name'] + '",\n'
        entry += '        description="OpenAI Example Agent from ' + a['source'] + '",\n'
        entry += '        capabilities=["general"],\n'
        entry += '        tool_permissions=["general"],\n'
        entry += '        system_prompt=r"""' + a['instructions'].replace('"""', '\"\"\"') + '""",\n'
        entry += '        metadata={"source": "' + a['source'] + '"}\n'
        entry += '    ),'
        new_entries.append(entry)
    
    # Check if they are already there
    # (Simple check to avoid duplicates if re-run)
    current_content = "".join(lines)
    filtered_entries = [e for e in new_entries if f'type=\"{all_found[new_entries.index(e)]['name']}\"' not in current_content]

    if filtered_entries:
        # Insert before the last '}'
        for i in range(len(lines)-1, -1, -1):
            if '}' in lines[i]:
                lines.insert(i, "\n".join(filtered_entries) + "\n")
                break
        
        # Also need to add to the Enum
        for a in all_found:
            enum_name = a['name'].upper().replace(' ', '_').replace('-', '_')
            enum_line = f'    {enum_name} = "{a["name"]}"\n'
            if enum_line not in current_content:
                for j in range(len(lines)):
                    if 'class ImportedSubagentType(Enum):' in lines[j]:
                        lines.insert(j+1, enum_line)
                        break

        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Successfully added {len(filtered_entries)} OpenAI agents to registry.")

if __name__ == "__main__":
    main()
