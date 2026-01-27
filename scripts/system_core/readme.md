---
name: project-initializer
type: core-script
language: python
description: "Orquestador inteligente para instanciar nuevos proyectos operativos. Duplica y personaliza la plantilla 'project_meta', inyectando referencias a agentes, skills y checklists basados en matrices de auditoría."
tags: [orchestration, scaffolding, project-management, automation, json]
---

# Project Initializer & Orchestrator

Este script es el corazón de la inicialización de operaciones en el sistema Hands-On AI.

## Función Principal
Transforma la plantilla estática `skills/marketing/project_meta` (ahora en formato JSON puro) en una instancia viva de proyecto, personalizada con los datos del contexto actual.

## Capacidades
1.  **Duplicación de Estructura:** Clona la arquitectura de carpetas y JSONs de la plantilla.
2.  **Inyección de Contexto:** Reemplaza variables `{{placeholder}}` en todos los archivos JSON con datos reales (Cliente, Fechas, Stacks).
3.  **Razonamiento de Recursos:** (En desarrollo) Consulta las matrices de auditoría para recomendar automáticamente qué Agentes y Skills son necesarios para el objetivo declarado.

## Uso
Importar la clase `ProjectOrchestrator` y ejecutar `initialize_project()` con un diccionario de contexto.