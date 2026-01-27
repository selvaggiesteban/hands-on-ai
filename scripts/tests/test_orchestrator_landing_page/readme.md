---
name: test_orchestrator_landing_page
type: script
language: python
description: "Valida la arquitectura Hub-and-Spoke + Event-Driven del orquestador mediante un caso de uso práctico: creación de una Landing Page de E-commerce con catálogo y Mercado Pago."
tags: [orchestrator, event-driven, architecture, testing, integration]
---

# Test del Orquestador Principal - Caso Landing Page

Script de prueba para validar la correcta orquestación de tareas en un flujo complejo de desarrollo de software, simulando una arquitectura basada en eventos y un enfoque Hub-and-Spoke.

## Caso de Uso
Validación de una **Landing Page de E-commerce** con:
*   Catálogo de 20 productos.
*   Integración de pasarela de pagos (Mercado Pago).

## Componentes Probados
*   **EnhancedEventBus:** Sistema de mensajería con prioridades.
*   **CircuitBreaker:** Mecanismo de resiliencia para llamadas a APIs.
*   **MetricsCollector:** Sistema de observabilidad y métricas.
*   **Orquestador:** Lógica central de distribución y seguimiento de tareas.

## Archivos
*   [test_orchestrator_landing_page.py](./test_orchestrator_landing_page.py): Código fuente del test.
