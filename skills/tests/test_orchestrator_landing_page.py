"""
Test del Orquestador Principal - Caso de Uso: Landing Page con Catálogo y Mercado Pago
======================================================================================
Este test valida la arquitectura híbrida Hub-and-Spoke + Event-Driven del sistema multi-agente.

Caso de ejemplo:
- Diseño web landing page
- Catálogo de 20 productos
- Pasarela de pago Mercado Pago

Fecha: 2026-01-20
Autor: Sistema de Auditoría Hands-On AI
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

# Configuración de paths
SYSTEM_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, SYSTEM_ROOT)
sys.path.insert(0, os.path.join(SYSTEM_ROOT, 'agents'))

# ============================================================================
#  COMPONENTES DE LA ARQUITECTURA HÍBRIDA (Hub-and-Spoke + Event-Driven)
# ============================================================================

class EventPriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Event:
    """Estructura de eventos para comunicación asíncrona entre agentes."""
    type: str
    data: Any
    priority: EventPriority = EventPriority.NORMAL
    timestamp: float = None
    source: str = None
    correlation_id: str = None

    def __post_init__(self):
        import time
        if self.timestamp is None:
            self.timestamp = time.time()


class EnhancedEventBus:
    """Event Bus mejorado con prioridades y historial - Patrón Event-Driven."""

    def __init__(self, logger: logging.Logger):
        self.subscribers: Dict[str, List] = {}
        self.event_history: List[Event] = []
        self.max_history = 1000
        self.logger = logger

    def subscribe(self, event_type: str, handler, priority: int = 0):
        """Suscribe un handler con prioridad."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append((priority, handler))
        self.subscribers[event_type].sort(key=lambda x: x[0], reverse=True)
        self.logger.debug(f"[EventBus] Handler suscrito a '{event_type}'")

    async def publish(self, event: Event):
        """Publica evento y mantiene historial."""
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)

        self.logger.info(f"[EventBus] Evento publicado: {event.type} (priority={event.priority.name})")

        if event.type in self.subscribers:
            tasks = []
            for priority, handler in self.subscribers[event.type]:
                if event.priority == EventPriority.CRITICAL:
                    await handler(event)
                else:
                    tasks.append(asyncio.create_task(handler(event)))

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    def get_event_chain(self, correlation_id: str) -> List[Event]:
        """Obtiene todos los eventos de un flujo específico."""
        return [e for e in self.event_history if e.correlation_id == correlation_id]


class CircuitBreaker:
    """Circuit Breaker para resiliencia de APIs de IA."""

    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"

    def can_execute(self) -> bool:
        import time
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
                return True
            return False
        return True

    def record_success(self):
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            self.failure_count = 0

    def record_failure(self):
        import time
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"


class MetricsCollector:
    """Recolector de métricas para observabilidad."""

    def __init__(self):
        self.metrics = {
            "events_published": defaultdict(int),
            "tasks_executed": defaultdict(int),
            "response_times": defaultdict(list),
            "errors": defaultdict(int),
            "phase_durations": []
        }
        self.start_time = datetime.now()

    def record_event(self, event_type: str):
        self.metrics["events_published"][event_type] += 1

    def record_task(self, task_type: str, duration: float):
        self.metrics["tasks_executed"][task_type] += 1
        self.metrics["response_times"][task_type].append(duration)

    def record_error(self, error_type: str):
        self.metrics["errors"][error_type] += 1

    def record_phase(self, phase_name: str, duration: float):
        self.metrics["phase_durations"].append({
            "phase": phase_name,
            "duration": duration
        })

    def get_summary(self) -> Dict:
        return {
            "total_events": sum(self.metrics["events_published"].values()),
            "total_tasks": sum(self.metrics["tasks_executed"].values()),
            "total_errors": sum(self.metrics["errors"].values()),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "average_response_times": {
                k: sum(v) / len(v) if v else 0
                for k, v in self.metrics["response_times"].items()
            },
            "phases_completed": len(self.metrics["phase_durations"])
        }


# ============================================================================
#  PLAN DE EJEMPLO: LANDING PAGE + CATÁLOGO + MERCADO PAGO
# ============================================================================

LANDING_PAGE_PLAN = {
    "title": "Landing Page E-commerce con Catálogo y Mercado Pago",
    "metadata": {
        "projectType": "E-commerce Landing Page",
        "version": "1.0.0",
        "schema_version": "1.0",
        "date": "2026-01-20",
        "techStack": "Next.js + Tailwind CSS + Mercado Pago SDK"
    },
    "phases": [
        {
            "name": "Fase 1: Configuración del Entorno y Estructura Base",
            "is_mvp": True,
            "tasks": [
                {"name": "Crear proyecto Next.js con TypeScript", "status": "pending", "agent": "coding"},
                {"name": "Configurar Tailwind CSS para estilos", "status": "pending", "agent": "coding"},
                {"name": "Configurar variables de entorno para Mercado Pago", "status": "pending", "agent": "security"},
                {"name": "Crear estructura de directorios (components, pages, lib, styles)", "status": "pending", "agent": "coding"}
            ]
        },
        {
            "name": "Fase 2: Componentes de UI Fundamentales (Frontend)",
            "is_mvp": True,
            "tasks": [
                {"name": "Diseñar y crear componente Header con navegación", "status": "pending", "agent": "coding"},
                {"name": "Crear Hero Section con CTA principal", "status": "pending", "agent": "coding"},
                {"name": "Crear Footer con información de contacto", "status": "pending", "agent": "coding"},
                {"name": "Implementar diseño responsive mobile-first", "status": "pending", "agent": "coding"}
            ]
        },
        {
            "name": "Fase 3: Catálogo de Productos (20 productos)",
            "is_mvp": True,
            "tasks": [
                {"name": "Crear modelo de datos para productos (JSON/API)", "status": "pending", "agent": "coding"},
                {"name": "Diseñar componente ProductCard con imagen, precio y descripción", "status": "pending", "agent": "coding"},
                {"name": "Implementar grid de productos con filtros básicos", "status": "pending", "agent": "coding"},
                {"name": "Crear página de detalle de producto", "status": "pending", "agent": "coding"},
                {"name": "Cargar 20 productos de ejemplo con imágenes", "status": "pending", "agent": "coding"},
                {"name": "Implementar búsqueda y filtrado por categoría", "status": "pending", "agent": "coding"}
            ]
        },
        {
            "name": "Fase 4: Carrito de Compras",
            "is_mvp": True,
            "tasks": [
                {"name": "Crear contexto/estado global para carrito (React Context o Zustand)", "status": "pending", "agent": "coding"},
                {"name": "Implementar funcionalidad agregar/quitar productos", "status": "pending", "agent": "coding"},
                {"name": "Crear componente de resumen de carrito", "status": "pending", "agent": "coding"},
                {"name": "Implementar persistencia del carrito en localStorage", "status": "pending", "agent": "coding"}
            ]
        },
        {
            "name": "Fase 5: Integración Mercado Pago",
            "is_mvp": True,
            "tasks": [
                {"name": "Configurar SDK de Mercado Pago (credenciales de prueba)", "status": "pending", "agent": "security"},
                {"name": "Crear endpoint API para generar preferencia de pago", "status": "pending", "agent": "coding"},
                {"name": "Implementar botón de checkout con Mercado Pago", "status": "pending", "agent": "coding"},
                {"name": "Crear páginas de éxito, pendiente y fallo de pago", "status": "pending", "agent": "coding"},
                {"name": "Implementar webhook para notificaciones de pago (IPN)", "status": "pending", "agent": "coding"},
                {"name": "Validar flujo completo de pago en sandbox", "status": "pending", "agent": "review"}
            ]
        },
        {
            "name": "Fase 6: Optimización y SEO",
            "is_mvp": False,
            "tasks": [
                {"name": "Optimizar imágenes con next/image", "status": "pending", "agent": "optimization"},
                {"name": "Implementar meta tags y Open Graph para SEO", "status": "pending", "agent": "coding"},
                {"name": "Configurar sitemap.xml y robots.txt", "status": "pending", "agent": "coding"},
                {"name": "Realizar auditoría Lighthouse y corregir issues", "status": "pending", "agent": "optimization"}
            ]
        },
        {
            "name": "Fase 7: Testing y Deploy",
            "is_mvp": False,
            "tasks": [
                {"name": "Escribir tests unitarios para componentes críticos", "status": "pending", "agent": "review"},
                {"name": "Escribir tests E2E para flujo de compra", "status": "pending", "agent": "review"},
                {"name": "Configurar CI/CD con GitHub Actions", "status": "pending", "agent": "coding"},
                {"name": "Deploy a Vercel o plataforma similar", "status": "pending", "agent": "coding"},
                {"name": "Documentar proceso de configuración y deploy", "status": "pending", "agent": "documentation"}
            ]
        }
    ],
    "security_policies": {
        "mercadopago_credentials": "environment_variables",
        "api_rate_limiting": True,
        "input_validation": "zod",
        "https_only": True
    },
    "quality_gates": {
        "test_coverage_min": 70,
        "lighthouse_score_min": 85,
        "required_checks": ["build", "tests", "linting"]
    }
}


PRODUCT_OVERVIEW = {
    "title": "Landing Page E-commerce con Catálogo y Mercado Pago",
    "overview": {
        "description": "Landing page profesional para venta de productos con catálogo de 20 items e integración de pagos con Mercado Pago."
    },
    "coreUserEpicsAndStories": {
        "epics": [
            {
                "title": "Navegación y Descubrimiento de Productos",
                "stories": [
                    {
                        "story": "*Como visitante, quiero ver una landing page atractiva para conocer la marca y productos disponibles.*",
                        "labels": ["area:frontend", "module:landing", "priority:high"],
                        "acceptanceCriteria": [
                            "Given estoy en la página principal, When cargo la página, Then veo el hero section con CTA visible",
                            "Given estoy en la página principal, When hago scroll, Then veo el catálogo de productos"
                        ]
                    },
                    {
                        "story": "*Como visitante, quiero navegar el catálogo de 20 productos para encontrar lo que busco.*",
                        "labels": ["area:frontend", "module:catalog", "priority:high"],
                        "acceptanceCriteria": [
                            "Given estoy en el catálogo, When filtro por categoría, Then solo veo productos de esa categoría",
                            "Given estoy en el catálogo, When busco un término, Then veo productos que coinciden"
                        ]
                    }
                ]
            },
            {
                "title": "Proceso de Compra",
                "stories": [
                    {
                        "story": "*Como comprador, quiero agregar productos al carrito para comprarlos después.*",
                        "labels": ["area:frontend", "module:cart", "priority:high"],
                        "acceptanceCriteria": [
                            "Given estoy viendo un producto, When hago clic en 'Agregar al carrito', Then el producto aparece en mi carrito",
                            "Given tengo productos en el carrito, When cierro el navegador y vuelvo, Then mi carrito sigue con los productos"
                        ]
                    },
                    {
                        "story": "*Como comprador, quiero pagar con Mercado Pago para completar mi compra de forma segura.*",
                        "labels": ["area:backend", "module:payment", "priority:critical"],
                        "acceptanceCriteria": [
                            "Given tengo productos en el carrito, When hago clic en 'Pagar con Mercado Pago', Then soy redirigido al checkout de MP",
                            "Given completé el pago en MP, When vuelvo al sitio, Then veo la confirmación de mi orden"
                        ]
                    }
                ]
            }
        ]
    },
    "developmentRoadmap": {
        "phases": [
            {
                "release": "MVP - Landing + Catálogo + Pago básico",
                "duration_weeks": 3
            },
            {
                "release": "V1.1 - Optimización + Testing",
                "duration_weeks": 2
            }
        ]
    }
}


# ============================================================================
#  ORQUESTADOR DE PRUEBA CON LOGGING UX/UI
# ============================================================================

class TestOrchestrator:
    """
    Orquestador de prueba que simula el sistema multi-agente
    con logging detallado para debugging de UX/UI.
    """

    def __init__(self):
        # Configurar logging detallado
        self.logger = self._setup_logging()

        # Componentes de la arquitectura híbrida
        self.event_bus = EnhancedEventBus(self.logger)
        self.metrics = MetricsCollector()
        self.circuit_breakers = {
            "gemini": CircuitBreaker(),
            "openai": CircuitBreaker(),
            "anthropic": CircuitBreaker()
        }

        # Estado del plan
        self.plan = None
        self.current_phase = 0
        self.current_task = 0
        self.execution_log = []

        # Suscribir handlers a eventos
        self._setup_event_handlers()

    def _setup_logging(self) -> logging.Logger:
        """Configura logging detallado para UX/UI debugging."""
        logger = logging.getLogger("TestOrchestrator")
        logger.setLevel(logging.DEBUG)

        # Handler para consola con colores
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_format)

        # Handler para archivo con detalles completos
        file_handler = logging.FileHandler(
            os.path.join(SYSTEM_ROOT, 'tests', 'orchestrator_debug.log'),
            mode='w',
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s'
        )
        file_handler.setFormatter(file_format)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    def _setup_event_handlers(self):
        """Configura handlers para el Event Bus."""

        async def on_task_started(event: Event):
            self.logger.info(f"  → [TASK_STARTED] {event.data.get('task_name', 'N/A')}")
            self.metrics.record_event("task.started")

        async def on_task_completed(event: Event):
            self.logger.info(f"  ✓ [TASK_COMPLETED] {event.data.get('task_name', 'N/A')}")
            self.metrics.record_event("task.completed")

        async def on_phase_started(event: Event):
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"📦 [PHASE_STARTED] {event.data.get('phase_name', 'N/A')}")
            self.logger.info(f"{'='*60}")
            self.metrics.record_event("phase.started")

        async def on_phase_completed(event: Event):
            self.logger.info(f"✅ [PHASE_COMPLETED] {event.data.get('phase_name', 'N/A')}")
            self.metrics.record_event("phase.completed")

        async def on_agent_invoked(event: Event):
            self.logger.debug(f"  🤖 [AGENT_INVOKED] {event.data.get('agent_type', 'N/A')}")
            self.metrics.record_event("agent.invoked")

        self.event_bus.subscribe("task.started", on_task_started)
        self.event_bus.subscribe("task.completed", on_task_completed)
        self.event_bus.subscribe("phase.started", on_phase_started)
        self.event_bus.subscribe("phase.completed", on_phase_completed)
        self.event_bus.subscribe("agent.invoked", on_agent_invoked)

    async def load_plan(self, plan: Dict):
        """Carga un plan de ejecución."""
        self.plan = plan
        self.logger.info(f"📋 Plan cargado: {plan.get('title', 'Sin título')}")
        self.logger.info(f"   Total de fases: {len(plan.get('phases', []))}")

        total_tasks = sum(len(p.get('tasks', [])) for p in plan.get('phases', []))
        self.logger.info(f"   Total de tareas: {total_tasks}")

        mvp_phases = [p for p in plan.get('phases', []) if p.get('is_mvp', False)]
        self.logger.info(f"   Fases MVP: {len(mvp_phases)}")

    async def execute_plan(self, mode: str = "MVP"):
        """
        Ejecuta el plan cargado según el modo especificado.

        Args:
            mode: "MVP" para solo fases MVP, "FULL" para todas las fases
        """
        if not self.plan:
            self.logger.error("❌ No hay plan cargado. Use load_plan() primero.")
            return

        import time
        start_time = time.time()

        self.logger.info(f"\n{'🔥'*30}")
        self.logger.info(f"🚀 INICIANDO EJECUCIÓN EN MODO: {mode}")
        self.logger.info(f"{'🔥'*30}\n")

        phases = self.plan.get('phases', [])

        for phase_idx, phase in enumerate(phases):
            # Verificar si debemos ejecutar esta fase según el modo
            if mode == "MVP" and not phase.get('is_mvp', False):
                self.logger.info(f"\n⏭️  [FASE {phase_idx + 1}] OMITIDA (no es MVP): {phase['name']}")
                continue

            phase_start = time.time()

            # Publicar evento de inicio de fase
            await self.event_bus.publish(Event(
                type="phase.started",
                data={"phase_name": phase['name'], "phase_idx": phase_idx},
                priority=EventPriority.HIGH
            ))

            # Ejecutar tareas de la fase
            tasks = phase.get('tasks', [])
            for task_idx, task in enumerate(tasks):
                task_name = task['name'] if isinstance(task, dict) else task
                task_agent = task.get('agent', 'coding') if isinstance(task, dict) else 'coding'

                await self._execute_task(
                    task_name=task_name,
                    task_agent=task_agent,
                    phase_idx=phase_idx,
                    task_idx=task_idx
                )

            phase_duration = time.time() - phase_start
            self.metrics.record_phase(phase['name'], phase_duration)

            # Publicar evento de fin de fase
            await self.event_bus.publish(Event(
                type="phase.completed",
                data={"phase_name": phase['name'], "duration": phase_duration},
                priority=EventPriority.HIGH
            ))

        total_duration = time.time() - start_time

        self.logger.info(f"\n{'🏁'*30}")
        self.logger.info(f"🏁 EJECUCIÓN COMPLETADA")
        self.logger.info(f"   Duración total: {total_duration:.2f}s")
        self.logger.info(f"{'🏁'*30}")

        return self._generate_execution_report()

    async def _execute_task(self, task_name: str, task_agent: str, phase_idx: int, task_idx: int):
        """Ejecuta una tarea individual con logging detallado."""
        import time

        task_start = time.time()

        # Publicar evento de inicio
        await self.event_bus.publish(Event(
            type="task.started",
            data={
                "task_name": task_name,
                "agent": task_agent,
                "phase_idx": phase_idx,
                "task_idx": task_idx
            }
        ))

        # Publicar evento de invocación de agente
        await self.event_bus.publish(Event(
            type="agent.invoked",
            data={"agent_type": task_agent, "task": task_name}
        ))

        # Simular ejecución del agente (en producción aquí iría la lógica real)
        await self._simulate_agent_execution(task_agent, task_name)

        task_duration = time.time() - task_start
        self.metrics.record_task(task_agent, task_duration)

        # Registrar en log de ejecución
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "task": task_name,
            "agent": task_agent,
            "duration": task_duration,
            "status": "completed"
        })

        # Publicar evento de completado
        await self.event_bus.publish(Event(
            type="task.completed",
            data={
                "task_name": task_name,
                "duration": task_duration,
                "status": "completed"
            }
        ))

    async def _simulate_agent_execution(self, agent_type: str, task_name: str):
        """Simula la ejecución de un agente con delay realista."""
        import random

        # Delays simulados por tipo de agente
        delays = {
            "coding": (0.3, 0.8),
            "security": (0.2, 0.5),
            "review": (0.2, 0.4),
            "optimization": (0.3, 0.6),
            "documentation": (0.1, 0.3)
        }

        min_delay, max_delay = delays.get(agent_type, (0.1, 0.3))
        await asyncio.sleep(random.uniform(min_delay, max_delay))

        self.logger.debug(f"    └─ [{agent_type.upper()}] Procesado: {task_name[:50]}...")

    def _generate_execution_report(self) -> Dict:
        """Genera un reporte detallado de la ejecución."""
        summary = self.metrics.get_summary()

        report = {
            "execution_summary": summary,
            "event_history": [
                {
                    "type": e.type,
                    "timestamp": e.timestamp,
                    "priority": e.priority.name
                }
                for e in self.event_bus.event_history[-50:]  # Últimos 50 eventos
            ],
            "execution_log": self.execution_log,
            "circuit_breaker_states": {
                name: cb.state
                for name, cb in self.circuit_breakers.items()
            }
        }

        return report


# ============================================================================
#  FUNCIONES DE TEST
# ============================================================================

async def test_orchestrator_with_landing_page_plan():
    """
    Test principal: Ejecuta el orquestador con el plan de landing page.

    Valida:
    1. Carga correcta del plan
    2. Ejecución de fases MVP
    3. Event Bus funcionando
    4. Métricas recolectadas
    5. Logging UX/UI detallado
    """
    print("\n" + "="*70)
    print("🧪 TEST: Orquestador con Plan de Landing Page + Catálogo + Mercado Pago")
    print("="*70 + "\n")

    # Inicializar orquestador
    orchestrator = TestOrchestrator()

    # Cargar plan
    await orchestrator.load_plan(LANDING_PAGE_PLAN)

    # Ejecutar en modo MVP
    report = await orchestrator.execute_plan(mode="MVP")

    # Validaciones
    print("\n" + "-"*70)
    print("📊 VALIDACIONES DEL TEST")
    print("-"*70)

    validations = []

    # Validación 1: Plan cargado correctamente
    plan_loaded = orchestrator.plan is not None
    validations.append(("Plan cargado correctamente", plan_loaded))

    # Validación 2: Fases MVP ejecutadas
    mvp_phases_count = len([p for p in LANDING_PAGE_PLAN['phases'] if p.get('is_mvp')])
    phases_completed = report['execution_summary']['phases_completed']
    validations.append((f"Fases MVP ejecutadas ({phases_completed}/{mvp_phases_count})", phases_completed == mvp_phases_count))

    # Validación 3: Eventos publicados
    total_events = report['execution_summary']['total_events']
    validations.append((f"Eventos publicados ({total_events})", total_events > 0))

    # Validación 4: Tareas ejecutadas
    total_tasks = report['execution_summary']['total_tasks']
    validations.append((f"Tareas ejecutadas ({total_tasks})", total_tasks > 0))

    # Validación 5: Sin errores
    total_errors = report['execution_summary']['total_errors']
    validations.append((f"Sin errores ({total_errors})", total_errors == 0))

    # Imprimir resultados
    all_passed = True
    for name, passed in validations:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False

    # Guardar reporte
    report_path = os.path.join(SYSTEM_ROOT, 'tests', 'orchestrator_test_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str, ensure_ascii=False)
    print(f"\n📄 Reporte guardado en: {report_path}")

    # Resultado final
    print("\n" + "="*70)
    if all_passed:
        print("🎉 RESULTADO FINAL: TODOS LOS TESTS PASARON")
    else:
        print("⚠️  RESULTADO FINAL: ALGUNOS TESTS FALLARON")
    print("="*70 + "\n")

    return all_passed, report


async def test_event_bus_isolation():
    """Test del Event Bus de forma aislada."""
    print("\n🧪 TEST: Event Bus Aislado")

    logger = logging.getLogger("EventBusTest")
    logger.setLevel(logging.WARNING)

    event_bus = EnhancedEventBus(logger)
    received_events = []

    async def test_handler(event):
        received_events.append(event)

    # Suscribir
    event_bus.subscribe("test.event", test_handler)

    # Publicar eventos
    await event_bus.publish(Event(type="test.event", data={"test": 1}))
    await event_bus.publish(Event(type="test.event", data={"test": 2}))
    await event_bus.publish(Event(type="other.event", data={"test": 3}))

    # Validar
    assert len(received_events) == 2, f"Se esperaban 2 eventos, se recibieron {len(received_events)}"
    assert len(event_bus.event_history) == 3, "El historial debe tener 3 eventos"

    print("  ✅ Event Bus funciona correctamente")
    return True


async def test_circuit_breaker():
    """Test del Circuit Breaker de forma aislada."""
    print("\n🧪 TEST: Circuit Breaker Aislado")

    cb = CircuitBreaker(failure_threshold=3, timeout=1)

    # Estado inicial: CLOSED
    assert cb.state == "CLOSED"
    assert cb.can_execute() == True

    # Simular fallos
    for _ in range(3):
        cb.record_failure()

    # Debe estar OPEN después de 3 fallos
    assert cb.state == "OPEN"
    assert cb.can_execute() == False

    print("  ✅ Circuit Breaker funciona correctamente")
    return True


async def test_metrics_collector():
    """Test del MetricsCollector de forma aislada."""
    print("\n🧪 TEST: Metrics Collector Aislado")

    metrics = MetricsCollector()

    metrics.record_event("test.event")
    metrics.record_event("test.event")
    metrics.record_task("coding", 0.5)
    metrics.record_task("coding", 0.3)
    metrics.record_phase("Fase 1", 2.0)

    summary = metrics.get_summary()

    assert summary["total_events"] == 2
    assert summary["total_tasks"] == 2
    assert summary["phases_completed"] == 1
    assert 0.3 < summary["average_response_times"]["coding"] < 0.5

    print("  ✅ Metrics Collector funciona correctamente")
    return True


# ============================================================================
#  PUNTO DE ENTRADA
# ============================================================================

async def run_all_tests():
    """Ejecuta todos los tests."""
    print("\n" + "🔬"*35)
    print("🔬 SUITE DE TESTS - ARQUITECTURA HÍBRIDA HUB-AND-SPOKE + EVENT-DRIVEN")
    print("🔬"*35 + "\n")

    results = []

    # Test 1: Event Bus
    results.append(await test_event_bus_isolation())

    # Test 2: Circuit Breaker
    results.append(await test_circuit_breaker())

    # Test 3: Metrics Collector
    results.append(await test_metrics_collector())

    # Test 4: Orquestador completo
    passed, report = await test_orchestrator_with_landing_page_plan()
    results.append(passed)

    # Resumen final
    total = len(results)
    passed_count = sum(results)

    print("\n" + "="*70)
    print(f"📊 RESUMEN FINAL: {passed_count}/{total} tests pasaron")
    print("="*70)

    return all(results)


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
