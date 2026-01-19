import os
import shutil
import re
import json

BASE_DIR = 'knowledge_base'
SKILLS_DIR = os.path.join(BASE_DIR, 'skills')
TECHS_DIR = os.path.join(BASE_DIR, 'technologies')
AGENTS_DIR = 'tools/agents'
CHAT2_FILE = 'chat2.txt'

STACK_TO_TECH_MAP = {
    'stacks/frontend/react': 'technologies/frontend/javascript/React',
    'stacks/frontend/vue': 'technologies/frontend/javascript/Vue',
    'stacks/frontend/angular': 'technologies/frontend/typescript/Angular',
    'stacks/frontend/nextjs': 'technologies/frontend/javascript/NextJS',
    'stacks/backend/nodejs': 'technologies/backend/javascript/Node-Express',
    'stacks/backend/python': 'technologies/backend/python/Python',
    'stacks/backend/django': 'technologies/backend/python/Django',
    'stacks/backend/go': 'technologies/backend/go/Go',
    'stacks/databases/sql': 'technologies/databases/Databases/SQL',
    'stacks/databases/nosql': 'technologies/databases/Databases/NoSQL',
    'stacks/devops': 'technologies/devops/DevOps/General',
    'stacks/cloud/aws': 'technologies/cloud/AWS/General',
    'stacks/cloud/azure': 'technologies/cloud/Azure/General',
    'stacks/cloud/gcp': 'technologies/cloud/GCP/General',
    'stacks/security': 'technologies/security/Security/General'
}

TEMPLATE_MASTER = r"""# [Nombre de la Tecnología]

## 📋 Contenido

- [Name](#name)
- [Overview](#overview)
- [Supported Operations](#supported-operations)
- [QA Checklist](#qa-checklist)
- [Q&A Manual/FAQs](#qa-manualfaqs)
- [Examples](#examples)
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

[SKILLS_LINK_SCALABILITY]

### Opciones de Ejecución (Execution Options)

**Ambientes soportados:**
- [ ] Local development
- [ ] Docker containers

### Conectividad (Connectivity)

**Protocolos soportados:**
- HTTP/HTTPS

[SKILLS_LINK_CONNECTIVITY]

### Comportamiento (Behavior)

**Modelo de ejecución:**
- Síncrono / Asíncrono

[SKILLS_LINK_BEHAVIOR]

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

[SKILLS_LINK_QA]

---

## ❓ Q&A Manual/FAQs

### Instalación
**Q: ¿Cómo instalo [Nombre oficial]?**
A: [Respuesta]

---

## 💡 Examples & Capabilities (Skills)

Esta tecnología cuenta con las siguientes capacidades especializadas (Skills):

[SKILLS_LIST]

---

## 📚 Referencias

- [Documentación oficial](https://ejemplo.com)
"""

TEMPLATE_PRACTICAL = r"""# [Nombre de la Skill]

## 📋 Información General

**Skill:** [Nombre de la Skill]
**Tecnología:** [Tecnología Padre]
**Categoría:** [Categoría]

---

## 📖 ¿Qué es?

[Definición breve y práctica de la skill]

---

## 🛠️ ¿Cómo se usa?

### Sintaxis / Comandos

```bash
# Ejemplo de uso
[comando]
```

### Pasos de Implementación

1. Paso 1
2. Paso 2
3. Paso 3

---

## ✨ Mejores Prácticas

- **Do:** [Práctica recomendada]
- **Do not:** [Práctica no recomendada]

---

## 💻 Ejemplos de Código

```[lenguaje]
// Snippet de código
function example() {
    return true;
}
```

---

## ⚠️ Errores Comunes

1. **Error:** [Descripción]
   **Solución:** [Solución]

---

## 🤖 Agentes Relacionados

Los siguientes agentes pueden asistir en la ejecución o validación de esta skill:

[AGENTS_LIST]
"""

def parse_agents(chat2_path):
    agents = []
    current_agent = {}
    
    if not os.path.exists(chat2_path):
        return []

    with open(chat2_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith('### ') and 'Agent' in line:
            if current_agent:
                agents.append(current_agent)
            current_agent = {
                'name': line.replace('###', '').strip().split('. ')[-1],
                'skills': [],
                'location': None
            }
        
        if line.startswith('**Ubicación:**'):
            try:
                loc = line.split('`')[1].strip()
                current_agent['location'] = loc
            except IndexError:
                pass

        if line.startswith('- ') and current_agent:
            skill = line.replace('- ', '').strip()
            current_agent['skills'].append(skill)

    if current_agent:
        agents.append(current_agent)
    
    return agents

def get_related_agents(skill_name, agents_db):
    related = []
    for agent in agents_db:
        if skill_name in agent['skills']:
            related.append(f"- [`{agent['name']}`](/tools/agents/{agent['name'].lower().replace(' ', '_').replace('.', '')}.py)")
    
    if not related:
        return "- No se encontraron agentes específicos vinculados directamente."
    return "\n".join(related)

def migrate_and_restructure():
    agents_db = parse_agents(CHAT2_FILE)
    print(f"Loaded {len(agents_db)} agents for linking.")

    for stack_path_rel, tech_target_rel in STACK_TO_TECH_MAP.items():
        src_path = os.path.join(BASE_DIR, stack_path_rel.replace('knowledge_base/', ''))
        src_skills = os.path.join(src_path, 'skills')
        
        if not os.path.exists(src_skills):
            continue
            
        dest_tech_root = os.path.join(BASE_DIR, tech_target_rel.replace('knowledge_base/', ''))
        dest_skills = os.path.join(dest_tech_root, 'skills')
        
        os.makedirs(dest_skills, exist_ok=True)
        
        skills_list = []
        for skill_folder in os.listdir(src_skills):
            s_src = os.path.join(src_skills, skill_folder)
            s_dest = os.path.join(dest_skills, skill_folder)
            
            if os.path.isdir(s_src):
                if os.path.exists(s_dest):
                    shutil.rmtree(s_dest)
                shutil.move(s_src, s_dest)
                skills_list.append(skill_folder)
                
                readme_path = os.path.join(s_dest, 'README.md')
                agents_link = get_related_agents(skill_folder, agents_db)
                tech_name = os.path.basename(dest_tech_root)
                
                content = TEMPLATE_PRACTICAL.replace('[Nombre de la Skill]', skill_folder)
                content = content.replace('[Tecnología Padre]', tech_name)
                content = content.replace('[Categoría]', 'Technical Skill')
                content = content.replace('[AGENTS_LIST]', agents_link)
                
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(content)

        tech_readme = os.path.join(dest_tech_root, 'README.md')
        tech_name = os.path.basename(dest_tech_root)
        
        skills_links = []
        for s in skills_list:
            skills_links.append(f"- [`{s}`](./skills/{s}/README.md)")
        
        skills_section = "\n".join(skills_links)
        
        master_content = TEMPLATE_MASTER.replace('[Nombre de la Tecnología]', tech_name)
        master_content = master_content.replace('[Nombre oficial]', tech_name)
        master_content = master_content.replace('[Categoría]', 'Technology Stack')
        master_content = master_content.replace('[Stack]', tech_name)
        master_content = master_content.replace('[SKILLS_LIST]', skills_section)
        
        # Link placeholder replacement
        scalability_links = ', '.join([f'[`{s}`](./skills/{s}/README.md)' for s in skills_list[:2]])
        qa_links = ', '.join([f'[`{s}`](./skills/{s}/README.md)' for s in skills_list[2:4]])
        
        master_content = master_content.replace('[SKILLS_LINK_SCALABILITY]', f"> 🚀 **Related Skills:** {scalability_links}")
        master_content = master_content.replace('[SKILLS_LINK_QA]', f"> ✅ **Related Skills:** {qa_links}")
        master_content = master_content.replace('[SKILLS_LINK_CONNECTIVITY]', "")
        master_content = master_content.replace('[SKILLS_LINK_BEHAVIOR]', "")
        
        with open(tech_readme, 'w', encoding='utf-8') as f:
            f.write(master_content)
            
    print("Migration completed.")
    create_agent_files(agents_db)

def create_agent_files(agents_db):
    for agent in agents_db:
        loc = agent.get('location')
        if not loc: continue
        
        real_path = loc
        for stack_k, tech_v in STACK_TO_TECH_MAP.items():
            if stack_k.replace('knowledge_base/', '') in loc:
                 real_path = loc.replace(stack_k.replace('knowledge_base/', ''), tech_v.replace('knowledge_base/', ''))
        
        full_path = os.path.join(BASE_DIR, real_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        content = f"# {agent['name']}\n\n"
        content += f"**Skills:**\n"
        for s in agent['skills']:
            content += f"- {s}\n"
            
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print("Agent docs created.")

if __name__ == "__main__":
    migrate_and_restructure()
