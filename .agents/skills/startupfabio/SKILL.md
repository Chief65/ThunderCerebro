---
name: startupfabio
description: >-
  Skill del bot de Discord Fabio (ThunderMC) alojado en Vultam. Se activa con "fabio",
  "startupfabio", "bot fabio", "conéctate al bot", "actualiza el bot", "sube el bot".
  Al activarse, el agente se conecta por SFTP al contenedor Pterodactyl de Vultam donde
  corre gateway_bot.py y adopta el rol de Operador del Bot (despliegue, edición y backups).
---

# 🐸 StartupFabio — Operador del Bot Fabio (Vultam)

## 🔌 Conexión

| Campo | Valor |
|---|---|
| **Proveedor** | Vultam (Panel Pterodactyl) — nodo Miami |
| **Host** | `mia43.vultam.net` |
| **Puerto** | `2022` |
| **Usuario** | `3ag1zpt6.22e65b5a` |
| **Clave SSH** | `$env:USERPROFILE\.ssh\id_rsa` (registrada en Vultam → Account → SSH Keys como `Beacon-PC`) |
| **Raíz remota** | `/home/container` |
| **Runtime** | Python 3.12 · `websockets` vía `requirements.txt` · Startup file = `gateway_bot.py` |

### Listar raíz (verificación al activar)
```powershell
echo "ls -la" | sftp -i "$env:USERPROFILE\.ssh\id_rsa" -P 2022 -o BatchMode=yes 3ag1zpt6.22e65b5a@mia43.vultam.net
```
> PowerShell marca exit code 1 por el mensaje "Connected to..." en stderr. No es un error si aparece el listado.

### Subir un archivo (con backup previo)
```powershell
@"
rename gateway_bot.py gateway_bot.py.bak
put "C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot\gateway_bot.py" gateway_bot.py
"@ | sftp -i "$env:USERPROFILE\.ssh\id_rsa" -P 2022 -o BatchMode=yes 3ag1zpt6.22e65b5a@mia43.vultam.net
```
> Si ya existe un `.bak`, borrarlo antes (`rm gateway_bot.py.bak`) o usar sufijo con fecha.

### Descargar (backup de datos vivos)
```powershell
@"
get postulaciones_db.json
get sorteos_db.json
"@ | sftp -i "$env:USERPROFILE\.ssh\id_rsa" -P 2022 -o BatchMode=yes 3ag1zpt6.22e65b5a@mia43.vultam.net
```

---

## 🛡️ Reglas de Operación (Producción)

1. **Servicio en vivo**: tratar como producción. **Pedir confirmación explícita al Sr Ramos antes de subir, sobrescribir o borrar** cualquier archivo.
2. **Backup obligatorio**: antes de sobrescribir, renombrar a `.bak` en remoto.
3. **Validar antes de subir**: `python -m py_compile gateway_bot.py` en local.
4. **Datos vivos** (`postulaciones_db.json`, `sorteos_db.json`): el bot los escribe en caliente. **Nunca sobrescribirlos con el bot encendido**; solo descargarlos. Fuente de verdad = Vultam, no el PC.
5. **Reinicio**: sin API Key, el reinicio lo hace el Sr Ramos desde el panel (Console → Restart). Avisarle tras cada subida.
6. **Instancia única**: nunca ejecutar `INICIAR_BOT.bat` en local mientras Vultam está activo (doble sesión de Gateway con el mismo token).
7. **`.env`**: contiene el token del bot. No mostrar su contenido en el chat.

## 📁 Código fuente local
- Desarrollo: `creator/lab/discord_bot/`
- Paquete de despliegue: `creator/output/deploy_fabio_vultam/`
