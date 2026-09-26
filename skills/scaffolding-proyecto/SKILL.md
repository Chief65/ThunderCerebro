---
name: scaffolding-proyecto
description: >
  Inicializar y estructurar proyectos nuevos con carpetas, configuración Claude,
  repositorio Git, entorno conda y archivos base. También crear o mejorar el
  CLAUDE.md de proyectos existentes. Usar cuando el usuario dice "nuevo proyecto",
  "quiero montar un proyecto", "crea la estructura para...", "inicializa un repo",
  "crea un CLAUDE.md para este proyecto", "configura Claude para este proyecto",
  "mejora mi CLAUDE.md", o cuando se detecta que un proyecto no tiene estructura
  definida o le falta configuración Claude. Cubre desde proyectos de datos/ETL
  hasta estudios de mercado o documentación. Para la guía completa de cómo
  escribir un buen CLAUDE.md de proyecto, consultar references/guia-claude-md-proyecto.md.
---

# Scaffolding de Proyectos — Estructura y Configuración

## Rol

Actúa como un arquitecto de proyectos. Tu trabajo es que cada proyecto nuevo
arranque con la estructura correcta desde el día uno: carpetas lógicas,
configuración Claude, control de versiones, entorno aislado y documentación base.
Un proyecto bien estructurado se mantiene solo; uno mal estructurado genera
deuda técnica desde la primera hora.

## Proceso

### Paso 1 — Entender el proyecto

Antes de crear nada, clarificar:

1. **Nombre del proyecto**: Corto, descriptivo, en kebab-case (`automatizacion-catalogos`).
2. **Tipo de proyecto**: Determina la estructura de carpetas.
   - **Datos/ETL**: SQL, Python, transformaciones, pipelines.
   - **Análisis/Estudio**: Notebooks, datos, informes, visualizaciones.
   - **Aplicación/Script**: Código fuente, tests, configuración.
   - **Documentación/Estrategia**: Docs, investigación, entregables.
   - **Mixto**: Combinación — preguntar qué pesa más.
3. **Stack técnico**: Python, R, SQL, PowerBI, etc. Determina el entorno.
4. **¿Repo privado o público?**: Por defecto privado.
5. **Modo de trabajo por defecto**: ¿Modo estudio o modo productivo?

### Paso 2 — Crear estructura de carpetas

Adaptar al tipo de proyecto. Plantillas base:

**Proyecto de Datos/ETL:**
```
nombre-proyecto/
├── CLAUDE.md                    # Contexto del proyecto para Claude
├── .claude/
│   └── skills/                  # Skills específicos del proyecto (si los hay)
├── .gitignore
├── .env.example                 # Template de credenciales (sin datos reales)
├── requirements.txt             # o environment.yml para conda
├── README.md                    # Descripción para humanos
├── sql/
│   ├── exploración/             # Queries de investigación
│   └── producción/              # Queries finales / vistas / MVs
├── scripts/
│   ├── etl/                     # Scripts de transformación
│   └── utils/                   # Funciones auxiliares
├── datos/                       # Datos locales (en .gitignore)
│   ├── raw/                     # Datos brutos
│   └── processed/               # Datos transformados
├── docs/                        # Documentación del proyecto
│   ├── especificaciones/
│   └── decisiones/              # ADRs (Architecture Decision Records)
└── tests/                       # Tests mínimos
```

**Proyecto de Análisis/Estudio:**
```
nombre-proyecto/
├── CLAUDE.md
├── .gitignore
├── requirements.txt
├── notebooks/                   # Jupyter/Quarto notebooks
├── datos/                       # En .gitignore
│   ├── raw/
│   └── processed/
├── informes/                    # Entregables
├── visualizaciones/             # Gráficos exportados
└── referencias/                 # Papers, docs externos
```

**Proyecto de Documentación/Estrategia:**
```
nombre-proyecto/
├── CLAUDE.md
├── .gitignore
├── investigacion/               # Notas de investigación, fuentes
├── borradores/                  # Versiones en progreso
├── entregables/                 # Versiones finales
│   ├── internos/                # Para equipo
│   └── externos/                # Para clientes/presentaciones
└── assets/                      # Imágenes, diagramas
```

### Paso 3 — Crear CLAUDE.md del proyecto

Este es el archivo más importante. Debe contener:

```markdown
# [Nombre del Proyecto]

## Propósito
[Una frase: qué problema resuelve este proyecto]

## Modo por defecto: [modo-estudio | modo-productivo]

## Estado actual
[En qué fase está el proyecto: investigación, desarrollo, testing, producción]

## Vault (cerebro-digital)
- Nota principal: `[[Nombre_Nota_Vault]]` en [carpeta PARA]
- Areas relacionadas: `[[Area_1]]`, `[[Area_2]]`

## Contexto técnico
- Stack: [tecnologías]
- Base de datos: [si aplica]
- Dependencias clave: [librerías principales]

## Archivos clave
| Archivo | Descripción | Estado |
|---------|-------------|--------|
| ... | ... | ✅/🔄/⬜ |

## Decisiones tomadas
[Decisiones de diseño importantes y su justificación]

## Próximos pasos
- [ ] [Tarea pendiente más inmediata]
```

**Regla**: El CLAUDE.md del proyecto NO repite lo que ya está en el global.
No poner identidad, tono ni principios — eso ya lo carga `~/.claude/CLAUDE.md`.

### Paso 4 — Crear .gitignore

Incluir siempre:
```
# Datos y credenciales
.env
datos/
*.csv
*.xlsx

# Python
__pycache__/
*.pyc
.venv/
*.egg-info/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Notebooks
.ipynb_checkpoints/
```

Adaptar según el stack del proyecto.

### Paso 5 — Crear .env.example

Si el proyecto necesita credenciales:
```
# Base de datos
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=

# APIs
API_KEY=
API_SECRET=

# FTP (si aplica)
FTP_HOST=
FTP_USER=
FTP_PASSWORD=
FTP_PATH=
```

**Nunca poner valores reales.** Solo el template.

### Paso 6 — Configurar entorno

Preguntar al usuario qué prefiere:

**Opción A — Conda** (recomendado para ciencia de datos):
```bash
conda create -n nombre-proyecto python=3.11 -y
conda activate nombre-proyecto
pip install -r requirements.txt
```

**Opción B — venv** (para scripts ligeros):
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

Generar `requirements.txt` con las dependencias iniciales según el stack.

### Paso 7 — Inicializar repositorio Git

```bash
cd nombre-proyecto
git init
git add .
git commit -m "feat: scaffold inicial del proyecto"
```

Si el usuario quiere repo en GitHub:
```bash
gh repo create nombre-proyecto --private --source=. --push
```

Verificar que `gh` (GitHub CLI) está disponible. Si no, dar instrucciones
para crear el repo manualmente.

### Paso 8 — Crear ficha en cerebro-digital (Obsidian)

Cada proyecto/area nuevo debe tener su nota espejo en el vault de Obsidian.

**Proceso:**

1. **Determinar clasificacion PARA:**
   - ¿Tiene deadline o entregable concreto? → `1_Proyectos/` (ficha ligera, tracking en Notion)
   - ¿Es mantenimiento continuo sin fecha fin? → `2_Areas/` (en subcarpeta existente: `Tecnologia/`, `Negocio/`, `Arquitectura_Agentes/`)
   - No crear subcarpetas nuevas sin consenso del usuario. Maximo 2 niveles de profundidad.

2. **Crear la nota** siguiendo convenciones del vault:
   - Nombre: `PascalCase_Con_Underscores.md` (ej: `Infra_Lab_IA_Local.md`)
   - Sin YAML frontmatter
   - Tags al pie
   - Al menos 1 `[[wikilink]]` a nota relacionada

3. **Contenido minimo de la ficha:**
   ```markdown
   # [Nombre del Proyecto/Area]

   [Una frase: que es y por que existe]

   ## Conexion con repos
   - Repo: `~/Proyectos/nombre-repo/`

   ## Relaciones
   - [[Area_o_Recurso_Relacionado]]

   ---
   **Estado:** Vivo (v1.0 - Mes YYYY).

   #tag1 #tag2
   ```

4. **Tags:** Revisar lista existente en `_Sistema/00_Reglas_Vault.md` antes de crear nuevos.
   Tags frecuentes: `#python`, `#consultoria`, `#formacion`, `#aprendizaje`, `#ia`, `#negocio`.
   Si ningun tag existente encaja, proponer uno nuevo al usuario — nunca crear sin confirmar.

5. **Actualizar notas relacionadas** en el vault para que enlacen de vuelta a la nueva nota.

**Vault path:** `~/.openclaw/workspace-arquimedes/cerebro-digital` (servidor iMac)
o `~/cerebro-digital` (otros equipos). Fallback legacy: `~/Proyectos/cerebro-digital`.

### Paso 9 — Verificación final

Checklist de entrega:
- [ ] Estructura de carpetas creada
- [ ] CLAUDE.md del proyecto escrito (con seccion Vault)
- [ ] .gitignore configurado
- [ ] .env.example (si necesita credenciales)
- [ ] requirements.txt / environment.yml
- [ ] Entorno conda/venv creado
- [ ] Repo Git inicializado
- [ ] Primer commit hecho
- [ ] (Opcional) Repo en GitHub creado
- [ ] Ficha en cerebro-digital creada y enlazada

## Herramientas MCP útiles

- **github**: Para crear repos, configurar ramas, crear .gitignore desde templates.
- **filesystem**: Para crear la estructura de carpetas y archivos.
- **sequential-thinking**: Para proyectos complejos donde la estructura no es obvia
  y hay que pensar las dependencias entre componentes.

## Reglas importantes

- **No sobreingeniar.** Un proyecto de un solo script no necesita 15 carpetas.
  Adaptar la estructura al tamaño real del proyecto.
- **Preguntar antes de crear.** No asumir el tipo de proyecto ni el stack.
  Pero si el contexto es claro, proponer y confirmar en vez de preguntar todo.
- **El CLAUDE.md es para Claude, el README.md es para humanos.** No mezclarlos.
  El CLAUDE.md contiene contexto de trabajo; el README contiene documentación
  para quien clone el repo.

## Crear o mejorar CLAUDE.md de proyecto existente

Si el usuario tiene un proyecto SIN CLAUDE.md o con uno que es realmente una
especificación técnica (no una guía de contexto para Claude), consultar
[references/guia-claude-md-proyecto.md](references/guia-claude-md-proyecto.md)
para la guía completa con plantilla, ejemplos y reglas de qué poner y qué no.
