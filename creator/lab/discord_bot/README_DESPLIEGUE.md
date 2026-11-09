# ThunderMC · Fabio — despliegue seguro

## Qué contiene este ZIP

Todos los archivos están en la **raíz del archivo**. Se incluyen los tres puntos de entrada del bot (`main.py`, `bot.py` y `gateway_bot.py`), los JSON de configuración existentes, `requirements.txt`, este documento y `test_fabio.py` (pruebas locales sin conexión a Discord).

**No se incluyen** `.env`, `postulaciones_db.json`, `sorteos_db.json` ni ninguna otra base `*_db.json`. **No deben borrarse ni reemplazarse** en el servidor.

## Pasos en Pterodactyl (Linux)

1. **Detén el bot** desde el panel para evitar escrituras durante el despliegue.
2. Haz una **copia de seguridad externa** del `.env` y de todos los archivos `*_db.json`. Comprueba que puedes recuperarlos.
3. Sube el ZIP a la **carpeta raíz actual del servidor** y extráelo allí. Reemplaza los archivos de código/configuración incluidos; **no borres** otros archivos del servidor ni su contenido de datos.
4. Revisa las variables de entorno (en `.env` existente o en el panel):
   - `DISCORD_BOT_TOKEN` (obligatoria; nunca la publiques).
   - `DISCORD_CHANNEL_ID` (canal donde el bot generará invitaciones de un uso).
   - `DISCORD_GUILD_ID`, `DISCORD_APP_ID`, `ADMIN_CHANNEL_ID` (ya cuentan con valores existentes de ThunderMC, pero verifica que son correctos).
   - `REVIEWER_ROLE_IDS` (separa IDs por comas para autorizar revisores no administradores; en su ausencia **solo** pueden gestionar solicitudes los administradores con permiso real).
   - `ROLE_ID_STAFF`, `ROLE_ID_MEDIA`, `ROLE_ID_CONTRIBUIDOR` (IDs de roles para la incorporación). **Importante:** por seguridad la asignación automática mediante búsqueda por nombre está desactivada de forma predeterminada; si necesitas conservar la búsqueda antigua, configura explícitamente `ALLOW_ROLE_NAME_FALLBACK=1` y revisa los roles que pueda elegir. Se recomienda configurar los tres IDs.
5. Asegúrate de utilizar **Python 3.12**, instala las dependencias con `python3 -m pip install -r requirements.txt` y arranca con `python3 main.py` (también funcionan `bot.py` o `gateway_bot.py`).
6. Comprueba los registros y realiza pruebas controladas de normativa, postulación, decisión administrativa, firma por DM y sorteos.

## Pruebas locales

Ejecuta desde la raíz del bot: `python3 -m unittest -v test_fabio`.

Los tests usan datos temporales y dobles de Discord: no modifican tus bases de datos de producción. No reemplazan una prueba de integración real con Discord, permisos, canales y roles de ThunderMC.

## Cambios destacados

- Autorización estricta para las acciones de administración (servidor, canal y permisos/roles).
- Validación conservadora de la estructura de las bases JSON; no se sobrescriben datos corruptos o con esquema inesperado.
- Escritura atómica con archivo temporal exclusivo y bloqueos asíncronos (para **una sola instancia del bot**).
- Confirmación temprana de interacciones de Discord y recuperación de mensajes de contrato cuando falla la edición por webhook.
- Prevención de firmas y registros de sorteo duplicados; protección de tokens en logs de errores.
- Reintentos HTTP más defensivos y actualización del contador de sorteos a partir del mensaje más reciente.

## Límites de la validación

El código se ha comprobado sintácticamente y con pruebas automáticas sin conexión. **No se ha ejecutado contra la API real de Discord ni tu entorno de Pterodactyl**; los permisos de servidor, el token, los IDs, las conexiones y las bases de datos actuales deben verificarse durante el despliegue. La base JSON implementa bloqueo **dentro de un único proceso**, por lo que no debes arrancar dos copias del bot a la vez.
