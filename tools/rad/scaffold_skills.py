import os
import re

CHAT_FILE = 'chat.txt'
BASE_DIR = 'knowledge_base'

FULL_TEMPLATE = """# [Nombre de la Tecnología]

## 📋 Contenido

- [Name](#name)
- [Overview](#overview)
- [Supported Operations](#supported-operations)
- [QA Checklist](#qa-checklist)
- [Q&A Manual/FAQs](#qa-manualfaqs)
- [Examples](#examples)

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
- **Característica 4:** Descripción
- **Característica 5:** Descripción

### Casos de Uso

1. **Caso de uso 1:** [Descripción]
2. **Caso de uso 2:** [Descripción]
3. **Caso de uso 3:** [Descripción]

### Ventajas

✅ Ventaja 1  
✅ Ventaja 2  
✅ Ventaja 3  

### Desventajas

❌ Desventaja 1  
❌ Desventaja 2  
❌ Desventaja 3  

---

## ⚙️ Supported Operations

### Escalabilidad (Scalability)

**Opciones de escalado:**
- Horizontal: [Descripción]
- Vertical: [Descripción]
- Auto-scaling: [Descripción]

**Límites:**
- Conexiones concurrentes: [Número]
- Throughput: [Número]
- Storage: [Número]

### Opciones de Ejecución (Execution Options)

**Ambientes soportados:**
- [ ] Local development
- [ ] Docker containers
- [ ] Kubernetes
- [ ] Serverless
- [ ] Cloud-managed

**Comandos principales:**
```bash
# Desarrollo
[comando start]

# Producción
[comando production]

# Tests
[comando test]
```

### Conectividad (Connectivity)

**Protocolos soportados:**
- HTTP/HTTPS
- WebSockets
- gRPC
- GraphQL
- [Otros]

**Integraciones:**
- Databases: [Lista]
- Authentication: [Lista]
- Messaging: [Lista]
- Storage: [Lista]

### Comportamiento (Behavior)

**Modelo de ejecución:**
- Síncrono / Asíncrono
- Bloqueante / No bloqueante
- Single-threaded / Multi-threaded

**Patrones de diseño recomendados:**
1. [Patrón 1]
2. [Patrón 2]
3. [Patrón 3]

### Dependencias (Dependencies)

**Dependencias principales:**
```json
{
  "dependency1": "version",
  "dependency2": "version",
  "dependency3": "version"
}
```

**Dependencias de desarrollo:**
```json
{
  "dev-dependency1": "version",
  "dev-dependency2": "version"
}
```

### Entregables (Deliverables)

**Artefactos generados:**
- [ ] Código fuente
- [ ] Binarios compilados
- [ ] Docker images
- [ ] Documentación
- [ ] Tests
- [ ] Configuraciones

**Estructura de proyecto:**
```
project/
├── src/
├── tests/
├── docs/
├── config/
└── README.md
```

### Roles (Roles)

**Roles del equipo:**

1. **Developer**
   - Responsabilidades: [Lista]
   - Skills requeridas: [Lista]

2. **DevOps Engineer**
   - Responsabilidades: [Lista]
   - Skills requeridas: [Lista]

3. **QA Engineer**
   - Responsabilidades: [Lista]
   - Skills requeridas: [Lista]

---

## ✅ QA Checklist

### Pre-development

- [ ] Revisar requisitos del proyecto
- [ ] Validar compatibilidad de versiones
- [ ] Configurar ambiente de desarrollo
- [ ] Instalar dependencias
- [ ] Configurar linters y formatters

### Durante desarrollo

- [ ] Seguir convenciones de código
- [ ] Escribir tests unitarios
- [ ] Documentar funciones complejas
- [ ] Realizar code review
- [ ] Ejecutar linters

### Pre-producción

- [ ] Todos los tests pasan
- [ ] Code coverage > 80%
- [ ] Sin vulnerabilidades críticas
- [ ] Performance optimizada
- [ ] Documentación actualizada
- [ ] Logs configurados
- [ ] Monitoring configurado

### Post-deployment

- [ ] Health checks activos
- [ ] Monitoring activo
- [ ] Logs centralizados
- [ ] Backups configurados
- [ ] Rollback plan definido

---

## ❓ Q&A Manual/FAQs

### Instalación y Setup

**Q: ¿Cómo instalo [Nombre oficial]?**  
A: [Respuesta detallada]

**Q: ¿Qué versión debo usar?**  
A: [Respuesta detallada]

**Q: ¿Requisitos mínimos del sistema?**  
A: [Respuesta detallada]

### Desarrollo

**Q: ¿Cómo estructuro mi proyecto?**  
A: [Respuesta detallada]

**Q: ¿Cuáles son las mejores prácticas?**  
A: [Respuesta detallada]

**Q: ¿Cómo manejo errores?**  
A: [Respuesta detallada]

### Testing

**Q: ¿Qué framework de testing usar?**  
A: [Respuesta detallada]

**Q: ¿Cómo escribo buenos tests?**  
A: [Respuesta detallada]

**Q: ¿Qué cobertura es suficiente?**  
A: [Respuesta detallada]

### Producción

**Q: ¿Cómo despliego a producción?**  
A: [Respuesta detallada]

**Q: ¿Cómo monitoreo la aplicación?**  
A: [Respuesta detallada]

**Q: ¿Estrategias de escalado?**  
A: [Respuesta detallada]

### Troubleshooting

**Q: Error común 1**  
A: [Solución]

**Q: Error común 2**  
A: [Solución]

**Q: Error común 3**  
A: [Solución]

---

## 💡 Examples

### Ejemplo 1: Uso básico

**Descripción:** [Qué hace este ejemplo]

**Código:**
```bash
# Código del ejemplo
[código completo y funcional]
```

**Explicación:**
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

**Resultado esperado:**
```
[Output]
```

---


### Ejemplo 2: Uso intermedio

**Descripción:** [Qué hace este ejemplo]

**Código:**
```bash
# Código del ejemplo
[código completo y funcional]
```

**Explicación:**
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

**Resultado esperado:**
```
[Output]
```

---


### Ejemplo 3: Uso avanzado

**Descripción:** [Qué hace este ejemplo]

**Código:**
```bash
# Código del ejemplo
[código completo y funcional]
```

**Explicación:**
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

**Resultado esperado:**
```
[Output]
```

---

## 📚 Referencias

- [Documentación oficial](https://ejemplo.com)
- [Guía de mejores prácticas](https://ejemplo.com)
"""

def parse_chat_file():
    # Only parsing skills list now, not template
    if not os.path.exists(CHAT_FILE):
        print(f"Error: {CHAT_FILE} not found.")
        return []

    # Read chat file logic (simplified to just get skills)
    # This relies on the previous logic being sound for extracting skills
    # We will just re-implement the skill extraction part
    
    with open(CHAT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('## 📚 ESTRUCTURA README.MD PARA CADA TECNOLOGÍA')
    skills_content = parts[0]
    
    lines = skills_content.split('\n')
    current_path = None
    current_category = "General"
    skills = []
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if line.startswith('### '):
            path_match = re.search(r'`(.*?)`', line)
            if path_match:
                current_path = path_match.group(1).strip()
                if current_path.endswith('/'): current_path = current_path[:-1]
                
                pre_path = line.split('`')[0].replace('###', '').strip()
                pre_path = re.sub(r'\(\d+\)\s*-?', '', pre_path).strip()
                pre_path = pre_path.replace('-', ' ').strip()
                
                if pre_path:
                    current_category = pre_path
                else:
                    if 'generic' in current_path: current_category = "Generic"
                    elif 'automation' in current_path: current_category = "Automation"
                    else: current_category = current_path.split('/')[-1].capitalize()
                    
        if re.match(r'^\d+\.', line):
            item_match = re.match(r'^\d+\.\s*\*\*(.*?)/?\*\*\s*-\s*(.*)', line)
            if item_match and current_path:
                folder_name = item_match.group(1).strip()
                if folder_name.endswith('/'): folder_name = folder_name[:-1]
                description = item_match.group(2).strip()
                
                skills.append({
                    'path': current_path,
                    'folder': folder_name,
                    'description': description,
                    'category': current_category
                })
    return skills

def create_skills(skills):
    print(f"Found {len(skills)} skills to create.")
    
    created_count = 0
    for skill in skills:
        full_path = os.path.join(BASE_DIR, skill['path'], skill['folder'])
        os.makedirs(full_path, exist_ok=True)
        readme_path = os.path.join(full_path, 'README.md')
        
        # Customize template
        content = FULL_TEMPLATE.replace('[Nombre de la Tecnología]', skill['description'])
        content = content.replace('[Nombre oficial]', skill['description'])
        content = content.replace('[Categoría]', skill['category'])
        content = content.replace('[Stack]', skill['category'])
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        created_count += 1
                
    print(f"Successfully created/updated {created_count} README files.")

if __name__ == "__main__":
    skills = parse_chat_file()
    if skills:
        create_skills(skills)
    else:
        print("Failed to parse skills.")