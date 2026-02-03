"""
Hands-On Auditor & Semantic Bridge
Unifies file extraction, roadmap verification, and semantic gap analysis.
Replaces: universal_extractor.py, roadmap_auditor.py
"""

import os
import json
import shutil
import subprocess
import sys
import warnings
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import zipfile
import xml.dom.minidom

# --- Optional AI/Media Libraries ---
try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

try:
    from pptx import Presentation
    HAS_PPTX = True
except ImportError:
    HAS_PPTX = False

try:
    import pytesseract
    from PIL import Image
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

try:
    import whisper
    HAS_WHISPER = True
except ImportError:
    HAS_WHISPER = False

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)

class HandsOnAuditor:
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.timestamp = datetime.now().isoformat()
        
        # Shared Data State
        self.project_data = defaultdict(lambda: {
            "files": [],
            "content_summary": "",
            "stats": {"count": 0, "errors": 0, "by_extension": defaultdict(int)},
            "meta_status": "unknown"
        })
        self.global_stats = {
            "total_files": 0,
            "processed": 0,
            "errors": 0,
            "ai_ops": 0
        }
        
        # Semantic Bridge Data
        self.semantic_insights = []

    def run_full_audit(self):
        print(f"🚀 Starting Hands-On Audit on: {self.root_path}")
        
        # 1. Project Discovery & Meta Enforcement
        self._discover_and_enforce_meta()
        
        # 2. Universal Scan & Extraction
        self._scan_and_extract()
        
        # 3. Roadmap & Environment Verification
        self._verify_environment()
        
        # 4. Semantic Bridge Analysis
        self._run_semantic_bridge()
        
        # 5. Report Generation
        self._save_reports()

    # --- Phase 1: Meta Enforcement ---
    def _discover_and_enforce_meta(self):
        print("\n--- Phase 1: Project Discovery & Meta Enforcement ---")
        try:
            # Source of truth for template
            root_dir = self.root_path.parent
            template_source = root_dir / "skills" / "marketing" / "project_meta"
            
            if not template_source.exists():
                print(f"⚠️ Template not found at {template_source}. Skipping enforcement.")
                return

            for item in os.listdir(self.root_path):
                item_path = self.root_path / item
                if item_path.is_dir() and not item.startswith('.'):
                    self._ensure_project_meta(item, item_path, template_source)
                    
        except Exception as e:
            print(f"❌ Phase 1 Error: {e}")

    def _ensure_project_meta(self, project_name, project_path, template_source):
        target_dir = project_path / "project_meta"
        
        if not target_dir.exists():
            try:
                print(f"🛠️ Creating project_meta for [{project_name}]...")
                shutil.copytree(template_source, target_dir)
                self.project_data[project_name]["meta_status"] = "created"
            except Exception as e:
                print(f"❌ Failed to copy project_meta to {project_name}: {e}")
                self.project_data[project_name]["meta_status"] = "failed"
        else:
            # Recursive sync for missing files
            missing_count = 0
            for root, dirs, files in os.walk(template_source):
                rel_path = Path(root).relative_to(template_source)
                dest_root = target_dir / rel_path
                
                if not dest_root.exists():
                    os.makedirs(dest_root, exist_ok=True)
                
                for file in files:
                    src_file = Path(root) / file
                    dest_file = dest_root / file
                    if not dest_file.exists():
                        try:
                            shutil.copy2(src_file, dest_file)
                            missing_count += 1
                        except Exception:
                            pass
            
            if missing_count > 0:
                print(f"🔄 Synced {missing_count} missing meta files to [{project_name}]")
                self.project_data[project_name]["meta_status"] = "updated"
            else:
                self.project_data[project_name]["meta_status"] = "ok"

    # --- Phase 2: Extraction ---
    def _scan_and_extract(self):
        print("\n--- Phase 2: Universal Extraction ---")
        
        # Whisper Lazy Loader
        whisper_model = None
        
        def load_whisper():
            nonlocal whisper_model
            if whisper_model is None and HAS_WHISPER:
                print("⏳ Loading Whisper AI model (tiny)...")
                try:
                    whisper_model = whisper.load_model("tiny")
                    print("✅ Whisper loaded.")
                except:
                    whisper_model = False
            return whisper_model

        # Extractors
        def extract_text(path):
            try:
                with open(path, 'r', encoding='utf-8') as f: return f.read()
            except: return "[Binary/Error]"

        for root, dirs, files in os.walk(self.root_path):
            if '.git' in root or '__pycache__' in root or 'node_modules' in root:
                continue
                
            for file in files:
                file_path = Path(root) / file
                self.global_stats["total_files"] += 1
                
                # Determine Project
                try:
                    rel = file_path.relative_to(self.root_path)
                    project_name = rel.parts[0] if len(rel.parts) > 1 else "_ROOT_"
                except:
                    project_name = "_EXTERNAL_"

                ext = file_path.suffix.lower()
                
                # Update Stats
                self.project_data[project_name]["stats"]["by_extension"][ext] += 1
                
                content = ""
                
                try:
                    # Logic dispatch
                    if ext == '.docx':
                        # Minimal docx
                        try:
                            with zipfile.ZipFile(file_path) as z:
                                xml_c = z.read('word/document.xml')
                                dom = xml.dom.minidom.parseString(xml_c)
                                content = "".join([t.firstChild.nodeValue for t in dom.getElementsByTagName('w:t') if t.firstChild])
                        except Exception as e: content = f"[DOCX Error: {e}]"
                        
                    elif ext in ['.pdf'] and HAS_PYPDF:
                        try:
                            reader = PdfReader(file_path)
                            content = "\n".join([p.extract_text() for p in reader.pages])
                        except Exception as e: content = f"[PDF Error: {e}]"
                        
                    elif ext in ['.png', '.jpg'] and HAS_OCR:
                        try:
                            content = pytesseract.image_to_string(Image.open(file_path))
                            self.global_stats["ai_ops"] += 1
                        except Exception as e: content = f"[OCR Error: {e}]"
                        
                    elif ext in ['.mp3', '.wav', '.mp4'] and HAS_WHISPER:
                        model = load_whisper()
                        if model:
                            try:
                                res = model.transcribe(str(file_path), fp16=False)
                                content = res['text']
                                self.global_stats["ai_ops"] += 1
                            except Exception as e: content = f"[Whisper Error: {e}]"
                    
                    elif ext in ['.py', '.js', '.md', '.txt', '.json', '.html', '.css']:
                        content = extract_text(file_path)
                    else:
                        continue # Skip binaries not handled

                    # Log Success
                    self.project_data[project_name]["files"].append({
                        "path": str(rel),
                        "content": content,
                        "size": os.path.getsize(file_path)
                    })
                    self.project_data[project_name]["stats"]["count"] += 1
                    self.global_stats["processed"] += 1
                    
                    # Print progress every 100 files
                    if self.global_stats["processed"] % 100 == 0:
                        print(f"   Processed {self.global_stats['processed']} files...")

                except Exception as e:
                    self.project_data[project_name]["stats"]["errors"] += 1
                    self.global_stats["errors"] += 1

    # --- Phase 3: Verification ---
    def _verify_environment(self):
        print("\n--- Phase 3: Environment Verification ---")
        # Simplified checks
        checks = {
            "Python": lambda: sys.version.split()[0],
            "Docker": lambda: subprocess.run(['docker', '--version'], capture_output=True, text=True).stdout.strip() if shutil.which('docker') else "Not Found"
        }
        
        self.env_status = {}
        for name, func in checks.items():
            try:
                self.env_status[name] = func()
            except:
                self.env_status[name] = "Error"
        
        print(f"   Environment: {self.env_status}")

    # --- Phase 4: Semantic Bridge ---
    def _run_semantic_bridge(self):
        print("\n--- Phase 4: Semantic Bridge Analysis (Updating Project Meta) ---")
        """
        Updates the original project_meta/project_metadata.json file with real data
        harvested during the scan, replacing placeholders like {{project_name}}
        and {{technology_stack}}.
        """
        
        # Map common extensions to tech names
        ext_map = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.html': 'HTML', '.css': 'CSS', '.php': 'PHP',
            '.java': 'Java', '.cs': 'C#', '.go': 'Go',
            '.rb': 'Ruby', '.sql': 'SQL', '.rs': 'Rust'
        }
        
        current_date = datetime.now().strftime("%Y-%m-%d")

        for project, data in self.project_data.items():
            if project in ["_ROOT_", "_EXTERNAL_"]: continue
            
            meta_file = self.root_path / project / "project_meta" / "project_metadata.json"
            
            if not meta_file.exists():
                print(f"⚠️ Metadata file not found for [{project}]. Skipping update.")
                continue

            try:
                # 1. Determine Stack
                # Sort extensions by count
                sorted_exts = sorted(data["stats"]["by_extension"].items(), key=lambda x: x[1], reverse=True)
                top_langs = []
                for ext, count in sorted_exts:
                    if ext in ext_map:
                        top_langs.append(ext_map[ext])
                        if len(top_langs) >= 3: break
                
                tech_stack = ", ".join(top_langs) if top_langs else "Unknown"

                # 2. Read File
                with open(meta_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 3. Perform Replacements (Semantic Bridge)
                original_content = content
                
                content = content.replace("{{project_name}}", project)
                content = content.replace("{{technology_stack}}", tech_stack)
                content = content.replace("{{date}}", current_date)
                content = content.replace("{{auditor_role}}", "Hands-On Auditor")
                
                # 4. Write Back (if changed)
                if content != original_content:
                    with open(meta_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"   📝 Updated project_metadata.json for [{project}] (Stack: {tech_stack})")
                else:
                    print(f"   ✓ No changes needed for [{project}]")
                    
            except Exception as e:
                print(f"   ❌ Failed to update metadata for [{project}]: {e}")

    # --- Phase 5: Reporting ---
    def _save_reports(self):
        print("\n--- Phase 5: Generating Master Report ---")
        
        # 1. Master Audit Report (Technical)
        report_path = "src_audit_report_ai.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# HANDS-ON AI AUDIT REPORT\n")
            f.write(f"Generated: {self.timestamp}\n")
            f.write(f"Global Stats: {json.dumps(self.global_stats, indent=2)}\n")
            f.write(f"Environment: {json.dumps(self.env_status, indent=2)}\n\n")
            
            for project, data in self.project_data.items():
                f.write(f"## Project: {project}\n")
                f.write(f"Files: {data['stats']['count']} | Errors: {data['stats']['errors']} | Meta: {data['meta_status']}\n")
                f.write("-" * 40 + "\n")
                # Write file details (truncated)
                for file_entry in data['files'][:50]: # Limit detailed listing
                    f.write(f"* {file_entry['path']} ({file_entry['size']} bytes)\n")
                if len(data['files']) > 50:
                    f.write(f"* ... and {len(data['files']) - 50} more files.\n")
                f.write("\n")

        print(f"✅ Master Report generated: {report_path}")

if __name__ == "__main__":
    src_dir = os.path.join(os.getcwd(), 'src')
    auditor = HandsOnAuditor(src_dir)
    auditor.run_full_audit()
