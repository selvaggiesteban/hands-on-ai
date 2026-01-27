---
name: ux_test_runner
type: script
language: python
description: "Runner de pruebas de UX/UI para el orquestador CLI. Simula la interacción de un usuario ejecutando una secuencia maestra de comandos para validar la respuesta y estabilidad de la interfaz."
tags: [ux, testing, cli, automation, smoke-test]
---

# UX Test Runner

Este script automatiza la validación de la experiencia de usuario (UX) del CLI del orquestador. Ejecuta una secuencia predefinida de comandos simulando entradas de usuario y analiza la salida para confirmar que todos los menús y respuestas se muestran correctamente.

## Pruebas Realizadas

1.  Cambio de directorio raíz (`/root`).
2.  Visualización de ayuda (`/help`).
3.  Estado del sistema (`/status`).
4.  Menú de configuración (`/config`).
5.  Sincronización (`/sync`).
6.  Roadmap (`/roadmap`).
7.  Publicación y compresión (`/publish`, `/compress`).
8.  Sistema de templates (`/templates`).
9.  Inicialización (`/init`).
10. Impresión del plan (`/print`).
11. Chat básico (`/chat`).
12. Ejecución de tareas (`/run`).

## Archivos

*   [ux_test_runner.py](./ux_test_runner.py): Script de ejecución de pruebas.
