---
id: web-events-integration-guide
title: "Guía de Integración del Web Events Checklist"
category: frontend
subcategory: events
type: guide
version: "1.0.0"
last_updated: "2026-01-14"
author: hands-on-ai
status: active
machine_readable: true
tags:
  - integration
  - agents
  - orchestrator
  - coding-agent
  - review-agent
  - security-agent
  - qa-agent
  - python
  - implementation
agents:
  target_audience:
    - orchestrator
    - coding
    - review
    - security
    - qa
    - optimization
related_documents:
  - path: "knowledge_base/technologies/frontend/web-events/INDEX.md"
    type: index
  - path: "knowledge_base/technologies/frontend/web-events/README.md"
    type: checklist
  - path: "knowledge_base/technologies/frontend/web-events/media-and-advanced.md"
    type: checklist
  - path: "knowledge_base/technologies/frontend/web-events/ecommerce-and-social.md"
    type: checklist
  - path: "knowledge_base/technologies/frontend/web-events/data-ui-best-practices.md"
    type: checklist
  - path: "project_meta/security/threat-model.yaml"
    type: security
  - path: "project_meta/ai-context/prompt-library.json"
    type: configuration
  - path: "tools/agents/orchestrator_agent.py"
    type: implementation
  - path: "tools/agents/coding_agent.py"
    type: implementation
  - path: "tools/agents/security_agent.py"
    type: implementation
  - path: "tools/agents/review_agent.py"
    type: implementation
  - path: "tools/rag/knowledge_indexer.py"
    type: implementation
programming_language: python
implementation_type: agent-system
architecture_pattern: multi-agent
---

# Guía de Integración del Web Events Checklist

## 🎯 Objetivo

Esta guía explica cómo el sistema hands-on-ai utiliza el **Web Events Checklist** (750+ items) como sistema de validación y control de calidad para proyectos de desarrollo web.

---

## 🏗️ Arquitectura de Integración

```
┌─────────────────────────────────────────────────────────────┐
│                  ORCHESTRATOR AGENT                         │
│            (Coordinador Principal)                          │
└────────────┬────────────────────────────────────────────────┘
             │
             ├──► Planning Agent
             │    └─► Genera tareas desde plan.json
             │
             ├──► Coding Agent
             │    ├─► Consulta Web Events Checklist (RAG)
             │    └─► Genera código completo con todos los eventos
             │
             ├──► Review Agent
             │    ├─► Carga checklist relevante
             │    ├─► Valida contra prompt: web_events_validation
             │    └─► Score de completitud (0-100%)
             │
             ├──► Security Agent
             │    ├─► Carga threat-model.yaml > web_events_security
             │    ├─► Valida contra prompt: security_events_audit
             │    └─► Reporta vulnerabilidades (BLOCKERS)
             │
             ├──► Optimization Agent (Performance)
             │    ├─► Valida contra prompt: performance_validation
             │    └─► Score de performance + recomendaciones
             │
             └──► QA Agent (Accessibility)
                  ├─► Valida contra prompt: accessibility_audit
                  └─► Score WCAG 2.1 AA (debe ser ≥ 90)
```

---

## 📂 Estructura de Archivos

### Knowledge Base (Checklist)
```
knowledge_base/technologies/frontend/web-events/
├── INDEX.md                        ← Índice principal (LEER PRIMERO)
├── INTEGRATION-GUIDE.md           ← Esta guía
├── README.md                       ← Eventos básicos (mouse, keyboard, forms, etc.)
├── media-and-advanced.md          ← Media, auth, PWA, APIs modernas
├── ecommerce-and-social.md        ← E-commerce, social, chat, notificaciones
└── data-ui-best-practices.md      ← UI de datos, A11y, security, best practices
```

### Configuración de Agentes
```
project_meta/
├── ai-context/
│   └── prompt-library.json         ← Prompts de validación (6 nuevos)
│       ├── web_events_validation
│       ├── ecommerce_validation
│       ├── accessibility_audit
│       ├── security_events_audit
│       └── performance_validation
│
└── security/
    └── threat-model.yaml           ← Threat model con web_events_security
        ├── mouse_keyboard_events
        ├── form_events
        ├── file_upload_events
        ├── authentication_events
        ├── ecommerce_events
        ├── chat_messaging_events
        └── security_headers
```

---

## 🔄 Flujo de Trabajo Completo

### Fase 1: Planning
```python
# planning_agent.py
def generate_tasks_for_feature(feature_name, user_story):
    """
    Genera tareas incluyendo validaciones del checklist
    """
    # Consultar checklist para el tipo de feature
    if feature_name == "shopping_cart":
        checklist_ref = "knowledge_base/technologies/frontend/web-events/ecommerce-and-social.md#carrito"
    elif feature_name == "login":
        checklist_ref = "knowledge_base/technologies/frontend/web-events/media-and-advanced.md#authentication"
    else:
        checklist_ref = "knowledge_base/technologies/frontend/web-events/README.md"

    tasks = [
        {
            "id": "task-001",
            "name": f"Implement {feature_name}",
            "type": "coding",
            "checklist_reference": checklist_ref
        },
        {
            "id": "task-002",
            "name": f"Security audit {feature_name}",
            "type": "security",
            "checklist_reference": checklist_ref
        },
        {
            "id": "task-003",
            "name": f"Accessibility validation {feature_name}",
            "type": "qa",
            "checklist_reference": "data-ui-best-practices.md#accessibility"
        }
    ]

    return tasks
```

### Fase 2: Coding (con Checklist)
```python
# coding_agent.py
from tools.rag.knowledge_indexer import PlanningRAG

def generate_code_with_checklist(task):
    """
    Genera código consultando el checklist primero
    """
    rag = PlanningRAG()

    # 1. Cargar checklist relevante desde RAG
    checklist_items = rag.query_context(
        query=f"web events checklist for {task['name']}",
        filter={"path": "web-events/"},
        k=10
    )

    # 2. Cargar prompt template
    prompt_template = load_prompt("api_endpoint")  # o el que corresponda

    # 3. Generar código con contexto del checklist
    prompt = f"""
    {prompt_template}

    IMPORTANT: Implement ALL items from this checklist:

    {checklist_items}

    Task: {task['name']}
    Requirements: {task['requirements']}

    Generate complete, production-ready code that includes:
    - All events from checklist
    - Security controls (see threat-model.yaml)
    - Accessibility (WCAG AA)
    - Error handling
    - Loading states
    - Tests
    """

    code = llm.generate(prompt)

    return {
        "code": code,
        "checklist_used": checklist_items,
        "ready_for_review": True
    }
```

### Fase 3: Security Audit
```python
# security_agent.py
import yaml

def audit_web_events_security(code, feature_type):
    """
    Audita código contra threat model
    """
    # 1. Cargar threat model
    with open("project_meta/security/threat-model.yaml") as f:
        threat_model = yaml.safe_load(f)

    # Obtener controles específicos del tipo de evento
    if "login" in feature_type.lower():
        event_security = threat_model['threat_model']['web_events_security']['authentication_events']
    elif "cart" in feature_type.lower() or "checkout" in feature_type.lower():
        event_security = threat_model['threat_model']['web_events_security']['ecommerce_events']
    elif "upload" in feature_type.lower():
        event_security = threat_model['threat_model']['web_events_security']['file_upload_events']
    else:
        event_security = threat_model['threat_model']['web_events_security']['form_events']

    # 2. Cargar prompt de auditoría
    prompt_template = load_prompt("security_events_audit")

    # 3. Ejecutar auditoría
    audit = llm.generate(prompt_template.format(
        component_name=feature_type,
        code=code,
        language="javascript"
    ))

    # 4. Validar controles obligatorios
    missing_controls = []
    for control in event_security['controls']:
        if not validate_control_in_code(code, control):
            missing_controls.append(control)

    # 5. Generar reporte
    return {
        "threats": event_security['threats'],
        "controls_implemented": len(event_security['controls']) - len(missing_controls),
        "controls_missing": missing_controls,
        "vulnerabilities": audit,
        "validation_checklist": event_security.get('validation_checklist'),
        "status": "BLOCKED" if missing_controls else "PASSED"
    }

def validate_control_in_code(code, control):
    """
    Valida si un control está implementado
    """
    control_patterns = {
        "bcrypt": ["bcrypt.hash", "bcrypt.compare"],
        "CSRF": ["csrf", "csrfToken"],
        "HTTPS": ["https://", "secure: true"],
        "HttpOnly": ["httpOnly: true"],
        "Rate limiting": ["rateLimit", "rate-limit"],
        # ... más patterns
    }

    for keyword, patterns in control_patterns.items():
        if keyword.lower() in control.lower():
            return any(pattern in code for pattern in patterns)

    return False  # Si no se puede validar automáticamente
```

### Fase 4: Review (Completitud)
```python
# review_agent.py

def review_web_implementation(code, feature_type):
    """
    Revisa completitud contra checklist
    """
    # 1. Cargar checklist completo
    rag = PlanningRAG()
    checklist = rag.query_context(
        query=f"{feature_type} events checklist",
        filter={"path": "web-events/"},
        k=20
    )

    # 2. Aplicar prompt de validación
    prompt_template = load_prompt("web_events_validation")
    validation = llm.generate(prompt_template.format(
        feature_name=feature_type,
        code=code,
        language="javascript"
    ))

    # 3. Parsear resultados
    passed = extract_passed_items(validation)
    failed = extract_failed_items(validation)
    partial = extract_partial_items(validation)

    # 4. Calcular score
    total_items = len(passed) + len(failed) + len(partial)
    score = (len(passed) + len(partial) * 0.5) / total_items * 100

    # 5. Decisión
    status = "APPROVED" if score >= 80 else "REQUEST_CHANGES"

    return {
        "score": score,
        "status": status,
        "passed_items": passed,
        "failed_items": failed,
        "partial_items": partial,
        "recommendations": extract_recommendations(validation)
    }
```

### Fase 5: QA (Accessibility)
```python
# qa_agent.py (parte del review_agent o separado)

def validate_accessibility(code, component_name):
    """
    Valida WCAG 2.1 Level AA
    """
    # 1. Cargar prompt de accessibility audit
    prompt_template = load_prompt("accessibility_audit")

    # 2. Ejecutar auditoría
    audit = llm.generate(prompt_template.format(
        component_name=component_name,
        code=code,
        language="javascript"
    ))

    # 3. Ejecutar automated testing (axe-core)
    axe_results = run_axe_core(code)

    # 4. Calcular score
    score = calculate_a11y_score(audit, axe_results)

    # 5. Decisión
    status = "PASSED" if score >= 90 else "FAILED"

    return {
        "score": score,
        "status": status,
        "critical_issues": extract_critical_issues(audit),
        "important_issues": extract_important_issues(audit),
        "minor_issues": extract_minor_issues(audit),
        "axe_violations": axe_results['violations']
    }
```

### Fase 6: Performance Validation
```python
# optimization_agent.py

def validate_performance(code, component_name):
    """
    Valida performance de eventos
    """
    # 1. Cargar prompt de performance
    prompt_template = load_prompt("performance_validation")

    # 2. Ejecutar validación
    validation = llm.generate(prompt_template.format(
        component_name=component_name,
        code=code,
        language="javascript"
    ))

    # 3. Verificaciones automáticas
    checks = {
        "has_debounce": check_debounce(code),
        "has_throttle": check_throttle(code),
        "has_passive_listeners": check_passive_listeners(code),
        "has_cleanup": check_cleanup(code),
        "uses_raf": check_request_animation_frame(code)
    }

    # 4. Calcular score
    score = sum(checks.values()) / len(checks) * 100

    return {
        "score": score,
        "checks": checks,
        "bottlenecks": extract_bottlenecks(validation),
        "recommendations": extract_optimizations(validation)
    }
```

---

## 🔧 Configuración del Orchestrator

### orchestrator_agent.py - Flujo Completo
```python
# orchestrator_agent.py

class WebEventsOrchestrator:
    def __init__(self, plan_path, product_path):
        self.coding_agent = CodingAgent()
        self.security_agent = SecurityAgent()
        self.review_agent = ReviewAgent()
        self.qa_agent = QAAgent()
        self.optimization_agent = OptimizationAgent()

    def execute_web_feature_pipeline(self, feature_name, requirements):
        """
        Pipeline completo con validación del checklist
        """
        print(f"\n=== Pipeline for {feature_name} ===\n")

        # 1. CODING
        print("Phase 1: Code Generation (with checklist)")
        code_result = self.coding_agent.generate_code_with_checklist({
            "name": feature_name,
            "requirements": requirements
        })
        code = code_result['code']

        # 2. SECURITY AUDIT
        print("Phase 2: Security Audit")
        security_result = self.security_agent.audit_web_events_security(
            code, feature_name
        )

        if security_result['status'] == "BLOCKED":
            print("❌ SECURITY AUDIT FAILED - CRITICAL ISSUES")
            return {
                "status": "BLOCKED",
                "reason": "Security vulnerabilities found",
                "details": security_result
            }

        # 3. REVIEW (Completitud)
        print("Phase 3: Review (Completeness)")
        review_result = self.review_agent.review_web_implementation(
            code, feature_name
        )

        if review_result['score'] < 80:
            print(f"⚠️  REVIEW SCORE LOW: {review_result['score']}%")
            # Intentar auto-fix o pedir cambios
            if review_result['score'] < 50:
                return {
                    "status": "REJECTED",
                    "reason": "Incomplete implementation",
                    "details": review_result
                }

        # 4. ACCESSIBILITY AUDIT
        print("Phase 4: Accessibility Validation (WCAG AA)")
        a11y_result = self.qa_agent.validate_accessibility(code, feature_name)

        if a11y_result['status'] == "FAILED":
            print("❌ ACCESSIBILITY AUDIT FAILED")
            return {
                "status": "FAILED",
                "reason": "Accessibility requirements not met",
                "details": a11y_result
            }

        # 5. PERFORMANCE VALIDATION
        print("Phase 5: Performance Validation")
        perf_result = self.optimization_agent.validate_performance(
            code, feature_name
        )

        if perf_result['score'] < 70:
            print(f"⚠️  PERFORMANCE SCORE LOW: {perf_result['score']}%")

        # 6. FINAL DECISION
        overall_score = (
            review_result['score'] * 0.4 +
            (100 if security_result['status'] == "PASSED" else 0) * 0.3 +
            a11y_result['score'] * 0.2 +
            perf_result['score'] * 0.1
        )

        print(f"\n=== Overall Score: {overall_score:.1f}% ===")

        if overall_score >= 80:
            status = "APPROVED"
        elif overall_score >= 60:
            status = "NEEDS_IMPROVEMENT"
        else:
            status = "REJECTED"

        return {
            "status": status,
            "overall_score": overall_score,
            "code": code,
            "security_audit": security_result,
            "review": review_result,
            "accessibility": a11y_result,
            "performance": perf_result
        }


# Uso
orchestrator = WebEventsOrchestrator(
    plan_path="project_meta/planning/plan.json",
    product_path="project_meta/product_overview/product-overview.json"
)

result = orchestrator.execute_web_feature_pipeline(
    feature_name="shopping_cart",
    requirements={
        "add_to_cart": True,
        "update_quantity": True,
        "remove_items": True,
        "calculate_total": True,
        "apply_coupons": True
    }
)

print(f"\nFinal Status: {result['status']}")
print(f"Overall Score: {result['overall_score']:.1f}%")
```

---

## 📊 Métricas y Reportes

### Reporte de Validación
```json
{
  "feature": "shopping_cart",
  "timestamp": "2026-01-14T10:30:00Z",
  "status": "APPROVED",
  "overall_score": 87.5,

  "security": {
    "status": "PASSED",
    "threats_mitigated": 4,
    "controls_implemented": 9,
    "controls_missing": 0,
    "vulnerabilities": []
  },

  "completeness": {
    "score": 92.3,
    "passed_items": 12,
    "failed_items": 1,
    "partial_items": 0,
    "total_items": 13
  },

  "accessibility": {
    "score": 95,
    "wcag_level": "AA",
    "critical_issues": 0,
    "important_issues": 1,
    "minor_issues": 3
  },

  "performance": {
    "score": 88,
    "has_debounce": true,
    "has_throttle": true,
    "has_cleanup": true,
    "bottlenecks": []
  },

  "checklist_reference": "knowledge_base/technologies/frontend/web-events/ecommerce-and-social.md#carrito"
}
```

---

## 🎓 Mejores Prácticas de Uso

### 1. Siempre Consultar el INDEX Primero
```python
# ✅ CORRECTO
rag = PlanningRAG()
index_doc = rag.load_document("web-events/INDEX.md")
# Leer sección relevante del INDEX
# Entonces cargar documento específico

# ❌ INCORRECTO
# Cargar documento random sin conocer la estructura
```

### 2. Usar el Threat Model para Security
```python
# ✅ CORRECTO
threat_model = load_threat_model()
event_security = threat_model['web_events_security'][event_type]
# Validar contra controles específicos

# ❌ INCORRECTO
# Auditar security sin consultar threat model
```

### 3. Validar Accesibilidad SIEMPRE
```python
# ✅ CORRECTO
a11y_result = qa_agent.validate_accessibility(code, name)
if a11y_result['score'] < 90:
    return "FAILED"  # BLOCKER

# ❌ INCORRECTO
# Saltar validación de accesibilidad
```

### 4. Performance NO es Opcional
```python
# ✅ CORRECTO
if 'scroll' in code or 'resize' in code:
    assert has_debounce_or_throttle(code), "Must use debounce/throttle"

# ❌ INCORRECTO
# Asumir que performance es "nice to have"
```

---

## 🚨 Errores Comunes y Soluciones

### Error 1: Checklist Incompleto
**Problema**: Agent solo valida eventos obvios

**Solución**:
```python
# Cargar TODO el checklist, no solo primeros resultados
checklist = rag.query_context(
    query=feature_type,
    filter={"path": "web-events/"},
    k=50  # ← Aumentar k para más resultados
)
```

### Error 2: No Consultar Threat Model
**Problema**: Security agent no encuentra controles específicos

**Solución**:
```python
# SIEMPRE cargar threat-model.yaml primero
threat_model = load_yaml("project_meta/security/threat-model.yaml")
controls = threat_model['threat_model']['web_events_security'][event_type]
```

### Error 3: Ignorar Failed Items
**Problema**: Aprobar código con < 80% completitud

**Solución**:
```python
# NUNCA aprobar con score bajo
if review_score < 80:
    return "REQUEST_CHANGES"  # No aprobar
```

### Error 4: No Usar Prompts Específicos
**Problema**: Usar prompts genéricos para validación

**Solución**:
```python
# Usar prompts específicos del prompt-library.json
prompt = load_prompt("web_events_validation")  # ✅ Específico
# NO usar: load_prompt("code_review")  # ❌ Genérico
```

---

## ✅ Checklist de Integración

Para verificar que la integración está completa:

- [ ] Checklist documents creados en `knowledge_base/technologies/frontend/web-events/`
- [ ] Prompts agregados en `prompt-library.json`
- [ ] Threat model actualizado con `web_events_security`
- [ ] Coding Agent consulta checklist antes de generar código
- [ ] Security Agent usa threat-model.yaml
- [ ] Review Agent valida completitud contra checklist
- [ ] QA Agent valida accessibility (WCAG AA)
- [ ] Optimization Agent valida performance
- [ ] Orchestrator ejecuta pipeline completo
- [ ] Reportes incluyen scores de cada fase
- [ ] BLOCKERS detienen el pipeline
- [ ] Documentación completa para usuarios

---

## 📖 Recursos Adicionales

### Para Desarrolladores
- [MDN Web Events](https://developer.mozilla.org/en-US/docs/Web/Events)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

### Para Agentes AI
- `INDEX.md` - Leer primero siempre
- `prompt-library.json` - Usar prompts específicos
- `threat-model.yaml` - Consultar para security

---

**Esta guía debe ser consultada al configurar nuevos agentes o al extender el sistema de validación.**
