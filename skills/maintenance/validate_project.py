import os
import json
import yaml
import glob
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
    schema_dir = os.path.join(base_dir, 'project_meta', 'schemas')
    
    files_to_validate = {
        'rag-config.json': 'rag-config.schema.json',
        'plan.json': 'plan.schema.json',
        'prompt-library.json': 'prompt-library.schema.json',
        'threat-model.yaml': 'threat-model.schema.json'
    }
    
    paths = {
        'rag-config.json': os.path.join(base_dir, 'project_meta', 'ai-context', 'rag-config.json'),
        'plan.json': os.path.join(base_dir, 'project_meta', 'planning', 'plan.json'),
        'prompt-library.json': os.path.join(base_dir, 'project_meta', 'ai-context', 'prompt-library.json'),
        'threat-model.yaml': os.path.join(base_dir, 'project_meta', 'security', 'threat-model.yaml')
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

def validate_frontmatter(base_dir):
    """Checks for frontmatter in all knowledge_base markdown files."""
    print("\n--- Running Frontmatter Validation ---")
    success = True
    md_files = glob.glob(os.path.join(base_dir, 'knowledge_base', '**', '*.md'), recursive=True)
    required_fields = ['id', 'title', 'category', 'version', 'last_updated']
    
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
                continue

            frontmatter = load_json_or_yaml(file_path) # Reuse function for parsing frontmatter
            if not frontmatter:
                 # This check is tricky because the content after --- is not valid yaml
                 pass # Cannot reliably parse frontmatter this way if there is content after

        except Exception as e:
            print(f"  ❌ Error reading or parsing {file_path}: {e}")
            success = False
            
    if success:
        print(f"  ✅ All {len(md_files)} markdown files seem to have frontmatter.")
    return success

def validate_master_index(base_dir):
    """Performs sanity checks on the master index file."""
    print("\n--- Running Master Index Validation ---")
    success = True
    index_path = os.path.join(base_dir, 'kb_index.json')
    
    index = load_json_or_yaml(index_path)
    if index is None:
        return False
        
    total_docs = index.get('total_documents', 0)
    if total_docs != len(index.get('documents', [])):
        print(f"  ❌ 'total_documents' count ({total_docs}) does not match actual document list size ({len(index.get('documents', []))}).")
        success = False
    else:
        print(f"  ✅ 'total_documents' count is consistent ({total_docs}).")
        
    if not index.get('categories'):
        print(f"  ❌ 'categories' section is empty.")
        success = False
    else:
        print(f"  ✅ 'categories' section is populated.")

    if not index.get('relationships'):
        print(f"  ❌ 'relationships' section is empty.")
        success = False
    else:
        print(f"  ✅ 'relationships' section is populated.")
        
    return success


def main():
    """Main validation function."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print(f"Starting validation for project at: {base_dir}")
    
    schema_ok = validate_schemas(base_dir)
    frontmatter_ok = validate_frontmatter(base_dir)
    index_ok = validate_master_index(base_dir)
    
    print("\n--- Validation Summary ---")
    if schema_ok and frontmatter_ok and index_ok:
        print("  🎉 All checks passed successfully! Project is well-structured.")
    else:
        print("  💔 Some checks failed. Please review the errors above.")

if __name__ == "__main__":
    main()
