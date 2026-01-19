# Orchestrator Principal - Hands On AI (Full Authority System)
# Sistema de control centralizado con acceso total al disco local (Windows 10).
# Integra Comandos, Procesos, Automatizaciones y Templates con UI/UX optimizada.

import os
import sys
import json
import shutil
import asyncio
import subprocess
import glob
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable

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


class Orchestrator:
    def __init__(self):
        self.active_root = SYSTEM_ROOT
        self.ai = None
        self.chat_manager = None
        self._init_ai()
        self._init_ui()
        self._init_chat_manager()
        self._init_toolbox()

    def _init_ai(self):
        if AI_AVAILABLE:
            try:
                config = MultiModelConfig(parallel_execution=True)
                self.ai = MultiModelProcessor(config)
                logger.info("AI MultiModelProcessor initialized successfully.")
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

    def _init_toolbox(self):
        """Define el cinturón de herramientas del agente."""
        self.TOOL_DEFINITIONS = [
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
            }
        ]
        self.AVAILABLE_TOOLS: Dict[str, Callable] = {
            "write_file": self._tool_write_file,
            "read_file": self._tool_read_file,
            "list_directory": self._tool_list_directory
        }
        logger.info("Toolbox initialized.", tools=list(self.AVAILABLE_TOOLS.keys()))

    # =========================================================================
    #  HERRAMIENTAS (TOOLBELT)
    # =========================================================================

    def _tool_write_file(self, file_path: str, content: str) -> str:
        full_path = os.path.join(self.active_root, file_path)
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info("Tool executed: write_file", path=full_path, size=len(content))
            return f"Archivo '{file_path}' escrito exitosamente."
        except Exception as e:
            logger.error("Tool failed: write_file", path=full_path, error=str(e))
            return f"Error al escribir archivo '{file_path}': {e}"

    def _tool_read_file(self, file_path: str) -> str:
        full_path = os.path.join(self.active_root, file_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info("Tool executed: read_file", path=full_path, size=len(content))
            return content
        except Exception as e:
            logger.error("Tool failed: read_file", path=full_path, error=str(e))
            return f"Error al leer archivo '{file_path}': {e}"

    def _tool_list_directory(self, dir_path: str) -> str:
        full_path = os.path.join(self.active_root, dir_path)
        try:
            entries = os.listdir(full_path)
            logger.info("Tool executed: list_directory", path=full_path, count=len(entries))
            return json.dumps(entries)
        except Exception as e:
            logger.error("Tool failed: list_directory", path=full_path, error=str(e))
            return f"Error al listar directorio '{dir_path}': {e}"
            
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
        print("  /chat      - 🆕 Iniciar una nueva conversación (Borrar memoria).")
        print("  /exit      - Cerrar el orquestador.")

        print("\n⚙️  [ Procesos Inteligentes ]")
        print("  /init      - Deep Research + Memoria -> Generar Plan y Metadatos.")
        print("  /audit     - IA Auditor: Compara Código vs. Plan.")
        print("  /print     - Ver el Plan Maestro generado.")

        print("\n📄 [ Templates Adaptativos ]")
        print("  /templates - Generar entregables adaptados con IA.")

        print("\n⚡ [ Automatizaciones ]")
        print("  /sync      - Sincronizar Knowledge Base.")
        print("  /run       - Ejecutar Agentes.")

        print("\n💬 [ Chat con Contexto ]")
        print("  Escribe directamente para chatear. Usa /chat para reiniciar.")
        print("═"*70)

    def main_loop(self):
        print("¡Hola! Sistema Hands-On AI listo. /help para opciones.")
        
        while True:
            try:
                current_dir_name = os.path.basename(self.active_root)
                ai_status = "🟢" if (self.ai and self.ai.get_available_providers()) else "🔴"
                
                prompt = input(f"\n📂 ({current_dir_name}) {ai_status} > ").strip()
                
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
        elif cmd == '/root':    self.cmd_root()
        elif cmd == '/config':  self.cmd_config()
        elif cmd == '/chat':    self.cmd_new_chat()
        elif cmd == '/init':    await self.cmd_init()
        elif cmd == '/print':   self.cmd_print()
        elif cmd == '/audit':   await self.cmd_audit()
        elif cmd == '/sync':    self.cmd_sync()
        elif cmd == '/run':     self.cmd_run_agent()
        elif cmd == '/templates': await self.cmd_templates()
        elif not prompt.startswith('/'):
            await self.chat_ai(prompt)
        else:
            print(f"⚠️ Comando '{cmd}' no reconocido.")

    # =========================================================================
    #  LOGICA DE NEGOCIO (CORE)
    # =========================================================================

    def cmd_root(self):
        print(f"\n📍 Actual: {self.active_root}")
        path = input("Nueva Ruta > ").strip().strip('"').strip("'")
        if os.path.exists(path) and os.path.isdir(path):
            self.active_root = os.path.abspath(path)
            print(f"✅ Root cambiado a: {self.active_root}")
            self._init_chat_manager() # Recargar memoria del nuevo contexto
        else:
            print("❌ Ruta inválida.")

    def cmd_new_chat(self):
        """Reinicia la memoria de conversación."""
        if self.chat_manager:
            self.chat_manager.clear_history()
            print("\n🧹 Memoria de conversación borrada. Iniciando nuevo chat.")
        else:
            print("⚠️ Chat Manager no inicializado.")

    def cmd_config(self):
        """Configuración interactiva de IA."""
        # Cargar configuración actual para mostrarla
        current_provider = "Ninguno"
        current_model = "N/A"
        has_key = "NO"

        if os.path.exists(ENV_FILE):
            with open(ENV_FILE, 'r') as f:
                for line in f:
                    if line.startswith("AI_PROVIDER="): current_provider = line.split("=")[1].strip()
                    if line.startswith("AI_MODEL="): current_model = line.split("=")[1].strip()
                    if line.startswith("AI_API_KEY="): 
                        key = line.split("=")[1].strip()
                        if key: has_key = "SÍ (***)"

        print("\n🔐 --- Configuración de Inteligencia Artificial (Enero 2026) ---")
        print(f"   Estado Actual: {current_provider} | Modelo: {current_model} | Key Configurada: {has_key}")
        print("----------------------------------------------------------------")
        print("Seleccione NUEVO proveedor principal:")
        print("1. OpenAI")
        print("2. Anthropic")
        print("3. Google Gemini")
        
        sel = input("\nOpción [1-3] (Enter para mantener actual y salir): ").strip()
        if not sel: 
            print("✅ Configuración mantenida.")
            return

        provider = ""
        model = ""
        
        if sel == '1':
            provider = "OPENAI"
            print("\nModelos OpenAI:")
            print("  1. o1 (Full Reasoning)")
            print("  2. o1-mini")
            print("  3. gpt-4o (Omni Stable)")
            print("  4. gpt-4o-mini")
            print("  5. Otro (Ingresar ID manual)")
            m = input("Modelo [1-5]: ").strip()
            model_map = {'1': 'o1', '2': 'o1-mini', '3': 'gpt-4o', '4': 'gpt-4o-mini'}
            if m == '5': model = input("ID del modelo: ").strip()
            else: model = model_map.get(m, 'o1')
            
        elif sel == '2':
            provider = "ANTHROPIC"
            print("\nModelos Anthropic:")
            print("  1. claude-opus-4-5-20251101")
            print("  2. claude-sonnet-4-5-20250929")
            print("  3. claude-haiku-4-5-20251001")
            print("  4. claude-3-5-sonnet-latest")
            print("  5. Otro (Ingresar ID manual)")
            m = input("Modelo [1-5]: ").strip()
            model_map = {
                '1': 'claude-opus-4-5-20251101', 
                '2': 'claude-sonnet-4-5-20250929', 
                '3': 'claude-haiku-4-5-20251001', 
                '4': 'claude-3-5-sonnet-latest'
            }
            if m == '5': model = input("ID del modelo: ").strip()
            else: model = model_map.get(m, 'claude-sonnet-4-5-20250929')
            
        elif sel == '3':
            provider = "GEMINI"
            print("\n🔍 Consultando modelos disponibles en Google AI...")
            # Intentar listar modelos reales si hay key
            temp_key = input(" (Opcional) Ingrese API KEY temporal para ver lista, o Enter para saltar: ").strip()
            
            real_models = []
            if temp_key and AI_AVAILABLE:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=temp_key)
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            real_models.append(m.name.replace('models/', ''))
                except: pass

            if real_models:
                print("\n✅ Modelos Disponibles para tu cuenta:")
                for i, rm in enumerate(real_models, 1):
                    print(f"  {i}. {rm}")
                m = input(f"Modelo [1-{len(real_models)}]: ").strip()
                if m.isdigit() and 1 <= int(m) <= len(real_models):
                    model = real_models[int(m)-1]
                else:
                    model = "gemini-1.5-flash"
            else:
                print("\nModelos Google (Estándar):")
                print("  1. gemini-1.5-pro (Recomendado)")
                print("  2. gemini-1.5-flash (Rápido)")
                print("  3. gemini-1.0-pro")
                print("  4. Otro (Manual)")
                m = input("Modelo [2]: ").strip()
                model_map = {'1': 'gemini-1.5-pro', '2': 'gemini-1.5-flash', '3': 'gemini-1.0-pro'}
                if m == '4': model = input("ID del modelo: ").strip()
                else: model = model_map.get(m, 'gemini-1.5-flash')
        
        else:
            print("❌ Selección inválida.")
            return

        api_key = input(f"\n🔑 Ingrese su API KEY para {provider}: ").strip()
        if not api_key:
            print("❌ API Key vacía. Cancelado.")
            return

        # Guardar en .env
        try:
            with open(ENV_FILE, 'w', encoding='utf-8') as f:
                f.write(f"AI_PROVIDER={provider}\n")
                f.write(f"AI_MODEL={model}\n")
                f.write(f"AI_API_KEY={api_key}\n")
            
            print(f"\n✅ Configuración guardada en {ENV_FILE}")
            print(f"   Proveedor: {provider}")
            print(f"   Modelo: {model}")
            
            # Recargar IA
            print("🔄 Reiniciando motor de IA...")
            self._init_ai()
            if self.ai and self.ai.get_available_providers():
                print("🟢 IA Conectada y Lista.")
            else:
                print("🔴 IA Configurada pero NO Conectada (Revise Key o Dependencias).")
                
        except Exception as e:
            print(f"❌ Error guardando configuración: {e}")

    async def cmd_init(self):
        """
        PROCESO CENTRAL DE INTELIGENCIA
        1. Deep Research (Escaneo de archivos)
        2. Context Memory (Historial de Chat)
        3. Strategic Planning (Generación de JSONs)
        """
        print(f"\n🚀 [IA] Iniciando Análisis Profundo en: {self.active_root}")
        
        if not self.ai:
            print("❌ IA no activa. Use /config.")
            return

        # 1. Scaffolding Base
        target_meta = os.path.join(self.active_root, 'project_meta')
        if not os.path.exists(target_meta):
            print("📦 Desplegando estructura base...")
            try:
                shutil.copytree(os.path.join(SYSTEM_ROOT, 'project_meta'), target_meta)
            except: pass

        # 2. Recolección de Datos (Research + Memory)
        print("🔍 Deep Research: Leyendo código fuente...")
        code_context = self._scan_directory(self.active_root)
        
        print("🧠 Memory Recall: Consultando historial de conversación...")
        memory_context = ""
        if self.chat_manager:
            msgs = self.chat_manager.get_full_history()
            # Tomar los últimos 10 turnos relevantes
            relevant_msgs = msgs[-10:] if len(msgs) > 10 else msgs
            memory_context = "\n".join([f"{m.role.upper()}: {m.content}" for m in relevant_msgs])

        # 3. Prompt de Ingeniería
        print("🤖 Razonando Estrategia (Code + Context)...")
        prompt = f"""
        ACTÚA COMO UN CTO Y ARQUITECTO DE SOFTWARE PRINCIPAL.
        
        CONTEXTO DEL CÓDIGO FUENTE (ESTADO ACTUAL):
        {code_context[:40000]}
        
        CONTEXTO DE LA CONVERSACIÓN CON EL USUARIO (PREFERENCIAS Y OBJETIVOS):
        {memory_context}
        
        TAREA:
        Actualiza los metadatos del proyecto ('product-overview' y 'plan') reflejando la realidad del código 
        PERO alineada con los deseos expresados por el usuario en el chat.
        
        Si el usuario pidió algo (ej: "Usar Python") y no está en el código, agrégalo como Tarea Pendiente en el Plan.

        FORMATO JSON ÚNICO:
        {{
            "overview": {{ "title": "...", "description": "...", "goals": [] }},
            "plan": {{
                "techStack": {{ "languages": [], "frameworks": [] }},
                "phases": [
                    {{ "name": "Fase 1: Análisis", "tasks": ["..."] }},
                    {{ "name": "Fase 2: Implementación", "tasks": ["..."] }}
                ]
            }}
        }}
        """
        
        try:
            resp = await self.ai.process_single(prompt)
            data = self._extract_json(resp.content)
            
            if data:
                self._save_json(data.get('overview'), os.path.join(target_meta, 'product_overview', 'product-overview.json'))
                self._save_json(data.get('plan'), os.path.join(target_meta, 'planning', 'plan.json'))
                print("✅ [IA] Estrategia Actualizada y Sincronizada.")
                self.cmd_print()
            else:
                print("❌ La IA no generó una estructura válida.")
        except Exception as e:
            print(f"❌ Error crítico en IA: {e}")

    async def cmd_audit(self):
        """Auditoría Técnica con IA"""
        print("\n🕵️ [IA Auditor] Iniciando revisión de consistencia...")
        
        plan_path = os.path.join(self.active_root, 'project_meta', 'planning', 'plan.json')
        if not os.path.exists(plan_path):
            print("⚠️ No existe plan.json. Ejecuta /init.")
            return

        code_context = self._scan_directory(self.active_root, max_chars=20000)
        with open(plan_path, 'r', encoding='utf-8') as f:
            plan_content = f.read()

        prompt = f"""
        ERES UN AUDITOR TÉCNICO RIGUROSO.
        
        PLAN PROMETIDO (plan.json):
        {plan_content}
        
        REALIDAD DEL CÓDIGO:
        {code_context}
        
        TAREA:
        Genera un reporte de auditoría breve.
        1. ¿Qué tecnologías prometidas NO están instaladas/detectadas?
        2. ¿Qué tareas marcadas como hechas parecen incompletas?
        3. Calificación de cumplimiento (0-100%).
        """
        
        if self.ai:
            resp = await self.ai.process_single(prompt)
            print("\n📊 --- REPORTE DE AUDITORÍA IA ---")
            print(resp.content)
            print("-----------------------------------")

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

        messages: List[Message] = self.chat_manager.get_context(limit=20) if self.chat_manager else [Message(role='user', content=prompt)]

        sys_prompt = f"Eres un asistente de desarrollo de software experto que opera en el directorio '{self.active_root}'. Puedes y debes usar las herramientas provistas para completar las tareas solicitadas."

        MAX_TOOL_CALLS = 5
        for _ in range(MAX_TOOL_CALLS):
            response = await self.ai.process_single(
                messages=messages,
                system_prompt=sys_prompt,
                tools=self.TOOL_DEFINITIONS
            )

            if response.tool_calls:
                print(f"\n🤖 Invocando herramienta: {response.tool_calls[0]['function']['name']}...")
                logger.info("AI requested tool call", tool_calls=response.tool_calls)
                messages.append(Message(role="assistant", content=response.content or "", tool_calls=response.tool_calls))
                
                for tool_call in response.tool_calls:
                    tool_name = tool_call['function']['name']
                    tool_args = tool_call['function']['arguments']
                    tool_id = tool_call['id']
                    
                    if tool_name in self.AVAILABLE_TOOLS:
                        tool_function = self.AVAILABLE_TOOLS[tool_name]
                        try:
                            result = tool_function(**tool_args)
                            messages.append(Message(role="tool", content=result, tool_call_id=tool_id))
                        except Exception as e:
                            error_msg = f"Error ejecutando la herramienta {tool_name}: {e}"
                            logger.error("Tool execution failed", tool=tool_name, error=str(e))
                            messages.append(Message(role="tool", content=error_msg, tool_call_id=tool_id))
                    else:
                        error_msg = f"Herramienta desconocida: {tool_name}"
                        logger.warning("Unknown tool requested", tool_name=tool_name)
                        messages.append(Message(role="tool", content=error_msg, tool_call_id=tool_id))
            else:
                print(f"\n🤖 {response.content}\n")
                if self.chat_manager:
                    self.chat_manager.add_message('assistant', response.content)
                return  # Termina el bucle si no hay más tool calls

        print("\n🤖 Límite de invocaciones de herramientas alcanzado. La tarea puede estar incompleta.")

    def cmd_print(self):
        """Genera un reporte legible del Plan Maestro, sin JSON."""
        plan_path = os.path.join(self.active_root, 'project_meta', 'planning', 'plan.json')
        overview_path = os.path.join(self.active_root, 'project_meta', 'product_overview', 'product-overview.json')

        if not os.path.exists(plan_path) or not os.path.exists(overview_path):
            print("❌ No se han generado los metadatos. Ejecuta /init primero.")
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
    
    def cmd_sync(self):
        # (Stub)
        print("🔄 Sync ejecutado.")

    def cmd_run_agent(self):
        # (Stub)
        print("🕵️ Agentes listos.")

    def _scan_directory(self, path, max_chars=50000):
        buffer = []
        total = 0
        ignore = ['.git', 'node_modules', '__pycache__', 'dist', 'project_meta']
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in ignore]
            for file in files:
                if file.endswith(('.py', '.js', '.md', '.json', '.txt')):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                            c = f.read()
                            buffer.append(f"FILE {file}:\n{c}\n")
                            total += len(c)
                            if total > max_chars: return "\n".join(buffer)
                    except: pass
        return "\n".join(buffer)

    def _extract_json(self, text):
        try:
            if "```json" in text: text = text.split("```json")[1].split("```")[0]
            elif "```" in text: text = text.split("```")[1].split("```")[0]
            return json.loads(text.strip())
        except: return None

    def _save_json(self, data, path):
        if data:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2)

if __name__ == "__main__":
    app = Orchestrator()
    try:
        app.main_loop()
    except KeyboardInterrupt: pass
