# Catalogo de MCPs disponibles

Configuraciones pre-validadas para inyectar en proyectos via `.mcp.json`.
Cada entrada incluye el JSON exacto listo para copiar al bloque `mcpServers`.

---

## MCPs individuales

### shopify
Gestion de tienda Shopify: pedidos, productos, colecciones, clientes, descuentos.
```json
"shopify": {
  "command": "npx",
  "args": ["-y", "shopify-mcp-server"],
  "env": {
    "SHOPIFY_ACCESS_TOKEN": "${SHOPIFY_ACCESS_TOKEN}",
    "MYSHOPIFY_DOMAIN": "${MYSHOPIFY_DOMAIN}"
  }
}
```

### klaviyo
Email marketing, automatizaciones, segmentos, metricas.
```json
"klaviyo": {
  "type": "http",
  "url": "https://mcp.klaviyo.com/mcp"
}
```

### saleslayer-pim
Catalogo PIM Garza: productos, variantes, pictogramas. Servidor custom local.
```json
"saleslayer-pim": {
  "type": "stdio",
  "command": "node",
  "args": ["${USERPROFILE}\\mcp-saleslayer\\index.js"],
  "env": {
    "SALESLAYER_CONN_ID": "${SALESLAYER_CONN_ID}"
  }
}
```

### asana
Gestion de tareas y proyectos: buscar, crear, actualizar tareas.
```json
"asana": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@roychri/mcp-server-asana"],
  "env": {
    "ASANA_ACCESS_TOKEN": "${ASANA_ACCESS_TOKEN}"
  }
}
```

### microsoft-365
Crear y editar documentos Office 365 (Word, Excel, PowerPoint, Teams).
```json
"microsoft-365": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@pnp/cli-microsoft365-mcp-server@latest"],
  "env": {
    "CLIMICROSOFT365_AUTO_OPEN_BROWSER_ON_LOGIN": "true"
  }
}
```

### mermaid-mcp
Generar diagramas Mermaid (flujos, arquitectura, ER, secuencia).
```json
"mermaid-mcp": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "mermaid-mcp-server"]
}
```

### puppeteer
Navegacion web programatica: screenshots, scraping, testing de UI.
```json
"puppeteer": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
}
```

### consensus
Busqueda de papers academicos con IA. Para investigacion y estudio.
```json
"consensus": {
  "type": "http",
  "url": "https://mcp.consensus.app/mcp"
}
```

### context7
Documentacion actualizada de librerias y frameworks. Consulta docs oficiales.
```json
"context7": {
  "type": "http",
  "url": "https://mcp.context7.com/mcp"
}
```

### oracle-db
Conexion a Oracle REPORTING (Imprex). Requiere SQLcl instalado.
```json
"oracle-db": {
  "command": "${ORACLE_SQLCL_PATH}",
  "args": ["-mcp", "${ORACLE_CONN_STRING}"]
}
```
> Variables de entorno necesarias:
> - `ORACLE_SQLCL_PATH`: ruta al binario SQLcl (macOS: `/opt/homebrew/Caskroom/sqlcl/.../sql`, Windows: `C:\sqlcl\sqlcl\bin\sql.exe`)
> - `ORACLE_CONN_STRING`: formato `user/pass@//host:port/service` (ej: `reporting/password@//172.16.62.4:1521/orcl`)

### canva-dev
Diseño con Canva: crear, editar y exportar diseños programaticamente.
```json
"canva-dev": {
  "command": "npx",
  "args": ["-y", "@canva/cli@latest", "mcp"]
}
```

### figma
Acceso a disenos en Figma (lectura de archivos, componentes, estilos).
```json
"figma-remote-mcp": {
  "type": "http",
  "url": "https://mcp.figma.com/mcp"
}
```

### miro
Pizarras colaborativas Miro (lectura y creacion de boards).
```json
"miro": {
  "type": "http",
  "url": "https://mcp.miro.com/"
}
```

### markitdown
Convertir archivos (PDF, Word, Excel, imagenes, audio) a Markdown. Util para digerir documentos.
```json
"markitdown": {
  "command": "npx",
  "args": ["-y", "@microsoft/markitdown-mcp"]
}
```
> Por Microsoft. No requiere API key.

### playwright
Automatizar navegadores web: testing, scraping, extraccion de datos via accessibility tree.
```json
"playwright": {
  "command": "npx",
  "args": ["-y", "@anthropic-ai/mcp-server-playwright"]
}
```
> Por Microsoft. Alternativa mas moderna a puppeteer. Requiere `npx playwright install chromium`.

### firecrawl
Extraccion avanzada de datos web: scraping, crawling, conversion a markdown.
```json
"firecrawl": {
  "command": "npx",
  "args": ["-y", "firecrawl-mcp"],
  "env": {
    "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"
  }
}
```
> Requiere API key de firecrawl.dev (tiene tier gratuito: 500 creditos/mes).

### google-trends-mcp
Acceso a Google Trends: tendencias de busqueda, comparativas entre terminos, estacionalidad y datos por region.
```json
"google-trends-mcp": {
  "command": "npx",
  "args": ["-y", "github:andrewlwn77/google-trends-mcp"]
}
```
> Verificar paquete npm exacto antes de instalar. Repo: `andrewlwn77/google-trends-mcp`.
> No requiere API key (usa la interfaz publica de Google Trends).

### mcp-shop-server
Busqueda de productos y precios en Amazon (.es, .de, .fr) y paginas de ofertas usando Playwright.
```json
"mcp-shop-server": {
  "command": "npx",
  "args": ["-y", "mcp-shop-server"]
}
```
> Verificar paquete npm exacto. Repo: `johan-perso/mcp-shop-server`.
> Requiere Playwright instalado: `npx playwright install chromium`. No requiere API key.

### perplexity
Busqueda web con IA, investigacion profunda y razonamiento. 4 herramientas: search, ask, research (deep), reason.
```json
"perplexity": {
  "command": "npx",
  "args": ["-y", "@perplexity-ai/mcp-server@latest"],
  "env": {
    "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"
  }
}
```
> Requiere `PERPLEXITY_API_KEY` (https://www.perplexity.ai/settings/api).
> **ATENCION: billing por llamada API** (separado de Perplexity Pro). Usar solo en proyectos que justifiquen el coste.
> Para busquedas web cotidianas, preferir brave-search (global, tier gratuito).

### supabase
Base de datos Supabase: gestionar tablas, ejecutar SQL, auth, storage, edge functions. API de management.
```json
"supabase": {
  "command": "npx",
  "args": ["-y", "@supabase/mcp-server-supabase@latest"],
  "env": {
    "SUPABASE_ACCESS_TOKEN": "${SUPABASE_ACCESS_TOKEN}"
  }
}
```
> Requiere `SUPABASE_ACCESS_TOKEN` (generar en https://supabase.com/dashboard/account/tokens).
> Gestiona todos tus proyectos Supabase — no necesita URL/anon-key por proyecto.

### notion
Acceso a Notion: buscar, leer y editar paginas y bases de datos. MCP oficial de Notion.
```json
"notion": {
  "command": "npx",
  "args": ["-y", "@notionhq/notion-mcp-server"],
  "env": {
    "OPENAPI_MCP_HEADERS": "{\"Authorization\":\"Bearer ${NOTION_TOKEN}\",\"Notion-Version\":\"2022-06-28\"}"
  }
}
```
> Requiere `NOTION_TOKEN` (crear integracion en https://www.notion.so/my-integrations).
> Las paginas/bases de datos deben compartirse con la integracion (menu "..." > Connections).

### obsidian
Acceso a vaults de Obsidian: leer, buscar y editar notas markdown.
```json
"obsidian": {
  "command": "npx",
  "args": ["-y", "@mauricio.wolff/mcp-obsidian"],
  "env": {
    "OBSIDIAN_VAULT_PATH": "${OBSIDIAN_VAULT_PATH}"
  }
}
```
> Requiere `OBSIDIAN_VAULT_PATH` con la ruta al vault. No requiere que Obsidian este abierto.

---

## Bundles (combinaciones frecuentes)

### ecommerce
Para proyectos de tienda online Garza (garza-ecommerce y similares).
**Incluye:** shopify + klaviyo + saleslayer-pim

### catalogo
Para proyectos de gestion de catalogo de producto.
**Incluye:** saleslayer-pim

### estudio
Para sesiones de master UNIR y aprendizaje tecnico.
**Incluye:** consensus + context7

### documentacion
Para proyectos de arquitectura tecnica y documentacion formal.
**Incluye:** mermaid-mcp + microsoft-365

### datos
Para proyectos que consultan Oracle REPORTING (Imprex/SAP).
**Incluye:** oracle-db

### diseno
Para proyectos con componente visual o colaborativo.
**Incluye:** figma-remote-mcp + miro + canva-dev

### gestion
Para sesiones de gestion de tareas.
**Incluye:** asana

### scraping
Para investigacion web y extraccion de datos.
**Incluye:** playwright + firecrawl + context7

### inteligencia-mercado
Para analisis de mercado, competencia y tendencias de consumo.
**Incluye:** google-trends-mcp + mcp-shop-server
> Se complementa con `consensus` (global) para papers academicos sobre segmentacion, pricing y mercado.

### completo-garza
Todo lo necesario para un proyecto integral Garza.
**Incluye:** shopify + klaviyo + saleslayer-pim + mermaid-mcp + asana + google-trends-mcp + mcp-shop-server
