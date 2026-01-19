import os
import re
from pathlib import Path

def find_markdown_files(root_dir):
    """Finds all markdown files in a directory."""
    return list(Path(root_dir).rglob("*.md"))

def check_links_and_references(files):
    """
    Checks for broken internal links and outdated directory references in markdown files.
    """
    broken_links = []
    outdated_references = []
    link_pattern = re.compile(r'[[^]]+]\((?!https?://|#)([^)]+)\)')
    reference_pattern = re.compile(r'01-Setup|02-Technologies|03-Templates|04-Tools')

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                content = f.read()
            except UnicodeDecodeError:
                print(f"Warning: Could not read {file_path} due to encoding issues. Skipping.")
                continue

        # Check for outdated references
        for match in reference_pattern.finditer(content):
            outdated_references.append({
                "file": str(file_path),
                "reference": match.group(0)
            })

        # Check for broken internal links
        for match in link_pattern.finditer(content):
            link_target = match.group(2).split('#')[0] # Ignore anchor part
            if not link_target:
                continue

            target_path = Path(file_path).parent / Path(link_target)
            
            if not target_path.exists():
                broken_links.append({
                    "file": str(file_path),
                    "link": link_target,
                    "resolved_path": str(target_path.resolve())
                })

    return broken_links, outdated_references

def main():
    """Main function to run the validation."""
    project_root = Path(__file__).parent.parent.resolve()
    markdown_files = find_markdown_files(project_root)

    print(f"Scanning {len(markdown_files)} markdown files...")

    broken_links, outdated_references = check_links_and_references(markdown_files)

    if not broken_links and not outdated_references:
        print("\n--- Validation PASSED ---")
        print("No broken internal links or outdated references found.")
        return

    if outdated_references:
        print("\n--- FAILED: Found Outdated References ---")
        # Unique references
        unique_refs = {f"- File: {ref['file']}, Reference: '{ref['reference']}'" for ref in outdated_references}
        for ref in sorted(list(unique_refs)):
            print(ref)
            
    if broken_links:
        print("\n--- FAILED: Found Broken Internal Links ---")
        for link in broken_links:
            print(f"- File: {link['file']}")
            print(f"  - Link: '{link['link']}'")
            print(f"  - Resolved Path: '{link['resolved_path']}' (Not Found)")
            
if __name__ == "__main__":
    main()
