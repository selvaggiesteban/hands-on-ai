import os
import re

BASE_DIR = 'knowledge_base/technologies'

TEMPLATE_MASTER = """# [Nombre de la Tecnología]

## 📋 Contenido

- [Name](#name)
- [Overview](#overview)
- [Supported Operations](#supported-operations)
- [QA Checklist](#qa-checklist)
- [Q&A Manual/FAQs](#qa-manualfaqs)
- [Examples & Capabilities (Skills)](#examples--capabilities-skills)
- [Referencias](#referencias)

---

## 🏷️ Name

**Nombre oficial:** [Nombre oficial]
**Categoría:** [Categoría]
**Stack:** [Stack]

---

## 📖 Overview

### ¿Qué es?

[Descripción breve de la tecnología - 2-3 párrafos]

### Características Principales

- **Característica 1:** Descripción
- **Característica 2:** Descripción
- **Característica 3:** Descripción

---

## ⚙️ Supported Operations

### Escalabilidad (Scalability)

**Opciones de escalado:**
- Horizontal: [Descripción]
- Vertical: [Descripción]

### Opciones de Ejecución (Execution Options)

**Ambientes soportados:**
- [ ] Local development
- [ ] Docker containers

### Conectividad (Connectivity)

**Protocolos soportados:**
- HTTP/HTTPS

### Comportamiento (Behavior)

**Modelo de ejecución:**
- Síncrono / Asíncrono

### Dependencias (Dependencies)

**Dependencias principales:**
```json
{
  "dependency1": "version"
}
```

### Entregables (Deliverables)

**Artefactos generados:**
- [ ] Código fuente

### Roles (Roles)

**Roles del equipo:**
1. **Developer**
2. **DevOps Engineer**

---

## ✅ QA Checklist

### Pre-development
- [ ] Revisar requisitos

---

## ❓ Q&A Manual/FAQs

### Instalación
**Q: ¿Cómo instalo [Nombre oficial]?**
A: [Respuesta]

---

## 💡 Examples & Capabilities (Skills)

Esta tecnología cuenta con las siguientes capacidades especializadas (Skills):

- [Sin skills registradas actualmente]

---

## 📚 Referencias

- [Documentación oficial](https://ejemplo.com)
"""

def update_remaining_technologies():
    print("Updating remaining technologies to Master Template...")
    count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        if 'skills' in root:
            continue
            
        for file in files:
            if file == 'README.md':
                path = os.path.join(root, file)
                
                # Check if it needs update (simple check: missing a key section like "Examples & Capabilities")
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "Examples & Capabilities (Skills)" not in content:
                    # Needs update
                    tech_name = os.path.basename(root)
                    category = os.path.basename(os.path.dirname(root))
                    
                    new_content = TEMPLATE_MASTER.replace('[Nombre de la Tecnología]', tech_name)
                    new_content = new_content.replace('[Nombre oficial]', tech_name)
                    new_content = new_content.replace('[Categoría]', category)
                    new_content = new_content.replace('[Stack]', tech_name)
                    
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print(f"Updated: {path}")
                    count += 1
    
    print(f"Total updated: {count}")

if __name__ == "__main__":
    update_remaining_technologies()
