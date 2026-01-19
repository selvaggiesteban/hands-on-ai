---
id: web-events-data-ui-bestpractices
title: "Web Events - Data UIs, Accesibilidad y Best Practices"
category: frontend
subcategory: events
type: checklist
version: "1.0.0"
last_updated: "2026-01-14"
author: hands-on-ai
status: active
machine_readable: true
tags:
  - data-tables
  - data-grids
  - calendar
  - date-picker
  - file-upload
  - modals
  - accessibility
  - a11y
  - wcag
  - analytics
  - security
  - best-practices
  - performance
  - testing
agents:
  primary:
    - qa
    - security
    - review
  secondary:
    - coding
    - optimization
related_documents:
  - path: "knowledge_base/technologies/frontend/web-events/INDEX.md"
    type: index
  - path: "project_meta/security/threat-model.yaml"
    type: security
    sections:
      - file_upload_events
      - api_events
      - security_headers
      - event_handler_rules
  - path: "project_meta/ai-context/prompt-library.json"
    type: configuration
    prompts:
      - accessibility_audit
      - security_events_audit
      - performance_validation
total_items: 230
event_categories:
  - name: "Tables & Data Grids"
    count: 16
  - name: "Calendar & Dates"
    count: 14
  - name: "File Upload"
    count: 16
  - name: "Modals & Overlays"
    count: 16
  - name: "Accessibility (A11y)"
    count: 14
  - name: "Analytics & Tracking"
    count: 18
  - name: "Security"
    count: 13
  - name: "Best Practices"
    count: 46
security_level: critical
accessibility_required: true
performance_critical: true
compliance:
  - wcag-2-1-aa
  - owasp-top-10
  - gdpr
  - core-web-vitals
---

# Web Events - Data UIs, Accesibilidad y Best Practices

## ✅ Eventos de Tablas y Data Grids

### Operaciones de Columnas
- [ ] **Ordenar columna ascendente** - Click en header
- [ ] **Ordenar columna descendente** - Segundo click en header
- [ ] **Remover ordenamiento** - Tercer click vuelve a estado original
- [ ] **Ordenamiento multi-columna** - Shift+click para múltiples
- [ ] **Filtrar columna** - Dropdown o input en header
- [ ] **Buscar en tabla** - Global search across todas las columnas
- [ ] **Reordenar columnas** - Drag & drop headers
- [ ] **Resize columnas** - Drag border de header
- [ ] **Mostrar/ocultar columnas** - Column visibility toggle
- [ ] **Fijar columnas** - Freeze columns (sticky)

### Operaciones de Filas
- [ ] **Seleccionar fila** - Click o checkbox
- [ ] **Seleccionar todas las filas** - Checkbox en header
- [ ] **Deseleccionar todas** - Toggle off
- [ ] **Seleccionar rango** - Shift+click para rango
- [ ] **Seleccionar múltiples** - Ctrl/Cmd+click
- [ ] **Expandir fila** - Ver detalles adicionales (nested table)
- [ ] **Editar celda inline** - Double-click para editar
- [ ] **Hover row highlight** - Visual feedback

### Acciones en Bulk
- [ ] **Acciones en lote** - Aplicar acción a seleccionadas
- [ ] **Eliminar múltiples** - Con confirmación
- [ ] **Exportar seleccionadas** - Solo las seleccionadas
- [ ] **Asignar categoría** - Bulk update
- [ ] **Cambiar estado** - Bulk status change

### Paginación y Datos
- [ ] **Cambiar página** - Next/Previous buttons
- [ ] **Ir a página específica** - Input de número
- [ ] **Cambiar items por página** - 10, 25, 50, 100
- [ ] **Mostrar info de paginación** - "Showing 1-25 of 1000"
- [ ] **Infinite scroll** - Como alternativa a paginación

### Exportación
- [ ] **Exportar CSV** - Formato comma-separated
- [ ] **Exportar Excel** - Formato .xlsx
- [ ] **Exportar PDF** - Formato imprimible
- [ ] **Exportar JSON** - Para desarrolladores
- [ ] **Copiar al portapapeles** - Copy table data

### Actualización de Datos
- [ ] **Refresh/reload datos** - Button para actualizar
- [ ] **Auto-refresh** - Polling interval
- [ ] **Real-time updates** - WebSocket para cambios live
- [ ] **Indicador de carga** - Skeleton o spinner
- [ ] **Indicador de cambios** - Highlight filas actualizadas

### Criterios de Validación Tablas
```javascript
function validateDataTable(table) {
  return {
    // Estructura
    hasAccessibleStructure: table.getAttribute('role') === 'grid',
    hasHeaders: table.querySelectorAll('th').length > 0,
    hasBody: table.querySelector('tbody') !== null,

    // Sorting
    hasSortableColumns: table.querySelectorAll('[data-sortable="true"]').length > 0,
    showsSortIndicator: table.querySelector('.sort-indicator') !== null,

    // Filtering
    hasColumnFilters: table.querySelectorAll('.column-filter').length > 0,
    hasGlobalSearch: table.closest('.table-container').querySelector('.table-search') !== null,

    // Selection
    hasRowSelection: table.querySelectorAll('input[type="checkbox"]').length > 0,
    hasSelectAll: table.querySelector('thead input[type="checkbox"]') !== null,
    hasBulkActions: document.querySelector('.bulk-actions') !== null,

    // Columns
    allowsColumnReorder: table.hasAttribute('data-reorderable'),
    allowsColumnResize: table.hasAttribute('data-resizable'),
    hasColumnVisibility: document.querySelector('.column-toggle') !== null,

    // Pagination
    hasPagination: table.closest('.table-container').querySelector('.pagination') !== null,
    hasPageSizeSelector: document.querySelector('select[name="pageSize"]') !== null,

    // Export
    hasExportOptions: document.querySelector('.export-btn') !== null,

    // Performance
    usesVirtualScrolling: table.hasAttribute('data-virtual-scroll'),
    hasLoadingState: table.querySelector('.table-loading') !== null,

    // Accessibility
    hasAccessibleHeaders: table.querySelectorAll('th[scope]').length > 0,
    hasAriaLabels: table.querySelectorAll('[aria-label]').length > 0,
    supportKeyboardNav: table.hasAttribute('tabindex')
  };
}
```

### Performance para Tablas Grandes
- **Virtual Scrolling**: Solo renderizar filas visibles
- **Pagination**: Limitar filas por página
- **Lazy Loading**: Cargar datos bajo demanda
- **Debounce Search**: Esperar antes de filtrar
- **Server-side Processing**: Para millones de registros

---

## ✅ Eventos de Calendarios y Fechas

### Date Picker
- [ ] **Abrir date picker** - Click en input
- [ ] **Cerrar date picker** - ESC o click fuera
- [ ] **Seleccionar fecha** - Click en día
- [ ] **Seleccionar rango de fechas** - Click inicio, luego fin
- [ ] **Cambiar mes** - Flechas prev/next
- [ ] **Cambiar año** - Dropdown o arrows
- [ ] **Ir a hoy** - Button "Today"
- [ ] **Validar fecha** - Formato y rango válido
- [ ] **Deshabilitar fechas** - Past dates, weekends, etc.
- [ ] **Resaltar fechas especiales** - Holidays, events

### Calendar View
- [ ] **Vista mes** - Grid de 7x5/6
- [ ] **Vista semana** - Columnas por día
- [ ] **Vista día** - Timeline con horas
- [ ] **Vista agenda** - Lista de eventos
- [ ] **Cambiar entre vistas** - Toggle buttons

### Eventos de Calendario
- [ ] **Crear evento en calendario** - Click en fecha/hora
- [ ] **Editar evento** - Click en evento existente
- [ ] **Eliminar evento** - Con confirmación
- [ ] **Ver detalle de evento** - Modal o sidebar
- [ ] **Drag & drop eventos** - Mover a otra fecha
- [ ] **Resize evento** - Cambiar duración
- [ ] **Evento recurrente** - Diario, semanal, mensual, anual
- [ ] **Evento de día completo** - All-day event
- [ ] **Evento multi-día** - Spans varios días

### Funcionalidades Avanzadas
- [ ] **Múltiples calendarios** - Work, Personal, etc.
- [ ] **Color coding** - Por categoría
- [ ] **Recordatorios** - Notifications antes del evento
- [ ] **Time zones** - Soporte multi-timezone
- [ ] **Invite attendees** - Agregar participantes
- [ ] **Sincronización** - Con Google Calendar, Outlook
- [ ] **Export ICS** - Formato iCalendar

### Criterios de Validación Calendar
```javascript
function validateCalendar(calendar) {
  return {
    // Date Picker
    hasDatePicker: calendar.querySelector('input[type="date"]') !== null,
    hasCustomPicker: calendar.querySelector('.date-picker') !== null,
    allowsRangeSelection: calendar.hasAttribute('data-range'),

    // Views
    hasMultipleViews: calendar.querySelectorAll('[data-view]').length > 1,
    hasMonthView: calendar.querySelector('[data-view="month"]') !== null,
    hasWeekView: calendar.querySelector('[data-view="week"]') !== null,
    hasDayView: calendar.querySelector('[data-view="day"]') !== null,

    // Events
    allowsEventCreation: calendar.hasAttribute('data-editable'),
    allowsEventEdit: calendar.canEditEvents,
    allowsDragDrop: calendar.hasAttribute('data-draggable'),
    supportsRecurringEvents: calendar.supportsRecurrence,

    // Funcionalidad
    hasTimeZoneSupport: calendar.hasAttribute('data-timezone'),
    hasColorCoding: calendar.querySelectorAll('[data-category]').length > 0,
    hasReminders: calendar.hasReminderFeature,

    // Accessibility
    hasKeyboardNav: calendar.hasAttribute('tabindex'),
    hasAriaLabels: calendar.querySelectorAll('[aria-label]').length > 0,
    hasLiveRegion: calendar.querySelector('[aria-live]') !== null
  };
}
```

---

## ✅ Eventos de Subida de Archivos

### Selección de Archivos
- [ ] **Click en botón upload** - Abrir file picker
- [ ] **Seleccionar archivo(s)** - Input file
- [ ] **Drag & drop archivos** - En drop zone
- [ ] **Drag & drop carpetas** - Upload directorio completo
- [ ] **Pegar desde clipboard** - Ctrl+V para imágenes

### Validación
- [ ] **Validar tipo de archivo** - Por MIME type y extensión
- [ ] **Validar tamaño de archivo** - Máximo permitido
- [ ] **Validar cantidad** - Máximo de archivos
- [ ] **Validar dimensiones** - Para imágenes (width/height)
- [ ] **Mostrar errores de validación** - Mensajes específicos

### Preview y Edición
- [ ] **Preview de archivo** - Thumbnail antes de subir
- [ ] **Preview de imagen** - Full preview
- [ ] **Preview de video** - Player pequeño
- [ ] **Preview de PDF** - Primer página
- [ ] **Comprimir imagen** - Reducir tamaño automáticamente
- [ ] **Resize imagen** - Cambiar dimensiones
- [ ] **Crop imagen** - Recortar área específica
- [ ] **Rotar imagen** - 90°, 180°, 270°

### Upload Process
- [ ] **Iniciar upload** - Manual o automático
- [ ] **Progress bar** - Porcentaje de upload
- [ ] **Upload completado** - Success message
- [ ] **Upload fallido** - Error message con opción de reintentar
- [ ] **Cancelar upload** - Abort button
- [ ] **Remover archivo seleccionado** - Antes de upload
- [ ] **Upload múltiple** - Varios archivos simultáneos
- [ ] **Upload por lotes** - Queue system

### Funcionalidades Avanzadas
- [ ] **Resume upload** - Continuar si se interrumpe
- [ ] **Chunk upload** - Para archivos grandes
- [ ] **Upload directo a S3/Cloud** - Pre-signed URLs
- [ ] **Metadata** - Agregar título, descripción, tags
- [ ] **Organizing** - Carpetas/álbumes

### Criterios de Validación File Upload
```javascript
function validateFileUpload(uploader) {
  return {
    // Básico
    hasFileInput: uploader.querySelector('input[type="file"]') !== null,
    hasDropZone: uploader.querySelector('.drop-zone') !== null,

    // Drag & Drop
    supportsDragDrop: uploader.hasAttribute('data-drop-zone'),
    providesVisualFeedback: uploader.querySelector('.drag-over') !== null,

    // Validación
    validatesFileType: uploader.hasAttribute('accept'),
    validateFileSize: uploader.hasAttribute('data-max-size'),
    showsValidationErrors: uploader.querySelector('.upload-error') !== null,

    // Preview
    showsPreview: uploader.querySelector('.upload-preview') !== null,
    allowsRemoval: uploader.querySelectorAll('.remove-file').length > 0,

    // Progress
    hasProgressBar: uploader.querySelector('.upload-progress') !== null,
    showsPercentage: uploader.querySelector('.upload-percentage') !== null,

    // Múltiples archivos
    allowsMultiple: uploader.querySelector('input[multiple]') !== null,
    showsFileList: uploader.querySelector('.file-list') !== null,

    // Edición
    allowsCropping: uploader.hasCropFeature,
    allowsCompression: uploader.compressesImages,

    // Avanzado
    supportsChunking: uploader.hasChunkUpload,
    supportsResume: uploader.canResumeUpload
  };
}
```

### Aspectos de Seguridad
- **MIME Type Validation**: SIEMPRE validar en backend
- **File Extension**: No confiar solo en extensión
- **Virus Scanning**: Escanear archivos subidos
- **Size Limits**: Prevenir DoS con archivos enormes
- **Upload Path**: NUNCA permitir path traversal
- **Storage**: Almacenar fuera de webroot
- **Unique Filenames**: Renombrar archivos para evitar conflictos

---

## ✅ Eventos de Modales y Overlays

### Gestión de Modales
- [ ] **Abrir modal** - Button trigger
- [ ] **Cerrar modal (X button)** - Close icon en header
- [ ] **Cerrar modal (click fuera)** - Click en overlay
- [ ] **Cerrar modal (ESC key)** - Keyboard shortcut
- [ ] **Confirmar acción en modal** - Primary button
- [ ] **Cancelar acción en modal** - Secondary button o ESC

### Tipos de Modales
- [ ] **Modal de confirmación** - "¿Estás seguro?"
- [ ] **Modal de warning** - Advertencia antes de acción
- [ ] **Modal de error** - Mostrar error detallado
- [ ] **Modal informativo** - Información adicional
- [ ] **Modal de formulario** - Form en modal
- [ ] **Modal fullscreen** - Ocupa toda la pantalla

### Comportamiento
- [ ] **Lock scroll** - Deshabilitar scroll de body
- [ ] **Focus trap** - Tab navega solo dentro del modal
- [ ] **Restore focus** - Volver focus a trigger al cerrar
- [ ] **Stack modals** - Modal sobre otro modal
- [ ] **Animaciones** - Fade in/out, slide, scale

### Tooltips y Popovers
- [ ] **Abrir tooltip** - Hover o focus
- [ ] **Cerrar tooltip** - Mouseleave o blur
- [ ] **Posicionamiento tooltip** - Top, right, bottom, left
- [ ] **Tooltip con delay** - No mostrar inmediatamente
- [ ] **Abrir popover** - Click trigger
- [ ] **Cerrar popover** - Click fuera o close button

### Drawers y Sidebars
- [ ] **Abrir drawer/sidebar** - Slide from side
- [ ] **Cerrar drawer/sidebar** - Slide back
- [ ] **Push content** - Content moves with drawer
- [ ] **Overlay content** - Drawer over content

### Criterios de Validación Modales
```javascript
function validateModalSystem(modals) {
  return {
    // Estructura
    hasModalContainer: document.querySelector('.modal-overlay') !== null,
    hasMultipleModals: document.querySelectorAll('.modal').length > 0,

    // Funcionalidad
    closesOnOverlayClick: modals.closesOnBackdrop,
    closesOnEscKey: modals.closesOnEsc,
    hasCloseButton: document.querySelectorAll('.modal-close').length > 0,

    // Accessibility
    hasFocusTrap: modals.trapsFocus,
    restoresFocus: modals.restoresFocusOnClose,
    hasAccessibleRole: document.querySelectorAll('[role="dialog"]').length > 0,
    hasAriaModal: document.querySelectorAll('[aria-modal="true"]').length > 0,
    hasAriaLabel: document.querySelectorAll('[aria-labelledby]').length > 0,

    // UX
    locksBodyScroll: modals.preventsBackgroundScroll,
    hasAnimations: modals.hasEnterExitAnimations,
    supportsStacking: modals.allowsNestedModals,

    // Tooltips
    hasTooltips: document.querySelectorAll('[data-tooltip]').length > 0,
    hasPopovers: document.querySelectorAll('.popover').length > 0,

    // Drawers
    hasDrawers: document.querySelectorAll('.drawer').length > 0
  };
}
```

### Best Practices Modales
- **Evitar modales innecesarios**: Considerar inline editing primero
- **Confirmar acciones destructivas**: Delete, logout, etc.
- **Clear actions**: Botones con labels claros
- **Mobile friendly**: Fullscreen en mobile
- **Keyboard accessible**: Funciona sin mouse

---

## ✅ Accesibilidad (A11y)

### Navegación con Teclado
- [ ] **Navegación con Tab** - Entre elementos focusables
- [ ] **Navegación con Shift+Tab** - Reverse direction
- [ ] **Navegación con flechas** - En menús, listas, grids
- [ ] **Activar con Enter** - Links, buttons
- [ ] **Activar con Space** - Buttons, checkboxes
- [ ] **Cerrar con Escape** - Modales, dropdowns, menus
- [ ] **Skip to main content** - Skip navigation link
- [ ] **Keyboard shortcuts** - Documentados y customizables

### Focus Management
- [ ] **Focus visible** - Outline claro en elementos focusados
- [ ] **Focus trap** - En modales, no escape afuera
- [ ] **Focus restoration** - Al cerrar modal
- [ ] **Autofocus apropiado** - En modales/forms cuando apropiado
- [ ] **No focus invisible** - Elementos ocultos no focusables

### Screen Reader Support
- [ ] **ARIA labels** - aria-label, aria-labelledby
- [ ] **ARIA roles** - role="button", "navigation", etc.
- [ ] **ARIA live regions** - aria-live para updates dinámicos
- [ ] **ARIA states** - aria-expanded, aria-selected, aria-checked
- [ ] **Alt text** - En todas las imágenes
- [ ] **Landmark regions** - header, nav, main, aside, footer
- [ ] **Heading hierarchy** - h1, h2, h3 en orden correcto

### Preferencias de Usuario
- [ ] **Reduce motion** - prefers-reduced-motion
- [ ] **High contrast** - prefers-contrast
- [ ] **Dark mode** - prefers-color-scheme: dark
- [ ] **Zoom** - Soporte hasta 200%
- [ ] **Text spacing** - No romper con spacing aumentado

### Criterios de Validación A11y
```javascript
function validateAccessibility(app) {
  return {
    // Teclado
    fullKeyboardAccessible: app.hasNoKeyboardTraps && app.allInteractiveElementsFocusable,
    hasSkipLink: document.querySelector('a[href="#main-content"]') !== null,
    hasVisibleFocus: getComputedStyle(document.activeElement).outline !== 'none',

    // ARIA
    hasLandmarks: document.querySelectorAll('[role="main"], [role="navigation"]').length > 0,
    hasAriaLabels: document.querySelectorAll('[aria-label], [aria-labelledby]').length > 0,
    hasAriaLiveRegions: document.querySelectorAll('[aria-live]').length > 0,

    // Estructura
    hasProperHeadings: app.hasHeadingHierarchy,
    hasAltText: Array.from(document.querySelectorAll('img')).every(img => img.alt !== undefined),

    // Interactividad
    hasButtonRoles: document.querySelectorAll('[role="button"]').length > 0,
    hasFormLabels: Array.from(document.querySelectorAll('input')).every(input =>
      input.getAttribute('aria-label') || document.querySelector(`label[for="${input.id}"]`)
    ),

    // Preferencias
    respectsReducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
    respectsColorScheme: window.matchMedia('(prefers-color-scheme: dark)').matches,
    supportsZoom: document.querySelector('meta[name="viewport"]').content.includes('user-scalable=yes'),

    // Testing
    passesAXE: true, // Run axe-core automated testing
    passesLighthouse: app.lighthouseA11yScore >= 90,
    passesWAVE: true // Run WAVE accessibility checker
  };
}
```

### Testing A11y
- **Automated**: axe-core, pa11y, Lighthouse
- **Manual**: Keyboard navigation, screen reader testing
- **Tools**: NVDA, JAWS, VoiceOver, TalkBack
- **Standards**: WCAG 2.1 Level AA mínimo

---

## ✅ Analytics y Tracking

### Page Events
- [ ] **Page view** - Cada carga de página
- [ ] **Virtual page view** - En SPAs, cambios de ruta
- [ ] **Time on page** - Cuánto tiempo estuvo
- [ ] **Scroll depth** - 25%, 50%, 75%, 100%
- [ ] **Bounce** - Salió sin interactuar
- [ ] **Exit page** - Última página antes de salir

### Interaction Events
- [ ] **Click tracking** - Botones, enlaces importantes
- [ ] **Outbound link clicks** - Enlaces externos
- [ ] **Download tracking** - PDF, docs, etc.
- [ ] **Video events** - Play, pause, complete
- [ ] **Engagement events** - Likes, shares, comments
- [ ] **Search queries** - Qué buscan usuarios

### Conversion Events
- [ ] **Goal completado** - Sign up, purchase, etc.
- [ ] **Funnel tracking** - Pasos del funnel
- [ ] **Conversión completada** - Checkout completo
- [ ] **Abandono de carrito** - Dejó items en carrito

### E-commerce Tracking
- [ ] **Product view** - Ver producto
- [ ] **Add to cart** - Agregar al carrito
- [ ] **Remove from cart** - Remover del carrito
- [ ] **Checkout initiated** - Comenzó checkout
- [ ] **Purchase completed** - Transacción completa
- [ ] **Revenue tracking** - Monto de compra

### Form Tracking
- [ ] **Form started** - Usuario comenzó a llenar
- [ ] **Form completed** - Submit exitoso
- [ ] **Form abandoned** - Dejó sin completar
- [ ] **Field errors** - Qué campos tienen errores
- [ ] **Time to complete** - Cuánto tardó

### Error Tracking
- [ ] **JavaScript errors** - Errores en consola
- [ ] **404 errors** - Páginas no encontradas
- [ ] **API errors** - Fallas de backend
- [ ] **Validation errors** - Errores de form

### User Properties
- [ ] **User ID** - Si está logueado
- [ ] **User type** - Free, premium, etc.
- [ ] **Device type** - Desktop, mobile, tablet
- [ ] **Browser** - Chrome, Firefox, etc.
- [ ] **Operating System** - Windows, Mac, etc.
- [ ] **Location** - País, ciudad
- [ ] **Language** - Idioma del browser
- [ ] **Screen resolution** - Tamaño de pantalla

### Custom Events
- [ ] **Feature usage** - Uso de features específicas
- [ ] **A/B test variants** - Qué variante vio
- [ ] **Experiments** - Participación en experiments

### Implementación Analytics
```javascript
// Ejemplo de tracking
function trackEvent(category, action, label, value) {
  // Google Analytics 4
  gtag('event', action, {
    event_category: category,
    event_label: label,
    value: value
  });

  // También enviar a tu propio backend
  fetch('/api/analytics', {
    method: 'POST',
    body: JSON.stringify({
      category, action, label, value,
      timestamp: Date.now(),
      userId: getCurrentUserId(),
      sessionId: getSessionId()
    })
  });
}

// Track click
button.addEventListener('click', () => {
  trackEvent('engagement', 'button_click', 'signup_button');
});

// Track scroll depth
let scrollDepth = 0;
window.addEventListener('scroll', throttle(() => {
  const percent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
  if (percent > scrollDepth && [25, 50, 75, 100].includes(percent)) {
    scrollDepth = percent;
    trackEvent('engagement', 'scroll', `scroll_depth_${percent}`);
  }
}, 500));
```

### Privacy y GDPR
- [ ] **Cookie consent** - Banner de consentimiento
- [ ] **Opt-out** - Permitir deshabilitar tracking
- [ ] **Anonymize IP** - No guardar IPs completas
- [ ] **Data retention** - Política de retención
- [ ] **Privacy policy** - Enlace visible

---

## ✅ Seguridad

### Input Validation
- [ ] **Client-side validation** - UX inmediato
- [ ] **Server-side validation** - CRÍTICO, no confiar en client
- [ ] **Sanitizar inputs** - Limpiar HTML/scripts
- [ ] **Escapar outputs** - Prevenir XSS
- [ ] **Whitelist validation** - Validar contra valores permitidos

### Authentication Security
- [ ] **Strong password requirements** - Complejidad mínima
- [ ] **Password hashing** - bcrypt/argon2
- [ ] **Secure session management** - HttpOnly, Secure cookies
- [ ] **CSRF protection** - Tokens en forms
- [ ] **Rate limiting** - Prevenir brute force
- [ ] **Account lockout** - Después de intentos fallidos
- [ ] **2FA support** - Autenticación de dos factores

### Data Protection
- [ ] **HTTPS everywhere** - OBLIGATORIO en producción
- [ ] **Secure cookies** - Secure, HttpOnly, SameSite
- [ ] **Content Security Policy** - Header CSP
- [ ] **CORS configuration** - Orígenes permitidos
- [ ] **Sensitive data encryption** - En BD y tránsito

### Common Vulnerabilities
- [ ] **SQL Injection** - Prepared statements
- [ ] **XSS (Cross-Site Scripting)** - Sanitización
- [ ] **CSRF** - Tokens
- [ ] **Clickjacking** - X-Frame-Options header
- [ ] **Command Injection** - Validar inputs
- [ ] **Path Traversal** - Validar rutas de archivos
- [ ] **Open Redirect** - Validar URLs de redirección

### Headers de Seguridad
```javascript
// Express ejemplo
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  next();
});
```

---

## ✅ Mejores Prácticas de Implementación

### Performance
- [ ] **Debounce events frecuentes** - input, resize
- [ ] **Throttle scroll events** - Limitar frecuencia
- [ ] **Passive event listeners** - scroll, touch
- [ ] **Event delegation** - Para elementos dinámicos
- [ ] **Remove listeners** - Al desmontar componentes
- [ ] **Prevent memory leaks** - Cleanup en cleanup phase
- [ ] **requestAnimationFrame** - Para animaciones
- [ ] **Lazy load handlers** - Cargar bajo demanda
- [ ] **Code splitting** - Dividir bundles grandes
- [ ] **Tree shaking** - Eliminar código no usado

### UX Best Practices
- [ ] **Feedback inmediato** - En todas las interacciones
- [ ] **Loading states** - Spinners, skeletons
- [ ] **Optimistic UI** - Actualizar antes de confirm
- [ ] **Confirmaciones** - Para acciones destructivas
- [ ] **Undo/redo** - Cuando sea apropiado
- [ ] **Auto-save** - Prevenir pérdida de datos
- [ ] **Indicar campos requeridos** - Asterisco o label
- [ ] **Errores claros** - Usuario entiende qué hacer
- [ ] **Success feedback** - Confirmar acción exitosa
- [ ] **Progress indicators** - Para procesos largos

### Mobile Best Practices
- [ ] **Touch targets** - Mínimo 44x44px
- [ ] **Tap delay** - Eliminar 300ms delay
- [ ] **Touch feedback** - :active states
- [ ] **Swipe gestures** - Intuitive navigation
- [ ] **Responsive design** - Mobile-first
- [ ] **Viewport meta tag** - Configurado correctamente

### Testing Best Practices
- [ ] **Unit tests** - Para event handlers
- [ ] **Integration tests** - Para flujos
- [ ] **E2E tests** - User journeys completos
- [ ] **Accessibility tests** - axe, pa11y
- [ ] **Cross-browser testing** - Chrome, Firefox, Safari, Edge
- [ ] **Mobile testing** - iOS, Android
- [ ] **Screen reader testing** - NVDA, VoiceOver
- [ ] **Performance testing** - Lighthouse, WebPageTest

### Monitoring
- [ ] **Error tracking** - Sentry, Rollbar
- [ ] **Analytics events** - GA, Mixpanel
- [ ] **Performance metrics** - Core Web Vitals
- [ ] **Real User Monitoring** - RUM
- [ ] **A/B testing** - Experiments
- [ ] **Feature flags** - Toggles para features
- [ ] **Real-time monitoring** - Alertas
- [ ] **Log aggregation** - Centralized logging

---

## 📊 Checklist Resumido para Validación Rápida

### Eventos Básicos (Obligatorios)
- ✅ Mouse: click, hover, contextmenu
- ✅ Teclado: keydown, shortcuts, navegación Tab
- ✅ Formularios: submit, validación, error handling
- ✅ Carga: DOMContentLoaded, loading states
- ✅ Ventana: resize (debounce), scroll (throttle)

### Interactividad (Recomendado)
- ✅ Drag & Drop: si aplica a la funcionalidad
- ✅ Clipboard: copiar/pegar cuando sea útil
- ✅ Touch: soporte mobile básico
- ✅ Modales: implementación accesible
- ✅ Navegación: SPA routing o páginas tradicionales

### Avanzado (Según Requerimientos)
- ✅ E-commerce: carrito, checkout, pagos
- ✅ Chat: mensajería real-time
- ✅ Media: players de audio/video
- ✅ PWA: service worker, offline support
- ✅ Analytics: tracking de eventos críticos

### Obligatorio Siempre
- ✅ Accesibilidad: keyboard nav, ARIA, screen readers
- ✅ Seguridad: validación, sanitización, HTTPS
- ✅ Performance: debounce, throttle, lazy loading
- ✅ Error Handling: try-catch, error boundaries
- ✅ Testing: unit, integration, e2e tests

---

## 🎯 Criterios de Aprobación

Un proyecto pasa la validación si cumple:

1. **Core Events (100%)**: Todos los eventos básicos implementados
2. **Accessibility (WCAG AA)**: Navegación teclado + screen reader
3. **Security (OWASP)**: Sin vulnerabilidades críticas/altas
4. **Performance**: Lighthouse > 90
5. **Testing**: Coverage > 80%
6. **Documentation**: Eventos documentados

---

**Este checklist debe ser usado por los agentes de Review, Security y QA para validar completitud y calidad de implementaciones web.**
