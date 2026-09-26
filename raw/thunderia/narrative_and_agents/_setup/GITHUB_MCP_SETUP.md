# Conectar Antigravity CLI al repo de GitHub (ThunderStudios)

## 1. Crea el token
Ve a https://github.com/settings/tokens y crea un Personal Access Token con,
como mínimo, estos scopes:
- `repo` (control total de repos privados)
- `read:org`
- `read:user`

## 2. Localiza el mcp_config.json de tu instalación
La ruta exacta ha cambiado entre versiones de Antigravity, así que
compruébala en tu instalación en vez de asumirla:

- Dentro de Antigravity: menú "..." del panel del agente → **MCP Servers**
  → **Manage MCP Servers** → **View raw config**. Eso abre el archivo
  correcto directamente.
- Alternativamente, en terminal: `agy inspect` te lista, entre otras cosas,
  qué `mcp_config.json` está cargando.
- Rutas típicas vistas en distintas versiones (Windows / macOS-Linux):
  - `C:\Users\<TU_USUARIO>\.gemini\antigravity\mcp_config.json`
  - `~/.gemini/antigravity/mcp_config.json`
  - `~/.gemini/config/mcp_config.json` (versión unificada más reciente)

## 3. Decide el alcance
- **Global** (una de las rutas de arriba en tu carpeta de usuario): el
  servidor de GitHub estará disponible en todos tus proyectos.
- **Solo este proyecto** (recomendado si no quieres que el agente toque
  GitHub en tus proyectos personales/de prácticas): crea el archivo
  `.agents/mcp_config.json` dentro de `ThunderStudios/` con el mismo
  contenido. Algunas versiones de Antigravity CLI ya soportan esto a nivel
  de proyecto — confírmalo con `agy inspect` una vez instalado.

## 4. Contenido a copiar
Usa la plantilla `mcp_config.template.json` de esta misma carpeta,
sustituyendo `YOUR_GITHUB_PAT` por tu token real. Importante: Antigravity
usa la clave `serverUrl`, no `url`, para servidores MCP remotos.

## 5. Reinicia Antigravity y verifica
Reinicia la app/CLI y comprueba en el panel de MCP Servers (o con `/mcp`
en la CLI) que "github" aparece conectado con su lista de herramientas.

## Nota de seguridad
No subas nunca tu `mcp_config.json` con el token real a GitHub. Si este
archivo vive dentro de `ThunderStudios/`, añade `.agents/mcp_config.json`
(o el nombre que uses) a tu `.gitignore`.
