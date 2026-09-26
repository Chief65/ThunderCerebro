---
name: instalar-mcps
description: >
  Instalar MCPs pre-configurados en un proyecto via .mcp.json. Usar cuando el
  usuario dice "instala el mcp de shopify", "anade mcps de ecommerce", "configura
  mcps para este proyecto", "necesito el mcp de X", "pon los mcps de estudio",
  "instala mcps", "quita el mcp de X", o cuando se detecta que un proyecto necesita
  MCPs especificos que no estan en la configuracion global. Consultar
  references/mcp-catalog.md para el catalogo completo de MCPs y bundles disponibles.
---

# Instalar MCPs en Proyecto

## Rol

Gestionas la configuracion de MCP servers a nivel proyecto. Tu trabajo es inyectar
las configuraciones pre-validadas del catalogo en el `.mcp.json` del proyecto actual,
sin que el usuario tenga que escribir JSON a mano.

## Contexto

Los MCPs globales (filesystem, github, sequential-thinking, brave-search) ya estan
configurados en `~/.claude.json`. Todo lo demas se instala por proyecto en `.mcp.json`
en la raiz del proyecto.

El catalogo completo de MCPs disponibles esta en `references/mcp-catalog.md`.
Leelo SIEMPRE antes de actuar.

## Proceso

### Paso 1 — Identificar que instalar

Interpretar la peticion del usuario:

- **MCP individual**: "instala shopify" -> buscar `shopify` en el catalogo
- **Bundle**: "instala ecommerce" -> resolver bundle a MCPs individuales
- **Multiples**: "instala shopify y klaviyo" -> instalar ambos
- **Quitar**: "quita consensus" -> eliminar del .mcp.json
- **Listar**: "que mcps hay disponibles" -> mostrar catalogo resumido

Si la peticion es ambigua, preguntar. Si es clara, ejecutar directamente.

### Paso 2 — Leer estado actual

1. Leer `references/mcp-catalog.md` para obtener el JSON exacto de cada MCP.
2. Comprobar si existe `.mcp.json` en la raiz del proyecto actual.
   - Si existe: leerlo para hacer merge (no sobreescribir MCPs existentes).
   - Si no existe: crear uno nuevo.

### Paso 3 — Escribir .mcp.json

Construir el objeto JSON completo:

```json
{
  "mcpServers": {
    // MCPs existentes (si habia .mcp.json previo) +
    // MCPs nuevos del catalogo
  }
}
```

Reglas:
- El JSON debe ser valido y estar correctamente indentado (2 espacios).
- Si un MCP ya existe en el archivo, NO sobreescribirlo (el usuario puede
  haberlo personalizado). Avisar: "X ya esta configurado, lo dejo como esta."
- Si se pide quitar un MCP, eliminarlo del objeto y reescribir.
- Si el .mcp.json queda vacio (sin MCPs), eliminar el archivo.

### Paso 4 — Confirmar

Mostrar resumen breve:

```
MCPs instalados en .mcp.json:
- shopify (tienda Garza)
- klaviyo (email marketing)
- saleslayer-pim (catalogo PIM)

Reinicia Claude Code para que cargue los nuevos MCPs.
```

Si algun MCP requiere variables de entorno que el usuario podria no tener
configuradas, avisar:
```
shopify necesita: SHOPIFY_ACCESS_TOKEN, MYSHOPIFY_DOMAIN
```

## Operaciones especiales

### Listar MCPs disponibles

Si el usuario pregunta "que mcps hay" o "lista mcps", mostrar tabla resumida:

| MCP | Descripcion |
|-----|-------------|
| shopify | Tienda Shopify (pedidos, productos) |
| klaviyo | Email marketing |
| saleslayer-pim | Catalogo PIM Garza |
| asana | Gestion de tareas |
| microsoft-365 | Documentos Office |
| mermaid-mcp | Diagramas Mermaid |
| puppeteer | Navegacion web |
| consensus | Papers academicos |
| context7 | Docs de librerias |
| oracle-db | Oracle REPORTING |
| figma-remote-mcp | Disenos Figma |
| miro | Pizarras Miro |

**Bundles:** ecommerce, catalogo, estudio, documentacion, datos, diseno,
gestion, scraping, completo-garza.

### Ver MCPs instalados en proyecto actual

Leer `.mcp.json` del proyecto y mostrar que hay configurado.

### Migrar MCPs locales a .mcp.json

Si el usuario tiene MCPs configurados como "local scope" en `~/.claude.json`
(bajo `projects.<path>.mcpServers`), ofrecer migrarlos a `.mcp.json` para
que sean compartibles via git.

## Reglas

- NUNCA modificar `~/.claude.json`. Este skill solo toca `.mcp.json` del proyecto.
- NUNCA inventar configuraciones de MCPs. Solo usar las del catalogo.
- Si el usuario pide un MCP que no esta en el catalogo, decirlo y ofrecer
  anadirlo al catalogo si proporciona la configuracion.
- El `.mcp.json` va en la raiz del proyecto (junto a CLAUDE.md, .gitignore, etc).
