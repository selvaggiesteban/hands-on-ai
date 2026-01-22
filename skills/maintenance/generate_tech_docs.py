import os
import json

def generate_readme_content(tech_name, tech_data):
    content = f"# {tech_data.get('title', tech_name.replace('-', ' ').title())}\n\n"

    if tech_data.get('tags'):
        content += "## Stack / Tags\n"
        content += f"-   `[{', '.join(tech_data['tags'])}]`\n\n"

    if tech_data.get('operations'):
        content += "## Supported Operations\n"
        content += f"-   `[{', '.join(tech_data['operations'])}]`\n\n"

    if tech_data.get('qa_checklist'):
        content += "## QA Checklist\n"
        for item in tech_data['qa_checklist']:
            content += f"-   {item}\n"
        content += "\n"

    if tech_data.get('risks'):
        content += "## Dangers / Risks\n"
        for item in tech_data['risks']:
            content += f"-   {item}\n"
        content += "\n"

    return content

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    kb_index_path = os.path.join(root_dir, 'kb_index.json')
    tech_base_dir = os.path.join(root_dir, 'src', 'knowledge_base')

    if not os.path.exists(kb_index_path):
        print(f"Error: kb_index.json not found at {kb_index_path}")
        return

    with open(kb_index_path, 'r', encoding='utf-8') as f:
        kb_index = json.load(f)

    for category_top_level_dir in os.listdir(tech_base_dir):
        category_top_level_path = os.path.join(tech_base_dir, category_top_level_dir)
        if os.path.isdir(category_top_level_path):
            for tech_category_dir in os.listdir(category_top_level_path):
                tech_category_path = os.path.join(category_top_level_path, tech_category_dir)
                if os.path.isdir(tech_category_path):
                    for tech_folder_name in os.listdir(tech_category_path):
                        tech_full_path = os.path.join(tech_category_path, tech_folder_name)
                        if os.path.isdir(tech_full_path):
                            # Normalize tech_folder_name to match the slug in kb_index.json
                            normalized_tech_folder_name_for_comparison = tech_folder_name.lower()

                            for tech_slug, tech_data in kb_index.get('technologies', {}).items():
                                if normalized_tech_folder_name_for_comparison == tech_slug.lower():
                                    readme_output_path = os.path.join(tech_full_path, 'README.md')
                                    readme_content = generate_readme_content(tech_slug, tech_data)

                                    os.makedirs(os.path.dirname(readme_output_path), exist_ok=True)
                                    with open(readme_output_path, 'w', encoding='utf-8') as f:
                                        f.write(readme_content)
                                    print(f"Generated README.md for {tech_data.get('title', tech_slug)} at {readme_output_path}")
                                    break # Found a match, move to the next tech_folder_name
                            else:
                                print(f"Warning: Could not find KB index entry for technology folder '{tech_folder_name}'. Skipping generation.")

if __name__ == "__main__":
    main()
