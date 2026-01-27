---
name: test_full_pipeline_all_agents
type: script
language: python
description: "Ejecuta el pipeline completo en modo FULL para validar la efectividad y velocidad de la arquitectura multi-agente híbrida, incluyendo todos los agentes: Planning, Coding, Security, Review, Optimization, Documentation y Orchestrator."
tags: [pipeline, agents, testing, full-stack, automation]
---

# Test del Pipeline Completo con TODOS los Agentes

Este script ejecuta una simulación completa de la arquitectura multi-agente, validando la interacción entre todos los componentes y agentes disponibles.

## Funcionalidades Principales

*   **Configuración Multi-Modelo:** Soporte para Anthropic, OpenAI, Google, DeepSeek y Groq.
*   **Orquestación Completa:** Coordina la ejecución de tareas a través de múltiples agentes.
*   **Router Inteligente:** Selecciona el modelo más adecuado según la complejidad y tipo de tarea.
*   **Desarrollo Recursivo:** Implementa ciclos de mejora continua y refinamiento de tareas.
*   **Logging y Métricas:** Genera reportes detallados de rendimiento y uso de modelos.

## Archivos

*   [test_full_pipeline_all_agents.py](./test_full_pipeline_all_agents.py): Script principal de ejecución del test.
