"""
Hands-On AI - Enhanced Multi-Agent System Integration
=====================================================
Opción A: Integración Completa Activada

Componentes:
- PlanningWithFiles: Sistema de 3 archivos para memoria persistente
- SkillRegistry: Sistema de skills (anthropics/skills)
- SubagentRegistry: Subagentes especializados (VoltAgent)
- MultiModelProviders: 7 proveedores de IA
- IntelligentModelRouter: Routing inteligente por tarea
- AutonomousRecursiveDevelopment: Desarrollo auto-mejorable

Uso:
    from integrations import EnhancedMultiAgentSystem

    system = EnhancedMultiAgentSystem("/path/to/project")
    result = await system.execute_task("task description", mode="recursive")
"""

from .enhanced_multi_agent_system import (
    # Core System
    EnhancedMultiAgentSystem,

    # Planning
    PlanningWithFiles,

    # Skills
    Skill,
    SkillRegistry,

    # Subagents
    SubagentType,
    SubagentConfig,
    SubagentRegistry,

    # Models
    ModelConfig,
    MultiModelProviders,
    IntelligentModelRouter,

    # Autonomous Development
    AutonomousRecursiveDevelopment,

    # Utils
    export_integration_config,
)

__version__ = "2.0.0"
__all__ = [
    "EnhancedMultiAgentSystem",
    "PlanningWithFiles",
    "Skill",
    "SkillRegistry",
    "SubagentType",
    "SubagentConfig",
    "SubagentRegistry",
    "ModelConfig",
    "MultiModelProviders",
    "IntelligentModelRouter",
    "AutonomousRecursiveDevelopment",
    "export_integration_config",
]
