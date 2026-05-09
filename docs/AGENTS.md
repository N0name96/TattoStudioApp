# AGENTS.md - Guía para Agentes IA

## Contexto del Proyecto

TattoStudioApp es una plataforma multiplataforma (web + móvil) para la gestión de estudios de tatuaje. Antes de realizar cualquier cambio, lee `SPEC.md` y `ARQUITECTURE.md` para entender el alcance y la arquitectura.

## Arquitectura del Backend

El backend sigue **Clean Architecture + CQRS + SOLID**. Las dependencias van siempre hacia adentro:

```
API Layer → APPLICATION Layer → DOMAIN Layer ← INFRASTRUCTURE Layer
```

### Capas

| Capa | Responsabilidad | Ubicación |
|------|----------------|-----------|
| **API** | Endpoints HTTP, handlers, middleware | `src/api/` |
| **APPLICATION** | Use Cases, Commands, Queries, DTOs | `src/application/` |
| **DOMAIN** | Entities, Value Objects, Protocols (interfaces), Enums | `src/domain/` |
| **INFRASTRUCTURE** | Implementaciones concretas (Supabase, servicios externos) | `src/infrastructure/` |
| **CORE** | Errores personalizados, respuestas, config, seguridad | `src/core/` |

### Flujo de una petición (ejemplo)

```
1. HTTP Request → API Handler (api/v1/endpoints/)
2. Handler → Use Case (application/use_cases/)
3. Use Case → Command/Query (application/commands/ o queries/)
4. Command/Query → Repository Protocol (domain/repositories/)
5. Repository implementa → Supabase Repository (infrastructure/persistence/)
6. Response DTO → API Handler → HTTP Response
```

## Estructura del Proyecto

```
TattoStudioApp/
├── apps/
│   ├── web/          # React + Vite + TypeScript (frontend web cliente)
│   ├── mobile/       # React Native + Expo + TypeScript (app móvil)
│   └── admin/        # React + Vite + TypeScript (panel administración)
├── packages/
│   ├── shared/       # Código compartido (tipos, utils, validadores)
│   └── api-client/   # Cliente API compartido
├── backend/
│   └── src/
│       ├── api/              # CAPA API
│       ├── application/      # CAPA APPLICATION (CQRS)
│       ├── domain/           # CAPA DOMAIN
│       ├── infrastructure/   # CAPA INFRASTRUCTURE
│       └── core/             # CAPA CORE
└── docker-compose.yml
```

## Convenciones de Código - Backend (Python/FastAPI)

### General
- **Estilo**: PEP 8, formateado con `ruff`
- **Tipado**: Usar type hints en TODAS las funciones
- **Imports**: Ordenar con `isort` (stdlib → third-party → local)
- **Naming**:
  - `snake_case` para variables, funciones, módulos
  - `PascalCase` para clases
  - `UPPER_SNAKE_CASE` para constantes
- **Async**: Usar `async/await` para todas las operaciones I/O

### Comentarios y Legibilidad

**REGLA OBLIGATORIA**: Cada función, clase, método y objeto debe tener un comentario explicativo.

**Formato de comentarios**:
- Usar docstrings con triple comilla doble `"""` para clases y funciones públicas
- Usar comentarios `#` para lógica interna compleja
- **SIEMPRE dejar DOS líneas en blanco** entre el comentario/docstring y el código siguiente
- Los comentarios deben explicar el QUÉ y el POR QUÉ, no el CÓMO (el código ya explica el cómo)

**Legibilidad**:
- Código simple y directo, fácil de leer para un programador que lo ve por primera vez
- Evitar ternarios anidados o expresiones complejas en una sola línea
- Preferir múltiples líneas claras a una línea compacta ilegible
- Nombres descriptivos y autoexplicativos (no abreviaturas crípticas)
- Funciones cortas (< 30 líneas idealmente), hacer extract method si crece demasiado

```python
# CORRECTO - Con comentarios y espaciado

class CreateAppointmentCommand:
    """Command to create a new appointment in the system.

    This command validates the request, checks artist availability,
    creates the domain entity and persists it to the repository.
    """

    def __init__(
        self,
        appointment_repo: AppointmentRepository,
        artist_repo: ArtistRepository,
    ) -> None:
        """Initialize the command with required repositories.

        Args:
            appointment_repo: Repository for appointment persistence.
            artist_repo: Repository for artist lookups.
        """

        self._appointment_repo = appointment_repo
        self._artist_repo = artist_repo


    async def execute(
        self,
        client_id: UUID,
        request: CreateAppointmentRequest,
    ) -> AppointmentResponse:
        """Execute the appointment creation flow.

        Steps:
            1. Verify the artist exists.
            2. Check the artist is available at the requested time.
            3. Create the domain entity.
            4. Persist and return the result.

        Raises:
            EntityNotFoundError: If the artist does not exist.
            BusinessRuleError: If the artist is not available.
        """

        # Step 1: Verify the artist exists
        artist = await self._artist_repo.get_by_id(request.artist_id)

        if artist is None:
            raise EntityNotFoundError(f"Artist {request.artist_id} not found")

        # Step 2: Check availability for the requested slot
        existing = await self._appointment_repo.find_by_artist_and_date(
            artist_id=request.artist_id,
            date=request.date,
            start_time=request.start_time,
        )

        if existing is not None:
            raise BusinessRuleError("Artist is not available at this time")

        # Step 3: Create the domain entity with business rules applied
        appointment = Appointment.create(
            client_id=client_id,
            artist_id=request.artist_id,
            service_type=request.service_type,
            date=request.date,
            start_time=request.start_time,
            notes=request.notes,
        )

        # Step 4: Persist the appointment
        saved = await self._appointment_repo.save(appointment)

        # Map domain entity to response DTO
        return AppointmentResponse.model_validate(saved)


# INCORRECTO - Sin comentarios, sin espaciado, compacto

class CreateAppointmentCommand:
    def __init__(self, appointment_repo, artist_repo):
        self._appointment_repo = appointment_repo
        self._artist_repo = artist_repo
    async def execute(self, client_id, request):
        artist = await self._artist_repo.get_by_id(request.artist_id)
        if artist is None: raise EntityNotFoundError(f"Artist {request.artist_id} not found")
        existing = await self._appointment_repo.find_by_artist_and_date(artist_id=request.artist_id, date=request.date, start_time=request.start_time)
        if existing is not None: raise BusinessRuleError("Artist is not available at this time")
        appointment = Appointment.create(client_id=client_id, artist_id=request.artist_id, service_type=request.service_type, date=request.date, start_time=request.start_time, notes=request.notes)
        saved = await self._appointment_repo.save(appointment)
        return AppointmentResponse.model_validate(saved)
```

### Domain Layer
- Usar `@dataclass` para entidades
- Usar `Protocol` (typing) en vez de `ABC` para interfaces/repositorios
- Value Objects inmutables con `frozen=True`
- Enums con `str, Enum` para serialización directa

```python
# Correcto - Protocol (NO ABC)
from typing import Protocol, runtime_checkable

@runtime_checkable
class ArtistRepository(Protocol):
    async def get_by_id(self, artist_id: UUID) -> Artist | None: ...
    async def save(self, artist: Artist) -> Artist: ...
```

### Application Layer (CQRS)
- **Commands**: Escritura → `CreateXCommand`, `UpdateXCommand`, `DeleteXCommand`
- **Queries**: Lectura → `GetXQuery`, `ListXQuery`
- **DTOs**: Separados en `dto/requests/` y `dto/responses/` (schemas Pydantic)
- Los DTOs van separados de los handlers (API layer)

```python
# Correcto - Command con DTO separado
class CreateAppointmentCommand:
    def __init__(self, repo: AppointmentRepository, artist_repo: ArtistRepository):
        self._repo = repo
        self._artist_repo = artist_repo

    async def execute(self, client_id: UUID, request: CreateAppointmentRequest) -> AppointmentResponse:
        # Lógica de negocio aquí
        ...
```

### API Layer (Handlers)
- Handlers solo orquestan: reciben request, llaman al use case, retornan response
- Usar `SuccessResponse[T]` y `ErrorResponse` del CORE
- Manejar errores del DOMAIN con try/except → HTTP status codes apropiados

```python
# Correcto - Handler con respuesta tipada
@router.get("/{id}", response_model=SuccessResponse[ArtistResponse])
async def get_artist(id: UUID, query: GetArtistQuery = Depends()):
    try:
        artist = await query.execute(id)
        return SuccessResponse(data=artist)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
```

### Infrastructure Layer
- Implementar los Protocolos del Domain
- Usar cliente Supabase para persistencia
- Mappers para convertir entre datos de Supabase y entidades de Domain
- Servicios externos (Email, Stripe, Google Calendar) aquí

### Core Layer
- Errores jerárquicos: `BaseError` → `DomainError`, `ApplicationError`, `InfrastructureError`
- Respuestas estandarizadas: `SuccessResponse[T]`, `ErrorResponse`, `PaginatedResponse[T]`
- Configuración con `pydantic-settings`

## Testing - Backend

### Estructura de Tests

```
tests/
├── unit/
│   ├── domain/           # Test entidades, value objects, servicios de dominio
│   ├── application/      # Test commands, queries, use cases (mock repos)
│   └── core/             # Test errores, respuestas
├── integration/
│   ├── api/              # Test handlers con TestClient
│   └── infrastructure/   # Test repositorios contra Supabase (test project)
└── conftest.py           # Fixtures compartidos
```

### Comandos

```bash
cd backend
pytest                          # Todos los tests
pytest tests/unit/              # Solo unitarios
pytest tests/integration/       # Solo integración
pytest -k "test_create"         # Por nombre
pytest --cov=src                # Con cobertura
```

### Reglas de Testing
- **Unit tests**: Mockear dependencias externas (repositorios, servicios)
- **Domain tests**: Sin mocks, testear lógica pura
- **Application tests**: Mockear repositories (Protocolos), testear lógica de use cases
- **Integration tests**: Testear contra Supabase real (proyecto de test)

## Convenciones de Código - Frontend (React / React Native)

### General
- **Estilo**: Prettier con configuración del proyecto
- **Linting**: ESLint con las reglas del proyecto
- **Naming**:
  - `camelCase` para variables, funciones, hooks
  - `PascalCase` para componentes, interfaces, tipos
  - `UPPER_SNAKE_CASE` para constantes
- **Componentes**: Functional components con hooks
- **Props**: Definir con `interface` (no `type` para props)
- **Exports**: Un componente principal por archivo

### Estructura Feature-Based
Cada feature agrupa sus componentes, hooks, servicios y tipos:
```
features/artists/
├── components/    # Componentes específicos de artistas
├── hooks/         # Hooks de artistas (useArtists, useArtist)
├── services/      # Llamadas a API de artistas
└── types/         # Tipos de artistas
```

### Custom Hooks (Data Fetching)
```typescript
// Correcto
export function useArtists(filters?: ArtistFilters) {
  return useQuery({
    queryKey: ['artists', filters],
    queryFn: () => artistService.list(filters),
  });
}
```

### Services (API Layer)
```typescript
// Correcto - Servicio centralizado
export const artistService = {
  list: (filters?: ArtistFilters) =>
    api.get<Artist[]>('/artists', { params: filters }),
  getById: (id: string) =>
    api.get<Artist>(`/artists/${id}`),
};
```

### Zustand Store (Estado Global)
```typescript
// Correcto - Store tipado con persist
export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: (user, token) => set({ user, token, isAuthenticated: true }),
      logout: () => set({ user: null, token: null, isAuthenticated: false }),
    }),
    { name: 'auth-storage' }
  )
);
```

### Componentes
```tsx
// Correcto - Componente presentacional con interface
interface ArtistCardProps {
  artist: Artist;
  onSelect: (id: string) => void;
}

export function ArtistCard({ artist, onSelect }: ArtistCardProps) {
  return (
    <Card onClick={() => onSelect(artist.id)}>
      <h3>{artist.name}</h3>
    </Card>
  );
}
```

### API Client
```typescript
// lib/api.ts - Configuración centralizada de Axios
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// Interceptor para token
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
```

## Testing - Frontend

### Comandos
```bash
# Web
cd apps/web
npm run test                    # Vitest
npm run test:e2e               # Playwright

# Mobile
cd apps/mobile
npm run test                    # Jest
npm run test:e2e               # Detox
```

### Estructura de Tests
```
features/artists/
├── components/
│   └── ArtistCard.test.tsx
├── hooks/
│   └── useArtists.test.ts
└── services/
    └── artist.service.test.ts
```

### Reglas de Testing Frontend
- Testear hooks con `renderHook` de testing-library
- Testear componentes con `render` + screen queries
- Mockear servicios API en tests de hooks y componentes
- Testear stores de Zustand directamente

## Comandos de Verificación

Antes de considerar un cambio completo, ejecutar:

```bash
# Backend
cd backend
ruff check src/                 # Linting
ruff format src/                # Formateo
mypy src/                       # Type checking
pytest                          # Tests
```

## Cosas que NUNCA Hacer

### Backend
- ❌ Commitear `.env` o credenciales
- ❌ Usar `print()` en Python (usar `logging` o `logger`)
- ❌ Usar `ABC` para interfaces (usar `Protocol`)
- ❌ Poner lógica de negocio en handlers (usar use cases/commands)
- ❌ Poner lógica de negocio en repositorios
- ❌ Importar de Infrastructure en Domain (dependencia inversa)
- ❌ Hardcodear URLs, keys o configuraciones (usar env vars)
- ❌ Crear clases monolíticas (>200 líneas → dividir)
- ❌ Saltarse las capas (handler → repository directamente)

### Frontend
- ❌ Usar `any` en TypeScript (usar tipos específicos o `unknown`)
- ❌ Hacer fetch directo en componentes (usar services + hooks)
- ❌ Usar `@ts-ignore` o `@ts-nocheck`
- ❌ Hardcodear URLs o configuraciones (usar env vars)
- ❌ Crear componentes gigantes (>300 líneas → dividir)
- ❌ Importar de rutas relativas largas (usar aliases `@/`)
- ❌ Poner lógica de negocio en componentes (usar hooks/stores)
- ❌ Ignorar estados de loading y error en UI

## Cosas que SIEMPRE Hacer

### Antes de empezar CUALQUIER tarea
- ✅ **SIEMPRE** leer `SPEC.md` y `ARQUITECTURE.md` antes de implementar o modificar cualquier funcionalidad
- ✅ Revisar qué funcionalidades ya están desarrolladas y cuáles pendientes (consultar `SPEC.md`)
- ✅ Revisar la arquitectura actual y decisiones técnicas (consultar `ARQUITECTURE.md`)
- ✅ Identificar qué hay que cambiar o agregar según los documentos de especificación y arquitectura
- ✅ Si una funcionalidad no está en `SPEC.md`, **consultar antes de implementar**

### Backend
- ✅ Respetar la dirección de dependencias: API → APPLICATION → DOMAIN ← INFRASTRUCTURE
- ✅ Usar Protocolos (interfaces) para desacoplar capas
- ✅ Separar Commands (escritura) de Queries (lectura) - CQRS
- ✅ DTOs Pydantic separados de los handlers
- ✅ Usar `SuccessResponse[T]` y `ErrorResponse` del CORE
- ✅ Manejar errores de Domain en los handlers → HTTP status apropiados
- ✅ Testear lógica de dominio sin mocks
- ✅ Mockear repositorios en tests de application
- ✅ Type hints en todas las funciones
- ✅ **COMENTAR** cada función, clase y método con docstring
- ✅ **DOS líneas en blanco** entre docstring y código, y entre métodos
- ✅ Código **simple y legible** (no una-liner compactos ilegibles)
- ✅ Nombres descriptivos y autoexplicativos

### Frontend
- ✅ Usar feature-based structure (componentes, hooks, services, types por feature)
- ✅ Usar TanStack Query para data fetching (useQuery, useMutation)
- ✅ Usar Zustand para estado global (con persist si es necesario)
- ✅ Centralizar llamadas API en services
- ✅ Manejar estados de loading y error en todos los componentes
- ✅ Usar interfaces para props de componentes
- ✅ Testear hooks y componentes
- ✅ Usar aliases `@/` para imports

## Dependencias Principales

### Backend
| Paquete | Uso |
|---------|-----|
| fastapi | Framework web |
| supabase | Cliente Supabase |
| pydantic | Validación / DTOs |
| pydantic-settings | Configuración |
| python-jose | JWT |
| passlib | Hashing contraseñas |
| stripe | Pagos |
| celery | Tareas async |
| redis | Cache + cola |

### Frontend
| Paquete | Uso |
|---------|-----|
| react / react-native | UI framework |
| zustand | Estado global |
| axios / tanstack-query | HTTP client |
| react-router / expo-router | Navegación |
| tailwind / nativewind | Estilos |
| zod | Validación schemas |

## Workflow de Desarrollo

1. Leer `SPEC.md` para entender el requisito
2. Revisar `ARQUITECTURE.md` para saber dónde va el código según la capa
3. Crear rama feature/descripción
4. Implementar siguiendo Clean Architecture:
   - Definir/actualizar Entity en Domain si es necesario
   - Definir/actualizar Protocol en Domain
   - Crear DTO en Application (request/response)
   - Crear Command o Query en Application
   - Implementar Repository en Infrastructure (si es nuevo)
   - Crear Handler en API
5. Escribir tests unitarios para la lógica nueva
6. Ejecutar lint + typecheck + tests
7. Commit con mensaje descriptivo

## Notas para Agentes

- El proyecto usa Supabase como base de datos managed (no PostgreSQL directo)
- Los Protocolos de Python (`typing.Protocol`) son la forma de definir interfaces
- CQRS separa Commands (escritura) de Queries (lectura)
- Los schemas Pydantic van en `application/dto/`, NO en los handlers
- La capa CORE tiene errores y respuestas reutilizables
- **Después de completar una tarea, SIEMPRE preguntar al usuario cuáles son los próximos pasos** (ej: ¿necesitas algo más?, ¿seguimos con X funcionalidad?, ¿revisamos algo?)

## Agentes Disponibles (OpenCode)

El proyecto tiene configurados agentes especializados en `.opencode/agents/`. Usa `@` para invocarlos.

### @backend - Desarrollo Backend
- **Uso**: Desarrollo de código Python/FastAPI
- **Especialidad**: Clean Architecture, CQRS, SOLID, Supabase
- **Modelo**: Claude Sonnet (temperature 0.2)
- **Permisos**: Lectura, escritura, bash

**Cuándo usar**:
- Crear o modificar endpoints de la API
- Implementar commands, queries o use cases
- Crear o modificar entidades de dominio
- Implementar repositorios de Supabase
- Configurar logging o error handling

**Ejemplo**:
```
@backend crea el endpoint para crear citas con su command, 
query, DTOs y repositorio de Supabase
```

### @frontend - Desarrollo Frontend
- **Uso**: Desarrollo de código React/React Native
- **Especialidad**: TypeScript, Zustand, TanStack Query, Tailwind
- **Modelo**: Claude Sonnet (temperature 0.2)
- **Permisos**: Lectura, escritura, bash

**Cuándo usar**:
- Crear o modificar componentes de React/React Native
- Implementar hooks de data fetching
- Crear stores de Zustand
- Implementar servicios de API
- Diseñar interfaces de usuario

**Ejemplo**:
```
@frontend crea el componente de calendario para mostrar 
las citas con TanStack Query y loading states
```

### @reviewer - Revisión de Código
- **Uso**: Revisión de calidad, tests, rendimiento y seguridad
- **Especialidad**: Code review, testing, performance, security
- **Modelo**: Claude Sonnet (temperature 0.1)
- **Permisos**: Solo lectura y bash de verificación (pytest, lint, etc.)

**Cuándo usar**:
- Revisar código antes de hacer commit
- Verificar cobertura de tests
- Analizar rendimiento de queries o componentes
- Auditar seguridad del código
- Sugerir mejoras de arquitectura

**Ejemplo**:
```
@reviewer revisa el código de la feature de consentimientos 
y verifica que sigue Clean Architecture y tiene tests
```

### Invocación automática
Los agentes pueden ser invocados automáticamente por el agente principal cuando detecta que la tarea es específica:
- Tareas de backend → invoca `@backend`
- Tareas de frontend → invoca `@frontend`
- Tareas de revisión → invoca `@reviewer`

- Si una funcionalidad no está en SPEC.md, consultar antes de implementar
