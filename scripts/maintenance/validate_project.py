import os
import json
import yaml
import glob
import argparse
from jsonschema import validate, ValidationError

def load_json_or_yaml(file_path):
    """Loads a JSON or YAML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.endswith('.json'):
                return json.load(f)
            elif file_path.endswith(('.yaml', '.yml')):
                return yaml.safe_load(f)
    except Exception as e:
        print(f"  ❌ Error loading {os.path.basename(file_path)}: {e}")
        return None
    return None

def validate_schemas(base_dir):
    """Validates main config files against their JSON schemas."""
    print("--- Running Schema Validation ---")
    success = True
    schema_root = os.path.join(base_dir, 'skills', 'marketing', 'project_meta')
    schema_dir = os.path.join(schema_root, 'schemas')
    
    files_to_validate = {
        'rag-config.json': 'rag-config.schema.json',
        'plan.json': 'plan.schema.json',
        'prompt-library.json': 'prompt-library.schema.json',
        'threat-model.yaml': 'threat-model.schema.json'
    }
    
    paths = {
        'rag-config.json': os.path.join(schema_root, 'ai-context', 'rag-config.json'),
        'plan.json': os.path.join(schema_root, 'planning', 'plan.json'),
        'prompt-library.json': os.path.join(schema_root, 'ai-context', 'prompt-library.json'),
        'threat-model.yaml': os.path.join(schema_root, 'security', 'threat-model.yaml')
    }

    for data_file, schema_file in files_to_validate.items():
        schema_path = os.path.join(schema_dir, schema_file)
        data_path = paths[data_file]

        schema = load_json_or_yaml(schema_path)
        data = load_json_or_yaml(data_path)

        if schema is None or data is None:
            success = False
            continue

        try:
            validate(instance=data, schema=schema)
            print(f"  ✅ {data_file} is valid against {schema_file}.")
        except ValidationError as e:
            print(f"  ❌ {data_file} is INVALID against {schema_file}:")
            print(f"     - {e.message} (Path: {list(e.path)})")
            success = False
            
    return success

def validate_frontmatter(base_dir, fix=False):
    """Checks for frontmatter in all skills markdown files and optionally fixes them."""
    print("\n--- Running Frontmatter Validation ---")
    success = True
    md_files = glob.glob(os.path.join(base_dir, 'skills', '**', '*.md'), recursive=True)
    
    if not md_files:
        print("  ⚠️ No markdown files found to validate.")
        return False

    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip().startswith('---'):
                print(f"  ❌ Missing frontmatter in {file_path}")
                success = False
                if fix:
                    file_name = os.path.splitext(os.path.basename(file_path))[0]
                    new_header = f"---\nname: {file_name}\ndescription: Use when [describe the use case for this skill].\n---\n\n"
                    with open(file_path, 'w', encoding='utf-8') as f_write:
                        f_write.write(new_header + content)
                    print(f"  🛠️  FIXED: Added standard header to {file_path}")

        except Exception as e:
            print(f"  ❌ Error reading or parsing {file_path}: {e}")
            success = False
            
    if success:
        print(f"  ✅ All {len(md_files)} markdown files have frontmatter.")
    return success

def validate_master_index(base_dir):
    """Performs sanity checks on the main audit matrix files."""
    print("\n--- Running Master Index Validation ---")
    success = True
    
    matrix_files = [
        "matrix_agents_audit.json",
        "matrix_checklist_audit.json",
        "matrix_skills_audit.json",
        "matrix_scripts_audit.json"
    ]

    for matrix_file in matrix_files:
        matrix_path = os.path.join(base_dir, matrix_file)
        matrix_data = load_json_or_yaml(matrix_path)
        
        if matrix_data is None:
            print(f"  ❌ Error loading {matrix_file}.")
            success = False
            continue
            
        if not matrix_data.get('categories') or not matrix_data['categories']:
            print(f"  ❌ '{matrix_file}' has empty or missing 'categories' section.")
            success = False
        else:
            print(f"  ✅ '{matrix_file}' 'categories' section is populated.")
            
        if 'total_files' not in matrix_data or matrix_data['total_files'] <= 0:
            print(f"  ❌ '{matrix_file}' has invalid or missing 'total_files' count.")
            success = False
        else:
            print(f"  ✅ '{matrix_file}' 'total_files' count is valid.")

    return success

def main():
    """Main validation function."""
    parser = argparse.ArgumentParser(description="Validate the project structure.")
    parser.add_argument('--fix', action='store_true', help="Automatically fix frontmatter issues.")
    args = parser.parse_args()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    print(f"Starting validation for project at: {base_dir}")
    
    schema_ok = validate_schemas(base_dir)
    frontmatter_ok = validate_frontmatter(base_dir, fix=args.fix)
    index_ok = validate_master_index(base_dir)
    
    print("\n--- Validation Summary ---")
    if schema_ok and frontmatter_ok and index_ok:
        print("  🎉 All checks passed successfully! Project is well-structured.")
    else:
        print("  💔 Some checks failed. Please review the errors above.")

if __name__ == "__main__":
    main()
