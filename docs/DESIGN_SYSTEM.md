# TattoStudioApp - Design System

## 1. Identidad Visual

### Concepto
Estética minimalista en blanco y negro con alma retro. Evoca el mundo del tatuaje: tinta, piel, pasión. La interfaz respira, es limpia, pero tiene personalidad.

### Keywords
- Minimalista
- Blanco y negro
- Alma retro
- Sangre y tinta
- Simple y fluido

---

## 2. Paleta de Colores

### Primarios (Dominantes)

| Color | Hex | Uso |
|-------|-----|-----|
| **Negro puro** | `#000000` | Texto principal, iconos, borders |
| **Blanco puro** | `#FFFFFF` | Fondo principal, espacios |
| **Gris oscuro** | `#1A1A1A` | Fondo alternativo, cards |
| **Gris medio** | `#4A4A4A` | Texto secundario |
| **Gris claro** | `#E5E5E5` | Bordes sutiles, separadores |

### Accent (Resaltado)

| Color | Hex | Uso |
|-------|-----|-----|
| **Rojo oscuro** | `#8B0000` | CTAs primarios, alertas importantes, estado activo |
| **Rojo claro** | `#B22222` | Hover states, énfasis |
| **Rojo muy claro** | `#F5E6E6` | Background de alertas, badges |

### Semánticos

| Color | Hex | Uso |
|-------|-----|-----|
| **Éxito** | `#2D5016` | Confirmaciones, estado completado |
| **Advertencia** | `#8B6914` | Alertas, estado pendiente |
| **Error** | `#8B0000` | Errores (mismo que accent) |
| **Info** | `#1A1A1A` | Informativo |

---

## 3. Tipografía

### Fuentes

| Fuente | Uso | Google Fonts |
|--------|-----|--------------|
| **Playfair Display** | Títulos, headings | `Playfair Display` |
| **Inter** | Texto cuerpo, UI | `Inter` |

### Jerarquía

```
H1: Playfair Display, 32px, Bold, #000000
H2: Playfair Display, 24px, Bold, #000000
H3: Playfair Display, 20px, Semibold, #000000
H4: Playfair Display, 16px, Semibold, #000000

Body: Inter, 16px, Regular, #000000
Body Small: Inter, 14px, Regular, #4A4A4A
Caption: Inter, 12px, Regular, #4A4A4A

Button: Inter, 14px, Semibold, uppercase, letter-spacing: 0.05em
Label: Inter, 12px, Medium, uppercase, letter-spacing: 0.08em
```

---

## 4. Espaciado

### Escala base (4px)

| Token | Valor | Uso |
|-------|-------|-----|
| `xs` | 4px | Espacio mínimo |
| `sm` | 8px | Padding interno de inputs, badges |
| `md` | 16px | Gap entre elementos, padding de cards |
| `lg` | 24px | Separación entre secciones |
| `xl` | 32px | Margen de secciones |
| `2xl` | 48px | Separación mayor |
| `3xl` | 64px | Hero sections |

---

## 5. Bordes y Radios

```
Radius none: 0px  (elementos angulares, estilo retro)
Radius sm:   4px  (inputs, badges)
Radius md:   8px  (cards, botones)
Radius lg:   12px (modales, dropdowns)
Radius full: 9999px (avatars, pills)
```

**Nota**: Preferir bordes rectos (0px) para mantener el feel angular y retro. Usar radios solo cuando mejore la usabilidad.

---

## 6. Sombras

```css
/* Sombra sutil para cards */
shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05)

/* Sombra media para dropdowns */
shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07)

/* Sombra grande para modales */
shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1)
```

---

## 7. Componentes

### Botones

```
Primary:    bg=#8B0000, text=#FFFFFF, radius=4px, uppercase
Secondary:  bg=transparent, border=1px #000000, text=#000000, radius=4px
Ghost:      bg=transparent, text=#000000, underline on hover
Danger:     bg=#8B0000, text=#FFFFFF (igual que primary)
```

### Inputs

```
Default:    border=1px #E5E5E5, bg=#FFFFFF, text=#000000, radius=4px
Focus:      border=1px #000000, outline=2px #8B0000 (sutil)
Error:      border=1px #8B0000
Disabled:   bg=#F5F5F5, text=#999999
```

### Cards

```
Default:    bg=#FFFFFF, border=1px #E5E5E5, radius=0px (angular)
Hover:      border=1px #000000
Active:     border-left=3px #8B0000
```

### Badges

```
Default:    bg=#F5F5F5, text=#4A4A4A, radius=4px
Success:    bg=#E8F5E9, text=#2D5016
Error:      bg=#F5E6E6, text=#8B0000
Warning:    bg=#FFF8E1, text=#8B6914
```

---

## 8. Iconografía

- **Estilo**: Outline / Line icons (no filled)
- **Grosor**: 1.5px stroke
- **Color**: Negro (#000000) por defecto
- **Tamaños**: 16px, 20px, 24px, 32px

Librería recomendada: **Lucide Icons** (consistente, outline, gratuito)

---

## 9. Animaciones

### Principios
- **Rápidas**: 150-200ms para micro-interacciones
- **Fluidas**: ease-out para entradas, ease-in para salidas
- **Sutiles**: No llamar la atención, solo guiar

### Duraciones

```
Fast:    150ms  (hover states, toggles)
Normal:  200ms  (modals, dropdowns)
Slow:    300ms  (page transitions)
```

### Ejemplos

```css
/* Hover de botón */
transition: background-color 150ms ease-out

/* Aparición de modal */
animation: fadeIn 200ms ease-out

/* Slide de sidebar */
animation: slideIn 300ms ease-out
```

---

## 10. Layout

### Grid
- **Container max-width**: 1200px
- **Columnas**: 12 (web), 4 (mobile)
- **Gutter**: 24px (web), 16px (mobile)

### Breakpoints

```
sm:  640px   (mobile landscape)
md:  768px   (tablet)
lg:  1024px  (desktop)
xl:  1280px  (large desktop)
```

---

## 11. Ejemplos de Páginas

### Login
```
┌─────────────────────────────────────────┐
│                                         │
│          [LOGO en negro]                │
│                                         │
│     ┌─────────────────────────┐         │
│     │  Email                  │         │
│     └─────────────────────────┘         │
│     ┌─────────────────────────┐         │
│     │  Password               │         │
│     └─────────────────────────┘         │
│                                         │
│     [ ENTRAR ]  (rojo oscuro, full)     │
│                                         │
│     ¿No tienes cuenta? Regístrate      │
│                                         │
└─────────────────────────────────────────┘
```

### Dashboard
```
┌──────────────────────────────────────────────────────────┐
│  [Logo]     Dashboard      [Notif] [Avatar]             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│
│  │ Citas    │  │ Ingresos │  │ Clientes │  │ Artistas ││
│  │ hoy: 12  │  │ mes: 4.5k│  │ nuevos: 8│  │ activos:5││
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘│
│                                                          │
│  ┌──────────────────────────────────────────────────────┐│
│  │  Próximas citas                          [Ver todo]  ││
│  │  ─────────────────────────────────────────────────   ││
│  │  10:00  María García  Tatuaje brazo    [Confirmar]  ││
│  │  12:00  Juan López    Piercing oreja   [Completar]  ││
│  │  15:00  Ana Martín    Micropigmentación [Cancelar]  ││
│  └──────────────────────────────────────────────────────┘│
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 12. Referencias de Estilo

- **Apple.com**: Minimalismo, espacios, tipografía limpia
- **Stripe Dashboard**: Cards, data presentation
- **Linear.app**: UI oscura, minimalista, fluida
- **Classic tattoo flash sheets**: Para toques retro (ornamentos, marcos)
