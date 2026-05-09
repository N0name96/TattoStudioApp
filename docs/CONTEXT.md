# CONTEXT.md - Contexto del Proyecto TattoStudioApp

## Última actualización
2026-05-08

## Estado actual
En fase de diseño y planificación. Se han definido los ficheros de documentación base (SPEC.md, ARQUITECTURE.md, AGENTS.md).

## Resumen del proyecto
TattoStudioApp es una plataforma multiplataforma (web + móvil) para la gestión de estudios de tatuaje, piercing, micropigmentación, láser y gemas dentales.

## Stack tecnológico decidido

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Base de datos**: Supabase (PostgreSQL managed)
- **Arquitectura**: Clean Architecture + CQRS + SOLID
- **Capas**: API → APPLICATION → DOMAIN ← INFRASTRUCTURE + CORE
- **Interfaces**: Protocol (typing) en vez de ABC
- **DTOs**: Pydantic v2 separados en application/dto/
- **Logging**: Estructurado en JSON
- **Tareas asíncronas**: Celery + Redis

### Frontend Web
- **Framework**: React 18+ con TypeScript
- **Build**: Vite
- **Estado**: Zustand
- **Data Fetching**: TanStack Query
- **Routing**: React Router v6
- **UI**: Tailwind CSS + shadcn/ui
- **HTTP Client**: Axios

### Frontend Móvil
- **Framework**: React Native con Expo SDK 51+
- **Navegación**: Expo Router
- **Estado**: Zustand (compartido con web)
- **UI**: NativeWind (Tailwind para RN)

### Infraestructura
- **Containerización**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Hosting Backend**: Railway / Render / VPS
- **Hosting Web**: Vercel / Netlify
- **Móvil**: EAS (Expo Application Services)

## Funcionalidades principales (de SPEC.md)

1. **Organización de Calendario**
   - Conexión bidireccional con Google Calendar
   - Calendario visual de citas
   - Gestión de cabinas libres/ocupadas
   - Eventos personalizados

2. **Consentimientos**
   - Firma digital vía QR
   - Modelos para: tatuaje, piercing, micropigmentación, láser, gemas dentales
   - Firma remota/no presencial
   - Cumplimiento RGPD, eIDAS, normativa sanitaria

3. **Control de Clientes**
   - Base de datos con historial completo
   - Control de origen del cliente
   - Gestión de derechos de imagen

4. **Comunicaciones por Correo Electrónico**
   - Recordatorios automáticos (48h, 24h, 2h antes)
   - Cuidados post-servicio
   - Felicitaciones cumpleaños
   - Solicitud de reseña Google Maps

5. **Control de Caja y Productos**
   - Venta de artículos y control de stock
   - Cálculo automático comisiones artistas
   - Control de gastos
   - Compatible con Veri*Factu

6. **Métricas y Analíticas**
   - Segmentación por rango de edad
   - Gráficos origen de clientes
   - Rendimiento individual artistas

## Sistema de Diseño

### Concepto
Minimalista con alma retro. Blanco y negro dominantes con toque de rojo oscuro (#8B0000).

### Colores principales

| Color | Hex | Uso |
|-------|-----|-----|
| Negro puro | `#000000` | Texto, iconos, borders |
| Blanco puro | `#FFFFFF` | Fondo principal |
| Gris oscuro | `#1A1A1A` | Fondo alternativo, cards |
| Gris medio | `#4A4A4A` | Texto secundario |
| Gris claro | `#E5E5E5` | Bordes sutiles |
| **Rojo oscuro** | `#8B0000` | **Accent**: CTAs, alertas, activo |

### Tipografía

| Fuente | Uso |
|--------|-----|
| **Playfair Display** | Títulos (serif, elegante, retro) |
| **Inter** | Texto cuerpo (sans-serif, limpia) |

### Estilo visual
- Bordes rectos (0px radius) preferidos → feel angular y retro
- Iconos outline (Lucide Icons)
- Animaciones rápidas y sutiles (150-200ms)
- Espacios amplios, la interfaz respira

### Documentación completa
→ Ver `docs/DESIGN_SYSTEM.md`

## Decisiones técnicas clave

| Decisión | Elección | Razón |
|----------|----------|-------|
| Arquitectura | Clean Architecture + CQRS | Separación clara, testeable, escalable |
| Interfaces | Protocol (typing) | Nativo Python, duck typing, sin herencia |
| Base de datos | Supabase | Managed, Auth integrado, Storage, Realtime |
| Estado global | Zustand | Simplicidad, TS nativo, pequeño bundle |
| UI Web | Tailwind + shadcn/ui | Personalización, consistencia |
| Pagos | Stripe | API robusta, soporte global |
| Email | SendGrid / SMTP | Sencillo, fiable |

## Pendientes de definir
- [ ] Diseño UI/UX y branding (colores, tipografía)
- [ ] Proveedor de firma digital eIDAS
- [ ] Configuración exacta de Supabase (tablas, RLS)
- [ ] Despliegue inicial (CI/CD pipeline)
- [ ] Tests E2E (Playwright web, Detox móvil)

## Agentes OpenCode configurados

El proyecto tiene 3 agentes especializados en `.opencode/agents/`:

| Agente | Uso | Modelo | Temp |
|--------|-----|--------|------|
| `@backend` | Desarrollo Python/FastAPI | Claude Sonnet | 0.2 |
| `@frontend` | Desarrollo React/React Native | Claude Sonnet | 0.2 |
| `@reviewer` | Revisión código, tests, rendimiento | Claude Sonnet | 0.1 |

Configuración en `opencode.json` en la raíz del proyecto.

## Ficheros del proyecto
```
TattoStudioApp/
├── opencode.json               # Configuración de OpenCode y agentes
├── .opencode/
│   └── agents/
│       ├── backend.md          # Agente especializado en backend
│       ├── frontend.md         # Agente especializado en frontend
│       └── reviewer.md         # Agente especializado en revisión
└── docs/
    ├── SPEC.md                 # Especificaciones del proyecto
    ├── ARQUITECTURE.md         # Arquitectura técnica completa
    ├── AGENTS.md               # Guía para agentes IA
    ├── CONTEXT.md              # Este fichero (contexto de sesión)
    └── noname.txt              # Requerimientos originales
```

## Próximos pasos
1. Definir esquema de base de datos en Supabase
2. Crear estructura de directorios del proyecto
3. Implementar backend (API + Domain + Infrastructure)
4. Implementar frontend web y móvil
5. Configurar CI/CD
6. Despliegue inicial
