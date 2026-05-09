# TattoStudioApp - Especificación del Proyecto

## 1. Visión General

TattoStudioApp es una plataforma multiplataforma (web + móvil) diseñada para estudios de tatuaje que centraliza la organización de agendas, gestión de consentimientos legales, control de clientes, comunicaciones automatizadas, control de caja y métricas del negocio. La aplicación conecta a tatuadores con sus clientes de forma profesional, optimizando la operativa diaria del estudio y garantizando el cumplimiento legal.

## 2. Objetivos

- Digitalizar la gestión completa de un estudio de tatuaje, piercing, micropigmentación, láser y gemas dentales
- Centralizar la agenda del estudio con sincronización con Google Calendar
- Garantizar el cumplimiento legal mediante consentimientos informados con firma digital (eIDAS)
- Mantener un control exhaustivo de clientes con historial y origen
- Automatizar comunicaciones con clientes vía correo electrónico
- Gestionar la caja, stock de productos y comisiones de artistas
- Proporcionar métricas y analíticas para la toma de decisiones del estudio

## 3. Usuarios del Sistema

### 3.1 Cliente
- Persona que solicita un servicio (tatuaje, piercing, micropigmentación, láser, gemas dentales)
- Firma consentimientos informados de forma digital
- Recibe comunicaciones por correo electrónico
- Sus datos, origen y derechos de imagen son controlados

### 3.2 Artista/Tatuador
- Profesional que ofrece servicios en el estudio
- Gestiona su agenda y visualiza su calendario
- Recibe comisiones calculadas automáticamente sobre sus servicios
- Su rendimiento individual es medido y visible en métricas

### 3.3 Administrador del Estudio
- Gestiona la configuración general del estudio
- Controla la caja, stock, gastos y facturación
- Supervisa métricas y reportes del negocio
- Gestiona cabinas y recursos del estudio
- Configura modelos de consentimiento y políticas

## 4. Funcionalidades Principales

### 4.1 Organización de Calendario

**Descripción**: Sistema de calendario completo sincronizado con Google Calendar para la gestión de agendas del estudio.

**Conexión con Google Calendar**:
- Sincronización bidireccional con Google Calendar de cada artista
- Las citas creadas en TattoStudioApp aparecen en Google Calendar y viceversa
- Conflictos de horario detectados automáticamente

**Calendario Visual de Citas**:
- Vista diaria, semanal y mensual del calendario
- Drag & drop para reprogramar citas
- Código de colores por tipo de servicio y estado de cita
- Vista global del estudio y vista individual por artista

**Gestión de Cabinas**:
- Registro de cabinas del estudio (cabina 1, cabina 2, etc.)
- Asignación de cabina a cada cita
- Vista de cabinas libres/ocupadas en tiempo real
- Bloqueo de cabina por mantenimiento o limpieza

**Calendario de Eventos Personalizados**:
- Creación de eventos especiales (ferias, convenciones, promociones)
- Bloqueo de agenda por eventos del estudio
- Eventos recurrentes (formación, reuniones de equipo)
- Notificación a artistas y clientes afectados

**Flujo principal**:
1. Cliente solicita cita seleccionando servicio, artista y fecha
2. Sistema verifica disponibilidad de artista y cabina
3. Cita creada y sincronizada con Google Calendar
4. Confirmación enviada al cliente por email
5. Recordatorios automáticos programados

### 4.2 Consentimientos

**Descripción**: Sistema de consentimiento informado con firma digital que cumple con la normativa Sanitaria, GDPR y Firma Digital eIDAS.

**Firma Digital a través de QR**:
- Generación de código QR único por consentimiento
- El cliente escanea QR desde su móvil para acceder al documento
- Firma mediante pantalla táctil o dedo en el móvil
- Sello de tiempo y verificación de identidad

**Modelos de Consentimiento**:
- Consentimiento para tatuaje
- Consentimiento para piercing
- Consentimiento para micropigmentación
- Consentimiento para láser
- Consentimiento para gemas dentales
- Modelos personalizables por el estudio
- Versionado de modelos (control de cambios)

**Almacenamiento de Firmas en la Nube**:
- Documentos firmados almacenados de forma segura y encriptada
- Acceso histórico a todos los consentimientos firmados por cliente
- Exportación en PDF con validez legal
- Backup automático y redundancia

**Firma No Presencial**:
- Envío del consentimiento por enlace seguro al cliente
- Firma remota antes de la cita
- Verificación de identidad mediante código OTP
- Válido para clientes que no pueden acudir presencialmente

**Cumplimiento Legal**:
- RGPD: consentimiento explícito para tratamiento de datos
- Firma Digital eIDAS: cumplimiento del reglamento europeo
- Normativa Sanitaria: documentos adaptados por comunidad autónoma
- Auditoría completa de accesos y firmas

### 4.3 Control de Clientes

**Descripción**: Sistema integral de gestión de clientes con historial completo, control de origen y derechos de imagen.

**Base de Datos de Clientes**:
- Ficha completa del cliente (datos personales, contacto, alergias, condiciones médicas)
- Historial de todos los servicios recibidos
- Historial de consentimientos firmados
- Preferencias y notas del artista
- Buscador y filtrado avanzado

**Control de Origen del Cliente**:
- Registro de cómo conoció el cliente el estudio:
  - Instagram
  - TikTok
  - Recomendación de amigo
  - Google Maps / reseñas
  - Paseo / escaparate
  - Feria / evento
  - Otro
- Estadísticas de canales de adquisición
- ROI por canal de marketing

**Gestión de Derechos de Imagen**:
- Consentimiento específico para uso de imágenes del trabajo
- Opciones: uso en redes sociales, portafolio web, publicidad
- El cliente puede revocar el consentimiento en cualquier momento
- Control granular: qué fotos sí, qué fotos no

**Fichas de Cliente con Historial**:
- Timeline visual de todos los servicios
- Fotos de antes/después de cada servicio
- Notas del artista sobre preferencias y cuidados
- Alertas de alergias o condiciones especiales
- Próximas citas programadas

### 4.4 Comunicaciones por Correo Electrónico

**Descripción**: Sistema automatizado de comunicaciones con clientes a través de correo electrónico.

**Recordatorio de Citas**:
- Recordatorio automático 48h antes de la cita por correo electrónico
- Recordatorio 24h antes por correo electrónico
- Recordatorio 2h antes por correo electrónico
- Confirmación de asistencia con enlace de respuesta (Sí/No)
- Si el cliente cancela, liberar cabina y slot automáticamente

**Cuidados Post-Servicio**:
- Envío automático de instrucciones de cuidado según tipo de servicio
- Tatuaje: cuidados de la primera semana, hidratación, protección solar
- Piercing: limpieza, signos de infección, tiempos de curación
- Seguimiento a los 7 días preguntando cómo va la curación
- Solicitud de reseña en Google Maps tras el seguimiento positivo

**Felicitaciones por Cumpleaños**:
- Envío automático de felicitación por correo electrónico el día del cumpleaños
- Opción de incluir cupón de descuento o promoción especial
- Personalización del mensaje según historial del cliente

**Otros**:
- Avisos de promociones del estudio (segmentados por tipo de cliente)
- Notificación de cambios de cita (reprogramación, cancelación)

### 4.5 Control de Caja y Productos de Estudio

**Descripción**: Sistema de gestión financiera del estudio que incluye ventas, stock, comisiones y gastos. Compatible con Veri*Factu.

**Venta de Artículos y Control de Stock**:
- Catálogo de productos del estudio (cremas, tinta, agujas, joyería piercing, merchandising)
- Punto de venta (TPV) integrado
- Control de stock en tiempo real
- Alertas de stock mínimo
- Historial de compras y proveedores
- Código de barras / QR para productos

**Cálculo de Comisiones a Artistas**:
- Configuración de comisión por artista (porcentaje o fija)
- Cálculo automático de comisión por servicio realizado
- Comisión diferenciada por tipo de servicio (tatuaje, piercing, etc.)
- Informe mensual de comisiones por artista
- Exportación de comisiones para nóminas

**Control de Gastos del Estudio**:
- Registro de gastos operativos (alquiler, luz, agua, materiales)
- Categorización de gastos
- Adjuntar facturas y tickets (foto o PDF)
- Presupuesto mensual vs. real
- Alertas de exceso de presupuesto

**Compatible con Veri*Factu**:
- Facturación adaptada al sistema Veri*Factu de la AEAT
- Generación de facturas con código hash y QR verificable
- Envío automático de registros de facturación a la Agencia Tributaria
- Libro registro de facturas emitidas y recibidas
- Cumplimiento de los requisitos de conservación de datos

### 4.6 Métricas y Analíticas

**Descripción**: Dashboard de métricas diseñado para entender el rendimiento del estudio y tomar decisiones basadas en datos.

**Segmento de Clientes por Rango de Edad**:
- Distribución de clientes por grupos de edad (18-25, 26-35, 36-45, 46-55, 55+)
- Evolución temporal de cada segmento
- Servicios más populares por rango de edad
- Gasto medio por segmento

**Gráficos de Origen de Clientes**:
- Distribución porcentual de canales de adquisición
- Evolución temporal de cada canal
- Comparativa de coste de adquisición por canal
- Tasa de conversión por canal (visita → cita → servicio completado)

**Rendimiento Individual de Cada Artista**:
- Servicios realizados por período
- Ingresos generados
- Valoración media de clientes
- Tasa de cancelación y no-show
- Tasa de ocupación de agenda
- Comparativa entre artistas

**Otras Métricas**:
- Ingresos totales por período (día, semana, mes, año)
- Servicios más demandados
- Horas pico de demanda
- Tasa de retención de clientes
- Ticket medio por cliente
- Previsión de ingresos

## 5. Historias de Usuario

### Cliente
- Como cliente, quiero recibir un consentimiento informado por QR para firmarlo desde mi móvil antes del servicio
- Como cliente, quiero recibir recordatorios por correo electrónico para no olvidar mi cita
- Como cliente, quiero que me envíen los cuidados post-servicio automáticamente por correo electrónico
- Como cliente, quiero recibir una felicitación de cumpleaños con un posible descuento
- Como cliente, quiero poder firmar el consentimiento de forma remota si no puedo acudir al estudio

### Artista
- Como artista, quiero ver mi calendario sincronizado con Google Calendar
- Como artista, quiero ver qué cabina tengo asignada para cada cita
- Como artista, quiero consultar mi comisión acumulada del mes
- Como artista, quiero ver las métricas de mi rendimiento (citas, valoraciones, ingresos)

### Administrador
- Como admin, quiero gestionar la caja del estudio (ingresos, gastos, cierre de caja)
- Como admin, quiero controlar el stock de productos y recibir alertas de reposición
- Como admin, quiero calcular automáticamente las comisiones de cada artista
- Como admin, quiero ver gráficos de cómo nos conocen los clientes para invertir en marketing
- Como admin, quiero generar facturas compatibles con Veri*Factu
- Como admin, quiero gestionar los consentimientos y modelos de documentos
- Como admin, quiero controlar qué cabinas están libres u ocupadas en tiempo real

## 6. Requisitos No Funcionales

### Rendimiento
- Tiempo de carga de página < 2 segundos
- Soporte para 100+ usuarios concurrentes
- Imágenes optimizadas con CDN
- Sincronización con Google Calendar en < 5 segundos

### Seguridad
- Autenticación JWT con refresh tokens
- Datos sensibles encriptados (pagos, datos personales, consentimientos)
- Cumplimiento RGPD para datos de clientes
- Roles y permisos granulares
- Consentimientos con firma digital eIDAS
- Auditoría de accesos a datos sensibles

### Disponibilidad
- Uptime objetivo: 99.5%
- Backups diarios automáticos
- Modo offline básico para consulta de agenda (móvil)

### Escalabilidad
- Arquitectura modular para añadir funcionalidades
- Base de datos preparada para crecimiento horizontal
- API versionada para compatibilidad futura

### Cumplimiento Legal
- RGPD (Reglamento General de Protección de Datos)
- eIDAS (Reglamento de Identificación Electrónica y Servicios de Confianza)
- Normativa Sanitaria autonómica
- Veri*Factu (AEAT)

## 7. Plataformas Soportadas

| Plataforma | Tecnología | Mínimo |
|------------|-----------|--------|
| Web | React 18+ | Chrome, Firefox, Safari, Edge (2 últimas versiones) |
| iOS | React Native (Expo) | iOS 15+ |
| Android | React Native (Expo) | Android 10+ (API 29) |

## 8. Restricciones y Suposiciones

### Restricciones
- El sistema de pagos dependerá de un proveedor externo (Stripe o similar)
- Las imágenes y consentimientos se almacenarán en la nube (S3 o similar)
- La app móvil usará Expo para simplificar el desarrollo y despliegue
- La integración con Google Calendar requiere cuenta de Google Workspace o similar
- La firma digital eIDAS requiere un proveedor de servicios de confianza cualificado
- El envío de comunicaciones se realizará exclusivamente por correo electrónico
- Veri*Factu requiere certificado digital y registro en la AEAT

### Suposiciones
- Los estudios de tatuaje tendrán entre 1 y 20 artistas
- Los clientes accederán principalmente desde móvil
- Los artistas necesitarán acceso rápido a su agenda desde el móvil
- El idioma principal será español, con posibilidad de internacionalización futura
- Los clientes disponen de dirección de correo electrónico
- Los consentimientos se firmarán principalmente de forma presencial (QR en estudio)
- El estudio dispone de conexión a internet estable
