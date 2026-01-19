import os
import json
import re
import yaml
import glob
from datetime import datetime

def parse_frontmatter(content):
    """
    Parses YAML frontmatter from a file's content.
    """
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1))
            return frontmatter if isinstance(frontmatter, dict) else {}
        except yaml.YAMLError:
            return {}
    return {}

def parse_markdown_metadata(content):
    """
    Parses metadata from the standardized Markdown body (Name section).
    """
    metadata = {}
    
    # Extract fields from the '## 🏷️ Name' section
    # **Nombre oficial:** [Nombre completo]
    name_match = re.search(r'\*\*Nombre oficial:\*\*\s*(.*)', content)
    if name_match:
        metadata['title'] = name_match.group(1).strip()
        metadata['official_name'] = name_match.group(1).strip()

    # **Categoría:** [Category]
    category_match = re.search(r'\*\*Categoría:\*\*\s*(.*)', content)
    if category_match:
        metadata['category'] = category_match.group(1).strip()

    # **Stack:** [Stack]
    stack_match = re.search(r'\*\*Stack:\*\*\s*(.*)', content)
    if stack_match:
        metadata['stack'] = stack_match.group(1).strip()

    return metadata

def get_document_info(file_path):
    """
    Extracts information from a file, prioritizing frontmatter, then Markdown body.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        info = parse_frontmatter(content)
        
        # Merge/Fallback with Markdown body parsing
        md_info = parse_markdown_metadata(content)
        for k, v in md_info.items():
            if k not in info or not info[k]:
                info[k] = v

        info['file_path'] = file_path.replace('\\', '/')
        
        if not info.get('title'):
             # Fallback title
            info['title'] = os.path.basename(file_path)

        return info
    except Exception as e:
        # print(f"Error reading {file_path}: {e}")
        return None

def main():
    """
    Generates a detailed, structured index of the entire project knowledge base.
    """
    kb_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    master_index = {
        "version": "2.1",
        "indexed_at": datetime.now().isoformat(),
        "documents": [],
        "categories": {},
        "stacks": {},
        "total_documents": 0
    }

    # 1. Index all relevant documents
    # Using specific patterns to avoid indexing generated code or temp files
    patterns_to_index = [
        "knowledge_base/skills/**/*.md",
        "knowledge_base/stacks/**/*.md",
        "knowledge_base/technologies/**/*.md",
        "project_meta/**/*.json",
        "project_meta/**/*.yaml",
        "project_meta/**/*.md"
    ]

    all_files = []
    for pattern in patterns_to_index:
        full_pattern = os.path.join(kb_root, pattern)
        # Recursive glob requires python 3.10+ or root_dir arg in older versions, 
        # but here we use the glob string directly.
        # Note: glob.glob with recursive=True works with **
        matched = glob.glob(full_pattern, recursive=True)
        all_files.extend(matched)

    # Remove duplicates
    all_files = list(set(all_files))

    print(f"Scanning {len(all_files)} files...")

    for file_path in all_files:
        if "README.md" in file_path or file_path.endswith(".json") or file_path.endswith(".yaml"):
            doc_info = get_document_info(file_path)
            if doc_info:
                master_index["documents"].append(doc_info)

    # 2. Process documents to build categories and stacks indexes
    for doc in master_index["documents"]:
        # Build Categories Index
        category = doc.get('category')
        if category:
            if category not in master_index["categories"]:
                master_index["categories"][category] = {"count": 0, "documents": []}
            master_index["categories"][category]["count"] += 1
            master_index["categories"][category]["documents"].append(doc['file_path'])

        # Build Stacks Index
        stack = doc.get('stack')
        if stack:
            if stack not in master_index["stacks"]:
                master_index["stacks"][stack] = {"count": 0, "documents": []}
            master_index["stacks"][stack]["count"] += 1
            master_index["stacks"][stack]["documents"].append(doc['file_path'])

    # Add total documents count
    master_index["total_documents"] = len(master_index["documents"])

    # Save the index to a JSON file
    index_file_path = os.path.join(kb_root, 'kb_index.json')
    with open(index_file_path, 'w', encoding='utf-8') as f:
        json.dump(master_index, f, indent=4)

    print(f"Master Knowledge Base index generated successfully at {index_file_path}")
    print(f"Indexed {master_index['total_documents']} documents.")
    print(f"Categories found: {len(master_index['categories'])}")
    print(f"Stacks found: {len(master_index['stacks'])}")

if __name__ == "__main__":
    main()
