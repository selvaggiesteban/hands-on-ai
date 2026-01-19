# 🤖 Hands-on AI - Planning as Code para Desarrollo Asistido por IA

**Sistema completo de "Planning as Code" orientado a IA y automatización inteligente de desarrollo de software.**

[![AI-Assisted](https://img.shields.io/badge/AI-Assisted-blue)]()
[![Planning as Code](https://img.shields.io/badge/Planning-as--Code-green)]()
[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)]()

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Características Principales](#-características-principales)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Instalación](#-instalación)
- [Uso Rápido](#-uso-rápido)
- [Agentes IA Especializados](#-agentes-ia-especializados)
- [Sistema RAG](#-sistema-rag)
- [Seguridad y Compliance](#-seguridad-y-compliance)
- [Métricas y Observabilidad](#-métricas-y-observabilidad)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Roadmap](#-roadmap)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## 🎯 Descripción General

**Hands-on AI** es un framework revolucionario que transforma documentos de planning en código ejecutable mediante un sistema multi-agente de IA. Combina **Planning as Code**, **RAG (Retrieval-Augmented Generation)** y **agentes especializados** para automatizar todo el ciclo de desarrollo de software.

### Filosofía: Planning as Code

Cada aspecto del proyecto está definido en documentos estructurados que sirven como:
- **Source of truth** para el equipo humano
- **Input directo** para agentes de IA
- **Metadata** para optimización de tokens y contexto
- **Base de conocimiento** para aprendizaje continuo

---

## ✨ Características Principales

### 🤖 Sistema Multi-Agente

Sistema de agentes especializados que trabajan en conjunto:
- **Orchestrator Agent**: Coordinador principal del sistema
- **Planning Agent**: Analiza planning documents y genera tareas
- **Coding Agent**: Genera código desde especificaciones
- **Review Agent**: Code review automático con quality gates
- **Security Agent**: Análisis de vulnerabilidades (OWASP Top 10)
- **Optimization Agent**: Refactoring y mejoras de performance
- **Documentation Agent**: Generación automática de docs

### 📚 Sistema RAG Integrado

- **Indexación automática** de knowledge base y planning documents
- **Chunking estratégico** (semantic/fixed/code-aware)
- **Vector store** con ChromaDB/Pinecone/Qdrant
- **Retrieval inteligente** para minimizar uso de tokens
- **Caching** de embeddings y consultas

### 🔒 Security & Compliance

- **Threat modeling** automático desde planning
- **OWASP Top 10** mapping completo
- **Policy enforcement** en tiempo real
- **Secrets scanning** pre-commit
- **STRIDE analysis** integrado
- Compliance: GDPR, HIPAA, PCI-DSS

### 📊 Optimización de Tokens

- **Token budget tracking** por operación
- **Context optimization** automática
- **Prompt compression** inteligente
- **Cost monitoring** en tiempo real
- **Caching strategies** (Anthropic Claude)

### 🚀 RAD (Rapid Application Development)

- **Scaffolding AI-powered** desde plan.json
- **Code generation** desde user stories
- **Test generation** desde acceptance criteria
- **API documentation** automática
- **Infrastructure as Code** generation

### ✅ Web Events Checklist (NUEVO)

- **750+ eventos web modernos** documentados y validables
- **Validación automática** contra checklist completo
- **Security controls** integrados en threat model
- **Accessibility (A11y)** - WCAG 2.1 Level AA compliance
- **Performance validation** - Core Web Vitals
- **E-commerce específico** - PCI DSS compliance checks
- **Prompts especializados** para cada tipo de validación
- **Integración completa** con todos los agentes

Ver documentación: [`knowledge_base/technologies/frontend/web-events/`](knowledge_base/technologies/frontend/web-events/INDEX.md)

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                       │
│                  (Coordinador Principal)                    │
└────────────┬────────────────────────────────────────────────┘
             │
             ├──► Planning Agent ──► Genera tareas desde docs
             │
             ├──► Coding Agent ──► Genera código con RAG
             │         │
             │         └──► RAG System (Vector Store)
             │
             ├──► Review Agent ──► Code review + quality gates
             │
             ├──► Security Agent ──► OWASP + Policy Enforcement
             │
             ├──► Optimization Agent ──► Refactoring + Performance
             │
             └──► Documentation Agent ──► Auto-docs + README
                          │
                          └──► Token Budget Manager
                                    │
                                    └──► Feedback Loop System
```

### Flujo de Trabajo Automático

1. **Planning Analysis**: Lee plan.json y product-overview.json
2. **Task Generation**: Descompone user stories en tareas ejecutables
3. **Code Generation**: Genera código con contexto desde RAG
4. **Security Scan**: Valida contra políticas y OWASP
5. **Quality Check**: Code review + optimization suggestions
6. **Test Generation**: Crea tests desde acceptance criteria
7. **Documentation**: Actualiza docs y README
8. **Git Automation**: Commit + PR (opcional)

---

## 📦 Instalación

### Requisitos Previos

- Python 3.11+
- Node.js 18+
- Git

### Instalación Paso a Paso

```bash
# 1. Clonar el repositorio
git clone https://github.com/your-org/hands-on-ai.git
cd hands-on-ai

# 2. Crear entorno virtual Python
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias Python
pip install -r requirements.txt

# 4. Instalar dependencias Node.js (opcional)
npm install

# 5. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys (OpenAI, Anthropic, etc.)

# 6. Indexar knowledge base (primera vez)
python tools/rag/knowledge_indexer.py --index

# 7. Verificar instalación
python orchestrator.py --help
```

### Configuración de API Keys

Edita `.env` con tus credenciales:

```env
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Vector Store
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=...
```

---

## 🚀 Uso Rápido

### 1. Modo Interactivo (Recomendado)

```bash
python orchestrator.py
```

El sistema te guiará interactivamente:
1. Selecciona scope (mvp/e2e/full)
2. Selecciona potencia de agentes (p1/p2/p3/p4)
3. El sistema ejecuta el pipeline completo

### 3. Modo Automatizado (CI/CD)

Para una automatización completa, el sistema puede ejecutarse de forma no interactiva. Es ideal para pipelines de CI/CD, análisis nocturnos o webhooks.

**Requisitos:**
- El archivo `.env` debe estar configurado con las API keys correctas.
- Los archivos `plan.json` y `product-overview.json` deben existir o serán creados.

```bash
# Ejecuta el proceso de análisis y planificación de forma autónoma
# El comando `/init` escanea el código, lee el chat y actualiza los planes.
python orchestrator.py --command "/init"
```

Esta ejecución autónoma realizará el análisis profundo y actualizará los metadatos sin intervención manual.

### 4. Indexar Knowledge Base

```bash
# Indexar todos los documentos
python tools/rag/knowledge_indexer.py --index

# Consultar el índice
python tools/rag/knowledge_indexer.py --query "JWT authentication"
```

### 4. Monitorear Tokens

```bash
# Ver reporte de tokens
python tools/optimization/token_tracker.py

# Generar métricas
python tools/metrics/planning_metrics.py
```

---

## 🤖 Agentes IA Especializados

### Orchestrator Agent

Coordinador principal que gestiona el pipeline completo:

```python
from tools.agents.orchestrator_agent import PlanningOrchestrator

orchestrator = PlanningOrchestrator(
    plan_path="project_meta/planning/plan.json",
    product_path="project_meta/product_overview/product-overview.json"
)

results = orchestrator.execute_pipeline(scope="feature", feature_name="user-auth")
```

### Planning Agent

Genera tareas ejecutables desde user stories:

```python
from tools.agents.planning_agent import PlanningAgent

agent = PlanningAgent(product_overview, plan, ai_config)

# Generar todas las tareas
tasks = agent.generate_tasks(scope="full")

# Descomponer un epic
epic_tasks = agent.decompose_epic("Account Management")

# Generar GitHub issues
issues = agent.generate_github_issues(tasks, output_format="json")
```

### Coding Agent

Genera código desde especificaciones:

```python
from tools.agents.coding_agent import CodingAgent

agent = CodingAgent(plan, ai_config)

# Generar código para una tarea
result = agent.generate_code(task, context_from_rag)

# result['code_files'] contiene todos los archivos generados
for file in result['code_files']:
    print(f"{file['file_path']}: {len(file['code'])} bytes")
```

### Security Agent

Audita código contra OWASP y políticas:

```python
from tools.agents.security_agent import SecurityAgent

agent = SecurityAgent(security_policies, ai_config)

# Auditar código
audit_result = agent.audit(code, language="javascript")

if not audit_result['passed']:
    for vuln in audit_result['vulnerabilities']:
        print(f"[{vuln['severity']}] {vuln['category']}: {vuln['description']}")
```

### Review Agent

Code review automático:

```python
from tools.agents.review_agent import ReviewAgent

agent = ReviewAgent(ai_config)

review = agent.review_code(code, language="python")

print(f"Score: {review['score']:.2f}")
print(f"Approved: {review['approved']}")
```

---

## 📚 Sistema RAG

### Configuración

El sistema RAG está configurado en `project_meta/ai-context/rag-config.json`:

```json
{
  "vector_store": {
    "provider": "chromadb",
    "persist_directory": "./data/chroma_db"
  },
  "embedding_model": {
    "provider": "openai",
    "model": "text-embedding-3-small"
  },
  "chunking_strategy": {
    "strategy": "semantic",
    "chunk_size": 1000,
    "chunk_overlap": 200
  }
}
```

### Uso

```python
from tools.rag.knowledge_indexer import PlanningRAG

rag = PlanningRAG(config_path="project_meta/ai-context/rag-config.json")

# Indexar documentos
stats = rag.index_planning_docs()

# Consultar contexto relevante
results = rag.query_context("How to implement JWT authentication?", k=5)

for result in results:
    print(f"Score: {result['score']:.3f}")
    print(f"Source: {result['metadata']['file_name']}")
    print(f"Text: {result['text'][:150]}...")
```

---

## 🔒 Seguridad y Compliance

### Threat Model

Definido en `project_meta/security/threat-model.yaml`:

```yaml
threat_model:
  stride_analysis:
    - category: "Spoofing"
      controls: ["JWT with RS256", "MFA optional"]
    - category: "Tampering"
      controls: ["HTTPS/TLS 1.3", "Parameterized queries"]

  owasp_top10_mapping:
    A01_broken_access_control:
      status: "mitigated"
      controls: ["RBAC", "attribute-based policies"]
```

### Policy Enforcement

```python
from tools.security.policy_enforcer import SecurityPolicyEnforcer

enforcer = SecurityPolicyEnforcer(security_policies)

result = enforcer.validate_against_plan(code, language="javascript")

if not result['compliant']:
    print("Security violations found:")
    for violation in result['violations']:
        print(f"  - [{violation['severity']}] {violation['message']}")
```

---

## 📊 Métricas y Observabilidad

### Planning Health Dashboard

```python
from tools.metrics.planning_metrics import PlanningMetrics

metrics = PlanningMetrics(
    plan_path="project_meta/planning/plan.json",
    product_path="project_meta/product_overview/product-overview.json"
)

health = metrics.calculate_health_score()

print(f"Overall Score: {health['overall_score']:.1%}")
print("\nDetailed Scores:")
for metric, score in health['scores'].items():
    print(f"  {metric}: {score:.1%}")
```

### Token Usage Tracking

```python
from tools.optimization.token_tracker import TokenBudgetManager

manager = TokenBudgetManager(model="gpt-4-turbo")

# Track usage
manager.track_usage("code_generation", tokens_input=3000, tokens_output=2000)

# Generate report
print(manager.generate_report())

# Check costs
costs = manager.calculate_cost()
print(f"Total cost: ${costs['total_cost_usd']:.2f}")
```

---

## 📂 Estructura del Proyecto

```
hands-on-ai/
├── .github/
│   └── workflows/
│       └── ai-assisted-dev.yml        # CI/CD con AI
├── project_meta/
│   ├── ai-context/                    # Configuración AI
│   │   ├── token-budget.json
│   │   ├── prompt-library.json
│   │   ├── context-windows.json
│   │   └── rag-config.json
│   ├── architecture/                  # Schemas de arquitectura
│   │   ├── microservices-schema.json
│   │   └── event-driven-schema.yaml
│   ├── security/
│   │   └── threat-model.yaml          # Threat modeling
│   ├── planning/
│   │   └── plan.json                  # Plan técnico
│   └── product_overview/
│       └── product-overview.json      # Product backlog
├── knowledge_base/
│   ├── setup/                         # Metodología
│   ├── technologies/                  # 41 tecnologías documentadas
│   └── ai-prompts/                    # Biblioteca de prompts
├── tools/
│   ├── agents/                        # Agentes especializados
│   │   ├── orchestrator_agent.py
│   │   ├── planning_agent.py
│   │   ├── coding_agent.py
│   │   ├── review_agent.py
│   │   ├── security_agent.py
│   │   ├── optimization_agent.py
│   │   └── documentation_agent.py
│   ├── rag/
│   │   └── knowledge_indexer.py       # Sistema RAG
│   ├── security/
│   │   └── policy_enforcer.py         # Security enforcement
│   ├── optimization/
│   │   └── token_tracker.py           # Token management
│   ├── rad/
│   │   └── scaffolder.py              # AI scaffolding
│   ├── learning/
│   │   └── feedback_collector.py      # Feedback loop
│   └── metrics/
│       └── planning_metrics.py        # Métricas de planning
├── data/                              # Datos persistentes
│   ├── chroma_db/                     # Vector store
│   └── learning_db.json               # Learning examples
├── orchestrator.py                    # Orchestrator principal
├── requirements.txt                   # Dependencias Python
├── .commitlint.config.yaml            # Conventional commits
├── .eslintrc.json                     # ESLint config
└── README.md                          # Este archivo
```

---

## 🗺️ Roadmap

### ✅ Fase 1: Fundación (Completado)

- [x] Schema extendido de planning
- [x] Agentes especializados (7)
- [x] Sistema RAG básico
- [x] Token budget tracking
- [x] Security policy enforcement
- [x] Métricas de planning

### 🚧 Fase 2: Integración (En Progreso)

- [ ] Integración real con LLMs (OpenAI, Anthropic)
- [ ] Vector store production-ready (Pinecone/Qdrant)
- [ ] Fine-tuning de prompts
- [ ] Feedback loop operativo
- [ ] CI/CD completamente automatizado

### 🔮 Fase 3: Avanzado (Futuro)

- [ ] Multi-tenancy para múltiples proyectos
- [ ] Fine-tuning de modelos propios
- [ ] IDE extensions (VS Code, JetBrains)
- [ ] Collaboration features (multi-usuario)
- [ ] Analytics dashboard

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/amazing-feature`)
3. Commit con conventional commits (`feat(agents): add new capability`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

### Guías de Estilo

- **Python**: Seguir PEP 8, usar Black y Ruff
- **JavaScript/TypeScript**: ESLint con Airbnb style guide
- **Commits**: Conventional Commits (commitlint)
- **Documentación**: Markdown con ejemplos de código

---

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- OpenAI por GPT-4 y embeddings API
- Anthropic por Claude y prompt caching
- LangChain por el framework de agentes
- Comunidad open-source

---

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/your-org/hands-on-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/hands-on-ai/discussions)
- **Email**: support@hands-on-ai.dev

---

## 🌟 Star History

Si este proyecto te resulta útil, ¡considera darle una estrella! ⭐

---

**Construido con ❤️ por el equipo de Hands-on AI**

*Automatiza tu desarrollo con IA - Planning as Code*
