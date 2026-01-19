---
id: web-events-media-advanced
title: "Web Events - Media, APIs Modernas y Features Avanzados"
category: frontend
subcategory: events
type: checklist
version: "1.0.0"
last_updated: "2026-01-14"
author: hands-on-ai
status: active
machine_readable: true
tags:
  - media-events
  - audio
  - video
  - animations
  - transitions
  - authentication
  - profile
  - navigation
  - search
  - modern-apis
  - intersection-observer
  - pwa
  - progressive-web-app
  - service-worker
agents:
  primary:
    - review
    - coding
    - qa
  secondary:
    - security
    - optimization
related_documents:
  - path: "knowledge_base/technologies/frontend/web-events/INDEX.md"
    type: index
  - path: "project_meta/security/threat-model.yaml"
    type: security
    sections:
      - authentication_events
      - media_events
  - path: "project_meta/ai-context/prompt-library.json"
    type: configuration
    prompts:
      - web_events_validation
      - accessibility_audit
total_items: 200
event_categories:
  - name: "Media Events"
    count: 33
  - name: "Animations & Transitions"
    count: 14
  - name: "Authentication"
    count: 17
  - name: "Profile & Account"
    count: 11
  - name: "Navigation"
    count: 14
  - name: "Search & Filters"
    count: 13
  - name: "Modern APIs"
    count: 33
  - name: "PWA Features"
    count: 14
security_level: critical
accessibility_required: true
performance_critical: true
compliance:
  - authentication
  - pwa
---

# Web Events - Media, APIs Modernas y Features Avanzados

## ✅ Eventos de Media (Audio/Video)

### Controles de Reproducción
- [ ] **play** - Iniciar reproducción
- [ ] **pause** - Pausar reproducción
- [ ] **playing** - Reproducción activa (después de buffer)
- [ ] **ended** - Media terminado
- [ ] **seeking** - Usuario buscando posición
- [ ] **seeked** - Búsqueda completada
- [ ] **timeupdate** - Actualizar barra de progreso (cada ~250ms)
- [ ] **ratechange** - Cambio de velocidad de reproducción
- [ ] **volumechange** - Cambio de volumen

### Carga de Media
- [ ] **loadstart** - Comenzar a cargar
- [ ] **loadedmetadata** - Duración y dimensiones disponibles
- [ ] **loadeddata** - Primer frame cargado
- [ ] **canplay** - Suficiente data para reproducir
- [ ] **canplaythrough** - Puede reproducir sin parar
- [ ] **progress** - Progreso de buffering
- [ ] **waiting** - Esperando más datos (mostrar spinner)
- [ ] **stalled** - Descarga estancada
- [ ] **suspend** - Descarga suspendida intencionalmente
- [ ] **emptied** - Media removido/reiniciado

### Implementaciones Obligatorias
- [ ] **Controles personalizados** - No depender solo de controles nativos
- [ ] **Barra de progreso interactiva** - Click para seek
- [ ] **Control de volumen** - Slider con persistencia
- [ ] **Botón play/pause** - Con indicador visual claro
- [ ] **Pantalla completa** - Fullscreen API
- [ ] **Picture-in-picture** - PiP API para video
- [ ] **Subtítulos/captions** - Track support con toggle
- [ ] **Indicador de buffering** - Feedback visual durante wait
- [ ] **Manejo de errores** - Mostrar mensaje si falla carga

### Criterios de Validación
```javascript
// Validación de media player
function validateMediaPlayer(player) {
  return {
    hasCustomControls: player.controls === false && player.querySelector('.custom-controls'),
    hasPlayPauseButton: player.querySelector('.play-pause') !== null,
    hasProgressBar: player.querySelector('.progress-bar') !== null,
    hasVolumeControl: player.querySelector('.volume-control') !== null,
    hasFullscreenSupport: document.fullscreenEnabled,
    hasPiPSupport: document.pictureInPictureEnabled,
    hasSubtitleSupport: player.querySelectorAll('track').length > 0,
    hasErrorHandling: player.onerror !== null,
    hasLoadingIndicator: player.querySelector('.loading-spinner') !== null
  };
}
```

### Aspectos de Seguridad
- **Content Security Policy**: Validar origen de media
- **DRM**: Implementar si contenido es protegido
- **Hotlinking Prevention**: Prevenir uso no autorizado

---

## ✅ Eventos de Animación y Transición

### CSS Animations
- [ ] **animationstart** - Animación comienza
- [ ] **animationend** - Animación termina (limpiar clases)
- [ ] **animationiteration** - Cada repetición de animación
- [ ] **animationcancel** - Animación cancelada

### CSS Transitions
- [ ] **transitionstart** - Transición comienza
- [ ] **transitionend** - Transición termina (ejecutar callbacks)
- [ ] **transitionrun** - Transición ejecutándose
- [ ] **transitioncancel** - Transición cancelada

### Implementaciones Obligatorias
- [ ] **Animaciones de entrada/salida** - Para modales, dropdowns
- [ ] **Loading spinners animados** - CSS animations
- [ ] **Transiciones de página** - Smooth page transitions
- [ ] **Micro-interacciones** - Feedback en botones, hover states
- [ ] **Animaciones de scroll** - Reveal on scroll
- [ ] **Parallax effects** - Si diseño lo requiere

### Criterios de Validación
```javascript
// Validación de animaciones
function validateAnimations(app) {
  return {
    hasEnterExitAnimations: document.querySelectorAll('[class*="animate-"]').length > 0,
    hasLoadingSpinner: document.querySelector('.spinner') !== null,
    hasTransitionCallbacks: true, // verificar listeners de transitionend
    respectsReducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
    hasScrollAnimations: 'IntersectionObserver' in window
  };
}
```

### Accesibilidad
- **prefers-reduced-motion**: OBLIGATORIO respetar esta preferencia
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## ✅ Sistema de Autenticación

### Flujo de Login
- [ ] **Visitar página de login** - Renderizar formulario
- [ ] **Enviar formulario de login** - POST credentials
- [ ] **Login exitoso** - Guardar token, redireccionar a dashboard
- [ ] **Login fallido** - Mostrar error específico (max 3 intentos)
- [ ] **Logout** - Limpiar sesión, tokens, redireccionar a login
- [ ] **Sesión timeout** - Detectar expiración, mostrar modal, refresh token
- [ ] **Renovar token automáticamente** - Antes de expiración
- [ ] **Detectar múltiples sesiones** - Opcionalmente invalidar otras

### Registro y Verificación
- [ ] **Registro de nueva cuenta** - Validación completa
- [ ] **Verificación de email** - Enviar código, validar
- [ ] **Verificación de teléfono** - SMS/WhatsApp OTP
- [ ] **Confirmación de cuenta** - Click en link de email

### Recuperación de Contraseña
- [ ] **Olvidé contraseña** - Formulario email
- [ ] **Enviar email de reset** - Token con expiración
- [ ] **Reset de contraseña** - Nueva contraseña con validación
- [ ] **Confirmación de cambio** - Email notificando cambio

### Seguridad Avanzada
- [ ] **Cambio de contraseña** - Requiere contraseña actual
- [ ] **Habilitar 2FA** - TOTP, SMS, o app authenticator
- [ ] **Verificar código 2FA** - Durante login
- [ ] **Códigos de respaldo** - Para recuperación si pierde 2FA

### Criterios de Validación
```javascript
// Validación de sistema de autenticación
function validateAuthSystem(auth) {
  return {
    hasSecureStorage: auth.usesHttpOnlyCookies || auth.usesSecureStorage,
    hasTokenRefresh: auth.hasRefreshTokenMechanism,
    hasPasswordValidation: auth.validatePasswordStrength,
    has2FASupport: auth.supports2FA,
    hasRateLimiting: auth.hasRateLimit,
    hasSessionTimeout: auth.hasSessionExpiration,
    hasSecureLogout: auth.clearsAllTokens,
    hasAccountLockout: auth.locksAfterFailedAttempts,
    hasBruteForceProtection: auth.hasRateLimit && auth.hasCaptcha
  };
}
```

### Aspectos de Seguridad CRÍTICOS
- **Password Hashing**: OBLIGATORIO usar bcrypt/argon2 (NUNCA MD5/SHA1)
- **JWT Secrets**: Usar claves fuertes, rotar periódicamente
- **HTTPS Only**: NUNCA transmitir credenciales en HTTP
- **HttpOnly Cookies**: Para tokens de sesión
- **CSRF Tokens**: En todos los formularios de auth
- **Rate Limiting**: Máximo 5 intentos por IP/cuenta en 15 min
- **Account Lockout**: Bloquear temporalmente después de intentos fallidos
- **Audit Logging**: Registrar todos los eventos de autenticación

---

## ✅ Eventos de Perfil y Cuenta

### Gestión de Perfil
- [ ] **Ver perfil de usuario** - Mostrar información
- [ ] **Editar información personal** - Nombre, email, bio
- [ ] **Actualizar avatar/foto** - Upload + crop
- [ ] **Crop de imagen de perfil** - Canvas API o librería
- [ ] **Cambiar configuración de privacidad** - Público/privado
- [ ] **Modificar preferencias de notificaciones** - Por canal
- [ ] **Cambiar tema** - Dark/light/auto
- [ ] **Cambiar idioma** - i18n support

### Gestión de Datos
- [ ] **Exportar datos personales** - GDPR compliance
- [ ] **Eliminar cuenta** - Confirmación + password
- [ ] **Desactivar cuenta temporalmente** - Opción de reactivar

### Criterios de Validación
```javascript
// Validación de gestión de perfil
function validateProfileManagement(profile) {
  return {
    hasEditCapability: profile.canEdit,
    hasAvatarUpload: profile.canUploadAvatar,
    hasImageCropping: profile.hasCropTool,
    hasPrivacySettings: profile.hasPrivacyControls,
    hasNotificationPreferences: profile.hasNotificationSettings,
    hasThemeSelector: profile.hasThemeToggle,
    hasLanguageSelector: profile.hasLanguageSwitcher,
    hasDataExport: profile.canExportData, // GDPR
    hasAccountDeletion: profile.canDeleteAccount
  };
}
```

---

## ✅ Eventos de Navegación

### Navegación Principal
- [ ] **Cargar página inicial** - Home/dashboard
- [ ] **Cambiar de ruta/página** - SPA routing o page load
- [ ] **Click en enlaces internos** - Sin full page reload (SPA)
- [ ] **Click en enlaces externos** - Abrir en nueva pestaña con `rel="noopener"`
- [ ] **Navegación breadcrumb** - Mostrar path actual
- [ ] **Abrir/cerrar menú hamburguesa** - Mobile menu
- [ ] **Abrir/cerrar sidebar** - Desktop sidebar toggle
- [ ] **Abrir/cerrar dropdown** - Menús desplegables

### Navegación de Contenido
- [ ] **Scroll to top** - Botón flotante (mostrar después de scroll)
- [ ] **Scroll to section** - Smooth scroll con `scrollIntoView`
- [ ] **Infinite scroll** - Cargar más al llegar al final
- [ ] **Paginación** - Next/previous, números de página
- [ ] **Tabs** - Cambiar contenido sin cambiar ruta
- [ ] **Accordion** - Expandir/colapsar secciones

### Criterios de Validación
```javascript
// Validación de navegación
function validateNavigation(nav) {
  return {
    hasSPARouting: history.pushState !== undefined,
    hasSmoothScroll: CSS.supports('scroll-behavior', 'smooth'),
    hasInfiniteScroll: 'IntersectionObserver' in window,
    hasPagination: nav.querySelector('.pagination') !== null,
    hasBreadcrumbs: nav.querySelector('.breadcrumb') !== null,
    hasScrollToTop: nav.querySelector('.scroll-to-top') !== null,
    hasAccessibleNav: nav.querySelector('nav[role="navigation"]') !== null,
    hasKeyboardNav: true // verificar Tab navigation
  };
}
```

### Aspectos de Seguridad
- **Open Redirect**: Validar URLs de redirección
- **XSS in Routes**: Sanitizar parámetros de ruta
- **CSRF on Navigation**: Proteger acciones en cambios de ruta

---

## ✅ Eventos de Búsqueda y Filtros

### Funcionalidad de Búsqueda
- [ ] **Escribir en barra de búsqueda** - Input event con debounce
- [ ] **Enviar búsqueda** - Submit o Enter key
- [ ] **Búsqueda instantánea** - Autocomplete con sugerencias
- [ ] **Seleccionar sugerencia** - Ejecutar búsqueda
- [ ] **Limpiar búsqueda** - Botón X para clear
- [ ] **Sin resultados** - Mensaje útil con sugerencias

### Filtros y Ordenamiento
- [ ] **Aplicar filtros** - Checkboxes, selects, ranges
- [ ] **Remover filtro específico** - Click en tag de filtro
- [ ] **Limpiar todos los filtros** - Botón "Clear all"
- [ ] **Ordenar resultados** - A-Z, fecha, precio, relevancia
- [ ] **Cambiar vista** - Grid vs List
- [ ] **Filtros avanzados** - Modal con más opciones

### Funcionalidades Avanzadas
- [ ] **Búsqueda por voz** - Web Speech API
- [ ] **Historial de búsquedas** - LocalStorage
- [ ] **Búsquedas populares** - Mostrar trending
- [ ] **Búsqueda con filtros** - Combinar search + filters

### Criterios de Validación
```javascript
// Validación de búsqueda y filtros
function validateSearchAndFilters(search) {
  return {
    hasSearchInput: search.querySelector('input[type="search"]') !== null,
    hasAutocomplete: search.hasAttribute('autocomplete'),
    hasDebouncedSearch: true, // verificar implementación debounce
    hasFilterOptions: search.querySelectorAll('[data-filter]').length > 0,
    hasClearFilters: search.querySelector('.clear-filters') !== null,
    hasSortOptions: search.querySelector('select[name="sort"]') !== null,
    hasViewToggle: search.querySelector('.view-toggle') !== null,
    hasNoResultsState: search.querySelector('.no-results') !== null,
    hasLoadingState: search.querySelector('.search-loading') !== null
  };
}
```

### Optimización
- **Debounce**: Esperar 300ms después de última tecla antes de buscar
- **Caching**: Cachear resultados de búsquedas recientes
- **Pagination**: Para muchos resultados
- **Server-side**: Búsquedas complejas en backend

---

## ✅ APIs Web Modernas

### Intersection Observer
- [ ] **Elemento visible en viewport** - Callback cuando entra/sale
- [ ] **Lazy load imágenes** - Cargar cuando está cerca del viewport
- [ ] **Infinite scroll** - Detectar llegada al final
- [ ] **Animaciones on scroll** - Trigger cuando elemento visible
- [ ] **Analytics** - Trackear elementos vistos

```javascript
// Ejemplo de implementación
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      // Elemento visible
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.5 });
```

### Mutation Observer
- [ ] **DOM modificado** - Detectar cambios en DOM
- [ ] **Atributos cambiados** - Monitor attribute changes
- [ ] **Nodos agregados/removidos** - Detectar elementos nuevos
- [ ] **Re-inicializar plugins** - Cuando DOM cambia

### Resize Observer
- [ ] **Elemento redimensionado** - Sin usar window.resize
- [ ] **Ajustar componentes responsive** - Basado en tamaño container
- [ ] **Recalcular layouts** - Charts, grids

### Performance Observer
- [ ] **Medir FCP** - First Contentful Paint
- [ ] **Medir LCP** - Largest Contentful Paint
- [ ] **Medir FID** - First Input Delay
- [ ] **Medir CLS** - Cumulative Layout Shift
- [ ] **Detectar long tasks** - Tareas > 50ms
- [ ] **Navigation timing** - Performance de navegación

```javascript
// Core Web Vitals
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log(entry.name, entry.value);
  }
});
observer.observe({ entryTypes: ['largest-contentful-paint', 'first-input', 'layout-shift'] });
```

### Geolocation API
- [ ] **Solicitar permiso de ubicación** - Permission API
- [ ] **Obtener ubicación actual** - getCurrentPosition
- [ ] **Watch position** - Tracking continuo
- [ ] **Error de geolocalización** - Manejar permission denied
- [ ] **Usar ubicación para búsquedas** - "Tiendas cerca de mí"
- [ ] **Mostrar en mapa** - Integración con maps API

### Page Visibility API
- [ ] **Página visible** - document.visibilityState === 'visible'
- [ ] **Página oculta** - Pausar actividades
- [ ] **Pausar animaciones** - Cuando hidden
- [ ] **Pausar videos** - Cuando hidden
- [ ] **Detener polling** - Cuando hidden, reanudar cuando visible

### Fullscreen API
- [ ] **Entrar a pantalla completa** - requestFullscreen()
- [ ] **Salir de pantalla completa** - exitFullscreen()
- [ ] **Fullscreen change** - Detectar cambios
- [ ] **Fullscreen error** - Manejar errores

### Web Speech API
- [ ] **Iniciar reconocimiento de voz** - SpeechRecognition
- [ ] **Recibir resultado** - onresult event
- [ ] **Error en reconocimiento** - onerror event
- [ ] **Finalizar reconocimiento** - onend event
- [ ] **Text-to-speech** - SpeechSynthesis

### Battery API
- [ ] **Nivel de batería** - navigator.getBattery()
- [ ] **Estado de carga** - Charging/discharging
- [ ] **Modo ahorro energía** - Reducir operaciones pesadas

---

## ✅ Progressive Web Apps (PWA)

### Service Worker
- [ ] **Service Worker instalado** - install event
- [ ] **Service Worker activado** - activate event
- [ ] **Service Worker actualizado** - Detectar nueva versión
- [ ] **Interceptar fetch requests** - fetch event
- [ ] **Cachear recursos** - Cache API
- [ ] **Servir desde cache** - Offline-first strategy
- [ ] **Background sync** - Sync cuando vuelve online
- [ ] **Push notification recibida** - push event

### Instalación PWA
- [ ] **Mostrar banner "Agregar a inicio"** - beforeinstallprompt
- [ ] **App instalada** - appinstalled event
- [ ] **App abierta desde home screen** - Detectar standalone mode
- [ ] **Offline mode activado** - Mostrar banner
- [ ] **Conexión restaurada** - Online event
- [ ] **Actualización disponible** - Notificar usuario

### Criterios de Validación
```javascript
// Validación de PWA
function validatePWA(app) {
  return {
    hasServiceWorker: 'serviceWorker' in navigator,
    hasManifest: document.querySelector('link[rel="manifest"]') !== null,
    hasOfflineSupport: true, // verificar cache strategy
    hasInstallPrompt: app.hasInstallButton,
    hasUpdateNotification: app.notifiesOnUpdate,
    hasPushNotifications: 'PushManager' in window,
    hasBackgroundSync: 'sync' in registration,
    meetsLighthouseScore: app.lighthouseScore >= 90
  };
}
```

### Requisitos PWA
1. **HTTPS obligatorio** (excepto localhost)
2. **Manifest.json** con todos los campos requeridos
3. **Service Worker** registrado y activo
4. **Offline fallback** al menos una página
5. **Icons** en múltiples tamaños (192px, 512px)

---

*Continúa en el siguiente archivo para E-Commerce, Chat, y más...*
