---
name: maintenance-tools
type: script-collection
language: python
description: "Colección de scripts para el mantenimiento, validación y generación de documentación del proyecto. Incluye herramientas para RAD (Recursive Agent Development) y verificación de integridad."
tags: [maintenance, validation, documentation, automation, rad]
---

# Herramientas de Mantenimiento

Este directorio contiene scripts críticos para la salud y operación del repositorio.

## Scripts Principales

*   **check_links.py:** Verifica la validez de los enlaces internos en la documentación.
*   **generate_kb_index.py:** Genera índices para la base de conocimientos.
*   **generate_tech_docs.py:** Automatiza la creación de documentación técnica.
*   **validate_kb.py:** Valida la estructura y contenido de la Knowledge Base.
*   **validate_project.py:** Herramienta principal de auditoría del proyecto.

## Subdirectorios

### RAD (Recursive Agent Development)
Scripts para la migración, andamiaje y gestión de agentes y skills.
*   `migrate_*.py`: Scripts de migración de estructura.
*   `scaffolder.py`: Generador de nuevos componentes.
