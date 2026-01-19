---
id: web-events-index
title: "Web Events Checklist - Índice y Guía de Uso para Agentes IA"
category: frontend
subcategory: events
type: index
version: "1.0.0"
last_updated: "2026-01-14"
author: hands-on-ai
status: active
machine_readable: true
tags:
  - events
  - javascript
  - validation
  - security
  - accessibility
  - performance
  - checklist
agents:
  - coding
  - review
  - security
  - qa
  - optimization
related_documents:
  - path: "knowledge_base/technologies/frontend/web-events/README.md"
    type: checklist
    description: "Eventos básicos"
  - path: "knowledge_base/technologies/frontend/web-events/media-and-advanced.md"
    type: checklist
    description: "Media y APIs modernas"
  - path: "knowledge_base/technologies/frontend/web-events/ecommerce-and-social.md"
    type: checklist
    description: "E-commerce y social features"
  - path: "knowledge_base/technologies/frontend/web-events/data-ui-best-practices.md"
    type: checklist
    description: "Data UI y best practices"
  - path: "knowledge_base/technologies/frontend/web-events/INTEGRATION-GUIDE.md"
    type: guide
    description: "Guía técnica de integración"
  - path: "project_meta/security/threat-model.yaml"
    type: security
    section: web_events_security
  - path: "project_meta/ai-context/prompt-library.json"
    type: configuration
    prompts:
      - web_events_validation
      - ecommerce_validation
      - accessibility_audit
      - security_events_audit
      - performance_validation
total_items: 750
completeness_score: 100
accessibility_compliance: "WCAG 2.1 Level AA"
security_compliance: "OWASP Top 10"
performance_standards: "Core Web Vitals"
---

# Web Events Checklist - Índice y Guía de Uso para Agentes IA

## 📋 Descripción General

Este checklist completo de **más de 750 eventos web modernos** sirve como sistema de validación y control de calidad para proyectos de desarrollo web. Los agentes de IA del sistema hands-on-ai deben usar estos documentos como referencia obligatoria al validar, revisar o generar código web.

---

## 🎯 Propósito

El checklist está integrado en el sistema hands-on-ai para:

1. **Validación automática**: Los agentes validan código contra el checklist
2. **Control de calidad**: Garantizar completitud de implementaciones
3. **Seguridad**: Verificar que se cumplan todos los controles de seguridad
4. **Accesibilidad**: Asegurar cumplimiento WCAG 2.1 Level AA
5. **Performance**: Validar optimizaciones y best practices

---

## 📚 Estructura de Documentos

### 1. README.md - Eventos Básicos
**Ruta**: `knowledge_base/technologies/frontend/web-events/README.md`

**Contiene**:
- ✅ Eventos de Mouse (11 eventos)
- ✅ Eventos de Teclado (5 eventos + shortcuts)
- ✅ Eventos de Formulario (48 items de validación)
- ✅ Eventos de Carga y Recursos (13 eventos)
- ✅ Eventos de Ventana y Documento (15 eventos)
- ✅ Drag & Drop (10 eventos)
- ✅ Eventos de Portapapeles (7 eventos)
- ✅ Touch Events (9 eventos)
- ✅ Pointer Events (9 eventos)

**Cuándo usar**:
- Al validar interactividad básica
- Para verificar formularios y validaciones
- Al revisar eventos de mouse/teclado
- Para auditar drag & drop

---

### 2. media-and-advanced.md - Media y APIs Modernas
**Ruta**: `knowledge_base/technologies/frontend/web-events/media-and-advanced.md`

**Contiene**:
- ✅ Eventos de Media (33 eventos audio/video)
- ✅ Animaciones y Transiciones (14 eventos)
- ✅ Sistema de Autenticación (17 eventos)
- ✅ Perfil y Cuenta (11 eventos)
- ✅ Navegación (14 eventos)
- ✅ Búsqueda y Filtros (13 eventos)
- ✅ APIs Web Modernas (33 eventos)
  - Intersection Observer
  - Mutation Observer
  - Resize Observer
  - Performance Observer
  - Geolocation API
  - Page Visibility API
  - Fullscreen API
  - Web Speech API
  - Battery API
- ✅ PWA Features (14 eventos)

**Cuándo usar**:
- Al implementar players de audio/video
- Para validar sistemas de autenticación
- Al revisar navegación SPA
- Para verificar implementación PWA
- Cuando se usan APIs modernas del browser

---

### 3. ecommerce-and-social.md - E-Commerce y Features Sociales
**Ruta**: `knowledge_base/technologies/frontend/web-events/ecommerce-and-social.md`

**Contiene**:
- ✅ E-Commerce Completo (67+ eventos)
  - Navegación de productos (17 eventos)
  - Reviews y Ratings (9 eventos)
  - Carrito de Compras (15 eventos)
  - Proceso de Checkout (26 eventos)
  - Post-Compra (9 eventos)
- ✅ Eventos de Contenido (23 eventos)
  - Visualización de contenido
  - Interacciones sociales (likes, shares, comments)
  - Seguidores y listas
- ✅ Notificaciones (13 eventos)
- ✅ Mensajería y Chat (26 eventos)
  - Chat básico
  - Multimedia
  - Audio/Video calls
  - Grupos
  - Presence

**Cuándo usar**:
- **CRÍTICO**: Para cualquier implementación e-commerce
- Al validar carritos de compra
- Para auditar procesos de checkout (seguridad PCI DSS)
- Al revisar sistemas de chat/mensajería
- Para features sociales (likes, comments, follows)

---

### 4. data-ui-best-practices.md - UI de Datos y Best Practices
**Ruta**: `knowledge_base/technologies/frontend/web-events/data-ui-best-practices.md`

**Contiene**:
- ✅ Tablas y Data Grids (16 eventos)
  - Sorting, filtering, paginación
  - Bulk actions
  - Export
- ✅ Calendarios y Fechas (14 eventos)
  - Date pickers
  - Calendar views
  - Eventos recurrentes
- ✅ Subida de Archivos (16 eventos)
  - Validación
  - Preview
  - Crop/resize
  - Progress
- ✅ Modales y Overlays (16 eventos)
  - Modales
  - Tooltips
  - Popovers
  - Drawers
- ✅ **Accesibilidad (A11y)** (14 validaciones CRÍTICAS)
  - Keyboard navigation
  - Screen reader support
  - ARIA attributes
  - WCAG 2.1 Level AA
- ✅ **Analytics y Tracking** (18 eventos)
  - Page views
  - Conversions
  - E-commerce tracking
  - Error tracking
- ✅ **Seguridad** (13 controles OBLIGATORIOS)
  - Input validation
  - XSS prevention
  - CSRF protection
  - Authentication security
- ✅ **Best Practices** (46 items)
  - Performance
  - UX
  - Mobile
  - Testing
  - Monitoring

**Cuándo usar**:
- **OBLIGATORIO**: Para auditorías de accesibilidad
- **OBLIGATORIO**: Para auditorías de seguridad
- Al implementar tablas de datos
- Para validar calendarios
- Al revisar file uploads
- Para verificar modales y overlays
- Cuando se necesita validar performance
- Para verificar implementación de analytics

---

## 🤖 Uso por Agentes IA

### Review Agent
**Prompt Template**: `project_meta/ai-context/prompt-library.json > web_events_validation`

**Responsabilidades**:
1. Leer código a revisar
2. Identificar categoría de evento (mouse, form, ecommerce, etc.)
3. Cargar checklist correspondiente
4. Validar cada item del checklist
5. Generar reporte con:
   - ✅ Items PASSED
   - ❌ Items FAILED
   - ⚠️ Items PARTIALLY implemented
   - 📝 Recommendations

**Ejemplo de uso**:
```python
# En review_agent.py
from tools.rag.knowledge_indexer import PlanningRAG

def review_web_feature(code, feature_type):
    # Cargar checklist relevante
    rag = PlanningRAG()
    checklist = rag.query_context(
        f"web events checklist for {feature_type}",
        filter={"path": "knowledge_base/technologies/frontend/web-events/"}
    )

    # Aplicar validaciones del prompt template
    prompt = load_prompt("web_events_validation")
    validation_result = llm.generate(prompt.format(
        feature_name=feature_type,
        code=code,
        language="javascript"
    ))

    return validation_result
```

---

### Security Agent
**Prompt Template**: `project_meta/ai-context/prompt-library.json > security_events_audit`

**Responsabilidades**:
1. Auditar eventos contra threat model: `project_meta/security/threat-model.yaml > web_events_security`
2. Verificar controles de seguridad específicos por tipo de evento
3. Validar OWASP Top 10
4. Generar reporte de vulnerabilidades

**Checklist de Seguridad por Evento**:
- **Form Events**: `threat-model.yaml > form_events`
- **File Upload**: `threat-model.yaml > file_upload_events`
- **Authentication**: `threat-model.yaml > authentication_events`
- **E-commerce**: `threat-model.yaml > ecommerce_events`
- **Chat**: `threat-model.yaml > chat_messaging_events`

**Ejemplo de uso**:
```python
# En security_agent.py
def audit_event_security(code, event_type):
    # Cargar threat model
    threat_model = load_yaml("project_meta/security/threat-model.yaml")
    event_threats = threat_model['web_events_security'][event_type]

    # Aplicar prompt de auditoría
    prompt = load_prompt("security_events_audit")
    audit_result = llm.generate(prompt.format(
        component_name=event_type,
        code=code,
        language="javascript"
    ))

    # Validar contra controles requeridos
    for control in event_threats['controls']:
        validate_control_implementation(code, control)

    return audit_result
```

---

### Coding Agent
**Uso**: Referencia al generar código

**Responsabilidades**:
1. Consultar checklist antes de generar código
2. Implementar TODOS los eventos relevantes
3. Seguir patterns de seguridad
4. Incluir manejo de errores
5. Implementar accesibilidad desde el inicio

**Ejemplo de uso**:
```python
# En coding_agent.py
def generate_ecommerce_cart(requirements):
    # Consultar checklist de e-commerce
    cart_checklist = rag.query_context(
        "ecommerce cart checklist",
        filter={"path": "web-events/ecommerce-and-social.md"}
    )

    # Generar código que cumpla TODOS los items
    code = llm.generate(f"""
    Generate a shopping cart implementation that includes:

    From checklist:
    {cart_checklist}

    Requirements:
    {requirements}

    CRITICAL: Include ALL security controls from threat-model.yaml
    """)

    return code
```

---

### QA Agent
**Prompt Templates**:
- `accessibility_audit` - Para auditoría A11y
- `performance_validation` - Para performance
- `ecommerce_validation` - Para e-commerce

**Responsabilidades**:
1. Testing exhaustivo de todos los eventos del checklist
2. Validación de accesibilidad (WCAG AA)
3. Testing de performance
4. Cross-browser testing
5. Mobile testing

---

## 🔒 Validaciones de Seguridad CRÍTICAS

### Siempre Verificar

**En TODOS los formularios**:
- ✅ Validación server-side (OBLIGATORIO)
- ✅ Sanitización de inputs
- ✅ CSRF tokens
- ✅ Rate limiting
- ✅ Error messages seguros (no revelan info del sistema)

**En file uploads**:
- ✅ MIME type validation (server-side)
- ✅ File size limits
- ✅ Virus scanning
- ✅ Storage fuera de webroot
- ✅ Renamed files (UUID)

**En authentication**:
- ✅ bcrypt/argon2 para passwords (NUNCA MD5/SHA1)
- ✅ HttpOnly, Secure cookies
- ✅ Session timeout
- ✅ Rate limiting (5 intentos / 15min)
- ✅ Account lockout

**En e-commerce**:
- ✅ HTTPS enforcement
- ✅ PCI DSS compliance
- ✅ Tokenization (NO raw card numbers)
- ✅ Server-side price calculation
- ✅ Fraud detection

Ver detalles completos en:
- `project_meta/security/threat-model.yaml > web_events_security`
- Cada documento del checklist tiene sección "Aspectos de Seguridad"

---

## ♿ Validaciones de Accesibilidad OBLIGATORIAS

### WCAG 2.1 Level AA Compliance

**Keyboard Navigation** (CRÍTICO):
- ✅ Tab navigation funciona en TODOS los elementos interactivos
- ✅ Focus visible (outline claro)
- ✅ No keyboard traps
- ✅ Enter/Space activan elementos
- ✅ ESC cierra modales

**Screen Readers** (CRÍTICO):
- ✅ ARIA labels en todos los elementos interactivos
- ✅ ARIA roles correctos (button, navigation, dialog, etc.)
- ✅ ARIA states (expanded, selected, checked)
- ✅ ARIA live regions para contenido dinámico
- ✅ Alt text en TODAS las imágenes

**Visual** (CRÍTICO):
- ✅ Contrast ratio ≥ 4.5:1 para texto
- ✅ Contrast ratio ≥ 3:1 para UI components
- ✅ Funciona al 200% zoom
- ✅ No info solo por color

**Testing**:
- ✅ Keyboard-only navigation
- ✅ Screen reader (NVDA/VoiceOver)
- ✅ axe-core automated testing
- ✅ Lighthouse accessibility score ≥ 90

Ver checklist completo en:
`data-ui-best-practices.md > Accesibilidad (A11y)`

---

## 📊 Criterios de Aprobación

### Para que un código pase validación

**Obligatorio (100%)**:
1. ✅ **Core Events**: Todos los eventos básicos implementados
2. ✅ **Security**: Sin vulnerabilidades críticas/altas (OWASP)
3. ✅ **Accessibility**: WCAG 2.1 Level AA (score ≥ 90)
4. ✅ **Performance**: Lighthouse Performance ≥ 90
5. ✅ **Testing**: Coverage ≥ 80%

**Recomendado**:
6. ✅ **PWA**: Si aplicación móvil/progresiva
7. ✅ **Analytics**: Tracking de eventos críticos
8. ✅ **Error Handling**: Try-catch, error boundaries
9. ✅ **Documentation**: Eventos documentados

---

## 🔄 Flujo de Validación

### 1. Coding Agent genera código
```
Coding Agent → Consulta checklist relevante
            → Genera código completo
            → Incluye security + accessibility
```

### 2. Security Agent audita
```
Security Agent → Carga threat-model.yaml
               → Valida controles de seguridad
               → Genera reporte de vulnerabilidades
               → BLOCKER si hay vulnerabilidades críticas
```

### 3. Review Agent valida completitud
```
Review Agent → Carga checklist completo
             → Valida cada item
             → Score de completitud (0-100%)
             → REQUEST CHANGES si < 80%
```

### 4. QA Agent prueba
```
QA Agent → Accessibility audit (WCAG AA)
         → Performance validation
         → Cross-browser testing
         → FAIL si accessibility < 90
```

### 5. Aprobación final
```
Si TODO ✅:
  - Security: PASSED
  - Review: ≥ 80% completitud
  - Accessibility: ≥ 90 score
  - Performance: ≥ 90 score
Entonces: APPROVED ✅
```

---

## 📖 Ejemplos de Uso

### Ejemplo 1: Validar un Formulario de Login

**Agente**: Review Agent
**Checklist**: `README.md > Eventos de Formulario + media-and-advanced.md > Autenticación`

```javascript
// Código a validar
function handleLogin(e) {
  e.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  fetch('/api/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  });
}
```

**Validación**:
- ❌ FAILED: No hay validación client-side
- ❌ FAILED: No hay manejo de errores
- ❌ FAILED: No hay CSRF token
- ❌ FAILED: No hay rate limiting visible
- ❌ FAILED: No hay loading state
- ❌ FAILED: Password no está hasheado (debe ser server-side pero no verificable)
- ❌ FAILED: No hay accesibilidad (ARIA labels, error announcements)

**Score**: 15% - REJECTED

---

### Ejemplo 2: Validar Carrito de E-commerce

**Agente**: Security Agent + Review Agent
**Checklist**: `ecommerce-and-social.md > Carrito de Compras`
**Threat Model**: `threat-model.yaml > ecommerce_events`

```javascript
// Código a validar
function addToCart(productId, quantity, price) {
  const cart = getCart();
  cart.push({ productId, quantity, price });
  saveCart(cart);
  updateTotal();
}
```

**Security Audit**:
- 🔒 CRITICAL: Price viene del cliente (price tampering vulnerability)
- 🔒 HIGH: No hay validación de quantity (puede ser negativo)
- 🔒 HIGH: No hay CSRF protection
- 🔒 MEDIUM: No hay rate limiting

**Review Audit**:
- ❌ No hay feedback visual (loading, success)
- ❌ No persiste en servidor
- ❌ No maneja errores
- ❌ No tiene accesibilidad

**Score**: 20% - CRITICAL SECURITY ISSUES - BLOCKED

---

### Ejemplo 3: Validar Player de Video

**Agente**: Review Agent
**Checklist**: `media-and-advanced.md > Eventos de Media`

```javascript
// Código a validar
const video = document.getElementById('player');
video.addEventListener('play', () => console.log('playing'));
video.addEventListener('pause', () => console.log('paused'));
```

**Validación contra checklist de 33 eventos de media**:
- ✅ play event
- ✅ pause event
- ❌ playing event (después de buffer)
- ❌ ended event
- ❌ seeking/seeked
- ❌ timeupdate (para progress bar)
- ❌ volumechange
- ❌ loadstart/loadeddata/canplay (loading states)
- ❌ waiting (buffering indicator)
- ❌ error (error handling)
- ❌ Controles personalizados
- ❌ Accesibilidad (captions, keyboard controls)

**Score**: 6% (2 de 33) - REJECTED

---

## 🎓 Tips para Agentes

### Para Coding Agent
1. **Siempre consulta el checklist ANTES de generar código**
2. **No implementes solo lo mínimo** - usa el checklist completo
3. **Security first**: Implementa controles de seguridad desde el inicio
4. **Accessibility first**: No es "algo para agregar después"
5. **Usa los ejemplos de código** en el checklist como referencia

### Para Review Agent
1. **Sé exhaustivo**: Revisa TODO el checklist, no solo lo obvio
2. **Usa scoring**: Da un % de completitud
3. **Sé específico**: "Falta validación" vs "Falta validación de email format con regex en línea 45"
4. **Prioriza**: CRITICAL vs HIGH vs MEDIUM vs LOW

### Para Security Agent
1. **Usa threat-model.yaml** como guía obligatoria
2. **Verifica SIEMPRE server-side validation** (no confiar en client)
3. **PCI DSS** es OBLIGATORIO para e-commerce
4. **Reporta BLOCKERS** inmediatamente

### Para QA Agent
1. **Accessibility NO es opcional** - WCAG AA es requerimiento
2. **Testing real**: No solo automated - probar con keyboard y screen reader
3. **Mobile testing**: Touch events, responsive, 44x44px touch targets
4. **Performance**: Core Web Vitals son críticos

---

## 📞 Referencias Rápidas

### Documentos del Checklist
- `README.md` - Eventos básicos
- `media-and-advanced.md` - Media, auth, PWA
- `ecommerce-and-social.md` - E-commerce, social, chat
- `data-ui-best-practices.md` - UI, A11y, security, best practices

### Configuración de Agentes
- `project_meta/ai-context/prompt-library.json` - Prompts de validación
- `project_meta/security/threat-model.yaml` - Threat model y controles

### Herramientas de Testing
- axe-core - Accessibility automated testing
- Lighthouse - Performance y A11y scores
- OWASP ZAP - Security scanning
- Jest - Unit testing
- Cypress - E2E testing

---

## ✅ Checklist de Checklist (Meta)

Antes de aprobar código, verificar que se usó el checklist:

- [ ] ¿Se consultó el checklist correcto para el tipo de feature?
- [ ] ¿Se validaron TODOS los items aplicables?
- [ ] ¿Se verificó seguridad contra threat-model.yaml?
- [ ] ¿Se validó accesibilidad (WCAG AA)?
- [ ] ¿Se verificó performance (debounce/throttle)?
- [ ] ¿Se generó reporte detallado con score?
- [ ] ¿Se identificaron BLOCKERS?
- [ ] ¿Se dieron recomendaciones específicas?

---

**Este índice debe ser consultado por TODOS los agentes al inicio de cualquier tarea de validación, review o generación de código web.**
