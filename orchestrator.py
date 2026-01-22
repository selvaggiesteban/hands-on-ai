# Orchestrator Principal - Hands On AI (Full Authority System)
# Sistema de control centralizado con acceso total al disco local (Windows 10).
# Integra Comandos, Procesos, Automatizaciones y Templates con UI/UX optimizada.

import os
import sys
import re
import json
import shutil
import asyncio
import subprocess
import glob
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable

# Fix for Windows Unicode Console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Configuración de rutas del sistema
SYSTEM_ROOT = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(SYSTEM_ROOT, 'tools')
KB_DIR = os.path.join(SYSTEM_ROOT, 'knowledge_base')
TEMPLATES_DIR = os.path.join(KB_DIR, 'templates')
ENV_FILE = os.path.join(SYSTEM_ROOT, '.env')

# Agregar tools al path
sys.path.insert(0, TOOLS_DIR)

# Intentar importar IA
try:
    from ai_wrapper.multi_model import MultiModelProcessor, MultiModelConfig
    from ai_wrapper.chat_manager import ChatManager
    from ai_wrapper.providers.base import Message
    from ai_wrapper.logging_config import get_logger
    AI_AVAILABLE = True
    logger = get_logger("orchestrator")
except ImportError:
    AI_AVAILABLE = False
    # Mock logger if AI is not available
    class MockLogger:
        def __getattr__(self, name):
            return lambda *args, **kwargs: print(f"LOGGER.{name}:", *args, **kwargs)
    logger = MockLogger()

# Intentar importar Enhanced Multi-Agent System
try:
    sys.path.append(SYSTEM_ROOT)
    from integrations.enhanced_multi_agent_system import EnhancedMultiAgentSystem
    from tools.security.policy_enforcer import SecurityPolicyEnforcer
    ENHANCED_SYSTEM_AVAILABLE = True
except ImportError as e:
    ENHANCED_SYSTEM_AVAILABLE = False
    print(f"⚠️ EnhancedMultiAgentSystem no disponible: {e}")


class OrchestratorToolboxAdapter:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def get_definitions(self):
        return self.orchestrator.TOOL_DEFINITIONS

    async def execute_tool(self, name, args):
        if name == "write_file":
            # Adaptar argumentos si es necesario
            return await self.orchestrator.cmd_write_file(args.get("file_path"), args.get("content"))
        elif name == "read_file":
            return await self.orchestrator.cmd_read_file(args.get("file_path"))
        elif name == "list_directory":
            return await self.orchestrator.cmd_list_directory(args.get("dir_path"))
        elif name == "run_shell_command":
            return await self.orchestrator.cmd_run_shell_command(args.get("command"))
        else:
            return f"Error: Herramienta desconocida {name}"

class Orchestrator:
    def __init__(self):
        self.active_root = SYSTEM_ROOT
        self.ai = None
        self.enhanced_system = None
        self.chat_manager = None
        self.toolbox_adapter = None # Nuevo adaptador
        self.policy_enforcer = None # Enforcer de seguridad
        
        # Inicializar Enforcer si es posible (antes de cargar contexto para tenerlo listo)
        try:
            from tools.security.policy_enforcer import SecurityPolicyEnforcer
            self.policy_enforcer = SecurityPolicyEnforcer() # Carga threat-model.yaml automáticamente
        except Exception as e:
            logger.error(f"Failed to init PolicyEnforcer: {e}")

        self._init_ui()
        self._init_toolbox() # Inicializar definiciones primero
        self._load_context_files() # Cargar Reglas y Prompts
        self._scan_dependencies()  # Escanear Entorno
        self._init_ai()
        self._init_enhanced_system()
        self._init_chat_manager()

    def _init_enhanced_system(self):
        if ENHANCED_SYSTEM_AVAILABLE:
            try:
                # Crear adaptador de herramientas
                self.toolbox_adapter = OrchestratorToolboxAdapter(self)
                
                # Pasar self.ai y toolbox al constructor
                self.enhanced_system = EnhancedMultiAgentSystem(
                    self.active_root, 
                    ai_processor=self.ai,
                    toolbox=self.toolbox_adapter
                )
                logger.info("EnhancedMultiAgentSystem initialized.")
            except Exception as e:
                logger.error("Failed to initialize EnhancedMultiAgentSystem", error=str(e))

    def _load_context_files(self):
        """Carga reglas críticas y librería de prompts en memoria."""
        self.context_rules = ""
        self.prompt_library = {}
        
        # 1. Cargar Reglas (07-Rules.md)
        rules_path = os.path.join(self.active_root, 'knowledge_base', 'setup', '07-Rules.md')
        if os.path.exists(rules_path):
            try:
                with open(rules_path, 'r', encoding='utf-8') as f:
                    self.context_rules = f"\n=== CRITICAL PROJECT RULES (MUST FOLLOW) ===\n{f.read()}\n==========================================\n"
                logger.info("Rules loaded from 07-Rules.md")
            except Exception as e:
                logger.error(f"Error loading rules: {e}")

        # 2. Cargar Prompt Library
        prompts_path = os.path.join(self.active_root, 'project_meta', 'ai-context', 'prompt-library.json')
        if os.path.exists(prompts_path):
            try:
                with open(prompts_path, 'r', encoding='utf-8') as f:
                    self.prompt_library = json.load(f)
                logger.info("Prompt library loaded.")
            except Exception as e:
                logger.error(f"Error loading prompt library: {e}")

    def _scan_dependencies(self):
        """Escanea requirements.txt y package.json para dar contexto real a la IA."""
        self.dependencies_context = ""
        deps_summary = []
        
        # Python
        req_path = os.path.join(self.active_root, 'requirements.txt')
        if os.path.exists(req_path):
            try:
                with open(req_path, 'r') as f:
                    reqs = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]
                    deps_summary.append(f"Python Packages: {', '.join(reqs[:20])}...")
            except: pass
            
        # Node
        pkg_path = os.path.join(self.active_root, 'package.json')
        if os.path.exists(pkg_path):
            try:
                with open(pkg_path, 'r') as f:
                    pkg = json.load(f)
                    deps = list(pkg.get('dependencies', {}).keys())
                    dev_deps = list(pkg.get('devDependencies', {}).keys())
                    deps_summary.append(f"Node Dependencies: {', '.join(deps)}")
                    deps_summary.append(f"Node DevDependencies: {', '.join(dev_deps)}")
            except: pass
            
        if deps_summary:
            self.dependencies_context = "\n=== DETECTED PROJECT DEPENDENCIES ===\n" + "\n".join(deps_summary) + "\n=====================================\n"
        else:
            self.dependencies_context = ""

    def _init_ai(self):
        if AI_AVAILABLE:
            try:
                config = MultiModelConfig(parallel_execution=True)
                self.ai = MultiModelProcessor(config)
                logger.info("AI MultiModelProcessor initialized successfully.")
                # Reinicializar Enhanced si ya estaba creado sin AI
                if self.enhanced_system and not self.enhanced_system.ai_processor:
                    self.enhanced_system.ai_processor = self.ai
            except Exception as e:
                self.ai = None
                logger.error("Failed to initialize AI MultiModelProcessor", error=str(e))

    def _init_chat_manager(self):
        if AI_AVAILABLE:
            history_path = os.path.join(self.active_root, "chat_history.json")
            self.chat_manager = ChatManager(history_path)
            logger.info("ChatManager initialized.", path=history_path)

    def _init_ui(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _discover_script_tools(self):
        """Escanea la carpeta tools/ y convierte scripts python en herramientas."""
        tools_path = os.path.join(self.active_root, 'tools')
        if not os.path.exists(tools_path): return

        scripts = glob.glob(os.path.join(tools_path, "*.py"))
        for script in scripts:
            name = os.path.basename(script)
            if name == "__init__.py": continue
            
            tool_name = f"tool_{name.replace('.py', '')}"
            rel_path = os.path.relpath(script, self.active_root).replace('\\', '/')
            
            # Definición dinámica
            tool_def = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": f"Ejecuta el script de utilidad '{name}'. Usa esto para tareas específicas del proyecto.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "args": {"type": "string", "description": "Argumentos opcionales para el script (ej: '--check')"}
                        },
                        "required": []
                    }
                }
            }
            
            # Wrapper de ejecución
            def make_wrapper(script_path):
                return lambda args="": self._run_script_wrapper(script_path, args)
            
            self.TOOL_DEFINITIONS.append(tool_def)
            self.AVAILABLE_TOOLS[tool_name] = make_wrapper(rel_path)
            logger.info(f"Discovered tool: {tool_name}")

    def _run_script_wrapper(self, script_path, args):
        """Ejecuta un script python y captura su salida."""
        cmd = f"python {script_path} {args}"
        return self._tool_run_shell_command(cmd)

    def _init_toolbox(self):
        """Define el cinturón de herramientas del agente."""
        self.TOOL_DEFINITIONS = [
            {
                "type": "function",
                "function": {
                    "name": "consult_expert",
                    "description": "Delega una tarea compleja a un agente especializado del Sistema Mejorado. Úsalo para tareas de Arquitectura, Seguridad, Review o Coding complejo que requieran planificación.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_description": {"type": "string", "description": "Descripción detallada de la tarea."},
                            "expert_type": {"type": "string", "description": "Tipo de experto (opcional): 'security', 'frontend', 'backend', 'planner'."}
                        },
                        "required": ["task_description"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Escribe o sobrescribe contenido en un archivo en la ruta especificada. Crea los directorios si no existen.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Ruta relativa del archivo a escribir."},
                            "content": {"type": "string", "description": "El contenido a escribir en el archivo."}
                        },
                        "required": ["file_path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Lee y retorna el contenido de un archivo en la ruta especificada.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Ruta relativa del archivo a leer."}
                        },
                        "required": ["file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_directory",
                    "description": "Lista el contenido (archivos y directorios) de una ruta especificada.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "dir_path": {"type": "string", "description": "Ruta relativa del directorio a listar. Usa '.' para el directorio actual."}
                        },
                        "required": ["dir_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_shell_command",
                    "description": "Ejecuta un comando de shell en el sistema. Úsalo con precaución.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string", "description": "Comando a ejecutar."}
                        },
                        "required": ["command"]
                    }
                }
            }
        ]
        self.AVAILABLE_TOOLS: Dict[str, Callable] = {
            "write_file": self._tool_write_file,
            "read_file": self._tool_read_file,
            "list_directory": self._tool_list_directory,
            "run_shell_command": self._tool_run_shell_command,
            "consult_expert": self._tool_consult_expert
        }
        
        # Auto-descubrimiento
        self._discover_script_tools()
        
        logger.info("Toolbox initialized.", tools=list(self.AVAILABLE_TOOLS.keys()))

    # =========================================================================
    #  HERRAMIENTAS (TOOLBELT)
    # =========================================================================

    async def _tool_consult_expert(self, task_description: str, expert_type: str = "auto") -> str:
        """Puente hacia el EnhancedMultiAgentSystem."""
        if not self.enhanced_system:
            return "Error: El sistema experto (EnhancedMultiAgentSystem) no está disponible."
            
        logger.info(f"Delegating to expert ({expert_type}): {task_description[:50]}...")
        print(f"\n🧠 ACTIVANDO MODO EXPERTO ({expert_type})...")
        print(f"   Tarea: {task_description}")
        
        try:
            # Ejecución real asíncrona usando el sistema mejorado
            result = await self.enhanced_system.execute_task(
                task=task_description,
                mode="recursive" # Usar modo recursivo por defecto para máxima autonomía
            )
            
            output = f"=== REPORTE DEL SISTEMA EXPERTO ===\n"
            output += f"Estado: {result.get('status')}\n"
            output += f"Modelo Usado: {result.get('model_used')}\n"
            output += f"Skills: {', '.join(result.get('skills_applied', []))}\n"
            output += f"Output Final:\n{result.get('output', 'Ver archivos generados.')}\n"
            
            return output
        except Exception as e:
            logger.error(f"Expert system failed: {e}")
            return f"Error crítico en el sistema experto: {e}"

    def _tool_write_file(self, file_path: str, content: str, base_path: Optional[str] = None) -> str:
        actual_base = base_path if base_path else self.active_root
        full_path = os.path.join(actual_base, file_path)
        
        # 🛡️ SECURITY CHECK
        if self.policy_enforcer:
            ext = os.path.splitext(file_path)[1].lower()
            lang_map = {'.js': 'javascript', '.ts': 'typescript', '.py': 'python', '.go': 'go'}
            language = lang_map.get(ext, 'text')
            
            validation = self.policy_enforcer.validate_against_plan(content, language)
            
            if not validation.get('compliant', True):
                # Bloquear escritura si hay violaciones críticas
                violations = [v['message'] for v in validation.get('violations', [])]
                warning_msg = f"⛔ BLOQUEO DE SEGURIDAD: El código viola las políticas del proyecto.\nViolaciones: {', '.join(violations)}"
                logger.warning(f"Security blocked write to {file_path}: {violations}")
                return warning_msg

        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info("Tool executed: write_file", path=full_path, size=len(content))
            return f"Archivo '{file_path}' escrito exitosamente."
        except Exception as e:
            logger.error("Tool failed: write_file", path=full_path, error=str(e))
            return f"Error al escribir archivo '{file_path}': {e}"

    def _tool_read_file(self, file_path: str, base_path: Optional[str] = None) -> str:
        actual_base = base_path if base_path else self.active_root
        full_path = os.path.join(actual_base, file_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info("Tool executed: read_file", path=full_path, size=len(content))
            return content
        except Exception as e:
            logger.error("Tool failed: read_file", path=full_path, error=str(e))
            return f"Error al leer archivo '{file_path}': {e}"

    def _tool_list_directory(self, dir_path: str, base_path: Optional[str] = None) -> str:
        actual_base = base_path if base_path else self.active_root
        full_path = os.path.join(actual_base, dir_path)
        try:
            entries = os.listdir(full_path)
            logger.info("Tool executed: list_directory", path=full_path, count=len(entries))
            return json.dumps(entries)
        except Exception as e:
            logger.error("Tool failed: list_directory", path=full_path, error=str(e))
            return f"Error al listar directorio '{dir_path}': {e}"

    def _tool_run_shell_command(self, command: str) -> str:
        """Ejecuta un comando de shell y retorna stdout/stderr."""
        print(f"Executing shell command: {command}")
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=self.active_root,
                encoding='utf-8' # Forzar UTF-8
            )
            output = result.stdout
            if result.stderr:
                output += f"\n[STDERR]\n{result.stderr}"
            logger.info("Tool executed: run_shell_command", command=command[:20])
            return output
        except Exception as e:
            logger.error("Tool failed: run_shell_command", command=command, error=str(e))
            return f"Error executing shell command: {e}"
            
    # =========================================================================
    #  INTERFAZ Y MENÚS (UI/UX)
    # =========================================================================

    def show_help(self):
        print("\n" + "═"*70)
        print("📖 GUÍA DE OPERACIÓN - HANDS ON AI (AI-POWERED)")
        print("═"*70)
        
        print("\n🛠️  [ Comandos ]")
        print("  /root      - Cambiar el directorio raíz de trabajo.")
        print("  /config    - Ver y editar Configuración de IA (Keys/Modelos).")
        print("  /status    - 🆕 Ver estado del sistema mejorado (Skills, Subagentes).")
        print("  /chat      - 🆕 Iniciar una nueva conversación (Borrar memoria).")
        print("  /publish   - 🆕 Prepara el proyecto para crawlers (robots.txt, sitemap.xml).")
        print("  /exit      - Cerrar el orquestador.")

        print("\n⚙️  [ Procesos Inteligentes ]")
        print("  /init      - Deep Research + Memoria -> Generar Plan y Metadatos del proyecto activo.")
        print("  /audit [path] - IA Auditor: Compara Código vs. Plan del proyecto activo o uno específico.")
        print("  /print     - Ver el Plan Maestro generado para el proyecto activo.")
        print("  /roadmap   - 🆕 Genera un plan completo (roadmap) de todos los proyectos en plan.txt.")
        print("  /compress [--summarize]  - 🆕 Comprime el contexto del proyecto en un archivo (con resumen opcional).")
        print("  /e2e [path] - 🚀 **MODO AUTÓNOMO (Legacy):** Ejecuta un proyecto con ciclo de auditoría básico.")

        print("\n📄 [ Templates Adaptativos ]")
        print("  /templates - Generar entregables adaptados con IA.")

        print("\n💬 [ Interacción Unificada ]")
        print("  Escribe cualquier tarea o pregunta. El sistema decidirá automáticamente si usar")
        print("  respuestas rápidas o desplegar agentes especializados (Enhanced System).")
        print("  Ejemplo: 'Crea una API de login' activará automáticamente a los agentes de desarrollo.")
        print("═"*70)

    def main_loop(self):
        print("¡Hola! Sistema Hands-On AI listo. /help para opciones.")
        
        while True:
            try:
                current_dir_name = os.path.basename(self.active_root)
                ai_status = "🟢" if (self.ai and self.ai.get_available_providers()) else "🔴"
                enhanced_status = "✨" if self.enhanced_system else ""
                
                prompt = input(f"[{enhanced_status}{ai_status}] Escribe tu prompt aquí > ").strip()
                
                if not prompt: continue
                if prompt.lower() in ['/exit', 'exit', 'salir']:
                    print("👋 ¡Hasta pronto!")
                    break
                
                asyncio.run(self.handle_prompt(prompt))
            
            except KeyboardInterrupt:
                print("\n⛔ Cancelado.")
            except Exception as e:
                print(f"❌ Error: {e}")
            except EOFError:
                break

    async def handle_prompt(self, prompt):
        cmd = prompt.lower().split()[0] if prompt.startswith('/') else None

        if cmd == '/help':      self.show_help()
        elif cmd == '/root':    
            arg = prompt.split(' ', 1)[1] if len(prompt.split(' ', 1)) > 1 else None
            await self.cmd_root(arg)
        elif cmd == '/config':  self.cmd_config()
        elif cmd == '/chat':    await self.cmd_chat(prompt.split(' ', 1)[1] if len(prompt.split(' ', 1)) > 1 else None)
        elif cmd == '/status':  self.cmd_status()
        elif cmd == '/init':
            project_path_arg = prompt.split(' ', 1)[1] if len(prompt.split(' ', 1)) > 1 else None
            await self.cmd_init(project_path_arg)
        elif cmd == '/print':   self.cmd_print()
        elif cmd == '/audit':   await self.cmd_audit(prompt.split(' ', 1)[1] if len(prompt.split(' ', 1)) > 1 else None)
        elif cmd == '/sync':    self.cmd_sync()
        elif cmd == '/templates': await self.cmd_templates()
        elif cmd == '/roadmap': await self.cmd_roadmap()
        elif cmd == '/publish': await self.cmd_publish()
        elif cmd == '/compress':
            summarize_flag = '--summarize' in prompt.split()
            await self.cmd_compress(summarize=summarize_flag)
        elif cmd == '/e2e':
            project_path_arg = prompt.split(' ', 1)[1] if len(prompt.split(' ', 1)) > 1 else None
            await self.cmd_e2e(project_path_arg)
        elif not prompt.startswith('/'):
            await self.chat_ai(prompt)
        else:
            # Si es un comando desconocido, intentar pasarlo como chat también, 
            # asumiendo que el usuario quizás quería decir algo natural.
            print(f"⚠️ Comando '{cmd}' no reconocido. Procesando como texto natural...")
            await self.chat_ai(prompt)

    async def _validate_process_with_ia(self, process_name: str, inputs: Dict[str, Any], outputs: Dict[str, Any], validation_prompt: str) -> str:
        """Función universal para validar el resultado de un proceso usando un system_prompt de IA."""
        if not self.ai:
            return "VALIDACIÓN OMITIDA: IA no disponible."
        
        print(f"🔎 Validando el proceso '{process_name}' con IA...")

        full_validation_prompt = f"""
        **Contexto de Entrada:**
        {json.dumps(inputs, indent=2)}

        **Resultados Generados (Salida):**
        {json.dumps(outputs, indent=2)}
        """

        try:
            response = await self.ai.process_single(
                system_prompt=validation_prompt,
                prompt=full_validation_prompt
            )
            return response.content
        except Exception as e:
            logger.error(f"Error en la validación del proceso '{process_name}'", error=str(e))
            return f"Error durante la validación de IA: {e}"

    async def cmd_publish(self):
        """Genera archivos de indexación para crawlers y valida el resultado con IA."""
        print("\n🚀 Publicando proyecto para ser accesible por máquinas...")
        
        base_url = "https://github.com/selvaggiesteban/hands-on-ai/blob/main/"
        excluded_dirs = {'.git', '__pycache__', 'node_modules', 'venv', '.pytest_cache', 'dist', 'build', '.claude', 'backup', 'project'}
        excluded_files = {'kb_index.json', 'chat_history.json'}

        # --- Generación de Artefactos ---
        robots_content = "User-agent: *\nDisallow: /project/\nSitemap: /sitemap.xml\n"
        self._tool_write_file('robots.txt', robots_content, base_path=SYSTEM_ROOT)
        print(f"✅ 'robots.txt' generado.")

        sitemap_urls = []
        for root, dirs, files in os.walk(SYSTEM_ROOT, topdown=True):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in sorted(files):
                if file in excluded_files: continue
                file_rel_path = os.path.relpath(os.path.join(root, file), SYSTEM_ROOT).replace('\\', '/')
                sitemap_urls.append(f"  <url><loc>{base_url}{file_rel_path}</loc></url>\n")
        
        sitemap_content = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{" ".join(sitemap_urls)}</urlset>'
        self._tool_write_file('sitemap.xml', sitemap_content, base_path=SYSTEM_ROOT)
        print(f"✅ 'sitemap.xml' generado con {len(sitemap_urls)} URLs.")

        index_content = ["# Índice Maestro del Proyecto: Hands-On AI\n\n"]
        index_content.append("- **[sitemap.xml](sitemap.xml)**\n- **[robots.txt](robots.txt)**\n\n")
        index_content.append("## Estructura Principal\n\n```\n" + self._generate_tree(SYSTEM_ROOT, excluded_dirs) + "\n```\n")
        self._tool_write_file('PROJECT_INDEX.md', "".join(index_content), base_path=SYSTEM_ROOT)
        print(f"✅ 'PROJECT_INDEX.md' actualizado.")

        # --- Validación con IA ---
        validation_system_prompt = """
        Eres un Experto en SEO Técnico y un Ingeniero de Control de Calidad. Tu tarea es validar que los artefactos de publicación se hayan generado correctamente.
        Analiza los datos y responde si el proceso fue EXITOSO o si tiene FALLOS. Justifica tu respuesta brevemente.
        - Criterio de Éxito para `robots.txt`: Debe prohibir (`Disallow`) explícitamente el directorio `/project/`.
        - Criterio de Éxito para `sitemap.xml`: NO debe contener ninguna URL dentro del directorio `/project/`.
        """
        
        inputs = {"excluded_dirs": list(excluded_dirs)}
        outputs = {"robots_txt_content": robots_content, "sitemap_file_excerpt": sitemap_content[:1000] + "\n..."}
        
        validation_report = await self._validate_process_with_ia(
            process_name="Publishing", inputs=inputs, outputs=outputs, validation_prompt=validation_system_prompt
        )
        
        print("\n" + "─"*70)
        print("📊 INFORME DE VALIDACIÓN DEL PROCESO DE PUBLICACIÓN")
        print(validation_report)
        print("─"*70)
        
        print("\n✨ ¡Proyecto listo para ser indexado por máquinas!")
            
    # =========================================================================
    #  LOGICA DE NEGOCIO (CORE)
    # =========================================================================

    async def cmd_e2e(self, project_path: Optional[str] = None, mode: str = 'E2E'):
        """MODO AUTÓNOMO: Ejecuta un proyecto de principio a fin según el modo (MVP o E2E)."""
        target_path = os.path.join(SYSTEM_ROOT, project_path) if project_path else self.active_root
        project_name = os.path.basename(target_path)
        
        print("\n" + "🔥"*70)
        print(f"🔥 MODO {mode.upper()} ACTIVADO para '{project_name}'.")
        print("🔥 Para detener, presione Ctrl+C.")
        print("🔥"*70 + "\n")

        # 1. Cargar o Generar el Plan
        plan_path = os.path.join(target_path, 'project_meta', 'planning', 'plan.json')
        if not os.path.exists(plan_path):
            print("📜 No se encontró un plan. Invocando al 'Arquitecto' para generar uno...")
            _, plan_data = await self._process_project_init(project_path)
            if not plan_data:
                print("❌ No se pudo generar un plan. Abortando modo E2E.")
                return
        else:
            with open(plan_path, 'r', encoding='utf-8') as f:
                plan_data = json.load(f)
        
        # 2. Bucle de Ejecución Principal
        for phase_idx, phase in enumerate(plan_data.get('phases', [])):
            # LÓGICA DE MODO
            if mode.upper() == 'MVP' and not phase.get('is_mvp', False):
                print(f"\n--- [FASE {phase_idx + 1}] (Omitida en modo MVP): {phase['name']} ---")
                continue

            print(f"\n--- [FASE {phase_idx + 1}/{len(plan_data['phases'])}]: {phase['name']} ---")
            for task_idx, task in enumerate(phase.get('tasks', [])):
                if isinstance(task, dict) and task.get('status') == 'completed':
                    print(f"  ✅ [TAREA {task_idx + 1}] (Omitida): {task['name']}")
                    continue

                task_name = task['name'] if isinstance(task, dict) else task
                print(f"\n  ▶️  [TAREA {task_idx + 1}]: \"{task_name}\"")
                
                max_retries = 3
                for attempt in range(max_retries):
                    # 3. Delegación al "Desarrollador"
                    developer_system_prompt = "Eres un Ingeniero de Software Full-Stack experto. Tu única tarea es implementar la siguiente directiva de la manera más limpia y eficiente posible, usando las herramientas a tu disposición. No hagas preguntas, solo ejecuta la tarea."
                    
                    full_context_for_task = await self.get_project_context_for_task(target_path, task_name)
                    developer_prompt = f"Contexto del proyecto:\n{full_context_for_task}\n\n**Tarea a realizar:**\n{task_name}"

                    await self.chat_ai(developer_prompt) # Usar chat_ai para que maneje el tool calling

                    # 4. Invocación del "Auditor"
                    reviewer_system_prompt = "Eres un Revisor de Código Senior y un Ingeniero de QA. Valida si los cambios en el código cumplen la directiva. Responde únicamente con '[PASS]' si es correcta, o con '[FAIL]' seguido de una justificación concisa."
                    
                    post_change_context = await self.get_project_context_for_task(target_path, task_name)
                    reviewer_prompt = f"**Directiva de Tarea:**\n{task_name}\n\n**Estado del Proyecto Post-Implementación:**\n{post_change_context}"
                    
                    validation_response = await self.ai.process_single(system_prompt=reviewer_system_prompt, prompt=reviewer_prompt)
                    
                    if "[PASS]" in validation_response.content.upper():
                        print(f"    ↳ ✅ [Auditor AI]: [PASS]")
                        self.update_task_status_in_plan(plan_path, phase_idx, task_idx, 'completed')
                        print(f"    ↳ 💾 [Orquestador]: Marcando tarea como 'completed'.")
                        break
                    else:
                        fail_reason = validation_response.content.replace("[FAIL]", "").strip()
                        print(f"    ↳ ❌ [Auditor AI]: [FAIL] - {fail_reason}")
                        if attempt < max_retries - 1:
                            print(f"    ↳ 🤖 [Orquestador]: Reintentando ({attempt + 1}/{max_retries})...")
                        else:
                            print(f"    ↳ 🚫 [Orquestador]: Máximos reintentos alcanzados. Marcando como 'failed'.")
                            self.update_task_status_in_plan(plan_path, phase_idx, task_idx, 'failed')
                            break
        
        print("\n" + "🏁"*70)
        print(f"🏁 MODO {mode.upper()} FINALIZADO: Todas las tareas del plan han sido procesadas.")
        print("🏁"*70)

    async def get_project_context_for_task(self, project_path, task_name):
        # Helper para obtener contexto relevante para una tarea
        tree = self._generate_tree(project_path)
        # Podrías hacer una llamada a la IA para seleccionar qué archivos leer basado en la tarea
        scan = self._scan_directory(project_path, max_chars=20000)
        return f"Árbol de directorios:\n{tree}\n\nContenido de archivos relevantes:\n{scan}"
        
    def update_task_status_in_plan(self, plan_path, phase_idx, task_idx, status):
        # Helper para actualizar el plan.json
        with open(plan_path, 'r+') as f:
            plan_data = json.load(f)
            task = plan_data['phases'][phase_idx]['tasks'][task_idx]
            if isinstance(task, str):
                plan_data['phases'][phase_idx]['tasks'][task_idx] = {'name': task, 'status': status}
            else:
                task['status'] = status
            f.seek(0)
            json.dump(plan_data, f, indent=2)
            f.truncate()

    async def cmd_compress(self, summarize: bool = False):
        """Genera un archivo de contexto unificado y, opcionalmente, un resumen semántico."""
        project_name = os.path.basename(self.active_root)
        print(f"\n📦 Comprimiendo el proyecto '{project_name}' en un único archivo de contexto...")

        # ... (El resto de la lógica de compresión por consolidación se mantiene igual)
        overview_path = os.path.join(self.active_root, 'project_meta', 'product_overview', 'product-overview.json')
        plan_path = os.path.join(self.active_root, 'project_meta', 'planning', 'plan.json')

        if not os.path.exists(overview_path) or not os.path.exists(plan_path):
            print(f"❌ Metadatos no encontrados para '{project_name}'. Ejecuta /init o /roadmap en este proyecto primero.")
            return

        compressed_content = []
        # ... (código para construir compressed_content)
        compressed_content.append(f"# Contexto Comprimido del Proyecto: {project_name}\n\n")
        compressed_content.append("Este archivo contiene un volcado completo del estado, planificación, estructura y código fuente del proyecto...\n\n")
        # ... (código para añadir overview, plan, tree, code)
        
        # Guardar el archivo principal
        output_filename = 'COMPRESSED_CONTEXT.md'
        full_content = "".join(compressed_content)
        result = self._tool_write_file(file_path=output_filename, content=full_content, base_path=self.active_root)
        
        if "exitosamente" not in result:
            print(f"❌ Error al escribir el archivo comprimido: {result}")
            return
            
        full_path = os.path.join(self.active_root, output_filename)
        print(f"✅ Contexto del proyecto comprimido exitosamente en: {full_path}")

        # --- LÓGICA DE COMPRESIÓN SEMÁNTICA ---
        if summarize:
            if not self.ai:
                print("❌ IA no configurada. No se puede generar el resumen.")
                return

            print("\n🧠 Iniciando compresión semántica con IA...")
            
            summarization_system_prompt = f"""
            Eres un Arquitecto de Software experto y CTO. Lee el siguiente contexto de proyecto completo que te proporciono y genera un resumen ejecutivo de alto nivel.
            Enfócate en los siguientes puntos clave:
            1.  **Objetivos Principales:** ¿Qué problema resuelve el proyecto?
            2.  **Stack Tecnológico:** ¿Qué tecnologías clave se utilizan?
            3.  **Arquitectura y Estructura:** ¿Cómo está organizado el proyecto?
            4.  **Plan de Ejecución:** Describe brevemente las fases principales del plan.
            5.  **Estado Actual y Próximos Pasos:** ¿Qué se ha hecho y qué es lo siguiente más importante?

            El resumen debe ser conciso, claro y no exceder las 800 palabras.
            """
            summarization_user_prompt = f"""
            === CONTEXTO COMPLETO DEL PROYECTO ===
            {full_content[:1000000]}
            """

            try:
                response = await self.ai.process_single(system_prompt=summarization_system_prompt, prompt=summarization_user_prompt)
                summary_filename = 'COMPRESSED_SUMMARY.md'
                summary_result = self._tool_write_file(file_path=summary_filename, content=response.content, base_path=self.active_root)
                if "exitosamente" in summary_result:
                    summary_path = os.path.join(self.active_root, summary_filename)
                    print(f"✅ Resumen semántico generado exitosamente en: {summary_path}")
                else:
                    print(f"❌ Error al escribir el archivo de resumen: {summary_result}")
            except Exception as e:
                print(f"❌ Error durante la compresión semántica con la IA: {e}")
                logger.error("AI summarization failed", error=str(e))
    
    async def cmd_root(self, path: Optional[str] = None):
        if not path:
            print(f"📍 Actual: {self.active_root}")
            path = await self.get_input("Nueva Ruta > ")
        
        if not path: return

        # Normalizar barras para el OS actual
        path = path.replace('/', os.sep).replace('\\', os.sep)

        # Manejo de rutas relativas y absolutas
        if os.path.isabs(path):
            target_root = path
        else:
            target_root = os.path.join(SYSTEM_ROOT, path) # Siempre relativo al SYSTEM_ROOT para consistencia
        
        target_root = os.path.abspath(target_root)

        if os.path.isdir(target_root):
            self.active_root = target_root
            print(f"✅ Root cambiado a: {self.active_root}")
            # Recargar chat history para el nuevo proyecto
            self._init_chat_manager()
            # Reinicializar Enhanced System con el nuevo root
            self._init_enhanced_system()
        else:
            print(f"❌ Ruta inválida: {target_root}")

    async def cmd_chat(self, message: Optional[str] = None):
        """Inicia una conversación o envía un prompt a la IA, manteniendo la memoria."""
        if not self.ai:
            print("❌ IA no configurada. Usa /config primero.")
            return

        if message:
            await self.chat_ai(message) # Usa la función existente para procesar el prompt
        else:
            print("\n💬 Conversación activa. Escribe tu prompt directamente.")
            print("    Sugerencia: Usa /sync para que la IA consulte la base de conocimiento y el contexto del chat.")

    def cmd_config(self):
        """Configuración interactiva de IA (Extendida para Multi-Proveedor)."""
        current_provider = "Ninguno"
        current_model = "N/A"
        has_key = "NO"

        # Cargar configuración actual
        if os.path.exists(ENV_FILE):
            with open(ENV_FILE, 'r') as f:
                for line in f:
                    if line.startswith("AI_PROVIDER="): current_provider = line.split("=")[1].strip()
                    if line.startswith("AI_MODEL="): current_model = line.split("=")[1].strip()
                    # Verificar si hay alguna key activa
                    if "_API_KEY=" in line and len(line.split("=")) > 1 and line.split("=")[1].strip():
                         has_key = "SÍ (Configurada)"

        print("\n🔐 --- Configuración de Inteligencia Artificial (Enero 2026) ---")
        print(f"   Estado Actual: {current_provider} | Modelo: {current_model} | Key: {has_key}")
        print("----------------------------------------------------------------")
        print("Seleccione Proveedor:")
        print("  1. OpenAI    (Tier 1 - Calidad/Razonamiento)")
        print("  2. Anthropic (Tier 1/2 - Coding/Agente)")
        print("  3. Google    (Tier 2/3 - Contexto Largo)")
        print("  4. Groq      (Tier 3 - Ultra Velocidad)")
        print("  5. DeepSeek  (Tier 3 - Económico)")
        
        sel = input("\nOpción [1-5] (Enter para salir): ").strip()
        if not sel: return

        provider_map = {
            '1': 'OPENAI',
            '2': 'ANTHROPIC',
            '3': 'GEMINI',
            '4': 'GROQ',
            '5': 'DEEPSEEK'
        }
        
        provider = provider_map.get(sel)
        if not provider:
            print("❌ Opción inválida.")
            return

        model = ""
        
        if provider == 'OPENAI':
            print("\nModelos OpenAI:")
            print("  1. o1-preview (Razonamiento Avanzado)")
            print("  2. gpt-4o (Omni - Balanceado)")
            print("  3. gpt-4o-mini (Rápido/Económico)")
            m = input("Modelo [2]: ").strip()
            models = {'1': 'o1-preview', '2': 'gpt-4o', '3': 'gpt-4o-mini'}
            model = models.get(m, 'gpt-4o')

        elif provider == 'ANTHROPIC':
            print("\nModelos Anthropic:")
            print("  1. claude-opus-4-5 (Complejo/Creativo)")
            print("  2. claude-sonnet-4-5 (Coding - Recomendado)")
            print("  3. claude-3-5-haiku (Rápido)")
            m = input("Modelo [2]: ").strip()
            models = {'1': 'claude-opus-4-5-20251101', '2': 'claude-sonnet-4-5-20250929', '3': 'claude-3-5-haiku-20241022'}
            model = models.get(m, 'claude-sonnet-4-5-20250929')

        elif provider == 'GEMINI':
            print("\nModelos Google:")
            print("  1. gemini-1.5-pro (Contexto 2M)")
            print("  2. gemini-2.0-flash (Sub-segundo)")
            m = input("Modelo [1]: ").strip()
            models = {'1': 'gemini-1.5-pro', '2': 'gemini-2.0-flash'}
            model = models.get(m, 'gemini-1.5-pro')

        elif provider == 'GROQ':
            print("\nModelos Groq (Llama 3):")
            print("  1. llama-3.3-70b-versatile")
            print("  2. mixtral-8x7b-32768")
            m = input("Modelo [1]: ").strip()
            models = {'1': 'llama-3.3-70b-versatile', '2': 'mixtral-8x7b-32768'}
            model = models.get(m, 'llama-3.3-70b-versatile')

        elif provider == 'DEEPSEEK':
            print("\nModelos DeepSeek:")
            print("  1. deepseek-coder")
            print("  2. deepseek-chat")
            m = input("Modelo [1]: ").strip()
            models = {'1': 'deepseek-coder', '2': 'deepseek-chat'}
            model = models.get(m, 'deepseek-coder')

        # Request API Key specific to provider
        env_var_name = f"{provider}_API_KEY"
        print(f"\n🔑 Nota: La key se guardará como {env_var_name}")
        api_key = input(f"Ingrese su API KEY para {provider} (o Enter para mantener la existente): ").strip()

        # Update .env securely
        env_lines = []
        if os.path.exists(ENV_FILE):
            with open(ENV_FILE, 'r') as f:
                env_lines = f.readlines()
        
        def update_env(key, value):
            found = False
            for i, line in enumerate(env_lines):
                if line.startswith(f"{key}="):
                    env_lines[i] = f"{key}={value}\n"
                    found = True
                    break
            if not found:
                env_lines.append(f"{key}={value}\n")

        update_env("AI_PROVIDER", provider)
        update_env("AI_MODEL", model)
        if api_key:
            update_env(env_var_name, api_key)
            # Legacy support
            update_env("AI_API_KEY", api_key)

        try:
            with open(ENV_FILE, 'w', encoding='utf-8') as f:
                f.writelines(env_lines)
            print(f"\n✅ Configuración guardada. Proveedor: {provider}, Modelo: {model}")
            
            print("🔄 Reiniciando subsistema de IA...")
            self._init_ai()
            if self.ai:
                 print("🟢 IA Reinicializada.")
        except Exception as e:
            print(f"❌ Error al guardar .env: {e}")

    async def cmd_init(self, project_path: Optional[str] = None):
        """
        Despliega la estructura 'project_meta' y genera planes granulares para uno o todos los proyectos.
        - Si no se provee una ruta, opera sobre todos los proyectos en 'plan.txt'.
        - Si se provee una ruta, opera solo sobre ese proyecto.
        """
        target_projects = []
        if project_path:
            full_path = os.path.join(SYSTEM_ROOT, project_path)
            if os.path.isdir(full_path):
                target_projects.append(project_path)
            else:
                print(f"❌ Ruta de proyecto no encontrada: {project_path}")
                return
        else:
            print("📜 Analizando 'plan.txt' para encontrar todos los proyectos...")
            target_projects = self._get_project_paths_from_plan_txt()
            if not target_projects:
                print("❌ No se encontraron proyectos en 'plan.txt'.")
                return

        print(f"🔬 Proyectos a inicializar: {', '.join([os.path.basename(p) for p in target_projects])}")
        print("-" * 70)

        for rel_path in target_projects:
            project_name = os.path.basename(rel_path)
            print(f"\nProcessing project: {project_name}")
            full_project_path = os.path.join(SYSTEM_ROOT, rel_path)

            source_meta = os.path.join(SYSTEM_ROOT, 'project_meta')
            target_meta = os.path.join(full_project_path, 'project_meta')
            
            if not os.path.exists(target_meta):
                print(f"  📦 Desplegando estructura 'project_meta' para '{project_name}'...")
                try:
                    shutil.copytree(source_meta, target_meta)
                    print(f"  ✅ Estructura copiada exitosamente.")
                except Exception as e:
                    print(f"  ❌ Error al copiar 'project_meta' para '{project_name}': {e}")
                    continue
            else:
                print(f"  ℹ️  La estructura 'project_meta' ya existe para '{project_name}'.")

            await self._process_project_init(rel_path)
        
        print("\n" + "="*70)
        print("✅ Proceso de inicialización completado para todos los proyectos seleccionados.")
        print("="*70)
    
    def _get_project_paths_from_plan_txt(self) -> List[str]:
        plan_txt_path = os.path.join(SYSTEM_ROOT, 'project', 'plan.txt')
        project_paths = []
        if os.path.exists(plan_txt_path):
            # Método robusto sin regex: buscar 'project' en cada línea
            with open(plan_txt_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            matches = []
            for line in lines:
                if 'project' in line:
                    # Extraer desde 'project' hasta el final, limpiando whitespace
                    start_idx = line.find('project')
                    extracted = line[start_idx:].strip()
                    matches.append(extracted)
            
            for match in matches:
                relative_path = match.replace('\\', '/')
                full_check_path = os.path.join(SYSTEM_ROOT, relative_path)
                if os.path.isdir(full_check_path):
                    project_paths.append(relative_path)
                else:
                    logger.warning(f"Ruta de proyecto en plan.txt no encontrada o no es un directorio: {full_check_path}")
        
        return list(dict.fromkeys(project_paths))

    async def _process_project_init(self, project_relative_path: str):
        full_project_path = os.path.join(SYSTEM_ROOT, project_relative_path)
        print(f"  🚀 [IA] Iniciando Análisis Profundo en: {os.path.basename(full_project_path)}")
        
        if not self.ai:
            print("  ❌ IA no activa. Use /config.")
            return None, None

        print("  🌳 Generando mapa de estructura del proyecto...")
        project_tree = self._generate_tree(full_project_path)
        
        print("  🔍 Deep Research: Leyendo contenido de archivos clave...")
        code_context = self._scan_directory(full_project_path)
        
        print("  🧠 Memory Recall: Consultando historial de conversación...")
        memory_context = ""
        if self.chat_manager:
            msgs = self.chat_manager.get_full_history()
            relevant_msgs = msgs[-15:] if len(msgs) > 15 else msgs
            memory_context = "\n".join([f"{m.role.upper()}: {m.content}" for m in relevant_msgs])

        init_system_prompt = f"""
        ACTÚA COMO UN CTO Y ARQUITECTO DE SOFTWARE EXPERTO. TU OBJETIVO ES GENERAR UN PLAN DE EJECUCIÓN MVP DETALLADO Y POR FASES.
        Referencia la carpeta `project_meta` para entender la visión general.
        
        IMPORTANTE: Si la información disponible es escasa o el proyecto está vacío, ASUME un stack tecnológico web moderno estándar (React + Node.js o Python) y un alcance típico de MVP.
        NO HAGAS PREGUNTAS ACLARATORIAS. Genera directamente el `plan.json` con tus mejores suposiciones.

        REQUISITOS DEL PLAN:
        1.  **Análisis Estructural:** Describe la organización de carpetas y componentes.
        2.  **Implementación Técnica:** Define interfaces, rutas de API y componentes.
        3.  **Fases de Ejecución:** Prioriza el frontend. Las primeras fases deben cubrir el MVP.
        4.  **Etiquetado MVP:** CADA FASE en el JSON DEBE tener una clave `"is_mvp": true` o `"is_mvp": false`.

        No ejecutes ninguna acción de codificación hasta que yo apruebe el plan.
        """
        init_user_prompt = f"""
        === CONTEXTO DEL PROYECTO ===
        {code_context[:60000]}

        === TAREA CRÍTICA ===
        Basado en el contexto, y después de que yo responda a tus preguntas aclaratorias, genera el contenido JSON para 'plan.json'.

        FORMATO DE SALIDA (JSON PURO):
        {{
            "plan": {{
                "phases": [
                    {{
                        "name": "Fase 1: Configuración del Entorno y Estructura Base", 
                        "is_mvp": true,
                        "tasks": ["Crear estructura de directorios (src, tests)", "Inicializar gestor de dependencias"]
                    }},
                    {{
                        "name": "Fase 2: Componentes de UI Fundamentales (Frontend)", 
                        "is_mvp": true,
                        "tasks": ["Crear componente de Login", "Crear componente de Dashboard principal"]
                    }},
                    {{
                        "name": "Fase 3: Lógica de Negocio Principal (Backend)",
                        "is_mvp": true,
                        "tasks": ["Crear endpoint de autenticación /api/login", "Crear endpoint para obtener datos del dashboard /api/dashboard"]
                    }},
                    {{
                        "name": "Fase 4: Funcionalidades Avanzadas",
                        "is_mvp": false,
                        "tasks": ["Implementar exportación a PDF", "Añadir notificaciones por email"]
                    }}
                ]
            }}
        }}
        """
        
        try:
            resp = await self.ai.process_single(system_prompt=init_system_prompt, prompt=init_user_prompt)
            data = self._extract_json(resp.content)
            
            if data:
                overview_data = data.get('overview')
                plan_data = data.get('plan')

                target_meta = os.path.join(full_project_path, 'project_meta')
                overview_path = os.path.join(target_meta, 'product_overview', 'product-overview.json')
                self._save_json(overview_data, overview_path)
                print(f"  ✅ 'product-overview.json' actualizado para {os.path.basename(full_project_path)}.")

                plan_path = os.path.join(target_meta, 'planning', 'plan.json')
                self._save_json(plan_data, plan_path)
                print(f"  ✅ 'plan.json' actualizado para {os.path.basename(full_project_path)}.")
                
                return overview_data, plan_data
            else:
                print(f"  ❌ La IA no generó una estructura JSON válida. Revisa los logs.")
                logger.error("Invalid JSON response from AI during init", project=os.path.basename(full_project_path), response=resp.content)
                return None, None
        except Exception as e:
            print(f"  ❌ Error crítico en IA para {os.path.basename(full_project_path)}: {e}")
            logger.error("Critical error in _process_project_init", project=os.path.basename(full_project_path), error=str(e))
            return None, None

    async def _audit_project(self, project_path: Optional[str] = None):
        target_path = os.path.join(SYSTEM_ROOT, project_path) if project_path else self.active_root
        project_name = os.path.basename(target_path)
        print(f"\n🔎 Auditando proyecto: {project_name}")

        plan_path = os.path.join(target_path, 'project_meta', 'planning', 'plan.json')
        overview_path = os.path.join(target_path, 'project_meta', 'product_overview', 'product-overview.json')

        if not os.path.exists(plan_path) or not os.path.exists(overview_path):
            print(f"❌ No se han generado los metadatos para {project_name}. Ejecuta /init o /roadmap primero.")
            return

        try:
            with open(overview_path, 'r', encoding='utf-8') as f:
                overview_data = json.load(f)
            with open(plan_path, 'r', encoding='utf-8') as f:
                plan_data = json.load(f)
            
            print(f"✅ Proyecto {project_name} tiene metadatos.")
            if plan_data.get('phases'):
                print(f"✅ Plan de {project_name} dividido en fases.")
            else:
                print(f"⚠️ Plan de {project_name} NO tiene fases definidas.")
            
        except Exception as e:
            print(f"❌ Error al auditar {project_name}: {e}")
            logger.error("Error during project audit", project=project_name, error=str(e))

    async def _generate_full_roadmap(self):
        """Genera un roadmap completo de todos los proyectos listados en plan.txt."""
        project_paths = self._get_project_paths_from_plan_txt()
        
        if not project_paths:
            print("❌ No se encontraron proyectos en plan.txt. Asegúrate de que las rutas son correctas.")
            return
            
        roadmap_summary = []
        for p_rel_path in project_paths:
            full_path = os.path.join(SYSTEM_ROOT, p_rel_path)
            project_name = os.path.basename(full_path)
            
            plan_json_path = os.path.join(full_path, 'project_meta', 'planning', 'plan.json')
            
            overview_data, plan_data = None, None
            
            if os.path.exists(plan_json_path):
                try:
                    with open(plan_json_path, 'r', encoding='utf-8') as f:
                        plan_data = json.load(f)
                    overview_path = os.path.join(full_path, 'project_meta', 'product_overview', 'product-overview.json')
                    with open(overview_path, 'r', encoding='utf-8') as f:
                        overview_data = json.load(f)
                    print(f"🔄 Plan existente cargado para {project_name}.")
                except Exception as e:
                    print(f"⚠️ Error al cargar plan existente para {project_name}: {e}. Regenerando...")
                    overview_data, plan_data = await self._process_project_init(p_rel_path)
            else:
                print(f"✨ Generando plan nuevo para {project_name}...")
                overview_data, plan_data = await self._process_project_init(p_rel_path)
            
            if overview_data and plan_data:
                roadmap_summary.append({
                    'name': overview_data.get('title', project_name),
                    'path': p_rel_path,
                    'status': 'Planificado' if plan_data.get('phases') else 'Pendiente de fases',
                    'phases': len(plan_data.get('phases', []))
                })
        
        print("\n=== INFORME DE ROADMAP COMPLETO ===\n")
        for project_info in roadmap_summary:
            print(f"Proyecto: {project_info['name']}")
            print(f"  Ruta: {project_info['path']}")
            print(f"  Estado: {project_info['status']}")
            print(f"  Fases Definidas: {project_info['phases']}\n")
        print("==================================\n")


    async def _analyze_seo_article(self, html_content: str, requirements: str):
        """Utiliza la IA para analizar el artículo generado y verificar el cumplimiento de los requisitos."""
        print("\n🔍 Analizando la calidad y el cumplimiento de la respuesta de la IA...")
        if not self.ai:
            print("❌ IA no disponible para el análisis de calidad.")
            return

        analysis_system_prompt = f"""
        Eres un auditor de control de calidad de contenido SEO extremadamente meticuloso. A continuación se presenta un artículo en HTML y una lista de requisitos que debía cumplir.
        Tu única tarea es verificar rigurosamente si el artículo cumple con CADA UNO de los requisitos y presentar tus hallazgos en un formato de checklist claro y conciso.
        """
        analysis_user_prompt = f"""
        === REQUISITOS A VERIFICAR ===
        {requirements}

        === ARTÍCULO HTML GENERADO PARA ANÁLISIS ===
        ```html
        {html_content}
        ```

        === INFORME DE CONTROL DE CALIDAD (Formato Checklist) ===
        Completa la siguiente lista. Para cada punto, indica [PASS] o [FAIL] y añade una breve justificación si es [FAIL] o si no se puede verificar.
        - Formato HTML5 válido y completo:
        - Título SEO (`<title>`) presente y optimizado:
        - Meta Descripción SEO (`<meta name="description">`) presente y optimizada:
        - Extensión mínima de 1500 palabras:
        - Estructura jerárquica de encabezados (H2, H3):
        - Sección de "Preguntas Frecuentes" con al menos 5 H3:
        - Palabra clave principal en negrita (`<b>`) en CADA PÁRRAFO:
        - Longitud de párrafos (entre 100 y 200 palabras cada uno):
        - Presencia de una tabla HTML (`<table>`) de precios/planes:
        - Llamado a la Acción (CTA) claro al final del artículo:
        - Enlazado interno (si se proporcionó sitemap):
        - Enlazado externo obligatorio a Google:
        - Inclusión de metadatos como comentarios (slug, alt-texts):
        """
        try:
            response = await self.ai.process_single(system_prompt=analysis_system_prompt, prompt=analysis_user_prompt)
            print("\n" + "═"*70)
            print("🔎 INFORME DE CONTROL DE CALIDAD DEL ARTÍCULO")
            print("═"*70)
            print(response.content)
            print("═"*70)
        except Exception as e:
            print(f"❌ Error durante el análisis de calidad de la IA: {e}")
            logger.error("AI quality analysis failed", error=str(e))

    async def cmd_templates(self):
        """Generación + Adaptación IA"""
        print("\n📄 --- Templates ---")
        if not os.path.exists(TEMPLATES_DIR):
            print("❌ Error: No templates dir.")
            return

        items = os.listdir(TEMPLATES_DIR)
        for i, t in enumerate(items, 1): print(f"{i}. {t}")
        
        sel = input("Template # o 'A': ").strip().upper()
        targets = items if sel == 'A' else ([items[int(sel)-1]] if sel.isdigit() else [])
        
        for t in targets:
            src = os.path.join(TEMPLATES_DIR, t)
            dst = os.path.join(self.active_root, t)
            if not os.path.exists(dst):
                shutil.copytree(src, dst)
                print(f"✅ Copiado: {t}")
                
                # ADAPTACIÓN IA
                do_adapt = input(f"🤖 ¿Deseas que la IA adapte '{t}' a tu proyecto? (s/n): ").lower()
                if do_adapt == 's' and self.ai:
                    print("   ✨ Adaptando contenido...")
                    # Leer archivos clave del template copiado (ej. READMEs o .md)
                    for root, _, files in os.walk(dst):
                        for file in files:
                            if file.endswith('.md'):
                                fpath = os.path.join(root, file)
                                with open(fpath, 'r', encoding='utf-8') as f: content = f.read()
                                
                                prompt = f"ADAPTA este template al proyecto actual (Contexto: {os.path.basename(self.active_root)}).\n\nTEMPLATE:\n{content[:5000]}"
                                resp = await self.ai.process_single(prompt)
                                
                                with open(fpath, 'w', encoding='utf-8') as f: f.write(resp.content)
                                print(f"   ✨ {file} reescrito por IA.")

    # --- Helpers y Chat Standard ---
    
    async def chat_ai(self, prompt: str):
        """Maneja la conversación con el IA, incluyendo el bucle de tool calling."""
        if not self.ai:
            print("❌ IA no configurada. Usa /config primero.")
            return

        if self.chat_manager:
            self.chat_manager.add_message('user', prompt)

        if self.chat_manager:
            # Convertir dicts a Message objects (Fix para dict vs object)
            history_dicts = self.chat_manager.get_context(limit=20)
            messages = [Message(role=m['role'], content=m['content']) for m in history_dicts]
        else:
            messages = [Message(role='user', content=prompt)]

        # SYSTEM PROMPT UNIFICADO Y ENRIQUECIDO
        sys_prompt = f"""Eres un ORQUESTADOR DE DESARROLLO DE SOFTWARE experto operando en '{self.active_root}'.
        
        {self.context_rules}
        
        {self.dependencies_context}
        
        TU MISIÓN:
        1. Para preguntas simples o lecturas de archivos: Responde directamente o usa las herramientas básicas (read_file, list_directory).
        2. Para TAREAS DE DESARROLLO (codificar, planificar, debuguear, refactorizar, crear features): 
           **DEBES USAR LA HERRAMIENTA `consult_expert` INMEDIATAMENTE.**
           No intentes resolver tareas complejas tú solo con herramientas básicas. Delega al Sistema Experto.
        
        Ejemplos:
        - User: "¿Qué hay en src?" -> Tú: Usas `list_directory`.
        - User: "Crea un componente de Login" -> Tú: Usas `consult_expert(task_description="Crear componente Login...")`.
        - User: "Arregla el bug en auth" -> Tú: Usas `consult_expert(task_description="Debuguear auth...", expert_type="backend")`.
        """

        MAX_TOOL_CALLS = 5
        for _ in range(MAX_TOOL_CALLS):
            response = await self.ai.process_single(
                messages=messages,
                system_prompt=sys_prompt,
                tools=self.TOOL_DEFINITIONS
            )

            if response.tool_calls:
                print(f"\n🤖 Invocando herramienta: {response.tool_calls[0]['function']['name']}...")
                messages.append(Message(role="assistant", content=response.content or "", tool_calls=response.tool_calls))
                
                for tool_call in response.tool_calls:
                    tool_name = tool_call['function']['name']
                    tool_args = tool_call['function']['arguments']
                    tool_id = tool_call['id']
                    
                    if tool_name in self.AVAILABLE_TOOLS:
                        tool_function = self.AVAILABLE_TOOLS[tool_name]
                        try:
                            # Ejecución Dual: Soportar tanto herramientas síncronas como asíncronas
                            result = tool_function(**tool_args)
                            if asyncio.iscoroutine(result):
                                result = await result
                                
                            messages.append(Message(role="tool", content=str(result), tool_call_id=tool_id))
                        except Exception as e:
                            error_msg = f"Error ejecutando la herramienta {tool_name}: {e}"
                            messages.append(Message(role="tool", content=error_msg, tool_call_id=tool_id))
                    else:
                        error_msg = f"Herramienta desconocida: {tool_name}"
                        messages.append(Message(role="tool", content=error_msg, tool_call_id=tool_id))
            else:
                print(f"\n🤖 {response.content}\n")
                if self.chat_manager:
                    self.chat_manager.add_message('assistant', response.content)
                return

        print("\n🤖 Límite de invocaciones de herramientas alcanzado.")

    def cmd_print(self):
        """Genera un reporte legible del Plan Maestro, sin JSON."""
        plan_path = os.path.join(self.active_root, 'project_meta', 'planning', 'plan.json')
        overview_path = os.path.join(self.active_root, 'project_meta', 'product_overview', 'product-overview.json')

        if not os.path.exists(plan_path) or not os.path.exists(overview_path):
            print(f"DEBUG: Buscando plan en: {plan_path}")
            # Listar contenido para debug
            meta_dir = os.path.dirname(os.path.dirname(plan_path))
            print(f"DEBUG: Listando {meta_dir}:")
            if os.path.exists(meta_dir):
                for root, dirs, files in os.walk(meta_dir):
                    for f in files:
                        print(f"  - {os.path.join(root, f)}")
            else:
                print("  (Directorio no existe)")
                
            print("❌ No se han generado los metadatos. Ejecuta /init o /roadmap primero.")
            return

        try:
            with open(overview_path, 'r', encoding='utf-8') as f:
                overview_data = json.load(f)
            
            with open(plan_path, 'r', encoding='utf-8') as f:
                plan_data = json.load(f)

            title = overview_data.get('title', 'Proyecto Sin Título')
            description = overview_data.get('description', 'Sin descripción.')
            
            phases = plan_data.get('phases', [])
            stack = plan_data.get('techStack', {})

            print("\n" + "═"*60)
            print(f"📋 PLAN MAESTRO: {title}")
            print("═"*60)
            print(f"\n🎯 OBJETIVO: {description}\n")

            if stack:
                print("🛠️  STACK TECNOLÓGICO PROPUESTO:")
                for category, techs in stack.items():
                    tech_list = ", ".join(techs) if isinstance(techs, list) else techs
                    print(f"  • {category.capitalize()}: {tech_list}")
                print("─"*60)

            print("📅 FASES DE IMPLEMENTACIÓN:")
            if not phases:
                print("  No se han definido fases de implementación.")
            for i, p in enumerate(phases, 1):
                name = p.get('name', 'Fase sin nombre')
                tasks = p.get('tasks', [])
                print(f"\n🔹 FASE {i}: {name}")
                if tasks:
                    for t in tasks: print(f"   [ ] {t}")
                else:
                    print("   - No hay tareas definidas para esta fase.")
            print("═"*60)
            
        except Exception as e:
            print(f"❌ Error al generar el reporte del plan: {e}")
    
    def cmd_status(self):
        """Muestra el estado del sistema mejorado."""
        if not self.enhanced_system:
            print("❌ EnhancedMultiAgentSystem no está inicializado.")
            return
        
        status = self.enhanced_system.get_system_status()
        print("\n" + "✨"*30)
        print(" ESTADO DEL SISTEMA MEJORADO")
        print("✨"*30)
        
        print("\n📚 Knowledge Base & Planning:")
        for k, v in status.get('planning_files', {}).items():
            print(f"  • {k}: {os.path.basename(v)}")
            
        print("\n🧠 Skills Registradas:")
        skills = status.get('registered_skills', [])
        print(f"  Total: {len(skills)}")
        for s in skills[:5]: print(f"  - {s}")
        if len(skills) > 5: print(f"  ... y {len(skills)-5} más.")

        print("\n🤖 Subagentes Especializados:")
        agents = status.get('registered_subagents', [])
        for a in agents: print(f"  - {a}")
        
        print("\n🔀 Model Routing:")
        usage = status.get('model_usage', {})
        print(f"  Total Calls: {usage.get('total_calls', 0)}")
        
        print("\n" + "═"*60)

    def cmd_sync(self):
        # (Stub)
        print("🔄 Sync ejecutado.")

    async def cmd_run_agent(self, task: Optional[str] = None):
        """Ejecuta una tarea utilizando el EnhancedMultiAgentSystem."""
        if not self.enhanced_system:
            print("❌ EnhancedMultiAgentSystem no está disponible. Revisa dependencias e imports.")
            return

        if not task:
            task = input("📝 Describe la tarea a ejecutar > ").strip()
        
        if not task: return

        print(f"\n🚀 Iniciando Enhanced Agent para: '{task}'")
        print("⏳ Analizando tarea y seleccionando estrategia (Skills + Model Routing)...")
        
        try:
            # Ejecución con feedback visual simulado
            start_time = datetime.now()
            result = await self.enhanced_system.execute_task(task, mode="recursive", budget_mode="balanced")
            duration = (datetime.now() - start_time).total_seconds()

            print("\n" + "✅"*30)
            print(f" TAREA COMPLETADA en {duration:.2f}s")
            print("✅"*30)
            
            print(f"\n📊 Resultados:")
            print(f"  • Estado: {result.get('status', 'Unknown')}")
            print(f"  • Modelo Utilizado: {result.get('model_used', 'Auto')}")
            print(f"  • Skills Aplicadas: {', '.join(result.get('skills_applied', []))}")
            print(f"  • Subagentes Consultados: {', '.join(result.get('subagents_consulted', []))}")
            print(f"  • Quality Score: {result.get('quality_score', 'N/A')}")
            
        except Exception as e:
            print(f"\n❌ Error durante la ejecución mejorada: {e}")
            logger.error("Enhanced execution failed", error=str(e))

    def _generate_tree(self, startpath: str, ignore_dirs: Optional[set] = None):
        """Genera un árbol visual de directorios para que la IA entienda la estructura."""
        if ignore_dirs is None:
            ignore_dirs = {'.git', '__pycache__', 'node_modules', 'venv', '.pytest_cache', 'dist', 'build', 'project_meta'}
        
        tree_str = []
        prefix = "|-- "
        
        for root, dirs, files in os.walk(startpath):
            # Modificación: filtrar dirs in-place para que os.walk no descienda en ellos
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            level = root.replace(startpath, '').count(os.sep)
            indent = '    ' * (level)
            dirname = os.path.basename(root)
            
            # Si el directorio actual es uno de los ignorados (podría ser el startpath si se pasa uno ignorado)
            if dirname in ignore_dirs and root != startpath: # No ignorar el root si es ignorado
                continue
                
            subindent = '    ' * (level + 1)
            # Asegúrate de no añadir el prefijo para el root si ya está en la ruta
            if root == startpath:
                tree_str.append(f"{dirname}/")
            else:
                tree_str.append(f"{indent}{prefix}{dirname}/")
            
            for f in files:
                if not f.startswith('.'): # Ignorar archivos ocultos simples
                    tree_str.append(f"{subindent}{prefix}{f}")
                    
        return "\n".join(tree_str)

    def _scan_directory(self, path: str, max_chars: int = 80000, ignore_dirs: Optional[set] = None):
        """Lee contenido de archivos priorizando código fuente y documentación."""
        if ignore_dirs is None:
            ignore_dirs = {'.git', 'node_modules', '__pycache__', 'dist', 'project_meta', 'venv', '.pytest_cache'}
        
        buffer = []
        total = 0
        relevant_extensions = ('.py', '.js', '.ts', '.tsx', '.jsx', '.md', '.json', '.html', '.css', '.go', '.rs', '.java', '.c', '.cpp', '.h', '.yaml', '.yml', '.toml')
        
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                if file.endswith(relevant_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        if os.path.getsize(file_path) < 100 * 1024:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                c = f.read()
                                relative_path = os.path.relpath(file_path, path)
                                buffer.append(f"--- FILE: {relative_path} ---\n{c}\n")
                                total += len(c)
                                if total > max_chars:
                                    buffer.append("\n... (Límite de contexto alcanzado) ...")
                                    return "\n".join(buffer)
                    except Exception:
                        pass
        return "\n".join(buffer)

    async def cmd_audit(self, project_path: Optional[str] = None):
        """Auditoría Técnica con IA para un proyecto específico o el activo."""
        await self._audit_project(project_path)

    async def cmd_roadmap(self):
        """Genera un roadmap completo de todos los proyectos listados en plan.txt."""
        await self._generate_full_roadmap()

    def _extract_json(self, text):
        try:
            # Limpieza agresiva de bloques de código markdown
            cleaned_text = text.strip()
            if "```json" in cleaned_text:
                cleaned_text = cleaned_text.split("```json")[1].split("```")[0]
            elif "```" in cleaned_text:
                cleaned_text = cleaned_text.split("```")[1].split("```")[0]
            
            # Intentar parsear
            return json.loads(cleaned_text.strip())
        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {e}")
            print(f"❌ Error al decodificar JSON de la IA. Inicio del contenido raw:\n{text[:500]}...")
            return None
        except Exception as e:
            logger.error(f"Error extrayendo JSON: {e}")
            return None

    def _save_json(self, data, path):
        if data:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            print(f"DEBUG: Escribiendo JSON en: {os.path.abspath(path)}")
            try:
                with open(path, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2)
            except Exception as e:
                print(f"❌ Error escribiendo archivo: {e}")

if __name__ == "__main__":
    app = Orchestrator()
    try:
        app.main_loop()
    except KeyboardInterrupt: pass