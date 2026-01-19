---
id: web-events-ecommerce-social
title: "Web Events - E-Commerce, Social y Contenido"
category: frontend
subcategory: events
type: checklist
version: "1.0.0"
last_updated: "2026-01-14"
author: hands-on-ai
status: active
machine_readable: true
tags:
  - ecommerce
  - shopping-cart
  - checkout
  - payment
  - social-features
  - likes
  - comments
  - shares
  - notifications
  - chat
  - messaging
  - real-time
agents:
  primary:
    - review
    - security
    - coding
  secondary:
    - qa
    - optimization
related_documents:
  - path: "knowledge_base/technologies/frontend/web-events/INDEX.md"
    type: index
  - path: "project_meta/security/threat-model.yaml"
    type: security
    sections:
      - ecommerce_events
      - chat_messaging_events
  - path: "project_meta/ai-context/prompt-library.json"
    type: configuration
    prompts:
      - ecommerce_validation
      - security_events_audit
total_items: 200
event_categories:
  - name: "E-Commerce Navigation"
    count: 17
  - name: "Reviews & Ratings"
    count: 9
  - name: "Shopping Cart"
    count: 15
  - name: "Checkout Process"
    count: 26
  - name: "Post-Purchase"
    count: 9
  - name: "Content Visualization"
    count: 23
  - name: "Social Interactions"
    count: 23
  - name: "Notifications"
    count: 13
  - name: "Chat & Messaging"
    count: 26
security_level: critical
accessibility_required: true
performance_critical: true
compliance:
  - pci-dss
  - gdpr
  - payment-security
---

# Web Events - E-Commerce, Social y Contenido

## ✅ Eventos de E-Commerce

### Navegación de Productos

#### Listado y Visualización
- [ ] **Ver lista de productos** - Grid/list view con paginación
- [ ] **Ver detalle de producto** - Página individual con toda la info
- [ ] **Ver galería de imágenes** - Múltiples imágenes con thumbnails
- [ ] **Zoom en imagen de producto** - Lens/lightbox para ver detalles
- [ ] **Ver video de producto** - Si disponible
- [ ] **Cambiar variante** - Color, talla, modelo (actualizar precio/stock)
- [ ] **Ver disponibilidad de stock** - En tiempo real
- [ ] **Ver tabla de tallas** - Modal informativo

#### Búsqueda y Filtrado
- [ ] **Buscar productos** - Full-text search
- [ ] **Filtrar por categoría** - Checkbox/select
- [ ] **Filtrar por precio** - Range slider
- [ ] **Filtrar por marca** - Multi-select
- [ ] **Filtrar por rating** - Stars filter
- [ ] **Filtrar por disponibilidad** - In stock/out of stock
- [ ] **Ordenar productos** - Precio, popularidad, fecha, rating
- [ ] **Comparar productos** - Side-by-side comparison
- [ ] **Quick view** - Modal con info rápida sin cambiar página

### Reviews y Ratings

- [ ] **Ver reseñas** - Lista paginada
- [ ] **Filtrar reseñas por rating** - 5 stars, 4 stars, etc.
- [ ] **Ordenar reseñas** - Más útiles, recientes, rating
- [ ] **Escribir reseña** - Form con rating + texto
- [ ] **Subir fotos en reseña** - Multiple images
- [ ] **Calificar producto** - Star rating system
- [ ] **Marcar reseña útil** - Thumbs up/down
- [ ] **Reportar reseña** - Si es spam/inapropiada
- [ ] **Verificar compra** - Badge "Verified Purchase"

### Carrito de Compras

#### Gestión del Carrito
- [ ] **Agregar producto al carrito** - Con feedback visual
- [ ] **Actualizar cantidad en carrito** - +/- buttons o input
- [ ] **Remover producto del carrito** - Con confirmación
- [ ] **Ver carrito** - Sidebar o página dedicada
- [ ] **Vaciar carrito completo** - Con confirmación
- [ ] **Persistencia del carrito** - LocalStorage o sesión
- [ ] **Sincronizar carrito** - Si usuario se loguea
- [ ] **Límites de cantidad** - Máximo por producto

#### Wishlist y Guardados
- [ ] **Agregar a wishlist** - Ícono corazón
- [ ] **Remover de wishlist** - Toggle
- [ ] **Ver wishlist** - Página dedicada
- [ ] **Mover de wishlist a carrito** - Quick action
- [ ] **Guardar para después** - Diferente a wishlist
- [ ] **Compartir wishlist** - Share link

#### Descuentos y Cálculos
- [ ] **Aplicar cupón de descuento** - Input + botón aplicar
- [ ] **Validar cupón** - Verificar validez y condiciones
- [ ] **Remover cupón** - Recalcular total
- [ ] **Ver total calculado** - Subtotal + descuentos + envío + impuestos
- [ ] **Calcular envío** - Basado en dirección/código postal
- [ ] **Ver breakdown de costos** - Desglose detallado

### Proceso de Checkout

#### Inicio y Datos
- [ ] **Proceder a checkout** - Desde carrito
- [ ] **Iniciar checkout** - Página de checkout
- [ ] **Checkout como invitado** - Sin crear cuenta
- [ ] **Login para checkout** - Si ya tiene cuenta
- [ ] **Autocompletar datos** - Si usuario logueado

#### Dirección de Envío
- [ ] **Ingresar dirección de envío** - Form completo
- [ ] **Seleccionar dirección guardada** - Si tiene varias
- [ ] **Validar dirección** - API de validación
- [ ] **Usar dirección de facturación diferente** - Checkbox + form adicional
- [ ] **Guardar dirección** - Para futuras compras

#### Método de Envío
- [ ] **Seleccionar método de envío** - Standard, express, overnight
- [ ] **Ver costos de envío** - Para cada opción
- [ ] **Ver tiempo estimado** - Días de entrega
- [ ] **Rastreo incluido** - Información de tracking

#### Pago
- [ ] **Ingresar información de pago** - Tarjeta de crédito/débito
- [ ] **Seleccionar método de pago guardado** - Tarjetas guardadas
- [ ] **Guardar método de pago** - Checkbox
- [ ] **Tokenización de tarjeta** - No guardar datos reales
- [ ] **Aplicar gift card** - Input + validación
- [ ] **Pagos alternativos** - PayPal, Apple Pay, Google Pay

#### Confirmación y Resultado
- [ ] **Ver resumen de orden** - Todos los detalles
- [ ] **Aceptar términos y condiciones** - Checkbox obligatorio
- [ ] **Confirmar compra** - Botón final
- [ ] **Procesar pago** - Loading state
- [ ] **Pago exitoso** - Página de confirmación
- [ ] **Pago fallido** - Mensaje de error específico
- [ ] **Enviar email de confirmación** - Con número de orden
- [ ] **Redireccionar a página de éxito** - Con detalles de orden

### Post-Compra

- [ ] **Ver historial de pedidos** - Lista de todas las compras
- [ ] **Ver detalle de pedido** - Página con toda la info
- [ ] **Rastrear envío** - Integración con courier
- [ ] **Cancelar pedido** - Si aún no se envió
- [ ] **Solicitar devolución** - Form con razón
- [ ] **Proceso de devolución** - Steps y tracking
- [ ] **Imprimir factura** - PDF descargable
- [ ] **Re-ordenar** - Copiar pedido anterior al carrito
- [ ] **Contactar soporte sobre pedido** - Chat/email

### Criterios de Validación E-Commerce
```javascript
function validateEcommerceFlow(ecommerce) {
  return {
    // Productos
    hasProductListing: ecommerce.hasProductGrid,
    hasProductDetail: ecommerce.hasDetailPage,
    hasImageGallery: ecommerce.hasGallery,
    hasVariantSelection: ecommerce.hasVariants,
    hasStockIndicator: ecommerce.showsStock,

    // Búsqueda y Filtros
    hasSearch: ecommerce.hasSearchBar,
    hasFilters: ecommerce.hasFilterOptions,
    hasSorting: ecommerce.hasSortOptions,

    // Reviews
    hasReviewSystem: ecommerce.allowsReviews,
    hasRatingDisplay: ecommerce.showsRatings,

    // Carrito
    hasAddToCart: ecommerce.hasCartFunctionality,
    hasCartPersistence: ecommerce.persistsCart,
    hasQuantityUpdate: ecommerce.allowsQuantityChange,
    hasWishlist: ecommerce.hasWishlistFeature,

    // Checkout
    hasSecureCheckout: ecommerce.usesHTTPS && ecommerce.hasSSLCertificate,
    hasGuestCheckout: ecommerce.allowsGuestCheckout,
    hasMultiplePaymentMethods: ecommerce.paymentMethods.length > 1,
    hasAddressValidation: ecommerce.validatesAddress,
    hasOrderConfirmation: ecommerce.sendsConfirmationEmail,

    // Post-compra
    hasOrderTracking: ecommerce.hasTrackingIntegration,
    hasOrderHistory: ecommerce.showsOrderHistory,
    hasReturnProcess: ecommerce.allowsReturns
  };
}
```

### Aspectos de Seguridad CRÍTICOS
- **PCI DSS Compliance**: NUNCA guardar números de tarjeta completos
- **Payment Gateway**: Usar Stripe, PayPal, etc. (no procesar directamente)
- **SSL/TLS**: OBLIGATORIO HTTPS en todo el flujo
- **Tokenización**: Guardar solo tokens, no datos de pago
- **3D Secure**: Implementar para autenticación adicional
- **Fraud Detection**: Integrar sistema de detección de fraude
- **Rate Limiting**: En checkout para prevenir bots
- **Session Security**: Timeouts y validación de sesión

---

## ✅ Eventos de Contenido

### Visualización de Contenido
- [ ] **Ver artículo/post completo** - Página dedicada
- [ ] **Expandir contenido truncado** - "Read more" button
- [ ] **Reproducir video embebido** - YouTube, Vimeo, etc.
- [ ] **Ver imagen en lightbox** - Click para fullscreen
- [ ] **Galería de imágenes** - Siguiente/anterior navigation
- [ ] **Cerrar lightbox/modal** - X button, ESC, click outside
- [ ] **Descargar archivo/documento** - Download button
- [ ] **Compartir contenido** - Share buttons
- [ ] **Imprimir página/contenido** - Print-friendly version
- [ ] **Leer más / Ver más** - Paginate long content

### Interacciones Sociales

#### Reacciones
- [ ] **Dar like/me gusta** - Toggle button con counter
- [ ] **Quitar like** - Toggle off
- [ ] **Dar dislike** - Si aplica (YouTube style)
- [ ] **Reacciones múltiples** - Facebook style (love, haha, wow, etc.)
- [ ] **Ver quién dio like** - Modal con lista
- [ ] **Animación de like** - Micro-interaction

#### Guardados y Favoritos
- [ ] **Guardar en favoritos** - Bookmark icon
- [ ] **Quitar de favoritos** - Toggle off
- [ ] **Ver favoritos guardados** - Colección personal
- [ ] **Organizar en colecciones** - Carpetas/tags
- [ ] **Compartir colección** - Si feature social

#### Compartir
- [ ] **Compartir en redes sociales** - Facebook, Twitter, LinkedIn, etc.
- [ ] **Copiar enlace para compartir** - Clipboard + feedback
- [ ] **Compartir por email** - Mailto o form
- [ ] **Compartir por WhatsApp** - Deep link
- [ ] **Código embed** - Para embeber en otros sitios
- [ ] **QR code** - Generar para compartir físicamente

#### Comentarios
- [ ] **Ver comentarios** - Lista con paginación
- [ ] **Comentar** - Form con validación
- [ ] **Editar comentario** - Solo autor, time limit
- [ ] **Eliminar comentario** - Con confirmación
- [ ] **Responder a comentario** - Threading/nested comments
- [ ] **Like a comentario** - Thumbs up
- [ ] **Ordenar comentarios** - Más recientes, más populares, antiguos
- [ ] **Reportar comentario/contenido** - Si es inapropiado
- [ ] **Moderar comentarios** - Si eres admin/moderador

#### Usuarios y Seguidores
- [ ] **Bloquear usuario** - No ver su contenido
- [ ] **Seguir usuario/página** - Subscribe to updates
- [ ] **Dejar de seguir** - Unsubscribe
- [ ] **Ver seguidores** - Lista
- [ ] **Ver siguiendo** - A quién sigue el usuario

#### Listas y Colecciones
- [ ] **Crear lista/colección** - Agregar título y descripción
- [ ] **Editar lista** - Modificar nombre/descripción
- [ ] **Agregar a lista** - Seleccionar lista existente
- [ ] **Remover de lista** - Quitar item
- [ ] **Eliminar lista** - Con confirmación
- [ ] **Compartir lista** - Pública o privada
- [ ] **Colaborar en lista** - Múltiples editores

### Criterios de Validación de Contenido Social
```javascript
function validateSocialFeatures(content) {
  return {
    // Visualización
    hasLightbox: content.querySelector('.lightbox') !== null,
    hasImageGallery: content.querySelector('.gallery') !== null,
    hasShareButtons: content.querySelectorAll('.share-btn').length > 0,

    // Reacciones
    hasLikeButton: content.querySelector('.like-btn') !== null,
    hasLikeCounter: content.querySelector('.like-count') !== null,
    hasReactionTypes: content.querySelectorAll('[data-reaction]').length > 1,

    // Favoritos
    hasBookmarkFeature: content.querySelector('.bookmark-btn') !== null,
    hasFavoritesPage: document.querySelector('[href="/favorites"]') !== null,

    // Comentarios
    hasCommentSection: content.querySelector('.comments') !== null,
    allowsComments: content.querySelector('.comment-form') !== null,
    hasCommentModeration: content.hasAttribute('data-moderated'),
    hasNestedComments: content.querySelector('.comment-reply') !== null,

    // Social
    hasFollowButton: content.querySelector('.follow-btn') !== null,
    hasUserProfiles: document.querySelector('[href^="/user/"]') !== null,
    hasBlockFeature: content.hasBlockFunctionality,

    // Colecciones
    hasCollections: content.hasCollectionFeature,
    allowsCollectionCreation: content.canCreateCollections
  };
}
```

### Aspectos de Seguridad
- **XSS in Comments**: OBLIGATORIO sanitizar HTML en comentarios
- **SQL Injection**: Parametrizar queries de búsqueda de contenido
- **CSRF**: Tokens en todas las acciones (like, comment, follow)
- **Rate Limiting**: Prevenir spam de likes/comments
- **Content Moderation**: Sistema de moderación y reportes
- **Privacy Controls**: Respetar configuraciones de privacidad

---

## ✅ Eventos de Notificaciones

### Tipos de Notificaciones
- [ ] **Recibir notificación push** - Browser push notification
- [ ] **Toast notification** - Pequeña notificación temporal
- [ ] **Banner notification** - Top of page banner
- [ ] **Badge notification** - Counter en icon (ej: "3" en bell icon)
- [ ] **Sound notification** - Audio alert (opcional)

### Interacciones
- [ ] **Click en notificación** - Navegar a contenido relacionado
- [ ] **Cerrar notificación** - X button o auto-dismiss
- [ ] **Marcar notificación como leída** - Individual
- [ ] **Marcar todas como leídas** - Bulk action
- [ ] **Eliminar notificación** - Remove from list
- [ ] **Ver historial de notificaciones** - Notification center

### Preferencias
- [ ] **Configurar preferencias de notificaciones** - Por tipo/canal
- [ ] **Habilitar notificaciones del navegador** - Permission request
- [ ] **Denegar notificaciones del navegador** - Handle denied state
- [ ] **Silenciar notificaciones** - Do not disturb mode
- [ ] **Horario de notificaciones** - Solo en ciertos horarios

### Estados de Notificación
- [ ] **Notificación de éxito** - Green, checkmark, auto-dismiss 3s
- [ ] **Notificación de error** - Red, X icon, persistente
- [ ] **Notificación de advertencia** - Yellow/orange, warning icon
- [ ] **Notificación informativa** - Blue, info icon
- [ ] **Notificación con acción** - Button en la notificación

### Criterios de Validación
```javascript
function validateNotificationSystem(notifications) {
  return {
    hasPushSupport: 'Notification' in window && 'serviceWorker' in navigator,
    hasToastComponent: document.querySelector('.toast-container') !== null,
    hasNotificationCenter: document.querySelector('.notification-center') !== null,
    hasBadgeCounter: document.querySelector('.notification-badge') !== null,

    // Funcionalidad
    allowsMarkAsRead: notifications.canMarkAsRead,
    allowsMarkAllAsRead: notifications.canMarkAllAsRead,
    allowsDeletion: notifications.canDelete,
    hasNotificationHistory: notifications.hasHistory,

    // Preferencias
    hasPreferencesPage: document.querySelector('[href="/notifications/settings"]') !== null,
    respectsUserPreferences: notifications.respectsSettings,
    hasPushPermission: Notification.permission === 'granted',

    // UX
    autoDismissesSuccess: notifications.autoDismissSuccess,
    persistsErrors: notifications.persistsErrors,
    hasAccessibleAnnouncements: document.querySelector('[role="alert"]') !== null
  };
}
```

### Best Practices
- **No spam**: No bombardear con notificaciones
- **Relevantes**: Solo notificaciones importantes
- **Timing**: Respetar timezone del usuario
- **Frequency**: Límite de notificaciones por día
- **Clear CTA**: Acción clara en notificación
- **Accessibility**: Usar `role="alert"` para screen readers

---

## ✅ Eventos de Mensajería y Chat

### Gestión de Chat
- [ ] **Abrir ventana de chat** - Modal o sidebar
- [ ] **Cerrar ventana de chat** - X button
- [ ] **Minimizar chat** - Collapse a small widget
- [ ] **Ver lista de conversaciones** - Sidebar con previews
- [ ] **Buscar en conversaciones** - Search bar
- [ ] **Seleccionar conversación** - Ver historial

### Envío y Recepción
- [ ] **Escribir mensaje** - Input con typing indicator
- [ ] **Typing indicator** - "User is typing..."
- [ ] **Enviar mensaje** - Enter key o send button
- [ ] **Enviar con Shift+Enter** - Nueva línea (no enviar)
- [ ] **Recibir mensaje** - Real-time o polling
- [ ] **Mensaje entregado** - Single checkmark
- [ ] **Mensaje leído** - Double checkmark
- [ ] **Ver historial de chat** - Scroll infinito hacia arriba

### Acciones en Mensajes
- [ ] **Eliminar mensaje** - Solo para emisor
- [ ] **Editar mensaje** - Solo para emisor, time limit
- [ ] **Reaccionar a mensaje** - Emojis (thumbs up, heart, etc.)
- [ ] **Responder mensaje específico** - Quote/reply
- [ ] **Reenviar mensaje** - A otra conversación
- [ ] **Copiar mensaje** - Clipboard
- [ ] **Marcar como no leído** - Flag conversation

### Conversaciones
- [ ] **Crear nueva conversación** - Con usuario o grupo
- [ ] **Archivar conversación** - Mover a archived
- [ ] **Desarchivar conversación** - Volver a inbox
- [ ] **Silenciar conversación** - Mute notifications
- [ ] **Bloquear contacto** - No recibir mensajes
- [ ] **Desbloquear contacto** - Restore messaging
- [ ] **Eliminar conversación** - Con confirmación
- [ ] **Buscar en conversación** - Find text in messages

### Multimedia y Archivos
- [ ] **Enviar archivo/imagen** - File picker
- [ ] **Drag & drop archivo** - En área de chat
- [ ] **Preview de imagen** - Antes de enviar
- [ ] **Comprimir imágenes** - Reducir tamaño
- [ ] **Enviar múltiples archivos** - Batch upload
- [ ] **Ver imagen en lightbox** - Click para fullscreen
- [ ] **Descargar archivo** - Download button

### Audio y Video
- [ ] **Grabación de audio** - Hold to record
- [ ] **Reproducir audio** - Player inline
- [ ] **Videollamada** - WebRTC integration
- [ ] **Llamada de voz** - Audio only call
- [ ] **Compartir pantalla** - Screen sharing
- [ ] **Detectar dispositivos** - Mic, camera availability

### Grupos
- [ ] **Crear grupo** - Nombre, descripción, miembros
- [ ] **Agregar participantes** - Invite to group
- [ ] **Remover participantes** - If admin
- [ ] **Salir de grupo** - Leave group
- [ ] **Cambiar nombre de grupo** - If admin
- [ ] **Cambiar foto de grupo** - If admin
- [ ] **Ver info del grupo** - Members, settings
- [ ] **Permisos de grupo** - Admin, moderator, member

### Presence y Estado
- [ ] **Estado online/offline** - Green dot indicator
- [ ] **Última vez visto** - "Last seen 5 minutes ago"
- [ ] **Estado personalizado** - "Busy", "Away", custom message
- [ ] **Cambiar estado** - Dropdown selector

### Criterios de Validación Chat
```javascript
function validateChatSystem(chat) {
  return {
    // Básico
    hasChatInterface: chat.querySelector('.chat-container') !== null,
    hasMessageInput: chat.querySelector('.message-input') !== null,
    hasMessageList: chat.querySelector('.message-list') !== null,

    // Real-time
    hasRealTimeMessaging: chat.usesWebSocket || chat.usesPolling,
    hasTypingIndicator: chat.showsTypingStatus,
    hasReadReceipts: chat.showsReadStatus,

    // Funcionalidad
    allowsFileUpload: chat.querySelector('input[type="file"]') !== null,
    allowsImageUpload: chat.acceptsImageFiles,
    allowsEdit: chat.canEditMessages,
    allowsDelete: chat.canDeleteMessages,
    allowsReactions: chat.hasReactionFeature,

    // Búsqueda y organización
    hasSearch: chat.querySelector('.chat-search') !== null,
    hasArchive: chat.hasArchiveFeature,
    allowsMute: chat.canMuteConversations,

    // Grupos
    hasGroupChat: chat.supportsGroupChats,
    hasGroupManagement: chat.canManageGroups,

    // Multimedia
    hasVoiceCall: chat.supportsVoiceCalls,
    hasVideoCall: chat.supportsVideoCalls,
    hasScreenShare: chat.supportsScreenSharing,
    hasVoiceRecording: chat.canRecordVoice,

    // Presencia
    showsOnlineStatus: chat.displaysPresence,
    showsLastSeen: chat.displaysLastSeen
  };
}
```

### Aspectos de Seguridad
- **End-to-End Encryption**: Para mensajes privados (opcional pero recomendado)
- **Message Sanitization**: Limpiar HTML/scripts en mensajes
- **File Validation**: Validar tipo y tamaño de archivos
- **Rate Limiting**: Prevenir spam de mensajes
- **Blocked Users**: Respetar lista de bloqueados
- **Report System**: Permitir reportar mensajes inapropiados
- **Data Retention**: Política clara de retención de mensajes

### Optimización de Performance
- **Virtual Scrolling**: Para conversaciones largas
- **Lazy Load Images**: Cargar imágenes bajo demanda
- **WebSocket Connection**: Para real-time (mejor que polling)
- **Message Pagination**: No cargar todo el historial de una vez
- **Optimize Re-renders**: Solo re-renderizar mensajes nuevos

---

*Continúa en el siguiente archivo para Tablas, Calendarios, Analytics y Best Practices...*
