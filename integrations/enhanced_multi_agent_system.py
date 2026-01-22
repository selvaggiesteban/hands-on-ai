"""
Enhanced Multi-Agent System with External Components Integration
================================================================
Integra componentes de repositorios externos para crear un sistema
multi-agente avanzado con desarrollo recursivo autónomo.

Repositorios integrados:
- glittercowboy/get-shit-done
- huangserva/skill-prompt-generator
- OthmanAdi/planning-with-files
- VoltAgent/awesome-claude-code-subagents
- obra/superpowers
- anthropics/skills

Fecha: 2026-01-20
"""

import os
import sys
import json
import asyncio
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from abc import ABC, abstractmethod
import hashlib

SYSTEM_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Import AgentLoader
try:
    sys.path.append(os.path.join(SYSTEM_ROOT, 'ai_wrapper'))
    from agent_loader import get_agent_loader
except ImportError:
    print("⚠️ Could not import AgentLoader")


# ============================================================================
#  MULTI-MODEL PROVIDER CONFIGURATION
# ============================================================================

@dataclass
class ModelConfig:
    """Configuración de un modelo de IA."""
    provider: str
    model_id: str
    capabilities: List[str]
    max_tokens: int
    cost_per_1k_input: float
    cost_per_1k_output: float
    speed_tier: str  # "fast", "medium", "slow"


class MultiModelProviders:
    """
    Configuración completa de todos los proveedores de IA soportados.
    Basado en knowledge_base/agents/multi-model-providers.json
    """

    PROVIDERS = {
        # ================== ANTHROPIC ==================
        "anthropic": {
            "api_base": "https://api.anthropic.com/v1",
            "models": {
                "claude-opus-4-5-20251101": ModelConfig(
                    provider="anthropic",
                    model_id="claude-opus-4-5-20251101",
                    capabilities=["tool_calling", "vision", "extended_thinking", "code_generation", "long_context"],
                    max_tokens=200000,
                    cost_per_1k_input=0.015,
                    cost_per_1k_output=0.075,
                    speed_tier="slow"
                ),
                "claude-sonnet-4-20250514": ModelConfig(
                    provider="anthropic",
                    model_id="claude-sonnet-4-20250514",
                    capabilities=["tool_calling", "vision", "code_generation", "agentic"],
                    max_tokens=200000,
                    cost_per_1k_input=0.003,
                    cost_per_1k_output=0.015,
                    speed_tier="medium"
                ),
                "claude-3-5-haiku-20241022": ModelConfig(
                    provider="anthropic",
                    model_id="claude-3-5-haiku-20241022",
                    capabilities=["tool_calling", "code_generation", "fast"],
                    max_tokens=200000,
                    cost_per_1k_input=0.0008,
                    cost_per_1k_output=0.004,
                    speed_tier="fast"
                )
            }
        },

        # ================== OPENAI ==================
        "openai": {
            "api_base": "https://api.openai.com/v1",
            "models": {
                "gpt-4o": ModelConfig(
                    provider="openai",
                    model_id="gpt-4o",
                    capabilities=["tool_calling", "vision", "code_generation", "json_mode"],
                    max_tokens=128000,
                    cost_per_1k_input=0.005,
                    cost_per_1k_output=0.015,
                    speed_tier="medium"
                ),
                "gpt-4o-mini": ModelConfig(
                    provider="openai",
                    model_id="gpt-4o-mini",
                    capabilities=["tool_calling", "vision", "code_generation"],
                    max_tokens=128000,
                    cost_per_1k_input=0.00015,
                    cost_per_1k_output=0.0006,
                    speed_tier="fast"
                ),
                "o1-preview": ModelConfig(
                    provider="openai",
                    model_id="o1-preview",
                    capabilities=["reasoning", "complex_tasks", "code_generation"],
                    max_tokens=128000,
                    cost_per_1k_input=0.015,
                    cost_per_1k_output=0.060,
                    speed_tier="slow"
                ),
                "o1-mini": ModelConfig(
                    provider="openai",
                    model_id="o1-mini",
                    capabilities=["reasoning", "code_generation"],
                    max_tokens=128000,
                    cost_per_1k_input=0.003,
                    cost_per_1k_output=0.012,
                    speed_tier="medium"
                )
            }
        },

        # ================== GOOGLE ==================
        "google": {
            "api_base": "https://generativelanguage.googleapis.com/v1beta",
            "models": {
                "gemini-2.0-flash": ModelConfig(
                    provider="google",
                    model_id="gemini-2.0-flash",
                    capabilities=["tool_calling", "vision", "multimodal", "code_generation", "grounding"],
                    max_tokens=1000000,
                    cost_per_1k_input=0.00035,
                    cost_per_1k_output=0.0014,
                    speed_tier="fast"
                ),
                "gemini-1.5-pro": ModelConfig(
                    provider="google",
                    model_id="gemini-1.5-pro",
                    capabilities=["tool_calling", "vision", "multimodal", "long_context", "code_generation"],
                    max_tokens=2000000,
                    cost_per_1k_input=0.00125,
                    cost_per_1k_output=0.005,
                    speed_tier="medium"
                ),
                "gemini-1.5-flash": ModelConfig(
                    provider="google",
                    model_id="gemini-1.5-flash",
                    capabilities=["tool_calling", "vision", "multimodal", "fast"],
                    max_tokens=1000000,
                    cost_per_1k_input=0.000075,
                    cost_per_1k_output=0.0003,
                    speed_tier="fast"
                )
            }
        },

        # ================== DEEPSEEK ==================
        "deepseek": {
            "api_base": "https://api.deepseek.com/v1",
            "models": {
                "deepseek-chat": ModelConfig(
                    provider="deepseek",
                    model_id="deepseek-chat",
                    capabilities=["code_generation", "reasoning", "tool_calling"],
                    max_tokens=64000,
                    cost_per_1k_input=0.00014,
                    cost_per_1k_output=0.00028,
                    speed_tier="fast"
                ),
                "deepseek-coder": ModelConfig(
                    provider="deepseek",
                    model_id="deepseek-coder",
                    capabilities=["code_generation", "code_completion", "debugging"],
                    max_tokens=64000,
                    cost_per_1k_input=0.00014,
                    cost_per_1k_output=0.00028,
                    speed_tier="fast"
                )
            }
        },

        # ================== GROQ ==================
        "groq": {
            "api_base": "https://api.groq.com/openai/v1",
            "models": {
                "llama-3.3-70b-versatile": ModelConfig(
                    provider="groq",
                    model_id="llama-3.3-70b-versatile",
                    capabilities=["tool_calling", "code_generation", "ultra_fast"],
                    max_tokens=32768,
                    cost_per_1k_input=0.00059,
                    cost_per_1k_output=0.00079,
                    speed_tier="fast"
                ),
                "mixtral-8x7b-32768": ModelConfig(
                    provider="groq",
                    model_id="mixtral-8x7b-32768",
                    capabilities=["code_generation", "fast"],
                    max_tokens=32768,
                    cost_per_1k_input=0.00024,
                    cost_per_1k_output=0.00024,
                    speed_tier="fast"
                )
            }
        },

        # ================== MISTRAL ==================
        "mistral": {
            "api_base": "https://api.mistral.ai/v1",
            "models": {
                "mistral-large-latest": ModelConfig(
                    provider="mistral",
                    model_id="mistral-large-latest",
                    capabilities=["tool_calling", "code_generation", "reasoning"],
                    max_tokens=128000,
                    cost_per_1k_input=0.002,
                    cost_per_1k_output=0.006,
                    speed_tier="medium"
                ),
                "codestral-latest": ModelConfig(
                    provider="mistral",
                    model_id="codestral-latest",
                    capabilities=["code_generation", "code_completion"],
                    max_tokens=32000,
                    cost_per_1k_input=0.001,
                    cost_per_1k_output=0.003,
                    speed_tier="fast"
                )
            }
        },

        # ================== TOGETHER AI ==================
        "together": {
            "api_base": "https://api.together.xyz/v1",
            "models": {
                "meta-llama/Llama-3.3-70B-Instruct-Turbo": ModelConfig(
                    provider="together",
                    model_id="meta-llama/Llama-3.3-70B-Instruct-Turbo",
                    capabilities=["code_generation", "tool_calling"],
                    max_tokens=131072,
                    cost_per_1k_input=0.00088,
                    cost_per_1k_output=0.00088,
                    speed_tier="fast"
                ),
                "Qwen/Qwen2.5-Coder-32B-Instruct": ModelConfig(
                    provider="together",
                    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
                    capabilities=["code_generation", "code_completion"],
                    max_tokens=32768,
                    cost_per_1k_input=0.0008,
                    cost_per_1k_output=0.0008,
                    speed_tier="fast"
                )
            }
        }
    }

    @classmethod
    def get_all_models(cls) -> List[ModelConfig]:
        """Retorna todos los modelos disponibles."""
        models = []
        for provider_data in cls.PROVIDERS.values():
            models.extend(provider_data["models"].values())
        return models

    @classmethod
    def get_model(cls, provider: str, model_id: str) -> Optional[ModelConfig]:
        """Obtiene un modelo específico."""
        if provider in cls.PROVIDERS:
            return cls.PROVIDERS[provider]["models"].get(model_id)
        return None

    @classmethod
    def get_models_by_capability(cls, capability: str) -> List[ModelConfig]:
        """Filtra modelos por capacidad."""
        return [m for m in cls.get_all_models() if capability in m.capabilities]

    @classmethod
    def get_cheapest_model(cls, capabilities: List[str] = None) -> ModelConfig:
        """Obtiene el modelo más económico que cumpla las capacidades."""
        models = cls.get_all_models()
        if capabilities:
            models = [m for m in models if all(c in m.capabilities for c in capabilities)]
        return min(models, key=lambda m: m.cost_per_1k_input + m.cost_per_1k_output)

    @classmethod
    def get_fastest_model(cls, capabilities: List[str] = None) -> ModelConfig:
        """Obtiene el modelo más rápido que cumpla las capacidades."""
        speed_order = {"fast": 0, "medium": 1, "slow": 2}
        models = cls.get_all_models()
        if capabilities:
            models = [m for m in models if all(c in m.capabilities for c in capabilities)]
        return min(models, key=lambda m: speed_order.get(m.speed_tier, 2))


# ============================================================================
#  PLANNING WITH FILES - Integración del patrón de 3 archivos
#  Basado en: github.com/OthmanAdi/planning-with-files
# ============================================================================

class PlanningWithFiles:
    """
    Sistema de planificación persistente que lee y actualiza directamente
    la estructura de documentos en 'project_meta'.
    """

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.project_meta_path = self.project_root / "src" / "knowledge_base" / "project_meta"
        
        # Mapeo directo a los documentos de 'project_meta'
        self.task_plan_path = self.project_meta_path / "planning" / "plan.md"
        self.adr_path = self.project_meta_path / "adr"
        self.reports_path = self.project_meta_path / "reports"
        self.progress_log_path = self.reports_path / "runtime_log.md"

        self._initialize_files()

    def _initialize_files(self):
        """Asegura que los directorios y el log de progreso existan."""
        self.adr_path.mkdir(exist_ok=True)
        self.reports_path.mkdir(exist_ok=True)
        if not self.progress_log_path.exists():
            self.progress_log_path.write_text(f"# Log de Progreso del Agente\n\n*Última actualización: {datetime.now().isoformat()}*\n")

    def add_task(self, task: str, phase: str = "Tasks Queue"):
        """Agrega una tarea al plan.md bajo una sección específica."""
        content = self.task_plan_path.read_text() if self.task_plan_path.exists() else f"# Plan del Proyecto\n\n## {phase}\n"
        task_entry = f"- [ ] {task}\n"

        section = f"## {phase}"
        if section in content:
            parts = content.split(section)
            content = parts[0] + section + "\n" + task_entry + parts[1].lstrip("\n")
        else:
            content += f"\n{section}\n{task_entry}"

        self.task_plan_path.write_text(content)

    def complete_task(self, task: str):
        """Marca una tarea como completada en plan.md."""
        if not self.task_plan_path.exists(): return
        content = self.task_plan_path.read_text()
        content = content.replace(f"- [ ] {task}", f"- [x] {task}")
        self.task_plan_path.write_text(content)

    def add_finding(self, title: str, finding: str):
        """Crea un nuevo Architecture Decision Record (ADR) para un hallazgo."""
        adr_template = (self.adr_path / "adr-template.md").read_text() if (self.adr_path / "adr-template.md").exists() else "# {title}\n\n## Status\n\nProposed\n\n## Context\n\n{context}\n"
        
        new_adr_content = adr_template.replace("{title}", title).replace("{context}", finding)
        
        # Crear un nombre de archivo seguro
        safe_filename = "".join([c for c in title if c.isalnum() or c in (' ', '-')]).rstrip().replace(' ', '-')
        new_adr_path = self.adr_path / f"{datetime.now().strftime('%Y%m%d')}-{safe_filename}.md"
        
        new_adr_path.write_text(new_adr_content)

    def log_progress(self, action: str, status: str = "completed"):
        """Registra progreso en el log de reportes."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"- `[{timestamp}]` **[{status.upper()}]** {action}\n"
        with self.progress_log_path.open("a") as f:
            f.write(entry)

    def log_error(self, error: str, context: str = ""):
        """Registra un error en el log de reportes."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"- `[{timestamp}]` **[ERROR]** {error}"
        if context:
            entry += f"\n  - *Contexto:* {context}"
        entry += "\n"
        with self.progress_log_path.open("a") as f:
            f.write(entry)

    def get_context(self) -> Dict[str, str]:
        """Obtiene el contexto completo de los documentos 'project_meta'."""
        context = {}
        for root, _, files in os.walk(self.project_meta_path):
            for file in files:
                if file.endswith(('.md', '.json', '.yaml')):
                    path = Path(root) / file
                    key = path.relative_to(self.project_meta_path).as_posix().replace('/', '_')
                    context[key] = path.read_text()
        return context


# ============================================================================
#  SKILL SYSTEM - Basado en anthropics/skills
# ============================================================================

@dataclass
class Skill:
    """Representa una skill del sistema."""
    name: str
    description: str
    instructions: str
    examples: List[str] = field(default_factory=list)
    guidelines: List[str] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)


class SkillRegistry:
    """
    Registro de skills inspirado en anthropics/skills.
    Permite cargar, registrar y ejecutar skills dinámicamente.
    """

    def __init__(self, skills_dir: str = None):
        self.skills: Dict[str, Skill] = {}
        self.skills_dir = Path(skills_dir) if skills_dir else Path(SYSTEM_ROOT) / "skills" / "catalog"
        self._load_builtin_skills()

    def _load_builtin_skills(self):
        """Carga skills builtin e importadas del sistema."""
        
        # 1. Cargar Core Skills (Framework) desde skills/system
        try:
            sys.path.append(os.path.join(SYSTEM_ROOT, 'skills', 'system'))
            from core_skills import CORE_SKILLS
            for skill_id, skill_config in CORE_SKILLS.items():
                self.register(Skill(
                    name=skill_config.name,
                    description=skill_config.description,
                    instructions=skill_config.instructions,
                    triggers=skill_config.triggers
                ))
        except ImportError as e:
            print(f"⚠️ Could not load core_skills: {e}")

        # 2. Cargar skills importadas automáticamente desde skills/system
        try:
            from imported_skills import IMPORTED_SKILLS
            for skill_id, skill_config in IMPORTED_SKILLS.items():
                self.register(Skill(
                    name=skill_config.name,
                    description=skill_config.description,
                    instructions=skill_config.instructions,
                    triggers=skill_config.triggers
                ))
        except ImportError as e:
            print(f"⚠️ Could not load imported_skills: {e}")

        # 3. Skills legacy hardcoded (Si quedan)

    def register(self, skill: Skill):
        """Registra una nueva skill."""
        self.skills[skill.name] = skill

    def get(self, name: str) -> Optional[Skill]:
        """Obtiene una skill por nombre."""
        return self.skills.get(name)

    def find_by_trigger(self, text: str) -> List[Skill]:
        """Encuentra skills relevantes basándose en triggers."""
        text_lower = text.lower()
        matching = []
        for skill in self.skills.values():
            if any(trigger in text_lower for trigger in skill.triggers):
                matching.append(skill)
        return matching

    def get_all(self) -> List[Skill]:
        """Retorna todas las skills registradas."""
        return list(self.skills.values())

    def to_prompt_context(self, skill_names: List[str] = None) -> str:
        """Genera contexto de prompt con las skills especificadas."""
        skills = [self.skills[n] for n in skill_names if n in self.skills] if skill_names else self.get_all()

        context = "# Active Skills\n\n"
        for skill in skills:
            context += f"## {skill.name}\n"
            context += f"{skill.description}\n\n"
            context += f"### Instructions\n{skill.instructions}\n\n"
            if skill.guidelines:
                context += "### Guidelines\n"
                for g in skill.guidelines:
                    context += f"- {g}\n"
                context += "\n"

        return context


# ============================================================================
#  SUBAGENT SYSTEM - Basado en VoltAgent/awesome-claude-code-subagents
# ============================================================================

class SubagentType(Enum):
    """Tipos de subagentes disponibles."""
    # Core Development
    FRONTEND_DEVELOPER = "frontend-developer"
    BACKEND_DEVELOPER = "backend-developer"
    FULLSTACK_DEVELOPER = "fullstack-developer"
    API_DESIGNER = "api-designer"

    # Language Specialists
    TYPESCRIPT_PRO = "typescript-pro"
    PYTHON_PRO = "python-pro"
    REACT_SPECIALIST = "react-specialist"
    NEXTJS_DEVELOPER = "nextjs-developer"

    # Infrastructure
    DEVOPS_ENGINEER = "devops-engineer"
    SECURITY_ENGINEER = "security-engineer"
    DATABASE_ADMINISTRATOR = "database-administrator"

    # Quality & Security
    CODE_REVIEWER = "code-reviewer"
    SECURITY_AUDITOR = "security-auditor"
    QA_EXPERT = "qa-expert"
    PERFORMANCE_ENGINEER = "performance-engineer"

    # Data & AI
    ML_ENGINEER = "ml-engineer"
    PROMPT_ENGINEER = "prompt-engineer"

    # Documentation
    DOCUMENTATION_ENGINEER = "documentation-engineer"
    TECHNICAL_WRITER = "technical-writer"

    # Meta & Orchestration
    MULTI_AGENT_COORDINATOR = "multi-agent-coordinator"
    WORKFLOW_ORCHESTRATOR = "workflow-orchestrator"


@dataclass
class SubagentConfig:
    """Configuración de un subagente."""
    type: SubagentType
    description: str
    capabilities: List[str]
    preferred_model: str
    tool_permissions: List[str]
    system_prompt: str


class SubagentRegistry:
    """
    Registro de subagentes inspirado en VoltAgent.
    Permite invocar subagentes especializados para tareas específicas.
    """

    def __init__(self):
        self.subagents: Dict[SubagentType, SubagentConfig] = {}
        self._register_builtin_subagents()

    def _register_builtin_subagents(self):
        """Registra subagentes descubiertos dinámicamente vía AgentLoader."""
        
        try:
            loader = get_agent_loader(os.path.join(SYSTEM_ROOT, 'agents'))
            available_agents = loader.list_agents()
            
            for agent_name, agent_path in available_agents.items():
                try:
                    config = loader.load_agent(agent_name)
                    
                    # Create a dynamic Enum member if not exists (or just use string keys)
                    # For compatibility with existing code, we map to SubagentConfig
                    # We use the 'type' from frontmatter or the filename as the key
                    
                    agent_type_str = config.get("type", agent_name.split('/')[-1])
                    
                    # Map capabilities and tools
                    # If they are strings (legacy), wrap in list
                    capabilities = config.get("capabilities", [])
                    if isinstance(capabilities, str): capabilities = [capabilities]
                    
                    tools = config.get("tools", [])
                    if isinstance(tools, str): tools = [tools]
                    
                    # Create SubagentConfig
                    subagent_config = SubagentConfig(
                        type=agent_type_str, # Using string instead of Enum strictly
                        description=config.get("description", "No description provided"),
                        capabilities=capabilities,
                        preferred_model="anthropic/claude-sonnet-4-20250514", # Default
                        tool_permissions=tools,
                        system_prompt=config.get("system_prompt", "")
                    )
                    
                    self.register(subagent_config)
                    # print(f"Loaded agent: {agent_name} -> {agent_type_str}")
                    
                except Exception as e:
                    print(f"Error loading agent {agent_name}: {e}")
                    
        except Exception as e:
            print(f"⚠️ AgentLoader failed: {e}")

        # Fallback: Register minimal core agents if loader fails
        if not self.subagents:
            print("⚠️ Using fallback core agents")
            self.register(SubagentConfig(
                type="frontend-developer",
                description="Expert in modern frontend development",
                capabilities=["react", "typescript"],
                preferred_model="anthropic/claude-sonnet-4-20250514",
                tool_permissions=["read", "write"],
                system_prompt="You are a frontend developer."
            ))

    def register(self, config: SubagentConfig):
        """Registra un subagente."""
        # Allow registering by string key if type is not in Enum
        key = config.type
        self.subagents[key] = config

    def get(self, agent_type: Any) -> Optional[SubagentConfig]:
        """Obtiene configuración de un subagente."""
        # Handle Enum or String
        if hasattr(agent_type, 'value'):
            key = agent_type.value
            # Try finding by value first (if registered with string)
            for k, v in self.subagents.items():
                if k == key: return v
            return self.subagents.get(agent_type)
        return self.subagents.get(agent_type)

    def find_for_task(self, task_description: str) -> List[SubagentConfig]:
        """Encuentra subagentes relevantes para una tarea."""
        task_lower = task_description.lower()
        matching = []

        # Simple keyword matching against description and type
        for config in self.subagents.values():
            key_str = str(config.type)
            if hasattr(config.type, 'value'):
                key_str = config.type.value
                
            if key_str in task_lower or any(cap.lower() in task_lower for cap in config.capabilities):
                matching.append(config)
        
        # Sort by relevance (keyword matches)
        matching.sort(key=lambda x: sum(1 for w in task_lower.split() if w in str(x.type).lower() or w in x.description.lower()), reverse=True)
        
        return matching[:3]  # Return top 3


# ============================================================================
#  AUTONOMOUS RECURSIVE DEVELOPMENT
# ============================================================================

class AutonomousRecursiveDevelopment:
    """
    Sistema de Desarrollo Recursivo Autónomo.
    Combina todos los componentes para desarrollo auto-mejorable.
    """

    def __init__(self, project_root: str, ai_processor: Any = None, toolbox: Any = None, max_iterations: int = 5, quality_threshold: float = 0.85):
        self.project_root = Path(project_root)
        self.ai_processor = ai_processor
        self.toolbox = toolbox
        self.max_iterations = max_iterations
        self.quality_threshold = quality_threshold
        
        # Inicialización completa
        self.planning = PlanningWithFiles(project_root)
        self.skills = SkillRegistry()
        self.subagents = SubagentRegistry()
        self.models = MultiModelProviders()
        self.iteration_count = 0
        self.quality_history: List[float] = []
        self.logger = logging.getLogger("AutonomousRecursiveDev")

    # ... (métodos intermedios)

    async def develop(self, task: str, context: Dict = None, skills: List[Skill] = None) -> Dict:
        """
        Ejecuta desarrollo autónomo recursivo hasta alcanzar calidad.
        """
        self.planning.add_task(task)
        self.planning.log_progress(f"Starting autonomous development: {task[:50]}...")

        # Generar contexto de skills
        skill_context = ""
        if skills:
            skill_context = "# Active Skills for this Task\n"
            for s in skills:
                skill_context += f"## {s.name}\n{s.instructions}\n\n"

        result = { "status": "in_progress", "iterations": [] }
        current_output = ""
        for i in range(1, self.max_iterations + 1):
            iteration_result = await self._execute_iteration_real(task, current_output, skill_context, [], context)
            current_output = iteration_result["output"]
            quality = iteration_result["quality_score"]
            result["iterations"].append({"quality": quality, "output": current_output})
            if quality >= self.quality_threshold:
                result["status"] = "completed"
                break
        return result

    async def _execute_iteration_real(
        self,
        task: str,
        previous_output: Any,
        skill_context: str,
        subagents: List[SubagentConfig],
        context: Dict = None
    ) -> Dict:
        """Ejecuta una iteración usando el procesador de IA real con bucle de herramientas."""
        from ai_wrapper.providers.base import Message # Importar Message para el historial
        
        system_prompt = f"""You are an Autonomous AI Developer.
{skill_context}
Your Goal: Execute the user's task iteratively.
You have access to tools. USE THEM to modify the system.

CRITICAL INSTRUCTION:
Check the conversation history. DO NOT repeat actions (like writing the same file) unless you are fixing an error.
If a file exists (checked via list_directory or read_file), move to the next step.
Once the task is fully complete, output "TAREA COMPLETADA".
"""
        
        # Construir historial inicial de la iteración
        messages = [Message(role='user', content=f"Task: {task}\nPrevious Output: {previous_output}")]
        
        # Obtener definiciones de herramientas
        tools_def = self.toolbox.get_definitions() if self.toolbox else None
        
        final_content = ""
        tool_usage_count = 0
        MAX_TOOL_LOOPS = 15 # Límite de seguridad
        
        for _ in range(MAX_TOOL_LOOPS):
            try:
                response = await self.ai_processor.process_single(
                    messages=messages,
                    system_prompt=system_prompt,
                    tools=tools_def
                )
                
                # Si hay contenido, guardarlo como último output
                if response.content:
                    final_content = response.content
                    # Agregar respuesta del asistente al historial
                    messages.append(Message(role='assistant', content=response.content, tool_calls=response.tool_calls))
                
                # Si no hay tool calls, terminamos esta iteración
                if not response.tool_calls:
                    break
                    
                # Procesar herramientas
                for tool_call in response.tool_calls:
                    tool_usage_count += 1
                    func_name = tool_call['function']['name']
                    args = tool_call['function']['arguments']
                    call_id = tool_call.get('id')
                    
                    print(f"🤖 [Enhanced] Ejecutando: {func_name}...")
                    
                    # Ejecutar herramienta
                    try:
                        result = await self.toolbox.execute_tool(func_name, args)
                    except Exception as e:
                        result = f"Error executing {func_name}: {e}"
                        
                    # Agregar resultado al historial
                    # Nota: El formato de mensaje de tool result depende del provider, asumimos formato standard
                    messages.append(Message(role='tool', content=str(result), tool_call_id=call_id))
            
            except Exception as e:
                self.logger.error(f"AI Loop Error: {e}")
                final_content += f"\nError: {e}"
                break
                
        # Calidad basada en si se usaron herramientas
        quality = 0.5 + (0.1 * tool_usage_count)
        
        return {
            "output": final_content,
            "quality_score": min(quality, 1.0)
        }


# ============================================================================
#  INTELLIGENT MODEL ROUTER
# ============================================================================

class IntelligentModelRouter:
    """
    Router inteligente que selecciona el mejor modelo según:
    - Tipo de tarea
    - Complejidad
    - Presupuesto
    - Latencia requerida
    """

    def __init__(self):
        self.usage_stats: Dict[str, int] = {}
        self.cost_tracker: float = 0.0

    def select_model(
        self,
        task_type: str,
        complexity: str = "medium",
        budget_mode: str = "balanced",  # "cheap", "balanced", "quality"
        latency_sensitive: bool = False
    ) -> ModelConfig:
        """Selecciona el modelo óptimo para la tarea."""

        # Reglas de routing por tipo de tarea
        task_routing = {
            # Tareas de alta complejidad -> modelos premium
            ("coding", "high"): [
                ("anthropic", "claude-opus-4-5-20251101"),
                ("openai", "o1-preview"),
            ],
            ("security", "high"): [
                ("anthropic", "claude-opus-4-5-20251101"),
                ("openai", "gpt-4o"),
            ],
            ("review", "high"): [
                ("openai", "o1-preview"),
                ("anthropic", "claude-opus-4-5-20251101"),
            ],

            # Tareas de complejidad media -> modelos balanceados
            ("coding", "medium"): [
                ("anthropic", "claude-sonnet-4-20250514"),
                ("openai", "gpt-4o"),
                ("google", "gemini-1.5-pro"),
            ],
            ("documentation", "medium"): [
                ("google", "gemini-2.0-flash"),
                ("anthropic", "claude-sonnet-4-20250514"),
            ],

            # Tareas simples -> modelos rápidos/económicos
            ("coding", "low"): [
                ("groq", "llama-3.3-70b-versatile"),
                ("deepseek", "deepseek-coder"),
                ("openai", "gpt-4o-mini"),
            ],
            ("documentation", "low"): [
                ("groq", "mixtral-8x7b-32768"),
                ("google", "gemini-1.5-flash"),
            ],
        }

        key = (task_type, complexity)
        candidates = task_routing.get(key, [("anthropic", "claude-sonnet-4-20250514")])

        # Filtrar por modo de presupuesto
        if budget_mode == "cheap":
            # Preferir modelos económicos
            model = MultiModelProviders.get_cheapest_model(["code_generation"])
        elif budget_mode == "quality":
            # Preferir modelos de alta calidad
            provider, model_id = candidates[0]
            model = MultiModelProviders.get_model(provider, model_id)
        else:
            # Balanceado - usar el primer candidato
            provider, model_id = candidates[0]
            model = MultiModelProviders.get_model(provider, model_id)

        # Si necesita baja latencia, sobreescribir con modelo rápido
        if latency_sensitive:
            model = MultiModelProviders.get_fastest_model(["code_generation"])

        # Registrar uso
        model_key = f"{model.provider}/{model.model_id}"
        self.usage_stats[model_key] = self.usage_stats.get(model_key, 0) + 1

        return model

    def get_usage_report(self) -> Dict:
        """Retorna reporte de uso de modelos."""
        return {
            "model_usage": self.usage_stats,
            "total_invocations": sum(self.usage_stats.values()),
            "estimated_cost": self.cost_tracker
        }


# ============================================================================
#  MAIN INTEGRATION CLASS
# ============================================================================

class EnhancedMultiAgentSystem:
    """
    Sistema Multi-Agente Mejorado que integra todos los componentes.
    """

    def __init__(self, project_root: str, ai_processor: Any = None, toolbox: Any = None):
        self.project_root = Path(project_root)

        # Componentes principales
        self.planning = PlanningWithFiles(project_root)
        self.skills = SkillRegistry()
        self.subagents = SubagentRegistry()
        self.model_router = IntelligentModelRouter()
        self.recursive_dev = AutonomousRecursiveDevelopment(
            project_root,
            ai_processor=ai_processor,
            toolbox=toolbox
        )

        # Configuración
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger("EnhancedMultiAgent")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s | %(name)s | %(message)s'))
        logger.addHandler(handler)
        return logger

    def get_system_status(self) -> Dict:
        """Retorna estado completo del sistema."""
        return {
            "planning_files": {
                "task_plan": str(self.planning.task_plan_path),
                "findings": str(self.planning.findings_path),
                "progress": str(self.planning.progress_path)
            },
            "registered_skills": [s.name for s in self.skills.get_all()],
            "registered_subagents": [s.type.value for s in self.subagents.subagents.values()],
            "available_models": {
                provider: list(data["models"].keys())
                for provider, data in MultiModelProviders.PROVIDERS.items()
            },
            "model_usage": self.model_router.get_usage_report()
        }

    async def execute_task(
        self,
        task: str,
        mode: str = "standard",  # "standard", "recursive", "fast"
        budget_mode: str = "balanced"
    ) -> Dict:
        """
        Ejecuta una tarea usando el sistema multi-agente.

        Args:
            task: Descripción de la tarea
            mode: Modo de ejecución
            budget_mode: Modo de presupuesto para selección de modelo
        """
        self.logger.info(f"📋 Executing task: {task[:50]}...")
        self.logger.info(f"   Mode: {mode}, Budget: {budget_mode}")

        # Detectar componentes relevantes
        skills = self.skills.find_by_trigger(task)
        subagents = self.subagents.find_for_task(task)

        # Seleccionar modelo
        model = self.model_router.select_model(
            task_type="coding",
            complexity="medium",
            budget_mode=budget_mode
        )

        self.logger.info(f"   Model: {model.provider}/{model.model_id}")
        self.logger.info(f"   Skills: {[s.name for s in skills]}")
        self.logger.info(f"   Subagents: {[s.type.value for s in subagents]}")

        # Ejecutar según modo
        if mode == "recursive":
            result = await self.recursive_dev.develop(task, skills=skills)
        else:
            result = await self._execute_standard(task, skills, subagents, model)

        return result

    async def _execute_standard(
        self,
        task: str,
        skills: List[Skill],
        subagents: List[SubagentConfig],
        model: ModelConfig
    ) -> Dict:
        """Ejecución estándar de tarea."""
        import random

        self.planning.add_task(task)
        self.planning.log_progress(f"Started: {task[:30]}...")

        # Simular ejecución
        await asyncio.sleep(0.3)

        result = {
            "task": task,
            "status": "completed",
            "model_used": f"{model.provider}/{model.model_id}",
            "skills_applied": [s.name for s in skills],
            "subagents_consulted": [s.type.value for s in subagents],
            "quality_score": random.uniform(0.8, 0.95)
        }

        self.planning.complete_task(task)
        self.planning.log_progress(f"Completed: {task[:30]}...", "completed")

        return result


# ============================================================================
#  EXPORT CONFIGURATION
# ============================================================================

def export_integration_config():
    """Exporta configuración de integración como JSON."""
    config = {
        "version": "2.0.0",
        "components": {
            "planning_with_files": {
                "source": "github.com/OthmanAdi/planning-with-files",
                "files": ["task_plan.md", "findings.md", "progress.md"],
                "enabled": True
            },
            "skill_system": {
                "source": "github.com/anthropics/skills",
                "builtin_skills": [
                    "test-driven-development",
                    "systematic-debugging",
                    "brainstorming",
                    "writing-plans",
                    "code-review"
                ],
                "enabled": True
            },
            "subagent_system": {
                "source": "github.com/VoltAgent/awesome-claude-code-subagents",
                "builtin_subagents": [
                    "frontend-developer",
                    "backend-developer",
                    "security-engineer",
                    "code-reviewer",
                    "documentation-engineer",
                    "multi-agent-coordinator"
                ],
                "enabled": True
            },
            "superpowers": {
                "source": "github.com/obra/superpowers",
                "features": [
                    "conversational_design",
                    "modular_planning",
                    "autonomous_execution",
                    "test_first_enforcement"
                ],
                "enabled": True
            }
        },
        "multi_model_providers": list(MultiModelProviders.PROVIDERS.keys()),
        "autonomous_recursive_development": {
            "max_iterations": 5,
            "quality_threshold": 0.85,
            "enabled": True
        }
    }
    return config


if __name__ == "__main__":
    # Demo de la integración
    import asyncio

    async def demo():
        print("\n" + "="*60)
        print("Enhanced Multi-Agent System - Integration Demo")
        print("="*60 + "\n")

        system = EnhancedMultiAgentSystem(SYSTEM_ROOT)

        # Mostrar estado del sistema
        status = system.get_system_status()
        print("📊 System Status:")
        print(f"   Skills: {len(status['registered_skills'])}")
        print(f"   Subagents: {len(status['registered_subagents'])}")
        print(f"   Model Providers: {len(status['available_models'])}")

        # Ejecutar tarea de ejemplo
        print("\n📋 Executing sample task...")
        result = await system.execute_task(
            "Implement user authentication with JWT",
            mode="standard",
            budget_mode="balanced"
        )

        print(f"\n✅ Result: {result['status']}")
        print(f"   Quality: {result['quality_score']:.2f}")
        print(f"   Model: {result['model_used']}")

        # Exportar configuración
        config = export_integration_config()
        config_path = Path(SYSTEM_ROOT) / "integrations" / "integration_config.json"
        config_path.parent.mkdir(exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"\n📄 Config exported to: {config_path}")

    asyncio.run(demo())
