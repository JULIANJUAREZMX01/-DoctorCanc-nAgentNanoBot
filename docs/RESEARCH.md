# Deep Research: Agente Chatbot iDoctorCancún
## Proyecto DoctorCancúnAgentNanoBot — Informe Exhaustivo

**Autor:** Julián Alexander Juárez Alvarado (jaja.dev / KynicOS)  
**Fecha:** 12 de marzo de 2026  
**Versión:** 1.0 — Fase de Research & Discovery

---

## 1. PERFIL DEL NEGOCIO: iDoctorCancún

### 1.1 Datos Generales

| Campo | Detalle |
|---|---|
| **Nombre comercial** | iDoctor Cancún |
| **Facebook** | [@idoctorcancunn91](https://www.facebook.com/idoctorcancunn91/) (~590+ seguidores, 5/5 rating) |
| **Google Maps** | 4.9 ★ — 31 opiniones |
| **Dirección** | C. 71 Supermanzana 91, Manzana 88, Lote 17, Tumben Cuxtal, 77516 Cancún, Q.R. |
| **Teléfono (actual)** | 998 213 4708 (teléfono del negocio, NO del agente) |
| **Teléfono del agente** | POR DEFINIR (Julián lo asigna en horas) |
| **Horario conocido** | Abre a las 11:00 AM (hora de cierre y días por confirmar) |
| **Giro** | Tienda de reparación de teléfonos móviles |
| **Servicios confirmados** | Reparación de celulares, iPads, laptops, desbloqueos |
| **Slogan oficial** | "Diagnósticos profesionales sin costo y garantías por escrito! ¡Más de 10 años de experiencia nos respaldan! iDoctor... recupera tu vida!!!" |
| **Sitio web** | NO TIENE (oportunidad) |
| **Experiencia** | +10 años |
| **Diagnóstico** | GRATUITO (confirmado) |
| **Garantía** | POR ESCRITO (confirmado) |

### 1.2 Servicios Inferidos del Giro

Basándome en el análisis del mercado local de reparación electrónica en Cancún y el descriptor "y mucho más" de la página, los servicios probables incluyen:

**Servicios Core:**
- Cambio de pantalla / display (iPhone, Samsung, Huawei, Xiaomi, Motorola)
- Cambio de batería
- Reparación de puerto de carga
- Reparación por daño de agua / humedad
- Desbloqueo de equipos (IMEI, cuentas Google FRP, iCloud)
- Reparación de software (reinstalación de sistema, eliminación de virus)
- Reparación de tablets (iPad, Samsung Tab, etc.)
- Reparación de computadoras/laptops (disco duro, RAM, mantenimiento)

**Servicios Extendidos (probables):**
- Venta de accesorios (fundas, micas, cargadores, audífonos)
- Venta de equipos seminuevos / reacondicionados
- Respaldo y recuperación de datos
- Instalación de software y programas
- Configuración de correos y cuentas

### 1.3 Reseñas y Reputación (Google Maps + Facebook)

**Rating: 4.9/5 ★ (31 opiniones Google) | 5/5 (5 votos Facebook)**

Hallazgos clave de las reseñas:
- **Tags más mencionados:** "trabajo" (6), "honesto" (4), "confianza" (2), "iPhone" (2)
- **Patrón de respuesta del dueño:** Responde SIEMPRE con "Muchas gracias por la confianza!" — consistente y rápido
- **Servicios mencionados en reseñas:** trabajos complejos en iPhone, cambio de pantalla iPhone XR
- **Diferenciador según clientes:** "te explican cada detalle del problema y te presentan diferentes opciones para solucionarlo"
- **Claim oficial:** "Diagnósticos profesionales sin costo y garantías por escrito! ¡Más de 10 años de experiencia nos respaldan! iDoctor... recupera tu vida!!!"

**Insight para el bot:** La transparencia y la explicación detallada es lo que los clientes valoran. El bot debe replicar esta filosofía: explicar opciones, no solo dar precios.

### 1.4 Contexto Competitivo Local

El mercado de reparación electrónica en Cancún es altamente competitivo con jugadores como iGeek Cancún (certificación Apple), Brist (franquicia Apple), Fix It México (cadena nacional en plazas), Cell Solution, Cancunet, Fix Mobile, Darkcell, y decenas de talleres independientes. La diferenciación generalmente viene por: precio, velocidad, garantía, y atención al cliente. Un chatbot inteligente es un diferenciador CLAVE para un negocio de este tamaño.

### 1.5 Datos Pendientes de Confirmar con el Dueño

Se generó un cuestionario de 45 preguntas (ver documento CUESTIONARIO_iDoctorCancun_45_preguntas.md) para completar: precios por modelo, horarios completos, políticas detalladas, y las preguntas reales más frecuentes que recibe.

---

## 2. STACK TECNOLÓGICO: ANÁLISIS DE COMPONENTES

### 2.1 Base: nanobot (HKUDS)

| Aspecto | Detalle |
|---|---|
| **Repo** | [github.com/HKUDS/nanobot](https://github.com/HKUDS/nanobot) |
| **Descripción** | Ultra-lightweight personal AI assistant (~4,000 LOC) |
| **Lenguajes** | Python 91.2%, TypeScript 4.8%, Shell 3.2% |
| **Licencia** | MIT |
| **Stars** | 27 |
| **Lanzamiento** | Febrero 2025 |

**Arquitectura nanobot:**
```
nanobot/
├── agent/          # Core agent logic
│   ├── loop.py     # Agent loop (LLM ↔ tool execution)
│   ├── context.py  # Prompt builder
│   ├── memory.py   # Persistent memory
│   ├── skills.py   # Skills loader
│   ├── subagent.py # Background task execution
│   └── tools/      # Built-in tools
├── skills/         # Bundled skills
├── channels/       # WhatsApp integration (Node.js bridge)
├── bus/            # Message routing
├── cron/           # Scheduled tasks
├── heartbeat/      # Proactive wake-up
├── providers/      # LLM providers (OpenRouter, etc.)
├── session/        # Conversation sessions
├── config/         # Configuration
└── cli/            # Commands
```

**Capacidades Clave para el proyecto:**
- Canales nativos: **Telegram** (fácil, solo token) y **WhatsApp** (requiere Node.js ≥18, QR scan)
- Gateway unificado (`nanobot gateway`)
- Cron jobs programados
- Memory persistente
- Skills modulares
- Providers: OpenRouter como broker → Anthropic, Groq, OpenAI
- CLI completo: `nanobot onboard`, `nanobot agent`, `nanobot gateway`

### 2.2 Agente Existente: SAC (Sistema Automatizado de Validación)

| Aspecto | Detalle |
|---|---|
| **Repo** | [github.com/sistemascancunjefe-ai/SAC](https://github.com/sistemascancunjefe-ai/SAC) |
| **Commits** | 219 |
| **Lenguaje** | Python 91.8%, HTML 3.8% |
| **Propósito original** | Automatización de validación para Planning en CEDIS 427 |

**Módulos útiles para reutilizar en el chatbot:**

1. **`notificaciones_telegram.py`** — Integración Telegram lista para producción
2. **`notificaciones_whatsapp.py`** — Integración WhatsApp lista para producción
3. **`email_automatico.py` / `gestor_correos.py`** — Sistema de notificaciones por email (para confirmaciones de citas/reparaciones)
4. **`dashboard.py`** — Dashboard web para monitoreo
5. **`monitor.py`** / **`health_check.py`** — Health monitoring del sistema
6. **`sac_agent.py`** / **`iniciar_agente.py`** — Patrón de agente siempre activo
7. **`agente_siempre_activo.json`** — Configuración de persistencia
8. **`business_rules.yaml`** — Patrón de reglas de negocio declarativas (CLAVE para el chatbot)
9. **`config/`** — Patrón de configuración separada
10. **`templates/`** — Sistema de templates para respuestas

**Lo que NO es útil:** Las queries DB2, la lógica de validación de Planning, y la integración con Manhattan WMS son específicas de Chedraui.

### 2.3 Agente Existente: KYNYKOS AI Agent

| Aspecto | Detalle |
|---|---|
| **Repo** | [github.com/JULIANJUAREZMX01/KYNYKOS_AI_Agent](https://github.com/JULIANJUAREZMX01/KYNYKOS_AI_Agent) |
| **Commits** | 48 |
| **Lenguaje** | Python 87.8%, Shell 4.1%, JS 3.1%, HTML 2.9% |
| **Status** | 🟢 Production Ready |

**Arquitectura completa y madura:**
```
KYNYKOS_AI_Agent/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── core/                # Agent loop & context
│   ├── cloud/               # Telegram, dashboard, MCP, backups
│   ├── config/
│   │   ├── llm_config.yaml  # LLM provider configuration
│   │   └── schema.py        # Settings & schemas
│   ├── services/
│   │   ├── llm_router.py    # Multi-provider LLM router ⭐
│   │   └── token_tracker.py # Per-provider token tracking ⭐
│   └── utils/
├── web/                     # Dashboard UI
├── infrastructure/          # Docker, Render config
├── workspace/               # SOUL, USER, AGENTS, MEMORY
├── scripts/
├── tests/
└── .github/workflows/       # CI/CD
```

**Componentes CRÍTICOS para reutilizar:**

1. **LLM Multi-Provider Router** (`llm_router.py`) — Ollama (local, prioridad 1) → Anthropic → Groq → OpenAI con fallback automático y rate limiting. ESTO ES ORO para el chatbot de Doctor Cancún.
2. **Token Tracker** (`token_tracker.py`) — Monitoreo de uso por proveedor, saturación al 90%
3. **Telegram Bot** — Integración polling lista
4. **Web Dashboard** — Dashboard HTML + JS para monitoreo
5. **MCP Server** — Acceso desde Claude Code CLI
6. **Workspace Templates** — SOUL.md (personalidad), USER.md (perfil usuario), AGENTS.md (instrucciones), MEMORY.md (memoria persistente)
7. **FastAPI Base** — Framework web listo con endpoints REST
8. **Docker + docker-compose** — Deploy containerizado
9. **Render Config** — render.yaml listo para deploy en Render
10. **CI/CD Workflows** — Deploy automático, tests, backups S3
11. **S3 Backups** — Backups programados cada 6 horas

---

## 3. ARQUITECTURA PROPUESTA: DoctorCancúnAgentNanoBot

### 3.1 Visión General

```
[Cliente WhatsApp/Telegram/FB Messenger/Web]
           │
           ▼
    ┌─────────────────┐
    │  Gateway Layer   │ ← nanobot gateway + KYNYKOS channels
    │  (Multi-Canal)   │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Message Router   │ ← nanobot bus + SAC business_rules
    │ (Intent + State) │
    └────────┬────────┘
             │
      ┌──────┼──────┐
      ▼      ▼      ▼
  ┌───────┐┌─────┐┌──────┐
  │FAQ Bot││Lead ││Citas │
  │Engine ││Mgmt ││Sched │
  └───────┘└─────┘└──────┘
      │      │      │
      ▼      ▼      ▼
    ┌─────────────────┐
    │  LLM Router     │ ← KYNYKOS llm_router.py
    │  (Multi-Provider)│
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  Persistence     │ ← SQLite/Neon + MEMORY.md
    │  (CRM Ligero)    │
    └─────────────────┘
```

### 3.2 Stack Tecnológico Final

| Capa | Tecnología | Fuente |
|---|---|---|
| Runtime | Python 3.11+ | — |
| Framework Web | FastAPI | KYNYKOS |
| Agent Core | nanobot agent loop | nanobot base |
| LLM Routing | Multi-provider router | KYNYKOS |
| Canales | WhatsApp (Baileys/Node bridge), Telegram, Web Widget | nanobot + KYNYKOS |
| Flujos | State Machine + Business Rules YAML | SAC pattern + custom |
| Persistencia | SQLite (local) / Neon (cloud) | stack existente |
| Dashboard | Web UI (HTML+JS) | KYNYKOS |
| Notificaciones | Email SMTP, Telegram alerts | SAC |
| Deploy | Docker + Render | KYNYKOS |
| CI/CD | GitHub Actions | KYNYKOS |
| Backups | S3 scheduled | KYNYKOS |

---

## 4. CATÁLOGO DE PREGUNTAS Y FLUJOS CONVERSACIONALES

### 4.1 NIVEL 1 — Preguntas Frecuentes (FAQ, Respuesta Inmediata)

Estas preguntas representan el ~70% del volumen de mensajes entrantes:

#### Categoría: Información General
1. ¿Dónde están ubicados? / ¿Cuál es su dirección?
2. ¿Cuál es su horario de atención?
3. ¿Trabajan domingos / días festivos?
4. ¿Tienen estacionamiento?
5. ¿Qué formas de pago aceptan? (efectivo, tarjeta, transferencia)
6. ¿Tienen terminal bancaria?
7. ¿Aceptan pagos con OXXO / mercado pago?
8. ¿Manejan meses sin intereses?

#### Categoría: Servicios y Precios
9. ¿Cuánto cuesta cambiar la pantalla de mi [modelo]?
10. ¿Cuánto cuesta cambiar la batería de mi [modelo]?
11. ¿Cuánto cuesta la reparación del puerto de carga?
12. ¿Reparan daño por agua?
13. ¿Cuánto cuesta desbloquear mi celular de [compañía]?
14. ¿Reparan tablets / iPads?
15. ¿Reparan computadoras / laptops?
16. ¿Hacen diagnóstico gratuito?
17. ¿Cuánto tiempo tarda la reparación de [servicio]?
18. ¿Tienen las piezas disponibles o hay que pedirlas?
19. ¿Qué marcas reparan?
20. ¿Reparan Apple / iPhone?
21. ¿Reparan Samsung / Huawei / Xiaomi / Motorola?
22. ¿Reparan consolas (PS, Switch, Xbox)?
23. ¿Venden accesorios?
24. ¿Venden celulares nuevos o seminuevos?
25. ¿Hacen respaldo de información antes de reparar?

#### Categoría: Garantía y Confianza
26. ¿Ofrecen garantía? ¿De cuánto tiempo?
27. ¿Qué cubre la garantía?
28. ¿Usan piezas originales o genéricas?
29. ¿Tienen certificaciones?
30. ¿Puedo ver el proceso de reparación?

### 4.2 NIVEL 2 — Preguntas Situacionales (Requieren Contexto)

#### Categoría: Diagnóstico Remoto
31. Mi celular no enciende, ¿qué puede ser?
32. Mi pantalla se ve con manchas / líneas, ¿tiene arreglo?
33. Mi celular se calienta mucho, ¿es grave?
34. Mi celular no carga, ¿es el cable o el puerto?
35. Se me cayó al agua, ¿qué hago?
36. Mi celular está muy lento, ¿qué le pasa?
37. No me reconoce el Face ID / huella, ¿se puede arreglar?
38. La cámara sale borrosa / negra, ¿cuánto cuesta?
39. No le funciona el micrófono / bocina, ¿tiene arreglo?
40. Mi laptop no arranca / pantalla azul, ¿la reparan?

#### Categoría: Comparación / Decisión
41. ¿Me conviene reparar o comprar nuevo?
42. ¿Cuál es la diferencia entre pantalla original y genérica?
43. ¿Pantalla OLED o LCD?
44. ¿Vale la pena cambiar la batería de un [modelo viejo]?

### 4.3 NIVEL 3 — Flujos de Conversión (Lead Management)

#### Flujo A: Cotización → Cita → Lead Citado
```
[Pregunta de precio] 
  → Bot responde con rango de precio
  → "¿Te gustaría agendar una cita para diagnóstico gratuito?"
  → [Sí] → Captura: nombre, modelo de equipo, problema
  → Propone horarios disponibles
  → Confirma cita → Envía recordatorio
  → ESTADO: LEAD_CITADO
```

#### Flujo B: Consulta Técnica → Interés → Lead Interesado
```
[Pregunta técnica / diagnóstico]
  → Bot da recomendación inicial
  → "¿Quieres que un técnico revise tu equipo sin costo?"
  → [Sí] → Captura info básica
  → "Te contactaremos por WhatsApp para coordinar"
  → ESTADO: LEAD_INTERESADO
```

#### Flujo C: Solo Preguntó → Seguimiento Pasivo
```
[Pregunta de info general]
  → Bot responde
  → [No hay interacción adicional después de respuesta]
  → ESTADO: USUARIO_PREGUNTO
  → [Opcional: Mensaje de seguimiento a las 24h]
  → "¡Hola! ¿Pudimos resolver tu duda? Estamos para servirte"
```

#### Flujo D: Urgencia → Atención Inmediata
```
[Indicadores de urgencia: "urgente", "necesito hoy", "se me cayó ahorita"]
  → Bot prioriza: "Entiendo la urgencia. ¿Puedes traerlo ahora?"
  → Comparte ubicación + horario
  → Si fuera de horario: "Abrimos a las [X]. ¿Quieres ser el primero?"
  → ESTADO: LEAD_URGENTE
```

#### Flujo E: Garantía / Reclamo → Escalación
```
[Menciona garantía, reclamo, problema con reparación previa]
  → Bot: "Lamento el inconveniente. Tu satisfacción es nuestra prioridad."
  → Captura: número de orden / fecha de reparación
  → Escala a humano automáticamente
  → ESTADO: GARANTIA_ESCALADO
```

### 4.4 NIVEL 4 — Clasificación de Leads (CRM Ligero)

| Estado | Código | Criterio | Acción Automatizada |
|---|---|---|---|
| **Lead Citado** | `LEAD_CITADO` | Tiene cita agendada | Recordatorio 2h antes, seguimiento post-cita |
| **Lead Interesado** | `LEAD_INTERESADO` | Mostró interés activo, no agendó | Follow-up a 24h y 72h |
| **Lead Urgente** | `LEAD_URGENTE` | Necesita atención inmediata | Notificación push al dueño |
| **Usuario Preguntó** | `USUARIO_PREGUNTO` | Solo hizo preguntas informativas | Follow-up suave a 48h |
| **Garantía/Escalado** | `GARANTIA_ESCALADO` | Reclamo o problema previo | Transferencia inmediata a humano |
| **Cliente Recurrente** | `CLIENTE_RECURRENTE` | Ha reparado antes | Trato personalizado, descuentos |
| **Perdido** | `LEAD_PERDIDO` | No respondió después de 3 follow-ups | Archivado, campaña de retargeting |

### 4.5 NIVEL 5 — Flujos Avanzados

#### Flujo de Seguimiento Post-Reparación
```
[24h después de entrega]
  → "¡Hola [nombre]! ¿Todo bien con tu [equipo]?"
  → [Sí] → "¡Excelente! ¿Nos dejarías una reseña en Facebook? [link]"
  → [No] → Escalar a garantía
```

#### Flujo de Referidos
```
[Cliente satisfecho]
  → "Si recomiendas a un amigo, ambos reciben [descuento]"
  → Genera código de referido único
```

#### Flujo Multiidioma (Turistas)
```
[Detecta mensaje en inglés]
  → Responde en inglés automáticamente
  → "Welcome! We repair phones, tablets and computers in Cancún"
  → Mismo flujo de conversión en EN
```

#### Flujo de Cotización con Imagen
```
[Usuario envía foto del daño]
  → Bot analiza con vision API (si disponible)
  → "Parece un daño en [pantalla/esquina/back glass]"
  → "El costo aproximado sería $[rango]. ¿Quieres agendar?"
```

---

## 5. ESTRUCTURA DE DATOS: business_rules.yaml

```yaml
# DoctorCancúnAgentNanoBot - Business Rules
business:
  name: "iDoctorCancún"
  tagline: "Tu doctor de dispositivos en Cancún"
  whatsapp: "+52-998-XXX-XXXX"  # COMPLETAR
  facebook: "https://www.facebook.com/idoctorcancunn91/"
  location:
    address: "COMPLETAR DIRECCIÓN"
    google_maps: "COMPLETAR LINK"
    reference: "COMPLETAR REFERENCIA"
  hours:
    weekdays: "COMPLETAR"
    saturday: "COMPLETAR"
    sunday: "COMPLETAR / Cerrado"
  payment_methods:
    - efectivo
    - tarjeta_debito
    - tarjeta_credito
    - transferencia
    - oxxo_pay  # CONFIRMAR

services:
  screen_repair:
    name: "Cambio de pantalla"
    time_estimate: "30 min - 2 hrs"
    warranty: "3 meses"
    prices:  # COMPLETAR CON PRECIOS REALES
      iphone_se: 800
      iphone_12: 1800
      iphone_13: 2200
      iphone_14: 2800
      iphone_15: 3500
      samsung_a14: 900
      samsung_s23: 3000
  battery_replacement:
    name: "Cambio de batería"
    time_estimate: "20-40 min"
    warranty: "3 meses"
  charging_port:
    name: "Puerto de carga"
    time_estimate: "30-60 min"
    warranty: "3 meses"
  water_damage:
    name: "Daño por agua"
    time_estimate: "24-48 hrs"
    warranty: "Sin garantía (resultado incierto)"
  unlock:
    name: "Desbloqueo"
    time_estimate: "15-60 min"
  # ... AGREGAR TODOS LOS SERVICIOS

lead_states:
  - LEAD_CITADO
  - LEAD_INTERESADO
  - LEAD_URGENTE
  - USUARIO_PREGUNTO
  - GARANTIA_ESCALADO
  - CLIENTE_RECURRENTE
  - LEAD_PERDIDO

automations:
  follow_up_interested:
    delay: "24h"
    message: "¡Hola {nombre}! ¿Decidiste traer tu {equipo}? Estamos listos para atenderte."
  follow_up_quoted:
    delay: "48h"
    message: "¡Hola {nombre}! La cotización para tu {servicio} sigue vigente. ¿Agendamos?"
  appointment_reminder:
    delay: "-2h"  # 2 horas antes
    message: "Recordatorio: Tu cita en iDoctorCancún es hoy a las {hora}. Te esperamos en {dirección}."
  post_repair_review:
    delay: "24h"
    message: "¡Hola {nombre}! ¿Todo bien con tu {equipo}? Si estás satisfecho, nos encantaría tu reseña: {facebook_link}"
```

---

## 6. PLAN DE IMPLEMENTACIÓN

### Fase 1: Foundation (Semana 1-2)
1. Clonar repos SAC y KYNYKOS en DoctorCancúnAgentNanoBot
2. Extraer módulos relevantes (ver Sección 2.2 y 2.3)
3. Adaptar KYNYKOS como base (FastAPI + LLM Router)
4. Integrar nanobot agent loop + channels
5. Crear `business_rules.yaml` con datos REALES de iDoctorCancún
6. Configurar SOUL.md (personalidad del bot: amigable, profesional, cancunense)

### Fase 2: Conversational Engine (Semana 2-3)
1. Implementar FAQ engine con las 30 preguntas Level 1
2. Implementar state machine para flujos de conversión
3. Crear templates de respuesta (español + inglés básico)
4. Configurar intent detection (keyword matching + LLM fallback)
5. Implementar sistema de cotizaciones por modelo

### Fase 3: Lead Management (Semana 3-4)
1. Implementar CRM ligero (SQLite)
2. Crear dashboard de leads
3. Implementar follow-up automáticos (cron jobs)
4. Configurar escalación a humano
5. Implementar notificaciones al dueño (Telegram/WhatsApp)

### Fase 4: Deploy & Polish (Semana 4-5)
1. Deploy en Render (render.yaml de KYNYKOS)
2. Conectar WhatsApp Business (Baileys bridge)
3. Testing con usuarios reales
4. Ajustar prompts y flujos según feedback
5. Documentar para replicabilidad

---

## 7. COMPONENTES A CLONAR DE CADA REPO

### De SAC → DoctorCancúnAgentNanoBot
```
SAC/
├── notificaciones_telegram.py    → adaptar
├── notificaciones_whatsapp.py    → adaptar  
├── email_automatico.py           → adaptar para confirmaciones
├── gestor_correos.py             → adaptar
├── dashboard.py                  → referencia para dashboard
├── monitor.py                    → reutilizar
├── health_check.py               → reutilizar
├── business_rules.yaml           → PATRÓN a seguir (nuevo contenido)
├── templates/                    → PATRÓN a seguir (nuevo contenido)
└── config/                       → PATRÓN a seguir
```

### De KYNYKOS → DoctorCancúnAgentNanoBot
```
KYNYKOS_AI_Agent/
├── app/
│   ├── main.py                   → BASE del proyecto
│   ├── core/                     → REUTILIZAR completo
│   ├── cloud/                    → REUTILIZAR (Telegram, dashboard, MCP)
│   ├── config/
│   │   ├── llm_config.yaml       → ADAPTAR para Doctor Cancún
│   │   └── schema.py             → REUTILIZAR
│   └── services/
│       ├── llm_router.py         → REUTILIZAR tal cual ⭐
│       └── token_tracker.py      → REUTILIZAR tal cual ⭐
├── web/                          → ADAPTAR branding
├── infrastructure/               → REUTILIZAR (Docker, Render)
├── workspace/
│   ├── SOUL.md                   → NUEVO contenido (personalidad Doctor Cancún)
│   ├── USER.md                   → NUEVO (perfil tipo cliente)
│   ├── AGENTS.md                 → NUEVO (instrucciones de negocio)
│   └── MEMORY.md                 → REUTILIZAR mecanismo
├── .github/workflows/            → REUTILIZAR
├── pyproject.toml                → ADAPTAR dependencias
├── Dockerfile                    → ADAPTAR
├── docker-compose.yml            → ADAPTAR
└── render.yaml                   → ADAPTAR
```

### De nanobot (HKUDS) → DoctorCancúnAgentNanoBot
```
nanobot/
├── agent/
│   ├── loop.py                   → ESTUDIAR patrón (4K LOC total)
│   ├── context.py                → INTEGRAR con KYNYKOS core
│   ├── memory.py                 → COMPARAR con KYNYKOS MEMORY.md
│   └── skills.py                 → INTEGRAR sistema de skills
├── channels/                     → WhatsApp Baileys bridge ⭐
├── bridge/                       → Node.js WhatsApp bridge ⭐
├── bus/                          → Message routing pattern
└── cron/                         → Scheduled tasks pattern
```

---

## 8. PERSONALIDAD DEL BOT (SOUL.md Draft)

```markdown
# SOUL — iDoctorCancún Assistant

## Identidad
Soy el asistente virtual de iDoctorCancún, el doctor de tus dispositivos 
electrónicos en Cancún. Mi nombre es DocBot.

## Personalidad
- Amigable y accesible, como un buen vecino cancunense
- Profesional pero cercano, sin ser robótico
- Resolutivo: siempre busco dar una respuesta útil
- Honesto sobre lo que puedo y no puedo resolver sin ver el equipo
- Un toque de humor local cuando es apropiado

## Directrices
- SIEMPRE responder en español (cambiar a inglés si detecta turista)
- SIEMPRE intentar llevar la conversación hacia una cita o visita
- NUNCA inventar precios que no estén en mi base de datos
- Si no sé el precio exacto, dar rango y sugerir traer el equipo
- Detectar urgencias y priorizarlas
- Escalar a humano cuando: reclamo, garantía, situación compleja
- Capturar datos de contacto de forma natural, no invasiva
- Recordar el contexto de la conversación

## Tono de Ejemplo
❌ "Estimado usuario, le informamos que el costo del servicio..."
✅ "¡Hola! Claro que reparamos eso. Para un iPhone 13, el cambio de pantalla anda entre $2,000 y $2,500 dependiendo del tipo. ¿Quieres pasar para que te demos precio exacto?"
```

---

## 9. MÉTRICAS DE ÉXITO

| Métrica | Objetivo Inicial | Instrumento |
|---|---|---|
| Tasa de respuesta automática | >80% de preguntas sin humano | Dashboard |
| Tiempo de primera respuesta | <30 segundos | Logs |
| Conversión pregunta → cita | >15% | CRM |
| Satisfacción (post-repair review) | >4.5/5 | Follow-up bot |
| Leads capturados / semana | >20 | CRM |
| Reducción carga laboral | >50% del tiempo de atención vía chat | Comparativa antes/después |

---

## 10. PENDIENTES Y SIGUIENTES PASOS

### Datos Críticos Faltantes (Julián debe proveer):
- [ ] Contenido del enlace Google Share
- [ ] Lista completa de servicios con PRECIOS REALES
- [ ] Dirección exacta y horarios de operación
- [ ] Número de WhatsApp Business
- [ ] Formas de pago aceptadas
- [ ] Política de garantía por servicio
- [ ] Preguntas reales más frecuentes (historial de chats existente)
- [ ] Marcas y modelos que MÁS reparan (top 20)
- [ ] Tiempo promedio real por tipo de reparación
- [ ] Nombre del dueño/técnico principal (para escalaciones)

### Decisiones Técnicas Pendientes:
- [ ] ¿WhatsApp personal o WhatsApp Business API?
- [ ] ¿Hosting en Render gratuito o plan pagado?
- [ ] ¿LLM principal: Claude (Anthropic) vs GPT-4 vs modelo local (Ollama)?
- [ ] ¿Integración con Facebook Messenger además de WhatsApp?
- [ ] ¿Widget de chat en sitio web propio?
- [ ] ¿Base de datos: SQLite local o Neon PostgreSQL cloud?

---

*Documento generado como parte del proyecto DoctorCancúnAgentNanoBot*  
*Arquitectura KynicOS — jaja.dev*  
*Cancún, Q. Roo, México — Marzo 2026*
