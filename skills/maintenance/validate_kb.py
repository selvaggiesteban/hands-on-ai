import os
import json
import re

def get_master_headers():
    return [
        "Name",
        "Overview",
        "Supported Operations",
        "QA Checklist",
        "Q&A Manual/FAQs",
        "Examples & Capabilities (Skills)", # Updated header name
        "Referencias"
    ]

def get_practical_headers():
    return [
        "Información General",
        "¿Qué es?",
        "¿Cómo se usa?",
        "Mejores Prácticas",
        "Ejemplos de Código",
        "Errores Comunes",
        "Agentes Relacionados"
    ]

def validate_kb_document(file_path, expected_headers):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read file: {e}"

    found_headers = []
    # Regex to find headers, handling emojis
    for match in re.finditer(r"^##\s*(?:[\U00010000-\U0010ffff]\s*)?(.*?)(?=\n|$)", content, re.MULTILINE):
        header_text = match.group(1).strip()
        # Remove markdown links if present in header (e.g. [Name](#name)) -> Name
        header_text = re.sub(r'\[(.*?)\]\(.*\)', r'\1', header_text)
        found_headers.append(header_text)

    missing_headers = []
    for expected in expected_headers:
        # Normalize: "Examples & Capabilities (Skills)" -> "examples&capabilities(skills)"
        norm_expected = re.sub(r'[^\w]', '', expected.lower())
        
        found = False
        for header in found_headers:
            norm_found = re.sub(r'[^\w]', '', header.lower())
            if norm_expected in norm_found: # Loose match
                found = True
                break
        
        if not found:
            missing_headers.append(expected)
            
    if missing_headers:
        return False, f"Missing headers: {', '.join(missing_headers)}"
    
    return True, ""

def main():
    kb_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # We walk the knowledge_base/technologies directory
    tech_dir = os.path.join(kb_root, 'knowledge_base', 'technologies')
    
    passed = 0
    failed = 0
    errors = []

    print("Validating Knowledge Base Structure...")

    for root, dirs, files in os.walk(tech_dir):
        for file in files:
            if file == "README.md":
                path = os.path.join(root, file)
                
                # Determine type based on path
                # .../technologies/frontend/javascript/React/README.md -> Master
                # .../technologies/frontend/javascript/React/skills/hooks/README.md -> Practical
                
                is_skill = 'skills' in path.replace('\\', '/').split('/')
                
                if is_skill:
                    is_valid, msg = validate_kb_document(path, get_practical_headers())
                    type_str = "Skill"
                else:
                    # It might be a category folder like 'frontend/README.md' (if exists) or the tech root
                    # We assume tech root if it has 'agents.md' sibling or we just validate as master if strictly tech
                    # For now, let's assume deeply nested READMEs in technologies (depth > X) are Tech Roots.
                    # But simpler: check if it's NOT a category index.
                    # The scaffolded structure put READMEs in specific tech folders.
                    is_valid, msg = validate_kb_document(path, get_master_headers())
                    type_str = "Tech"

                if is_valid:
                    passed += 1
                else:
                    # Verify if it's just a folder that shouldn't have a readme or is a category
                    # If it misses ALL headers, maybe it's just a placeholder.
                    # But we want strict validation for our generated files.
                    failed += 1
                    errors.append(f"[{type_str}] {path}: {msg}")

    print(f"\n--- Validation Summary ---")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if errors:
        print("\n--- Errors (First 10) ---")
        for e in errors[:10]:
            print(e)
        exit(1)
    else:
        print("\n✅ All documents match their respective templates.")
        exit(0)

if __name__ == "__main__":
    main()
