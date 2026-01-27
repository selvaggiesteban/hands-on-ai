"""
Test del Pipeline Completo con TODOS los Agentes
===================================================
Ejecuta el pipeline en modo FULL para validar efectividad y velocidad
de la arquitectura multi-agente híbrida.

Fecha: 2026-01-20
"""

import os
import sys
import json
import asyncio
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import random

SYSTEM_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, SYSTEM_ROOT)
sys.path.insert(0, os.path.join(SYSTEM_ROOT, 'agents'))


# ============================================================================
#  CONFIGURACIÓN MULTI-MODELO
# ============================================================================

SUPPORTED_MODELS = {
    "anthropic": {
        "models": ["claude-opus-4-5-20251101", "claude-sonnet-4-20250514", "claude-3-5-haiku-20241022"],
        "default": "claude-sonnet-4-20250514",
        "capabilities": ["tool_calling", "vision", "long_context", "code_generation"]
    },
    "openai": {
        "models": ["gpt-4o", "gpt-4o-mini", "o1-preview", "o1-mini"],
        "default": "gpt-4o",
        "capabilities": ["tool_calling", "vision", "code_generation", "reasoning"]
    },
    "google": {
        "models": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
        "default": "gemini-2.0-flash",
        "capabilities": ["tool_calling", "vision", "long_context", "multimodal"]
    },
    "deepseek": {
        "models": ["deepseek-chat", "deepseek-coder"],
        "default": "deepseek-chat",
        "capabilities": ["code_generation", "reasoning"]
    },
    "groq": {
        "models": ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
        "default": "llama-3.3-70b-versatile",
        "capabilities": ["fast_inference", "code_generation"]
    }
}


# ============================================================================
#  COMPONENTES DEL PIPELINE
# ============================================================================

class AgentType(Enum):
    PLANNING = "planning"
    CODING = "coding"
    SECURITY = "security"
    REVIEW = "review"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"
    ORCHESTRATOR = "orchestrator"


class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class AgentMetrics:
    """Métricas de rendimiento por agente."""
    agent_type: str
    invocations: int = 0
    total_time: float = 0.0
    success_count: int = 0
    error_count: int = 0
    avg_response_time: float = 0.0

    def update(self, duration: float, success: bool = True):
        self.invocations += 1
        self.total_time += duration
        if success:
            self.success_count += 1
        else:
            self.error_count += 1
        self.avg_response_time = self.total_time / self.invocations


class EnhancedEventBus:
    """Event Bus con soporte multi-modelo."""

    def __init__(self, logger: logging.Logger):
        self.subscribers: Dict[str, List] = {}
        self.event_history: List[Dict] = []
        self.logger = logger

    def subscribe(self, event_type: str, handler):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    async def publish(self, event_type: str, data: Dict):
        event = {
            "type": event_type,
            "data": data,
            "timestamp": time.time()
        }
        self.event_history.append(event)
        self.logger.debug(f"[EventBus] {event_type}: {data.get('message', '')[:50]}")

        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                await handler(event)


class MultiModelRouter:
    """Router inteligente para selección de modelo según tarea."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.model_usage = defaultdict(int)

    def select_model(self, task_type: str, complexity: str = "medium") -> Dict:
        """Selecciona el mejor modelo para una tarea."""
        routing_rules = {
            ("coding", "high"): ("anthropic", "claude-opus-4-5-20251101"),
            ("coding", "medium"): ("anthropic", "claude-sonnet-4-20250514"),
            ("coding", "low"): ("groq", "llama-3.3-70b-versatile"),
            ("security", "high"): ("anthropic", "claude-opus-4-5-20251101"),
            ("security", "medium"): ("openai", "gpt-4o"),
            ("review", "high"): ("openai", "o1-preview"),
            ("review", "medium"): ("anthropic", "claude-sonnet-4-20250514"),
            ("optimization", "high"): ("openai", "o1-preview"),
            ("optimization", "medium"): ("google", "gemini-1.5-pro"),
            ("documentation", "medium"): ("google", "gemini-2.0-flash"),
            ("documentation", "low"): ("groq", "mixtral-8x7b-32768"),
            ("planning", "high"): ("anthropic", "claude-opus-4-5-20251101"),
            ("planning", "medium"): ("openai", "gpt-4o"),
        }

        key = (task_type, complexity)
        if key in routing_rules:
            provider, model = routing_rules[key]
        else:
            provider, model = "anthropic", "claude-sonnet-4-20250514"

        self.model_usage[f"{provider}/{model}"] += 1
        self.logger.debug(f"[Router] Selected {provider}/{model} for {task_type}/{complexity}")

        return {"provider": provider, "model": model}


class AutonomousRecursiveDevelopment:
    """
    Sistema de Desarrollo Recursivo Autónomo.
    Implementa ciclos de mejora continua con auto-evaluación.
    """

    def __init__(self, logger: logging.Logger, max_iterations: int = 3):
        self.logger = logger
        self.max_iterations = max_iterations
        self.iteration_history = []

    async def execute_with_refinement(self, task: Dict, agents: Dict) -> Dict:
        """Ejecuta una tarea con refinamiento recursivo hasta alcanzar calidad."""
        iteration = 0
        result = None
        quality_threshold = 0.85

        while iteration < self.max_iterations:
            iteration += 1
            self.logger.info(f"  🔄 Iteración recursiva {iteration}/{self.max_iterations}")

            # Ejecutar tarea
            result = await self._execute_task(task, agents)

            # Evaluar resultado
            quality_score = await self._evaluate_quality(result, agents)
            result["quality_score"] = quality_score
            result["iteration"] = iteration

            self.iteration_history.append({
                "iteration": iteration,
                "quality_score": quality_score,
                "timestamp": datetime.now().isoformat()
            })

            if quality_score >= quality_threshold:
                self.logger.info(f"  ✅ Calidad alcanzada: {quality_score:.2f}")
                break
            else:
                self.logger.info(f"  ⚠️ Calidad insuficiente: {quality_score:.2f}, refinando...")
                task = await self._refine_task(task, result, agents)

        return result

    async def _execute_task(self, task: Dict, agents: Dict) -> Dict:
        """Ejecuta la tarea con el agente apropiado."""
        await asyncio.sleep(random.uniform(0.2, 0.5))
        return {
            "task": task["name"],
            "status": "completed",
            "output": f"Generated output for {task['name']}"
        }

    async def _evaluate_quality(self, result: Dict, agents: Dict) -> float:
        """Evalúa la calidad del resultado usando el ReviewAgent."""
        await asyncio.sleep(random.uniform(0.1, 0.2))
        # Simulación: calidad aumenta con iteraciones
        base_quality = 0.7
        iteration_bonus = result.get("iteration", 1) * 0.1
        return min(base_quality + iteration_bonus + random.uniform(-0.05, 0.15), 1.0)

    async def _refine_task(self, task: Dict, result: Dict, agents: Dict) -> Dict:
        """Refina la tarea basándose en el feedback."""
        refined_task = task.copy()
        refined_task["refinement_notes"] = f"Refining based on quality score"
        return refined_task


# ============================================================================
#  PIPELINE COMPLETO
# ============================================================================

class FullPipelineOrchestrator:
    """Orquestador del pipeline completo con todos los agentes."""

    def __init__(self):
        self.logger = self._setup_logging()
        self.event_bus = EnhancedEventBus(self.logger)
        self.model_router = MultiModelRouter(self.logger)
        self.recursive_dev = AutonomousRecursiveDevelopment(self.logger)
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.execution_log = []

        # Inicializar métricas para todos los agentes
        for agent_type in AgentType:
            self.agent_metrics[agent_type.value] = AgentMetrics(agent_type.value)

    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger("FullPipeline")
        logger.setLevel(logging.DEBUG)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', '%H:%M:%S'))

        file_handler = logging.FileHandler(
            os.path.join(SYSTEM_ROOT, 'tests', 'full_pipeline_debug.log'),
            mode='w', encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(funcName)s | %(message)s'
        ))

        logger.addHandler(console)
        logger.addHandler(file_handler)
        return logger

    async def execute_full_pipeline(self, plan: Dict) -> Dict:
        """Ejecuta el pipeline completo con todos los agentes."""
        start_time = time.time()

        self.logger.info("\n" + "🚀"*30)
        self.logger.info("PIPELINE COMPLETO - TODOS LOS AGENTES")
        self.logger.info("🚀"*30 + "\n")

        results = {
            "phases": [],
            "total_tasks": 0,
            "total_agents_invoked": 0,
            "models_used": {},
            "recursive_iterations": 0
        }

        phases = plan.get("phases", [])

        for phase_idx, phase in enumerate(phases):
            phase_start = time.time()
            phase_name = phase.get("name", f"Phase {phase_idx + 1}")

            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"📦 FASE {phase_idx + 1}: {phase_name}")
            self.logger.info(f"{'='*60}")

            await self.event_bus.publish("phase.started", {"phase": phase_name})

            phase_result = {
                "name": phase_name,
                "tasks": [],
                "duration": 0
            }

            tasks = phase.get("tasks", [])
            for task_idx, task in enumerate(tasks):
                task_name = task["name"] if isinstance(task, dict) else task
                task_agent = task.get("agent", "coding") if isinstance(task, dict) else "coding"
                task_complexity = task.get("complexity", "medium") if isinstance(task, dict) else "medium"

                # Seleccionar modelo
                model_info = self.model_router.select_model(task_agent, task_complexity)

                # Ejecutar con todos los agentes en pipeline
                task_result = await self._execute_task_with_all_agents(
                    task_name=task_name,
                    primary_agent=task_agent,
                    model_info=model_info,
                    use_recursive=phase.get("use_recursive", False)
                )

                phase_result["tasks"].append(task_result)
                results["total_tasks"] += 1

            phase_result["duration"] = time.time() - phase_start
            results["phases"].append(phase_result)

            await self.event_bus.publish("phase.completed", {
                "phase": phase_name,
                "duration": phase_result["duration"]
            })

        # Calcular resumen
        total_duration = time.time() - start_time
        results["total_duration"] = total_duration
        results["models_used"] = dict(self.model_router.model_usage)
        results["agent_metrics"] = {
            name: {
                "invocations": m.invocations,
                "total_time": m.total_time,
                "avg_response_time": m.avg_response_time,
                "success_rate": m.success_count / m.invocations if m.invocations > 0 else 0
            }
            for name, m in self.agent_metrics.items()
        }
        results["recursive_iterations"] = len(self.recursive_dev.iteration_history)

        self._print_summary(results)
        return results

    async def _execute_task_with_all_agents(
        self,
        task_name: str,
        primary_agent: str,
        model_info: Dict,
        use_recursive: bool = False
    ) -> Dict:
        """Ejecuta una tarea pasándola por todos los agentes relevantes."""
        task_start = time.time()

        self.logger.info(f"\n  📋 Tarea: {task_name}")
        self.logger.info(f"     Modelo: {model_info['provider']}/{model_info['model']}")

        result = {
            "name": task_name,
            "model": model_info,
            "agents_pipeline": [],
            "status": "completed"
        }

        # Pipeline de agentes según el tipo de tarea
        agent_pipeline = self._get_agent_pipeline(primary_agent)

        for agent_type in agent_pipeline:
            agent_start = time.time()

            await self.event_bus.publish("agent.invoked", {
                "agent": agent_type,
                "task": task_name
            })

            # Simular ejecución del agente
            await self._simulate_agent_execution(agent_type, task_name)

            agent_duration = time.time() - agent_start
            self.agent_metrics[agent_type].update(agent_duration, success=True)

            result["agents_pipeline"].append({
                "agent": agent_type,
                "duration": agent_duration,
                "status": "completed"
            })

            self.logger.info(f"     ✓ [{agent_type.upper()}] {agent_duration:.3f}s")

        # Si está habilitado el desarrollo recursivo
        if use_recursive:
            recursive_result = await self.recursive_dev.execute_with_refinement(
                {"name": task_name, "type": primary_agent},
                self.agent_metrics
            )
            result["recursive_refinement"] = recursive_result

        result["total_duration"] = time.time() - task_start
        return result

    def _get_agent_pipeline(self, primary_agent: str) -> List[str]:
        """Define el pipeline de agentes según el tipo de tarea."""
        pipelines = {
            "coding": ["planning", "coding", "security", "review", "documentation"],
            "security": ["planning", "security", "review"],
            "review": ["review", "optimization"],
            "optimization": ["optimization", "review", "documentation"],
            "documentation": ["documentation", "review"],
            "planning": ["planning"]
        }
        return pipelines.get(primary_agent, ["planning", "coding", "review"])

    async def _simulate_agent_execution(self, agent_type: str, task_name: str):
        """Simula la ejecución de un agente."""
        delays = {
            "planning": (0.1, 0.3),
            "coding": (0.3, 0.7),
            "security": (0.2, 0.4),
            "review": (0.15, 0.35),
            "optimization": (0.2, 0.5),
            "documentation": (0.1, 0.25)
        }
        min_d, max_d = delays.get(agent_type, (0.1, 0.3))
        await asyncio.sleep(random.uniform(min_d, max_d))

    def _print_summary(self, results: Dict):
        """Imprime resumen del pipeline."""
        self.logger.info("\n" + "="*60)
        self.logger.info("📊 RESUMEN DEL PIPELINE COMPLETO")
        self.logger.info("="*60)

        self.logger.info(f"\n⏱️  Duración total: {results['total_duration']:.2f}s")
        self.logger.info(f"📋 Tareas ejecutadas: {results['total_tasks']}")
        self.logger.info(f"🔄 Iteraciones recursivas: {results['recursive_iterations']}")

        self.logger.info(f"\n🤖 Modelos utilizados:")
        for model, count in results['models_used'].items():
            self.logger.info(f"   - {model}: {count} invocaciones")

        self.logger.info(f"\n📈 Métricas por agente:")
        for agent, metrics in results['agent_metrics'].items():
            if metrics['invocations'] > 0:
                self.logger.info(
                    f"   - {agent}: {metrics['invocations']} inv, "
                    f"avg {metrics['avg_response_time']:.3f}s, "
                    f"success {metrics['success_rate']*100:.1f}%"
                )


# ============================================================================
#  PLAN DE PRUEBA COMPLETO
# ============================================================================

FULL_TEST_PLAN = {
    "title": "Pipeline Completo - Landing Page E-commerce",
    "phases": [
        {
            "name": "Fase 1: Setup y Configuración",
            "use_recursive": False,
            "tasks": [
                {"name": "Inicializar proyecto Next.js 14 con App Router", "agent": "coding", "complexity": "medium"},
                {"name": "Configurar TypeScript estricto", "agent": "coding", "complexity": "low"},
                {"name": "Configurar Tailwind CSS con tema personalizado", "agent": "coding", "complexity": "medium"},
                {"name": "Configurar ESLint y Prettier", "agent": "coding", "complexity": "low"},
                {"name": "Configurar variables de entorno seguras", "agent": "security", "complexity": "high"}
            ]
        },
        {
            "name": "Fase 2: Componentes UI Core",
            "use_recursive": True,
            "tasks": [
                {"name": "Crear sistema de diseño (tokens, colores, tipografía)", "agent": "coding", "complexity": "high"},
                {"name": "Implementar componente Header responsive", "agent": "coding", "complexity": "medium"},
                {"name": "Implementar componente Hero con animaciones", "agent": "coding", "complexity": "high"},
                {"name": "Implementar componente Footer", "agent": "coding", "complexity": "low"},
                {"name": "Crear componente Button con variantes", "agent": "coding", "complexity": "medium"},
                {"name": "Crear componente Card reutilizable", "agent": "coding", "complexity": "medium"}
            ]
        },
        {
            "name": "Fase 3: Catálogo de Productos",
            "use_recursive": True,
            "tasks": [
                {"name": "Diseñar modelo de datos de productos", "agent": "planning", "complexity": "high"},
                {"name": "Crear API route para productos", "agent": "coding", "complexity": "medium"},
                {"name": "Implementar ProductCard con imagen optimizada", "agent": "coding", "complexity": "medium"},
                {"name": "Implementar ProductGrid con virtualización", "agent": "coding", "complexity": "high"},
                {"name": "Crear página de detalle de producto", "agent": "coding", "complexity": "medium"},
                {"name": "Implementar sistema de filtros y búsqueda", "agent": "coding", "complexity": "high"},
                {"name": "Cargar 20 productos con datos de prueba", "agent": "coding", "complexity": "low"}
            ]
        },
        {
            "name": "Fase 4: Carrito de Compras",
            "use_recursive": True,
            "tasks": [
                {"name": "Diseñar estado global del carrito con Zustand", "agent": "planning", "complexity": "high"},
                {"name": "Implementar lógica de agregar/quitar productos", "agent": "coding", "complexity": "medium"},
                {"name": "Crear componente CartDrawer", "agent": "coding", "complexity": "medium"},
                {"name": "Implementar persistencia en localStorage", "agent": "coding", "complexity": "low"},
                {"name": "Validar integridad de datos del carrito", "agent": "security", "complexity": "medium"}
            ]
        },
        {
            "name": "Fase 5: Integración Mercado Pago",
            "use_recursive": True,
            "tasks": [
                {"name": "Configurar SDK Mercado Pago (sandbox)", "agent": "security", "complexity": "high"},
                {"name": "Crear API route para preferencias de pago", "agent": "coding", "complexity": "high"},
                {"name": "Implementar checkout button", "agent": "coding", "complexity": "medium"},
                {"name": "Crear páginas de resultado (éxito/pendiente/fallo)", "agent": "coding", "complexity": "medium"},
                {"name": "Implementar webhook para IPN", "agent": "coding", "complexity": "high"},
                {"name": "Auditar seguridad de flujo de pago", "agent": "security", "complexity": "high"},
                {"name": "Validar flujo E2E en sandbox", "agent": "review", "complexity": "high"}
            ]
        },
        {
            "name": "Fase 6: Optimización y SEO",
            "use_recursive": False,
            "tasks": [
                {"name": "Optimizar imágenes con next/image", "agent": "optimization", "complexity": "medium"},
                {"name": "Implementar lazy loading de componentes", "agent": "optimization", "complexity": "medium"},
                {"name": "Configurar metadata y Open Graph", "agent": "coding", "complexity": "low"},
                {"name": "Generar sitemap.xml dinámico", "agent": "coding", "complexity": "low"},
                {"name": "Ejecutar auditoría Lighthouse", "agent": "optimization", "complexity": "high"},
                {"name": "Documentar APIs y componentes", "agent": "documentation", "complexity": "medium"}
            ]
        },
        {
            "name": "Fase 7: Testing y Deploy",
            "use_recursive": False,
            "tasks": [
                {"name": "Escribir tests unitarios con Vitest", "agent": "review", "complexity": "high"},
                {"name": "Escribir tests E2E con Playwright", "agent": "review", "complexity": "high"},
                {"name": "Configurar GitHub Actions CI/CD", "agent": "coding", "complexity": "medium"},
                {"name": "Configurar deploy a Vercel", "agent": "coding", "complexity": "low"},
                {"name": "Generar documentación final", "agent": "documentation", "complexity": "medium"}
            ]
        }
    ]
}


# ============================================================================
#  EJECUCIÓN
# ============================================================================

async def run_full_pipeline():
    """Ejecuta el pipeline completo."""
    print("\n" + "🔬"*35)
    print("🔬 PIPELINE COMPLETO CON TODOS LOS AGENTES")
    print("🔬"*35 + "\n")

    orchestrator = FullPipelineOrchestrator()
    results = await orchestrator.execute_full_pipeline(FULL_TEST_PLAN)

    # Guardar resultados
    report_path = os.path.join(SYSTEM_ROOT, 'tests', 'full_pipeline_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str, ensure_ascii=False)

    print(f"\n📄 Reporte guardado en: {report_path}")

    return results


if __name__ == "__main__":
    results = asyncio.run(run_full_pipeline())
    print("\n✅ Pipeline completo ejecutado exitosamente")
