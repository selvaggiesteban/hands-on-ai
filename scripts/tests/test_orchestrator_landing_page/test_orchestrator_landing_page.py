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