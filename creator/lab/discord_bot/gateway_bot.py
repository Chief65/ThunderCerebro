#!/usr/bin/env python3
"""
ThunderMC · Bot "Fabio" — Cliente Gateway de Discord (v2).

Dependencias: solo librería estándar + ``websockets``.

Funcionalidades
---------------
* Postulaciones (Staff / Media / Contribuidor):
  términos → formulario → ficha en el canal de administración →
  aceptar (contrato por DM) / rechazar (motivo) / poner en revisión →
  el candidato firma o declina el contrato.
* Normativa efímera (menú ``select_reglas_normativa``).
* Sorteos (``sorteo_participar`` y ``sorteo_ver_estado``) con contador en vivo.

Punto de entrada: ``gateway_runner()`` (lo importan ``main.py`` / ``bot.py`` en Vultam).

Configuración (.env o variables de entorno)
-------------------------------------------
DISCORD_BOT_TOKEN      Obligatorio.
DISCORD_CHANNEL_ID     Canal donde se generan las invitaciones de un solo uso.
REVIEWER_ROLE_IDS      Opcional. IDs de rol (separados por comas) autorizados a
                       resolver postulaciones. Si está vacío, solo los usuarios
                       con permiso Administrador pueden resolverlas.
ROLE_ID_STAFF          Opcional. Rol a asignar al firmar el contrato. Si falta,
ROLE_ID_MEDIA          se busca por nombre (nunca roles con permiso de
ROLE_ID_CONTRIBUIDOR   Administrador ni roles gestionados por integraciones).
"""

from __future__ import annotations

import asyncio
import json
import logging
import math
import os
import random
import re
import shutil
import sys
import tempfile
import time
import urllib.error
import urllib.request
from contextlib import asynccontextmanager, suppress
from dataclasses import dataclass
from typing import Any, AsyncIterator, Awaitable, Callable, Optional
import hashlib
import io
import py_compile
import tempfile
import urllib.parse
import zipfile
from datetime import datetime, timezone

import websockets
from websockets.exceptions import ConnectionClosed, WebSocketException

log = logging.getLogger("fabio")

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_env_file(path: str) -> dict[str, str]:
    values: dict[str, str] = {}
    if not os.path.exists(path):
        return values
    with open(path, "r", encoding="utf-8-sig") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


_ENV = _load_env_file(os.path.join(BASE_DIR, ".env"))


def _setting(key: str, default: str = "") -> str:
    return (os.environ.get(key) or _ENV.get(key) or default).strip()


def _setting_ids(key: str) -> frozenset[str]:
    return frozenset(p.strip() for p in _setting(key).split(",") if p.strip().isdigit())


TOKEN = _setting("DISCORD_BOT_TOKEN")
INVITE_CHANNEL_ID = _setting("DISCORD_CHANNEL_ID")
APP_ID = _setting("DISCORD_APP_ID", "1552716487100342404")
GUILD_ID = _setting("DISCORD_GUILD_ID", "1552715004669726802")
ADMIN_CHANNEL_ID = _setting("ADMIN_CHANNEL_ID", "1568307337859436716")  # Canal privado postu-media
POSTULACIONES_THREAD_ID = _setting("POSTULACIONES_THREAD_ID", "1568202156090073101")
REVIEWER_ROLE_IDS = _setting_ids("REVIEWER_ROLE_IDS")

API_BASE = "https://discord.com/api/v10"
GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"
GATEWAY_QUERY = "/?v=10&encoding=json"
USER_AGENT = "DiscordBot (https://thundermc.es, 2.0.0)"
HTTP_TIMEOUT = 12
HTTP_INTERACTION_TIMEOUT = 2.5
HTTP_RETRIES = 4

FILE_POSTULACIONES = os.path.join(BASE_DIR, "postulaciones_db.json")
FILE_SORTEOS = os.path.join(BASE_DIR, "sorteos_db.json")
FILE_SORTEO_CFG = os.path.join(BASE_DIR, "sorteo_config.json")
RULE_FILES = {
    "reglas_generales": os.path.join(BASE_DIR, "reglas_generales.json"),
    "reglas_discord": os.path.join(BASE_DIR, "reglas_discord.json"),
}

ADMIN_PANEL_CHANNEL_ID = _setting("ADMIN_PANEL_CHANNEL_ID", "1569343101544300664")
DEPLOY_LOG_CHANNEL_ID = _setting("DEPLOY_LOG_CHANNEL_ID", "1569343103255716011")
RAMOS_USER_ID = _setting("RAMOS_USER_ID", "1339648422650839146")
DEFAULT_CURRENT_ZIP_MSG_ID = _setting("CURRENT_ZIP_MSG_ID", "1569344094554292364")
FILE_ADMIN_PANEL_STATE = os.path.join(BASE_DIR, "admin_panel_state.json")

PROTECTED_FILES = frozenset({
    ".env",
    "postulaciones_db.json",
    "sorteos_db.json",
    "admin_panel_state.json",
})

ALLOWED_EXTENSIONS = frozenset({
    ".py", ".json", ".txt", ".yml", ".yaml", ".md", ".sh", ".bat"
})

CORE_FILES_TO_PACK = [
    "gateway_bot.py",
    "main.py",
    "bot.py",
    "requirements.txt",
    "reglas_generales.json",
    "reglas_discord.json",
    "sorteo_config.json",
    "test_fabio.py",
    "README_DESPLIEGUE.md",
]

# =============================================================================
# CONSTANTES DE DISCORD
# =============================================================================

EPHEMERAL = 1 << 6
PERM_ADMINISTRATOR = 1 << 3
NO_MENTIONS: dict[str, Any] = {"parse": []}

EMBED_FIELD_MAX = 1024
EMBED_FIELDS_MAX = 25

# Códigos de cierre del Gateway que no deben reintentarse (token/intents inválidos).
FATAL_CLOSE_CODES = {4004, 4010, 4011, 4012, 4013, 4014}
# Códigos tras los que la sesión no puede reanudarse.
NON_RESUMABLE_CLOSE_CODES = {4007, 4009}


class IType:
    COMPONENT = 3
    MODAL_SUBMIT = 5


class Resp:
    CHANNEL_MESSAGE = 4
    DEFERRED_CHANNEL_MESSAGE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7
    MODAL = 9


class ButtonStyle:
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4


class Color:
    FORM = 16762880
    PENDING = 3447003
    REVIEWING = 10181046
    CONTRACT = 15844367
    SUCCESS = 3066993
    DANGER = 15158332
    NEUTRAL = 9807270


# =============================================================================
# CLIENTE HTTP (REST)
# =============================================================================


class DiscordAPIError(Exception):
    def __init__(self, method: str, path: str, status: int, payload: Any):
        self.status = status
        self.code = payload.get("code") if isinstance(payload, dict) else None
        # Los tokens de interacciones y webhooks van en la URL. Nunca registrarlos.
        safe_path = re.sub(r"(/interactions/\d+/)[^/]+(?=/callback)", r"\1[redactado]", path)
        safe_path = re.sub(r"(/webhooks/\d+/)[^/?]+", r"\1[redactado]", safe_path)
        # El cuerpo de error de Discord puede contener datos privados del usuario.
        detail = f" (código Discord {self.code})" if self.code is not None else ""
        super().__init__(f"{method} {safe_path} -> HTTP {status}{detail}")


def _decode_body(raw: bytes) -> Any:
    if not raw:
        return None
    text = raw.decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except ValueError:
        return text


def _http_request(method: str, url: str, body: Any, headers: dict[str, str], timeout: float) -> tuple[int, Any, dict[str, str]]:
    """Petición HTTP bloqueante. Se ejecuta siempre en un hilo (asyncio.to_thread)."""
    all_headers = {"User-Agent": USER_AGENT, **headers}
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        all_headers["Content-Type"] = "application/json; charset=utf-8"
    request = urllib.request.Request(url, data=data, headers=all_headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            return resp.status, _decode_body(resp.read()), {k.lower(): v for k, v in resp.headers.items()}
    except urllib.error.HTTPError as exc:
        hdrs = {k.lower(): v for k, v in exc.headers.items()} if exc.headers else {}
        return exc.code, _decode_body(exc.read()), hdrs


async def discord_request(method: str, path: str, body: Any = None, *, auth: bool = True) -> Any:
    """
    Llamada REST asíncrona con gestión de rate limit (429) y reintentos.
    Solo se reintentan errores de red / 5xx en métodos idempotentes para no
    duplicar mensajes.
    """
    url = API_BASE + path
    headers = {"Authorization": f"Bot {TOKEN}"} if auth else {}
    idempotent = method in {"GET", "PUT", "PATCH", "DELETE"}
    is_callback = path.startswith("/interactions/") and path.endswith("/callback")
    timeout = HTTP_INTERACTION_TIMEOUT if is_callback else HTTP_TIMEOUT

    for attempt in range(1, HTTP_RETRIES + 1):
        last_attempt = attempt == HTTP_RETRIES
        try:
            status, payload, resp_headers = await asyncio.to_thread(_http_request, method, url, body, headers, timeout)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if not idempotent or last_attempt:
                raise DiscordAPIError(method, path, 0, str(exc)) from exc
            await asyncio.sleep(min(2 ** attempt, 10))
            continue

        if status == 429 and is_callback:
            raise DiscordAPIError(method, path, status, payload)
        if status == 429 and not last_attempt:
            retry_after = None
            if isinstance(payload, dict):
                retry_after = payload.get("retry_after")
            if retry_after is None:
                retry_after = resp_headers.get("retry-after", 1)
            try:
                wait = float(retry_after)
                if not math.isfinite(wait):
                    raise ValueError("valor no finito")
            except (ValueError, TypeError):
                wait = 1.0
            wait = min(max(wait, 0.05) + 0.1, 60.0)
            # No poner tokens de interacción/webhook en registros.
            safe_path = re.sub(r"(/interactions/\d+/)[^/]+(?=/callback)", r"\1[redactado]", path)
            safe_path = re.sub(r"(/webhooks/\d+/)[^/?]+", r"\1[redactado]", safe_path)
            log.warning("Rate limit en %s %s: esperando %.2fs", method, safe_path, wait)
            await asyncio.sleep(wait)
            continue

        if status >= 500 and idempotent and not last_attempt:
            await asyncio.sleep(min(2 ** attempt, 10))
            continue

        if status >= 400:
            raise DiscordAPIError(method, path, status, payload)
        return payload

    raise DiscordAPIError(method, path, 0, "reintentos agotados")


def _http_multipart_request(
    method: str,
    url: str,
    payload_json: Optional[dict[str, Any]],
    files: Optional[list[tuple[str, str, bytes, str]]],
    headers: dict[str, str],
    timeout: float = 30.0,
) -> tuple[int, Any, dict[str, str]]:
    boundary = f"----ThunderBoundary{int(time.time() * 1000)}"
    all_headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        **headers,
    }
    parts: list[bytes] = []
    if payload_json is not None:
        if "allowed_mentions" not in payload_json:
            payload_json["allowed_mentions"] = NO_MENTIONS
        parts.append(
            f"--{boundary}\r\n".encode("utf-8")
            + b'Content-Disposition: form-data; name="payload_json"\r\n'
            + b"Content-Type: application/json; charset=utf-8\r\n\r\n"
            + json.dumps(payload_json, ensure_ascii=False).encode("utf-8")
            + b"\r\n"
        )
    if files:
        for field_name, filename, data_bytes, ctype in files:
            parts.append(
                f"--{boundary}\r\n".encode("utf-8")
                + f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'.encode("utf-8")
                + f"Content-Type: {ctype}\r\n\r\n".encode("utf-8")
                + data_bytes
                + b"\r\n"
            )
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    body_data = b"".join(parts)

    req = urllib.request.Request(url, data=body_data, headers=all_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, _decode_body(resp.read()), {k.lower(): v for k, v in resp.headers.items()}
    except urllib.error.HTTPError as exc:
        hdrs = {k.lower(): v for k, v in exc.headers.items()} if exc.headers else {}
        return exc.code, _decode_body(exc.read()), hdrs


async def discord_multipart_request(
    method: str,
    path: str,
    payload_json: Optional[dict[str, Any]] = None,
    files: Optional[list[tuple[str, str, bytes, str]]] = None,
    *,
    auth: bool = True,
) -> Any:
    url = API_BASE + path
    headers = {"Authorization": f"Bot {TOKEN}"} if auth else {}
    status, payload, _ = await asyncio.to_thread(_http_multipart_request, method, url, payload_json, files, headers)
    if status >= 400:
        raise DiscordAPIError(method, path, status, payload)
    return payload


async def add_reaction(channel_id: str, message_id: str, emoji: str) -> None:
    encoded = urllib.parse.quote(emoji)
    path = f"/channels/{channel_id}/messages/{message_id}/reactions/{encoded}/@me"
    try:
        await discord_request("PUT", path)
    except Exception as exc:
        log.warning("No se pudo agregar reaccion %s al mensaje %s: %s", emoji, message_id, exc)


async def remove_reaction(channel_id: str, message_id: str, emoji: str) -> None:
    encoded = urllib.parse.quote(emoji)
    path = f"/channels/{channel_id}/messages/{message_id}/reactions/{encoded}/@me"
    try:
        await discord_request("DELETE", path)
    except Exception as exc:
        log.warning("No se pudo eliminar reaccion %s del mensaje %s: %s", emoji, message_id, exc)


async def post_message(channel_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return await discord_request(
        "POST", f"/channels/{channel_id}/messages", {"allowed_mentions": NO_MENTIONS, **payload}
    )


async def edit_message(channel_id: str, message_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return await discord_request(
        "PATCH", f"/channels/{channel_id}/messages/{message_id}", {"allowed_mentions": NO_MENTIONS, **payload}
    )


async def send_dm(user_id: str, payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Envía un DM. Devuelve None si no se pudo entregar (DMs cerrados, usuario fuera, etc.)."""
    try:
        channel = await discord_request("POST", "/users/@me/channels", {"recipient_id": str(user_id)})
        return await post_message(channel["id"], payload)
    except (DiscordAPIError, KeyError, TypeError) as exc:
        log.warning("No se pudo enviar DM a %s: %s", user_id, exc)
        return None


async def notify_admins(content: str) -> bool:
    try:
        await post_message(ADMIN_CHANNEL_ID, {"content": content})
        return True
    except DiscordAPIError as exc:
        log.error("No se pudo publicar en el canal de administración: %s", exc)
        return False


# =============================================================================
# INTERACCIONES
# =============================================================================


def _message_data(
    content: Optional[str] = None,
    *,
    embeds: Optional[list[dict[str, Any]]] = None,
    components: Optional[list[dict[str, Any]]] = None,
    ephemeral: bool = False,
) -> dict[str, Any]:
    data: dict[str, Any] = {"allowed_mentions": NO_MENTIONS}
    if content is not None:
        data["content"] = content
    if embeds is not None:
        data["embeds"] = embeds
    if components is not None:
        data["components"] = components
    if ephemeral:
        data["flags"] = EPHEMERAL
    return data


class Interaction:
    """Envoltorio de un evento INTERACTION_CREATE con helpers de respuesta."""

    def __init__(self, raw: dict[str, Any]):
        self.raw = raw
        self.id: str = raw["id"]
        self.token: str = raw["token"]
        self.application_id: str = raw.get("application_id") or APP_ID
        self.type: int = raw.get("type", 0)
        self.data: dict[str, Any] = raw.get("data") or {}
        self.custom_id: str = self.data.get("custom_id", "")
        self.member: dict[str, Any] = raw.get("member") or {}
        self.guild_id: str = raw.get("guild_id") or ""
        user = self.member.get("user") or raw.get("user") or {}
        self.user_id: str = user.get("id", "")
        self.user_name: str = user.get("username", "desconocido")
        self.channel_id: str = raw.get("channel_id") or (raw.get("channel") or {}).get("id", "")
        self.message: dict[str, Any] = raw.get("message") or {}
        self.responded = False

    # --- Lectura de datos -----------------------------------------------------

    @property
    def selected_value(self) -> str:
        values = self.data.get("values") or [""]
        return values[0]

    def modal_values(self) -> dict[str, str]:
        out: dict[str, str] = {}
        for row in self.data.get("components", []):
            # Action Row (type 1) clásico o Label (type 18) de Components V2.
            children = row.get("components") or ([row["component"]] if "component" in row else [])
            for comp in children:
                cid = comp.get("custom_id")
                if cid:
                    out[cid] = (comp.get("value") or "").strip()
        return out

    # --- Respuestas -------------------------------------------------------------

    async def _callback(self, payload: dict[str, Any]) -> None:
        await discord_request("POST", f"/interactions/{self.id}/{self.token}/callback", payload, auth=False)
        self.responded = True

    async def reply(
        self,
        content: Optional[str] = None,
        *,
        embeds: Optional[list[dict[str, Any]]] = None,
        components: Optional[list[dict[str, Any]]] = None,
        ephemeral: bool = True,
    ) -> None:
        await self._callback(
            {
                "type": Resp.CHANNEL_MESSAGE,
                "data": _message_data(content, embeds=embeds, components=components, ephemeral=ephemeral),
            }
        )

    async def open_modal(self, modal: dict[str, Any]) -> None:
        await self._callback({"type": Resp.MODAL, "data": modal})

    async def defer(self, *, ephemeral: bool = True) -> None:
        await self._callback(
            {"type": Resp.DEFERRED_CHANNEL_MESSAGE, "data": {"flags": EPHEMERAL} if ephemeral else {}}
        )

    async def defer_update(self) -> None:
        await self._callback({"type": Resp.DEFERRED_UPDATE_MESSAGE})

    async def update_message(
        self,
        *,
        content: Optional[str] = None,
        embeds: Optional[list[dict[str, Any]]] = None,
        components: Optional[list[dict[str, Any]]] = None,
    ) -> None:
        await self._callback(
            {"type": Resp.UPDATE_MESSAGE, "data": _message_data(content, embeds=embeds, components=components)}
        )

    async def edit_original(self, payload: dict[str, Any]) -> None:
        await discord_request(
            "PATCH",
            f"/webhooks/{self.application_id}/{self.token}/messages/@original",
            {"allowed_mentions": NO_MENTIONS, **payload},
            auth=False,
        )

    async def followup(self, content: str, *, ephemeral: bool = True) -> None:
        await discord_request(
            "POST",
            f"/webhooks/{self.application_id}/{self.token}",
            _message_data(content, ephemeral=ephemeral),
            auth=False,
        )

    async def notify(self, content: str) -> None:
        """Mensaje efímero al usuario, tanto si ya se respondió como si no."""
        if self.responded:
            await self.followup(content)
        else:
            await self.reply(content)


Handler = Callable[[Interaction], Awaitable[None]]
_EXACT_ROUTES: dict[tuple[int, str], Handler] = {}
_PREFIX_ROUTES: list[tuple[int, str, Handler]] = []


def route(itype: int, custom_id: Optional[str] = None, *, prefix: Optional[str] = None) -> Callable[[Handler], Handler]:
    def decorator(func: Handler) -> Handler:
        if custom_id is not None:
            _EXACT_ROUTES[(itype, custom_id)] = func
        if prefix is not None:
            _PREFIX_ROUTES.append((itype, prefix, func))
        return func

    return decorator


def _find_handler(inter: Interaction) -> Optional[Handler]:
    handler = _EXACT_ROUTES.get((inter.type, inter.custom_id))
    if handler:
        return handler
    for itype, prefix, func in _PREFIX_ROUTES:
        if inter.type == itype and inter.custom_id.startswith(prefix):
            return func
    return None


async def dispatch_interaction(raw: dict[str, Any]) -> None:
    try:
        inter = Interaction(raw)
    except (KeyError, TypeError, AttributeError):
        # El payload contiene un token de un solo uso: no escribirlo en el log.
        log.error("Interacción malformada recibida (tipo=%s)", raw.get("type") if isinstance(raw, dict) else "?")
        return

    log.info(
        "Interaccion %s | tipo=%s | usuario=%s (%s) | canal=%s",
        inter.custom_id or "-", inter.type, inter.user_name, inter.user_id, inter.channel_id,
    )
    handler = _find_handler(inter)
    try:
        if handler is None:
            await inter.reply("⚠️ Esta acción ya no está disponible.")
            return
        await handler(inter)
    except StoreCorruptedError as exc:
        log.critical("%s", exc)
        with suppress(Exception):
            await inter.notify("❌ Error interno de datos. Avisa a un administrador.")
    except Exception:
        log.exception("Error no controlado procesando %s", inter.custom_id)
        with suppress(Exception):
            await inter.notify("❌ Se produjo un error inesperado. Inténtalo de nuevo más tarde.")


# =============================================================================
# PERSISTENCIA (JSON atómico con bloqueo)
# =============================================================================


class StoreCorruptedError(RuntimeError):
    pass


class JsonStore:
    """
    Archivo JSON con escrituras atómicas (tmp + os.replace) y lock asíncrono.
    Si el archivo está corrupto NO se sobrescribe: se hace copia y se lanza error.
    """

    def __init__(self, path: str, default: Callable[[], dict[str, Any]]):
        self.path = path
        self._default = default
        self._lock = asyncio.Lock()

    def _read(self) -> dict[str, Any]:
        if not os.path.exists(self.path):
            return self._default()
        try:
            with open(self.path, "r", encoding="utf-8-sig") as fh:
                data = json.load(fh)
            if not isinstance(data, dict):
                raise ValueError("la raíz no es un objeto JSON")
            return data
        except (ValueError, OSError, UnicodeError) as exc:
            backup = f"{self.path}.corrupt-{int(time.time())}"
            backup_ok = False
            with suppress(OSError):
                shutil.copy2(self.path, backup)
                backup_ok = True
            suffix = f". Copia guardada en {backup}" if backup_ok else ". No se pudo crear una copia"
            raise StoreCorruptedError(
                f"{os.path.basename(self.path)} ilegible ({exc}){suffix}"
            ) from exc

    def _write(self, data: dict[str, Any]) -> None:
        # Archivo temporal único, en el mismo sistema de archivos, con permisos privados.
        directory = os.path.dirname(self.path) or "."
        name = os.path.basename(self.path)
        fd, tmp = tempfile.mkstemp(prefix=f".{name}.", suffix=".tmp", dir=directory)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2, ensure_ascii=False)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, self.path)
        finally:
            with suppress(FileNotFoundError):
                os.unlink(tmp)

    async def read(self) -> dict[str, Any]:
        async with self._lock:
            return await asyncio.to_thread(self._read)

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[dict[str, Any]]:
        """Transacción serializada dentro de una instancia del bot; nunca sobrescribe en fallo."""
        async with self._lock:
            data = await asyncio.to_thread(self._read)
            yield data
            await asyncio.to_thread(self._write, data)


STORE_POSTULACIONES = JsonStore(FILE_POSTULACIONES, lambda: {"counter": 100, "applications": {}})
STORE_SORTEOS = JsonStore(FILE_SORTEOS, lambda: {"entries": []})


# =============================================================================
# UTILIDADES
# =============================================================================


def _truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _field_value(text: str) -> str:
    text = (text or "").strip()
    return _truncate(text, EMBED_FIELD_MAX) if text else "No indicado"


def _quote(text: str) -> str:
    """Convierte un texto multilínea en cita de Markdown (cada línea con '> ')."""
    return "\n".join(f"> {line}" if line.strip() else ">" for line in text.splitlines()) or "> -"


def _button(label: str, custom_id: str, style: int, *, emoji: Optional[str] = None, disabled: bool = False) -> dict[str, Any]:
    btn: dict[str, Any] = {"type": 2, "style": style, "label": label, "custom_id": custom_id}
    if emoji:
        btn["emoji"] = {"name": emoji}
    if disabled:
        btn["disabled"] = True
    return btn


def _row(*components: dict[str, Any]) -> dict[str, Any]:
    return {"type": 1, "components": list(components)}


def _is_reviewer(inter: Interaction) -> bool:
    """Se exige el canal y servidor correctos MÁS permisos; visibilidad no es autorización."""
    if inter.channel_id != ADMIN_CHANNEL_ID or inter.guild_id != GUILD_ID:
        return False
    try:
        perms = int(inter.member.get("permissions") or 0)
    except (TypeError, ValueError):
        perms = 0
    if perms & PERM_ADMINISTRATOR:
        return True
    # Por defecto solo administradores. Otros revisores necesitan roles explícitos.
    return bool(REVIEWER_ROLE_IDS and REVIEWER_ROLE_IDS.intersection(inter.member.get("roles") or []))


async def _require_reviewer(inter: Interaction) -> bool:
    if _is_reviewer(inter):
        return True
    log.warning("Acción de administración denegada a %s (%s)", inter.user_name, inter.user_id)
    await inter.reply("⛔ No tienes permisos para gestionar postulaciones.")
    return False


# =============================================================================
# POSTULACIONES — MODELO
# =============================================================================


class Status:
    PENDING = "En revision"
    REVIEWING = "En revision activa"
    CONTRACT_SENT = "Contrato Enviado"
    SIGNED = "Aceptado y Firmado"
    DECLINED = "Contrato Declinado"
    REJECTED = "Rechazada"


ACTIVE_STATUSES = {Status.PENDING, Status.REVIEWING, Status.CONTRACT_SENT}
REVIEWABLE_STATUSES = {Status.PENDING, Status.REVIEWING}

STATUS_LABEL = {
    Status.PENDING: "🟡 En revisión",
    Status.REVIEWING: "🔍 En revisión activa",
    Status.CONTRACT_SENT: "📨 Contrato enviado",
    Status.SIGNED: "✅ Aceptado y firmado",
    Status.DECLINED: "↩️ Contrato declinado",
    Status.REJECTED: "❌ Rechazada",
}

STATUS_COLOR = {
    Status.PENDING: Color.PENDING,
    Status.REVIEWING: Color.REVIEWING,
    Status.CONTRACT_SENT: Color.CONTRACT,
    Status.SIGNED: Color.SUCCESS,
    Status.DECLINED: Color.NEUTRAL,
    Status.REJECTED: Color.DANGER,
}


@dataclass(frozen=True)
class FormField:
    custom_id: str
    label: str
    summary: str
    placeholder: str
    paragraph: bool = False
    min_length: Optional[int] = None
    max_length: int = 200
    required: bool = True

    def component(self) -> dict[str, Any]:
        comp: dict[str, Any] = {
            "type": 4,
            "custom_id": self.custom_id,
            "label": self.label,
            "style": 2 if self.paragraph else 1,
            "placeholder": self.placeholder,
            "max_length": self.max_length,
            "required": self.required,
        }
        if self.min_length:
            comp["min_length"] = self.min_length
        return _row(comp)


@dataclass(frozen=True)
class Category:
    key: str
    name: str
    display: str
    emoji: str
    requirements: str
    modal_id: str
    modal_title: str
    role_env: str
    role_keywords: tuple[str, ...]
    fields: tuple[FormField, ...]

    def modal(self) -> dict[str, Any]:
        return {
            "custom_id": self.modal_id,
            "title": self.modal_title,
            "components": [f.component() for f in self.fields],
        }


CATEGORIES: dict[str, Category] = {
    c.key: c
    for c in (
        Category(
            key="postulacion_staff",
            name="Staff / Moderación",
            display="Staff / Moderación",
            emoji="🛡️",
            requirements=(
                "`✅` Edad mínima requerida: **16 años** cumplidos.\n"
                "`✅` Micrófono funcional y presencia activa en Discord y Minecraft.\n"
                "`✅` Cero historial de sanciones graves o toxicidad en la red.\n"
                "`✅` Madurez, objetividad y respeto estricto del criterio del staff."
            ),
            modal_id="modal_submit_staff",
            modal_title="Postulación Staff | ThunderMC",
            role_env="ROLE_ID_STAFF",
            role_keywords=("staff",),
            fields=(
                FormField("field_nombre_real", "Nombre Real", "👤 Nombre Real",
                          "Tu nombre y apellido real", min_length=2, max_length=80),
                FormField("field_nick_edad", "Nick de Minecraft y Edad (Mínimo 16)", "🎮 Nick & Edad",
                          "Ej: Steve_Thunder | 17 años", min_length=3, max_length=60),
                FormField("field_pais", "País de Nacimiento", "🌎 País",
                          "Ej: España, México, Colombia, Argentina, Chile...", min_length=2, max_length=50),
                FormField("field_horas_exp", "Horas Jugadas y Experiencia como Staff", "⏱️ Horas Jugadas & Experiencia",
                          "Horas en el servidor y detalles de servidores previos donde fuiste staff...",
                          paragraph=True, min_length=10, max_length=1000),
                FormField("field_motivo", "¿Por qué quieres ser Staff en ThunderMC?", "💡 ¿Por qué quiere ser Staff?",
                          "¿Qué cualidades aportarías y qué te motiva a unirte a nuestro equipo?",
                          paragraph=True, min_length=15, max_length=1000),
            ),
        ),
        Category(
            key="postulacion_media",
            name="Media / Creador de Contenido",
            display="Media / Creador",
            emoji="🎥",
            requirements=(
                "`✅` Canales activos en Twitch, YouTube o TikTok.\n"
                "`✅` Compromiso para realizar directos o vídeos recurrentes en ThunderMC.\n"
                "`✅` Contenido respetuoso acorde a la imagen de marca de la network.\n"
                "`✅` Comunidad afín a Minecraft y videojuegos."
            ),
            modal_id="modal_submit_media",
            modal_title="Postulación Media | ThunderMC",
            role_env="ROLE_ID_MEDIA",
            role_keywords=("media", "creador"),
            fields=(
                FormField("field_nombre_nick", "Nombre Real y Nick de Minecraft", "👤 Nombre & Nick",
                          "Ej: Carlos Gómez / CarlosGamer99", min_length=3, max_length=80),
                FormField("field_pais_edad", "País de Nacimiento y Edad (Mínimo 16)", "🌎 País & Edad",
                          "Ej: México | 18 años", min_length=3, max_length=50),
                FormField("field_twitch", "Enlace de Twitch", "🟣 Twitch",
                          "https://twitch.tv/tu_canal (o Deja vacío si no tienes)", required=False),
                FormField("field_youtube", "Enlace de YouTube", "🔴 YouTube",
                          "https://youtube.com/@tu_canal (o Deja vacío si no tienes)", required=False),
                FormField("field_tiktok", "Enlace de TikTok u otras redes", "⚫ TikTok",
                          "https://tiktok.com/@tu_usuario (o Deja vacío si no tienes)", required=False),
            ),
        ),
        Category(
            key="postulacion_contribuidor",
            name="Contribuidor Oficial",
            display="Contribuidor Oficial",
            emoji="🛠️",
            requirements=(
                "`✅` Especialidades: Donación, Diseñador Gráfico, Builder o Developer.\n"
                "`✅` Portafolio o demostración tangible de trabajos previos.\n"
                "`✅` Capacidad para trabajar en equipo y cumplir plazos fijados.\n"
                "`✅` Compromiso con los estándares de calidad de ThunderMC."
            ),
            modal_id="modal_submit_contribuidor",
            modal_title="Postulación Contribuidor | ThunderMC",
            role_env="ROLE_ID_CONTRIBUIDOR",
            role_keywords=("contribuidor", "builder", "dev"),
            fields=(
                FormField("field_nombre_nick", "Nombre Real y Nick de Minecraft", "👤 Nombre & Nick",
                          "Ej: Alejandro / AlexDev", min_length=3, max_length=80),
                FormField("field_pais_edad", "País de Nacimiento y Edad", "🌎 País & Edad",
                          "Ej: España | 19 años", min_length=3, max_length=50),
                FormField("field_rol_contribucion", "Área (Donación, Diseñador, Builder, Dev)", "🛠️ Área Solicitada",
                          "Donación Monetaria, Diseñador Gráfico, Builder, Developer...", min_length=3, max_length=80),
                FormField("field_portafolio", "Experiencia y Portafolio / Enlaces de trabajo", "📁 Portafolio / Experiencia",
                          "Indica enlaces a proyectos, Behance, GitHub, capturas de builds, etc...",
                          paragraph=True, min_length=10, max_length=1000),
                FormField("field_propuesta", "Propuesta de colaboración y disponibilidad", "📝 Propuesta & Disponibilidad",
                          "¿En qué área te gustaría apoyar al servidor y cuántas horas puedes aportar?",
                          paragraph=True, min_length=10, max_length=1000),
            ),
        ),
    )
}
CATEGORY_BY_MODAL = {c.modal_id: c for c in CATEGORIES.values()}
CATEGORY_BY_DISPLAY = {c.display: c for c in CATEGORIES.values()}


def _normalize_db(db: dict[str, Any]) -> dict[str, Any]:
    """Completa únicamente claves ausentes. Nunca destruye datos de producción inválidos."""
    if "counter" not in db:
        db["counter"] = 100
    try:
        counter = int(db["counter"])
        if counter < 0:
            raise ValueError("contador negativo")
    except (TypeError, ValueError) as exc:
        raise StoreCorruptedError("postulaciones_db.json contiene un contador inválido") from exc
    db["counter"] = counter
    if "applications" not in db:
        db["applications"] = {}
    if not isinstance(db["applications"], dict) or any(
        not isinstance(value, dict) for value in db["applications"].values()
    ):
        raise StoreCorruptedError("postulaciones_db.json contiene postulaciones inválidas; no se modificará")
    return db


def _normalize_sorteos(db: dict[str, Any]) -> dict[str, Any]:
    if "entries" not in db:
        db["entries"] = []
    if not isinstance(db["entries"], list) or any(
        not isinstance(entry, dict) for entry in db["entries"]
    ):
        raise StoreCorruptedError("sorteos_db.json contiene participaciones inválidas; no se modificará")
    return db


def _category_of(app: dict[str, Any]) -> Optional[Category]:
    """Compatibilidad con fichas antiguas (sin campo 'categoria')."""
    return CATEGORIES.get(app.get("categoria", "")) or CATEGORY_BY_DISPLAY.get(app.get("tipo", ""))


def _active_application(db: dict[str, Any], user_id: str) -> Optional[dict[str, Any]]:
    for app in db["applications"].values():
        if app.get("user_id") == user_id and app.get("status") in ACTIVE_STATUSES and _category_of(app):
            return app
    return None


def _already_active_message(app: dict[str, Any]) -> str:
    return (
        f"⏳ Ya tienes una postulación en curso (`{app['id']}` · {app.get('tipo')} · "
        f"estado: **{STATUS_LABEL.get(app.get('status'), app.get('status'))}**).\n"
        "Espera a su resolución antes de enviar otra."
    )


def _transition_error(app: Optional[dict[str, Any]], post_id: str, allowed: set[str]) -> Optional[str]:
    if not app:
        return f"❌ No se encontró la postulación `{post_id}` en la base de datos."
    if not _category_of(app):
        return f"❌ La ficha `{post_id}` no es una postulación válida."
    if app.get("status") not in allowed:
        label = STATUS_LABEL.get(app.get("status"), app.get("status"))
        return f"ℹ️ La postulación `{post_id}` ya fue procesada (estado actual: **{label}**)."
    return None


# =============================================================================
# POSTULACIONES — EMBEDS
# =============================================================================


def build_terms_embed(cat: Category) -> dict[str, Any]:
    return {
        "title": f"{cat.emoji} Términos, Requisitos & Seguridad | {cat.name}",
        "description": (
            f"Has iniciado el proceso de postulación para el área de **{cat.name}**.\n"
            "-# ʟᴇᴇ ᴄᴏɴ ᴀᴛᴇɴᴄɪᴏ́ɴ ʟᴀꜱ ꜱɪɢᴜɪᴇɴᴛᴇꜱ ᴄᴏɴᴅɪᴄɪᴏɴᴇꜱ ᴀɴᴛᴇꜱ ᴅᴇ ᴄᴏɴᴛɪɴᴜᴀʀ\n\n"
            "**Requisitos Indispensables:**\n"
            f"{cat.requirements}\n\n"
            "**🔒 Cláusula de Seguridad y Protección de Datos:**\n"
            "> La información aportada será tratada de manera estrictamente confidencial y exclusivamente por la directiva de ThunderMC.\n"
            "> Al continuar, declaras formalmente que todos los datos suministrados son reales y verídicos. Falsear edad, nick o experiencia supondrá la **expulsión inmediata y veto permanente** de cualquier convocatoria futura.\n\n"
            "**⏱️ Tiempos de Evaluación:**\n"
            "> Tras enviar el formulario, el equipo revisará tu ficha. Recibirás respuesta por mensaje directo (DM) en un plazo estimado de hasta **3 días hábiles**."
        ),
        "color": Color.FORM,
        "footer": {"text": "ThunderMC Convocatorias • Pulsa el botón inferior para abrir tu formulario"},
    }


def build_receipt_embed(app: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": "📨 Postulación Recibida | ThunderMC",
        "description": (
            f"Hola **{app['username']}**, hemos recibido con éxito tu solicitud para el área de **{app['tipo']}**.\n\n"
            "**Información de tu expediente:**\n"
            f"> `📌` **ID de Solicitud:** `{app['id']}`\n"
            "> `⏳` **Estado:** `🟡 En revisión` *(puede tardar hasta 3d en obtener una respuesta)*\n"
            f"> `📅` **Fecha de Envío:** <t:{app['submitted_at']}:F>\n\n"
            "Nuestro equipo directivo analizará tu perfil. Te mantendremos informado en este mismo chat privado en cuanto se emita una resolución."
        ),
        "color": Color.FORM,
        "footer": {"text": "ThunderMC Network • Sistema Oficial de Selección"},
    }


def _status_line(app: dict[str, Any]) -> str:
    status = app.get("status", Status.PENDING)
    label = f"`{STATUS_LABEL.get(status, status)}`"
    reviewer = app.get("reviewer_id")
    if reviewer and status in {Status.REVIEWING, Status.CONTRACT_SENT, Status.REJECTED}:
        label += f" por <@{reviewer}>"
    return label


def _admin_components(app: dict[str, Any]) -> list[dict[str, Any]]:
    status = app.get("status")
    pid = app["id"]
    if status in REVIEWABLE_STATUSES:
        reviewing = status == Status.REVIEWING
        return [
            _row(
                _button("Aceptar Postulación", f"admin_accept_{pid}", ButtonStyle.SUCCESS, emoji="✅"),
                _button("Rechazar Postulación", f"admin_reject_{pid}", ButtonStyle.DANGER, emoji="❌"),
                _button("En Revisión" if reviewing else "Poner en Revisión", f"admin_review_{pid}",
                        ButtonStyle.SECONDARY, emoji="🔍", disabled=reviewing),
            )
        ]
    if status == Status.CONTRACT_SENT:
        return [_row(_button("Contrato Enviado (Esperando Firma)", f"noop_contract_{pid}",
                             ButtonStyle.SUCCESS, disabled=True))]
    return []


def build_admin_message(app: dict[str, Any]) -> dict[str, Any]:
    ts = app["submitted_at"]
    description = (
        f"**Candidato:** <@{app['user_id']}> (`{app['username']}`)\n"
        f"**ID de Usuario:** `{app['user_id']}`\n"
        f"**Fecha:** <t:{ts}:F> (<t:{ts}:R>)\n"
        f"**Estado:** {_status_line(app)}\n"
    )
    if app.get("dm_ok") is False:
        description += "**⚠️ Aviso:** no se pudo entregar el comprobante por DM (DMs cerrados).\n"
    description += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    fields = list(app.get("resumen_fields") or [])
    if app.get("status") == Status.REJECTED and app.get("reject_reason"):
        fields.append({"name": "📋 Motivo del rechazo", "value": _field_value(app["reject_reason"]), "inline": False})

    embed = {
        "title": f"📥 Nueva Postulación: {app['tipo']} | {app['id']}",
        "description": description,
        "fields": fields[:EMBED_FIELDS_MAX],
        "color": STATUS_COLOR.get(app.get("status"), Color.PENDING),
        "footer": {"text": f"ThunderMC Admin Panel • Ref: {app['id']}"},
    }
    return {"embeds": [embed], "components": _admin_components(app)}


async def refresh_admin_message(app: dict[str, Any]) -> None:
    msg_id = app.get("admin_msg_id")
    if not msg_id:
        return
    try:
        await edit_message(ADMIN_CHANNEL_ID, msg_id, build_admin_message(app))
    except DiscordAPIError as exc:
        log.warning("No se pudo actualizar la ficha %s en el canal admin: %s", app.get("id"), exc)


async def refresh_admin_current(post_id: str) -> None:
    """Siempre lee la última versión, nunca reintroduce botones desde una ficha obsoleta."""
    app = _normalize_db(await STORE_POSTULACIONES.read())["applications"].get(post_id)
    if app:
        await refresh_admin_message(app)


def build_contract_payload(app: dict[str, Any]) -> dict[str, Any]:
    pid = app["id"]
    embed = {
        "title": "📜 CONTRATO OFICIAL DE INCORPORACIÓN | THUNDERMC",
        "description": (
            f"Estimado/a **{app['username']}**,\n\n"
            f"Nos complace comunicarte que tu solicitud para formar parte del equipo de **{app['tipo']}** ha sido **APROBADA** por la directiva de ThunderMC.\n\n"
            "Para formalizar tu incorporación y activar tus accesos oficiales, es requisito indispensable leer y aceptar las siguientes cláusulas contractuales:"
        ),
        "color": Color.SUCCESS,
        "fields": [
            {
                "name": "⚖️ Cláusula 1: Compromiso, Conducta y Confidencialidad",
                "value": (
                    "> • Cumplir y hacer cumplir la normativa de ThunderMC sin favoritismos.\n"
                    "> • Absoluta confidencialidad respecto a canales internos, directrices y herramientas del equipo.\n"
                    "> • Trato impecable, respetuoso y profesional hacia todos los jugadores de la comunidad."
                ),
                "inline": False,
            },
            {
                "name": "🎁 Cláusula 2: Recompensas y Beneficios por tu Contribución",
                "value": (
                    "> `⭐` **Rango y Rol Exclusivo:** Asignación inmediata del rango correspondiente en Discord y Minecraft.\n"
                    "> `🗝️` **Beneficios In-Game Mensuales:** Paquete de llaves exclusivas, perks cosméticos y pase de temporada.\n"
                    "> `💎` **Comisiones & Tienda:** Para Media y Desarrolladores, porcentaje de comisiones y código de creador oficial en la tienda Tebex.\n"
                    "> `🏛️` **Voz y Voto:** Acceso directo a las reuniones de coordinación y planificación estratégica de la network."
                ),
                "inline": False,
            },
            {
                "name": "📌 Cláusula 3: Periodo de Prueba",
                "value": "> Tu incorporación contará con un periodo de adaptación supervisado por directores para garantizar tu correcta integración al flujo de trabajo.",
                "inline": False,
            },
        ],
        "footer": {"text": f"ThunderMC Team • Contrato ID: {pid} • Pulsa el botón inferior para firmar"},
    }
    buttons = _row(
        _button("✍️ Firmar y Aceptar Contrato", f"user_sign_contract_{pid}", ButtonStyle.SUCCESS),
        _button("Declinar Propuesta", f"user_decline_contract_{pid}", ButtonStyle.DANGER),
    )
    return {"embeds": [embed], "components": [buttons]}


def build_welcome_embed(app: dict[str, Any], invite: Optional[str]) -> dict[str, Any]:
    if invite:
        invite_block = f"**🔗 Tu invitación privada y exclusiva (de un solo uso, caduca en 24 h):**\n> {invite}\n\n"
    else:
        invite_block = (
            "**🔗 Invitación privada:**\n"
            "> ⚠️ No se pudo generar automáticamente. Un administrador te la enviará en breve.\n\n"
        )
    return {
        "title": "🎉 ¡Felicidades! Ahora eres parte del Team Thunder",
        "description": (
            "**¡Tu contrato ha quedado formalmente firmado y registrado!**\n\n"
            f"Te damos la bienvenida al equipo oficial de ThunderMC como **{app['tipo']}**.\n\n"
            f"{invite_block}"
            "**Próximos Pasos:**\n"
            "`1️⃣` Accede al Discord mediante el enlace proporcionado.\n"
            "`2️⃣` Dirígete al canal de coordinación interna para sincronizarte con el resto del equipo.\n"
            "`3️⃣` ¡Mucho éxito en esta nueva etapa junto a la familia Thunder!"
        ),
        "color": Color.SUCCESS,
        "footer": {"text": "ThunderMC Network • ¡Bienvenid@ al Equipo!"},
    }


def build_declined_embed(app: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": "↩️ Propuesta Declinada | ThunderMC",
        "description": (
            f"Has declinado la propuesta de incorporación como **{app['tipo']}** (ID `{app['id']}`).\n\n"
            "Gracias por tu tiempo e interés; la directiva ha sido notificada. "
            "Las puertas de ThunderMC siguen abiertas para futuras convocatorias."
        ),
        "color": Color.NEUTRAL,
        "footer": {"text": "ThunderMC Network • Gracias por tu interés en formar parte del proyecto"},
    }


def build_reject_embed(app: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "title": "Resolución de tu Postulación | ThunderMC",
        "description": (
            f"Estimado/a **{app['username']}**,\n\n"
            f"Queremos agradecerte sinceramente el tiempo, interés y entusiasmo dedicado al postularte para el área de **{app['tipo']}** en ThunderMC.\n\n"
            "Tras revisar minuciosamente tu perfil, lamentamos informarte de que en esta ocasión **tu solicitud no ha sido seleccionada**.\n\n"
            "**📋 Motivo de la Decisión:**\n"
            f"{_quote(reason)}\n\n"
            "**🌱 Futuras Convocatorias:**\n"
            "Nuestros procesos de selección son altamente competitivos y rigurosos. Te animamos a continuar disfrutando de la comunidad de ThunderMC y a presentar tu candidatura en futuras aperturas tras acumular mayor experiencia."
        ),
        "color": Color.DANGER,
        "footer": {"text": "ThunderMC Network • Gracias por tu interés en formar parte del proyecto"},
    }


# =============================================================================
# POSTULACIONES — ACCIONES DE SERVIDOR (rol / invitación)
# =============================================================================


def _match_role(roles: list[dict[str, Any]], keywords: tuple[str, ...]) -> Optional[dict[str, Any]]:
    candidates = []
    for role in roles:
        if role.get("id") == GUILD_ID or role.get("managed"):
            continue
        try:
            perms = int(role.get("permissions") or 0)
        except (TypeError, ValueError):
            perms = 0
        # Nunca autodetectar roles con permisos de gestión sensibles.
        dangerous = (
            PERM_ADMINISTRATOR | (1 << 2) | (1 << 4) | (1 << 5) | (1 << 28)
            | (1 << 29) | (1 << 30) | (1 << 31) | (1 << 34) | (1 << 36)
        )
        if perms & dangerous:
            continue
        name = (role.get("name") or "").lower()
        if any(k in name for k in keywords):
            candidates.append(role)
    # El de menor posición suele ser el menos privilegiado, pero no es garantía.
    candidates.sort(key=lambda r: r.get("position", 0))
    return candidates[0] if candidates else None


async def assign_category_role(cat: Category, user_id: str) -> tuple[bool, str]:
    """Devuelve (asignado, descripción) para informar a la administración."""
    role_id = _setting(cat.role_env)
    try:
        if not role_id:
            if _setting("ALLOW_ROLE_NAME_FALLBACK").lower() not in {"1", "true", "yes"}:
                return False, f"configura `{cat.role_env}` con un ID de rol explícito"
            roles = await discord_request("GET", f"/guilds/{GUILD_ID}/roles")
            role = _match_role(roles if isinstance(roles, list) else [], cat.role_keywords)
            if not role:
                return False, f"no hay rol configurado (`{cat.role_env}`) ni coincidencia segura"
            role_id = str(role["id"])
        if not role_id.isdecimal():
            return False, f"ID inválido en `{cat.role_env}`"
        await discord_request("PUT", f"/guilds/{GUILD_ID}/members/{user_id}/roles/{role_id}")
        return True, f"<@&{role_id}>"
    except DiscordAPIError as exc:
        log.warning("No se pudo asignar rol a %s: %s", user_id, exc)
        return False, f"error de Discord (HTTP {exc.status})"


async def create_single_use_invite() -> Optional[str]:
    if not INVITE_CHANNEL_ID:
        log.warning("DISCORD_CHANNEL_ID no configurado: no se pueden crear invitaciones.")
        return None
    try:
        res = await discord_request(
            "POST", f"/channels/{INVITE_CHANNEL_ID}/invites", {"max_age": 86400, "max_uses": 1, "unique": True}
        )
        return f"https://discord.gg/{res['code']}"
    except (DiscordAPIError, KeyError, TypeError) as exc:
        log.error("No se pudo crear la invitación: %s", exc)
        return None


# =============================================================================
# POSTULACIONES — HANDLERS
# =============================================================================


@route(IType.COMPONENT, "select_postulacion_tipo")
async def on_select_postulacion(inter: Interaction) -> None:
    cat = CATEGORIES.get(inter.selected_value)
    if not cat:
        await inter.reply("⚠️ Tipo de postulación no reconocido.")
        return
    active = _active_application(_normalize_db(await STORE_POSTULACIONES.read()), inter.user_id)
    if active:
        await inter.reply(_already_active_message(active))
        return
    await inter.reply(
        embeds=[build_terms_embed(cat)],
        components=[_row(_button("Acepto los Términos y Requisitos", f"btn_accept_terms_{cat.key}",
                                 ButtonStyle.SUCCESS, emoji="✅"))],
    )


@route(IType.COMPONENT, prefix="btn_accept_terms_")
async def on_accept_terms(inter: Interaction) -> None:
    cat = CATEGORIES.get(inter.custom_id[len("btn_accept_terms_"):])
    if not cat:
        await inter.reply("⚠️ Tipo de postulación no reconocido.")
        return
    active = _active_application(_normalize_db(await STORE_POSTULACIONES.read()), inter.user_id)
    if active:
        await inter.reply(_already_active_message(active))
        return
    await inter.open_modal(cat.modal())


async def on_submit_postulacion(inter: Interaction) -> None:
    cat = CATEGORY_BY_MODAL[inter.custom_id]
    raw_values = inter.modal_values()
    values = {f.custom_id: str(raw_values.get(f.custom_id, "")).strip() for f in cat.fields}
    invalid = [
        f.label for f in cat.fields
        if len(values[f.custom_id]) > f.max_length
        or (f.required and len(values[f.custom_id]) < (f.min_length or 1))
        or (values[f.custom_id] and len(values[f.custom_id]) < (f.min_length or 0))
    ]
    if invalid:
        await inter.reply("⚠️ Revisa la longitud de estos campos: " + ", ".join(invalid))
        return

    summary = [
        {"name": f.summary, "value": _field_value(values[f.custom_id]), "inline": not f.paragraph}
        for f in cat.fields
    ]

    # Confirmar recepción antes de acceder al disco o a otros endpoints.
    await inter.defer(ephemeral=True)
    blocked: Optional[dict[str, Any]] = None
    app: dict[str, Any] = {}
    async with STORE_POSTULACIONES.transaction() as db:
        _normalize_db(db)
        blocked = _active_application(db, inter.user_id)
        if not blocked:
            db["counter"] += 1
            post_id = f"TH-{db['counter']}"
            # Evita colisiones si en producción se restauró un contador antiguo.
            while post_id in db["applications"]:
                db["counter"] += 1
                post_id = f"TH-{db['counter']}"
            app = {
                "id": post_id,
                "user_id": inter.user_id,
                "username": inter.user_name,
                "categoria": cat.key,
                "tipo": cat.display,
                "submitted_at": int(time.time()),
                "status": Status.PENDING,
                "values": values,
                "resumen_fields": summary,
            }
            db["applications"][post_id] = app
            app = dict(app)

    if blocked:
        await inter.edit_original({"content": _already_active_message(blocked)})
        return

    post_id = app["id"]
    log.info("Postulacion %s registrada (%s) para %s", post_id, cat.display, inter.user_name)

    dm_ok = await send_dm(inter.user_id, {"embeds": [build_receipt_embed(app)]}) is not None
    app["dm_ok"] = dm_ok

    admin_msg_id = None
    try:
        admin_msg = await post_message(ADMIN_CHANNEL_ID, build_admin_message(app))
        admin_msg_id = admin_msg.get("id")
    except DiscordAPIError as exc:
        log.error("No se pudo publicar la ficha %s en el canal admin: %s", post_id, exc)

    async with STORE_POSTULACIONES.transaction() as db:
        stored = _normalize_db(db)["applications"].get(post_id)
        if stored is not None:
            stored["dm_ok"] = dm_ok
            stored["admin_msg_id"] = admin_msg_id

    lines = [f"✅ **¡Postulación enviada correctamente!** (ID: `{post_id}`)"]
    if dm_ok:
        lines.append("Tu ficha ha sido remitida a la directiva de ThunderMC. Hemos enviado un comprobante a tus mensajes directos (DM).")
    else:
        lines.append(
            "Tu ficha ha sido remitida a la directiva de ThunderMC.\n"
            "⚠️ **No hemos podido enviarte el comprobante por DM.** Activa los mensajes directos de este servidor "
            "o no podrás recibir la resolución."
        )
    if not admin_msg_id:
        lines.append(f"⚠️ No se pudo notificar a la directiva automáticamente. Abre un ticket indicando el ID `{post_id}`.")
    lines.append("Estado actual: **🟡 En revisión** *(puede tardar hasta 3 días hábiles en obtener una respuesta)*.")
    await inter.edit_original({"content": "\n".join(lines)})


for _modal_id in CATEGORY_BY_MODAL:
    route(IType.MODAL_SUBMIT, _modal_id)(on_submit_postulacion)


@route(IType.COMPONENT, prefix="admin_accept_")
async def on_admin_accept(inter: Interaction) -> None:
    post_id = inter.custom_id[len("admin_accept_"):]
    if not await _require_reviewer(inter):
        return
    await inter.defer_update()

    error: Optional[str] = None
    previous: tuple[Any, Any] = (None, None)
    snapshot: dict[str, Any] = {}
    async with STORE_POSTULACIONES.transaction() as db:
        app = _normalize_db(db)["applications"].get(post_id)
        error = _transition_error(app, post_id, REVIEWABLE_STATUSES)
        if not error:
            previous = (app.get("status"), app.get("reviewer_id"))
            app["status"] = Status.CONTRACT_SENT
            app["reviewer_id"] = inter.user_id
            # Identifica el intento; evita revertir una aceptación posterior.
            app["contract_attempt_id"] = inter.id
            app["contract_sent_at"] = int(time.time())
            snapshot = dict(app)
    if error:
        await inter.followup(error)
        return

    dm_message = await send_dm(snapshot["user_id"], build_contract_payload(snapshot))
    if dm_message is None:
        async with STORE_POSTULACIONES.transaction() as db:
            app = _normalize_db(db)["applications"].get(post_id)
            if (app and app.get("status") == Status.CONTRACT_SENT
                    and app.get("contract_attempt_id") == inter.id):
                app["status"], app["reviewer_id"] = previous
                app.pop("contract_sent_at", None)
                app.pop("contract_attempt_id", None)
        await refresh_admin_current(post_id)
        await inter.followup(
            f"⚠️ No se pudo enviar el contrato por DM a <@{snapshot['user_id']}> (DMs cerrados o ha salido del servidor). "
            f"La postulación `{post_id}` sigue en revisión: contacta con el candidato y vuelve a intentarlo."
        )
        return

    async with STORE_POSTULACIONES.transaction() as db:
        app = _normalize_db(db)["applications"].get(post_id)
        if app and app.get("contract_attempt_id") == inter.id:
            app["contract_msg_id"] = dm_message.get("id")
            app["contract_channel_id"] = dm_message.get("channel_id")
    await refresh_admin_current(post_id)
    log.info("Contrato %s enviado a %s por %s", post_id, snapshot["username"], inter.user_name)


@route(IType.COMPONENT, prefix="admin_reject_")
async def on_admin_reject(inter: Interaction) -> None:
    post_id = inter.custom_id[len("admin_reject_"):]
    if not await _require_reviewer(inter):
        return
    app = _normalize_db(await STORE_POSTULACIONES.read())["applications"].get(post_id)
    error = _transition_error(app, post_id, REVIEWABLE_STATUSES)
    if error:
        await inter.reply(error)
        return
    await inter.open_modal(
        {
            "custom_id": f"modal_reason_reject_{post_id}",
            "title": _truncate(f"Rechazar Postulación {post_id}", 45),
            "components": [
                FormField(
                    "field_reject_reason",
                    "Motivo del Rechazo (Se enviará al usuario)",
                    "",
                    "Explica con respeto y criterio qué aspectos no se ajustaron al perfil requerido...",
                    paragraph=True,
                    min_length=10,
                    max_length=1000,
                ).component()
            ],
        }
    )


@route(IType.MODAL_SUBMIT, prefix="modal_reason_reject_")
async def on_reject_reason(inter: Interaction) -> None:
    post_id = inter.custom_id[len("modal_reason_reject_"):]
    if not await _require_reviewer(inter):
        return
    reason = inter.modal_values().get("field_reject_reason", "").strip()
    if not 10 <= len(reason) <= 1000:
        await inter.reply("⚠️ El motivo debe tener entre 10 y 1.000 caracteres.")
        return

    # ACK antes de persistir; si la escritura tarda, el modal no expira.
    await inter.defer(ephemeral=True)
    error: Optional[str] = None
    snapshot: dict[str, Any] = {}
    async with STORE_POSTULACIONES.transaction() as db:
        app = _normalize_db(db)["applications"].get(post_id)
        error = _transition_error(app, post_id, REVIEWABLE_STATUSES)
        if not error:
            app["status"] = Status.REJECTED
            app["reject_reason"] = reason
            app["reviewer_id"] = inter.user_id
            app["resolved_at"] = int(time.time())
            snapshot = dict(app)
    if error:
        await inter.edit_original({"content": error})
        return

    dm_ok = await send_dm(snapshot["user_id"], {"embeds": [build_reject_embed(snapshot, reason)]}) is not None
    await refresh_admin_current(post_id)
    await notify_admins(
        f"❌ **POSTULACIÓN RECHAZADA:** `{post_id}` (<@{snapshot['user_id']}>) por <@{inter.user_id}>.\n"
        f"**Motivo:** *\"{_truncate(reason, 1500)}\"*"
        + ("" if dm_ok else "\n⚠️ El candidato **no ha recibido** el DM (DMs cerrados).")
    )
    result = f"✅ La postulación `{post_id}` ha sido **rechazada**"
    result += (
        f" y se le ha notificado por DM a <@{snapshot['user_id']}> con el motivo especificado."
        if dm_ok
        else f", pero **no se pudo notificar por DM** a <@{snapshot['user_id']}> (DMs cerrados)."
    )
    await inter.edit_original({"content": result})
    log.info("Postulacion %s rechazada por %s", post_id, inter.user_name)


@route(IType.COMPONENT, prefix="admin_review_")
async def on_admin_review(inter: Interaction) -> None:
    post_id = inter.custom_id[len("admin_review_"):]
    if not await _require_reviewer(inter):
        return
    await inter.defer_update()

    error: Optional[str] = None
    snapshot: dict[str, Any] = {}
    async with STORE_POSTULACIONES.transaction() as db:
        app = _normalize_db(db)["applications"].get(post_id)
        error = _transition_error(app, post_id, {Status.PENDING})
        if error and app and app.get("status") == Status.REVIEWING:
            error = f"ℹ️ La postulación `{post_id}` ya está siendo evaluada por <@{app.get('reviewer_id')}>."
        if not error:
            app["status"] = Status.REVIEWING
            app["reviewer_id"] = inter.user_id
            snapshot = dict(app)
    if error:
        await inter.followup(error)
        return

    await refresh_admin_current(post_id)
    await notify_admins(f"🔍 La postulación `{post_id}` está siendo evaluada activamente por <@{inter.user_id}>.")


async def _load_contract_for_candidate(inter: Interaction, post_id: str) -> Optional[str]:
    """Valida que el contrato existe, pertenece al usuario y sigue pendiente de firma."""
    app = _normalize_db(await STORE_POSTULACIONES.read())["applications"].get(post_id)
    if not app:
        return "❌ Contrato no localizado."
    if app.get("user_id") != inter.user_id:
        return "⛔ Este contrato no te pertenece."
    if app.get("status") != Status.CONTRACT_SENT:
        label = STATUS_LABEL.get(app.get("status"), app.get("status"))
        return f"ℹ️ Este contrato ya no está disponible (estado: **{label}**)."
    return None


# Bloqueo por expediente: dos clics de firma no deben generar dos invitaciones.
_contract_locks: dict[str, asyncio.Lock] = {}


@route(IType.COMPONENT, prefix="user_sign_contract_")
async def on_sign_contract(inter: Interaction) -> None:
    post_id = inter.custom_id[len("user_sign_contract_"):]
    # Confirmación inmediata: incluso un disco lento no debe caducar la interacción.
    await inter.defer_update()
    app = _normalize_db(await STORE_POSTULACIONES.read())["applications"].get(post_id)
    if not app:
        await inter.followup("❌ Contrato no localizado.")
        return
    if app.get("user_id") != inter.user_id:
        await inter.followup("⛔ Este contrato no te pertenece.")
        return
    if app.get("status") not in {Status.CONTRACT_SENT, Status.SIGNED}:
        await inter.followup("ℹ️ Este contrato ya no está disponible.")
        return
    lock = _contract_locks.setdefault(post_id, asyncio.Lock())
    async with lock:
        async with STORE_POSTULACIONES.transaction() as db:
            current = _normalize_db(db)["applications"].get(post_id)
            if not current or current.get("user_id") != inter.user_id:
                snapshot = None
            elif current.get("status") == Status.CONTRACT_SENT:
                current["status"] = Status.SIGNED
                current["resolved_at"] = int(time.time())
                current["welcome_delivered"] = False
                snapshot = dict(current)
            elif current.get("status") == Status.SIGNED and not current.get("welcome_delivered"):
                # Reintento después de un fallo al editar el DM, sin duplicar invitación.
                snapshot = dict(current)
            else:
                snapshot = None
        if snapshot is None:
            await inter.followup("ℹ️ Este contrato ya fue procesado.")
            return

        cat = _category_of(snapshot)
        role_ok = bool(snapshot.get("role_assigned"))
        role_info = snapshot.get("role_info") or "pendiente"
        if not role_ok:
            role_ok, role_info = (
                await assign_category_role(cat, inter.user_id)
                if cat else (False, "categoría desconocida")
            )
        invite = snapshot.get("onboarding_invite_url")
        if not invite:
            invite = await create_single_use_invite()

        # Persistir resultados antes del DM: la misma invitación se reutiliza si se reintenta.
        async with STORE_POSTULACIONES.transaction() as db:
            current = _normalize_db(db)["applications"].get(post_id)
            if current and current.get("status") == Status.SIGNED:
                current["role_assigned"] = role_ok
                current["role_info"] = role_info
                if invite:
                    current["onboarding_invite_url"] = invite
                snapshot = dict(current)

        welcome = {"embeds": [build_welcome_embed(snapshot, invite)], "components": []}
        delivered = False
        try:
            await inter.edit_original(welcome)
            delivered = True
        except DiscordAPIError as exc:
            log.warning("Falló la edición del contrato %s: %s", post_id, exc)
            channel_id, msg_id = snapshot.get("contract_channel_id"), snapshot.get("contract_msg_id")
            if channel_id and msg_id:
                try:
                    await edit_message(channel_id, msg_id, welcome)
                    delivered = True
                except DiscordAPIError as fallback_exc:
                    log.warning("Falló edición directa del contrato %s: %s", post_id, fallback_exc)
            if not delivered:
                delivered = await send_dm(inter.user_id, {"embeds": welcome["embeds"]}) is not None

        if delivered:
            async with STORE_POSTULACIONES.transaction() as db:
                current = _normalize_db(db)["applications"].get(post_id)
                if current and current.get("status") == Status.SIGNED:
                    current["welcome_delivered"] = True
        else:
            with suppress(DiscordAPIError):
                await inter.followup(
                    "⚠️ Tu firma está registrada, pero no se pudo entregar la bienvenida. "
                    "Un administrador deberá ayudarte."
                )

        await refresh_admin_current(post_id)
        notes = [
            f"🎉 **CONTRATO FIRMADO:** <@{snapshot['user_id']}> (`{snapshot['username']}`) "
            f"ha firmado para `{snapshot['tipo']}`.",
            "• Invitación de un solo uso generada para el candidato." if invite
            else "• ⚠️ **No se pudo generar la invitación**: envíasela manualmente.",
            f"• Rol asignado: {role_info}" if role_ok else
            f"• ⚠️ **Rol NO asignado** ({role_info}): asígnalo manualmente.",
        ]
        if not delivered:
            notes.append("• ⚠️ **No se pudo entregar la bienvenida**. Contacta con el candidato.")
        if not snapshot.get("onboarding_notified"):
            notified = await notify_admins("\n".join(notes))
            if notified:
                async with STORE_POSTULACIONES.transaction() as db:
                    current = _normalize_db(db)["applications"].get(post_id)
                    if current:
                        current["onboarding_notified"] = True
        log.info("Contrato %s firmado por %s (bienvenida=%s)", post_id, inter.user_name, delivered)


@route(IType.COMPONENT, prefix="user_decline_contract_")
async def on_decline_contract(inter: Interaction) -> None:
    post_id = inter.custom_id[len("user_decline_contract_"):]
    await inter.defer_update()
    error = await _load_contract_for_candidate(inter, post_id)
    snapshot: dict[str, Any] = {}
    if not error:
        async with STORE_POSTULACIONES.transaction() as db:
            app = _normalize_db(db)["applications"].get(post_id)
            if app and app.get("status") == Status.CONTRACT_SENT and app.get("user_id") == inter.user_id:
                app["status"] = Status.DECLINED
                app["resolved_at"] = int(time.time())
                snapshot = dict(app)
            else:
                error = "ℹ️ Este contrato ya no está disponible."
    if error:
        await inter.followup(error)
        return

    response = {"embeds": [build_declined_embed(snapshot)], "components": []}
    message_updated = False
    try:
        await inter.edit_original(response)
        message_updated = True
    except DiscordAPIError as exc:
        log.warning("No se pudo editar el contrato declinado %s: %s", post_id, exc)
        channel_id, message_id = snapshot.get("contract_channel_id"), snapshot.get("contract_msg_id")
        if channel_id and message_id:
            try:
                await edit_message(channel_id, message_id, response)
                message_updated = True
            except DiscordAPIError as fallback_exc:
                log.warning("Tampoco se pudo editar el DM %s: %s", post_id, fallback_exc)
        if not message_updated:
            with suppress(DiscordAPIError):
                await inter.followup("↩️ Tu decisión quedó registrada, pero no se pudo actualizar el contrato.")

    await refresh_admin_current(post_id)
    await notify_admins(
        f"↩️ **CONTRATO DECLINADO:** `{post_id}` — <@{snapshot['user_id']}> (`{snapshot['username']}`) "
        f"ha declinado la propuesta para `{snapshot['tipo']}`."
        + ("\n⚠️ No se pudo actualizar el mensaje privado del contrato." if not message_updated else "")
    )
    log.info("Contrato %s declinado por %s", post_id, snapshot["username"])


# =============================================================================
# NORMATIVA
# =============================================================================


def _load_first_embed(path: str) -> Optional[dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8-sig") as fh:
            embeds = json.load(fh).get("embeds") or []
        return embeds[0] if embeds and isinstance(embeds[0], dict) else None
    except (OSError, ValueError, AttributeError, IndexError, TypeError, UnicodeError) as exc:
        log.error("No se pudo cargar la normativa %s: %s", os.path.basename(path), exc)
        return None


@route(IType.COMPONENT, "select_reglas_normativa")
async def on_select_reglas(inter: Interaction) -> None:
    path = RULE_FILES.get(inter.selected_value)
    embed = _load_first_embed(path) if path else None
    if not embed:
        await inter.reply("⚠️ Esta normativa no está disponible en este momento.")
        return
    await inter.reply(embeds=[embed])


# =============================================================================
# SORTEOS
# =============================================================================

SORTEO_DEFAULTS = {
    "already_registered": "¡Ya estás participando en el sorteo!",
    "success_registration": "¡Te has registrado con éxito en el sorteo!",
    "status_registered": "✅ **Estado Actual:** Estás participando activamente.",
    "status_not_registered": "❌ **Estado Actual:** Aún no estás registrado en este sorteo.",
}
SORTEO_COUNTER_RE = re.compile(r"((?:Participantes|Entradas registradas): `)\d+( participantes`)")
_EMBED_KEYS = ("title", "description", "url", "timestamp", "color", "fields")
_sorteo_edit_lock = asyncio.Lock()


def _sorteo_text(key: str) -> str:
    try:
        with open(FILE_SORTEO_CFG, "r", encoding="utf-8-sig") as fh:
            value = json.load(fh).get(key)
        if isinstance(value, str) and 0 < len(value) <= 2000:
            return value
    except (OSError, ValueError, AttributeError, UnicodeError):
        pass
    return SORTEO_DEFAULTS[key]


def _clean_embed(embed: dict[str, Any]) -> dict[str, Any]:
    """Quita campos de solo lectura de un embed recibido para poder reenviarlo."""
    out = {k: embed[k] for k in _EMBED_KEYS if k in embed}
    for key in ("image", "thumbnail"):
        if isinstance(embed.get(key), dict) and embed[key].get("url"):
            out[key] = {"url": embed[key]["url"]}
    if isinstance(embed.get("footer"), dict):
        out["footer"] = {k: v for k, v in embed["footer"].items() if k in ("text", "icon_url")}
    if isinstance(embed.get("author"), dict):
        out["author"] = {k: v for k, v in embed["author"].items() if k in ("name", "url", "icon_url")}
    return out


async def _update_sorteo_counter(inter: Interaction) -> None:
    message = inter.message
    if not message or (message.get("author") or {}).get("id") != inter.application_id:
        return  # Solo se pueden editar mensajes enviados por el propio bot.
    embeds = message.get("embeds") or []
    if not embeds or not SORTEO_COUNTER_RE.search(embeds[0].get("description", "")):
        return
    async with _sorteo_edit_lock:
        total = len(_normalize_sorteos(await STORE_SORTEOS.read())["entries"])
        try:
            # El evento lleva una copia posiblemente antigua; consultar el mensaje actual.
            latest = await discord_request("GET", f"/channels/{inter.channel_id}/messages/{message['id']}")
            if (latest.get("author") or {}).get("id") != inter.application_id:
                return
            current_embeds = latest.get("embeds") or []
            if not current_embeds or not SORTEO_COUNTER_RE.search(current_embeds[0].get("description") or ""):
                return
            embed = _clean_embed(current_embeds[0])
            embed["description"] = SORTEO_COUNTER_RE.sub(
                lambda match: f"{match.group(1)}{total}{match.group(2)}", embed["description"]
            )
            await edit_message(
                inter.channel_id, message["id"],
                {"embeds": [embed] + [_clean_embed(e) for e in current_embeds[1:]]},
            )
        except (DiscordAPIError, KeyError, TypeError, AttributeError) as exc:
            log.warning("No se pudo actualizar el contador del sorteo: %s", exc)


@route(IType.COMPONENT, "sorteo_participar")
async def on_sorteo_participar(inter: Interaction) -> None:
    await inter.defer(ephemeral=True)
    async with STORE_SORTEOS.transaction() as data:
        entries = _normalize_sorteos(data)["entries"]
        already = any(str(e.get("userId")) == inter.user_id for e in entries)
        if not already:
            entries.append({"userId": inter.user_id, "username": inter.user_name, "joinedAt": int(time.time())})
    await inter.edit_original({"content": _sorteo_text("already_registered" if already else "success_registration")})
    if not already:
        log.info("Nueva entrada de sorteo: %s (total %d)", inter.user_name, len(entries))
        await _update_sorteo_counter(inter)


@route(IType.COMPONENT, "sorteo_ver_estado")
async def on_sorteo_estado(inter: Interaction) -> None:
    await inter.defer(ephemeral=True)
    entries = _normalize_sorteos(await STORE_SORTEOS.read())["entries"]
    entry = next((e for e in entries if str(e.get("userId")) == inter.user_id), None)
    if entry:
        content = _sorteo_text("status_registered")
        if entry.get("joinedAt"):
            try:
                joined_at = int(entry["joinedAt"])
                if joined_at > 0:
                    content += f" (Registrado: <t:{joined_at}:R>)"
            except (TypeError, ValueError, OverflowError):
                log.warning("Sorteo: marca de tiempo inválida para %s", inter.user_id)
    else:
        content = _sorteo_text("status_not_registered")
    await inter.edit_original({"content": content})


# =============================================================================
# AUTO-DEPLOY PIPELINE (HOT-RELOAD, VERIFICACIÓN Y GESTIÓN DE CÓDIGO)
# =============================================================================

_deploy_lock = asyncio.Lock()


def _get_current_zip_msg_id() -> str:
    try:
        if os.path.exists(FILE_ADMIN_PANEL_STATE):
            with open(FILE_ADMIN_PANEL_STATE, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                if data.get("current_zip_msg_id"):
                    return str(data["current_zip_msg_id"])
    except Exception:
        pass
    return DEFAULT_CURRENT_ZIP_MSG_ID


def _save_current_zip_msg_id(msg_id: str) -> None:
    try:
        with open(FILE_ADMIN_PANEL_STATE, "w", encoding="utf-8") as fh:
            json.dump({"current_zip_msg_id": msg_id}, fh, indent=2)
    except Exception as exc:
        log.warning("No se pudo guardar admin_panel_state.json: %s", exc)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while chunk := fh.read(65536):
            h.update(chunk)
    return h.hexdigest()


def _download_url(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def build_current_bot_zip_bytes() -> bytes:
    """Empaqueta el código actual de producción en memoria (bytes de zip)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(BASE_DIR):
            dirs[:] = [d for d in dirs if d not in {"__pycache__", ".git", "backups", "venv", ".idea"}]
            for fname in files:
                ext = os.path.splitext(fname)[1].lower()
                if fname in PROTECTED_FILES or fname.endswith("_db.json") or ext in {".bak", ".tmp", ".pyc"}:
                    continue
                if ext in ALLOWED_EXTENSIONS or fname in CORE_FILES_TO_PACK:
                    abs_path = os.path.join(root, fname)
                    rel_path = os.path.relpath(abs_path, BASE_DIR).replace("\\", "/")
                    zf.write(abs_path, rel_path)
    buf.seek(0)
    return buf.getvalue()


async def update_live_zip_message(zip_bytes: bytes) -> None:
    msg_id = _get_current_zip_msg_id()
    now_str = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S UTC")
    embed = {
        "title": "📦 Código Actual de Fabio en Producción (Descarga Directa)",
        "description": (
            "Este archivo representa la **versión activa y en tiempo real** del bot en el contenedor de Vultam.\n\n"
            "**Detalles del Paquete:**\n"
            "> `📁` Archivos incluidos: `gateway_bot.py`, `main.py`, `bot.py`, `requirements.txt` y configuraciones JSON.\n"
            "> `🛡️` **Excluidos:** `.env` y bases de datos vivas (`postulaciones_db.json`, `sorteos_db.json`).\n"
            "> `🔄` **Auto-Actualización:** Cada vez que se aplique un cambio exitoso en este canal, este mensaje se mantendrá al día con la última versión operativa."
        ),
        "color": 3066993,
        "footer": {
            "text": f"ThunderMC Bot • Producción Vultam (Miami) • Actualizado: {now_str}"
        },
    }
    payload = {
        "embeds": [embed],
        "attachments": [{"id": 0, "filename": "fabio_codigo_actual.zip"}],
    }
    files = [("files[0]", "fabio_codigo_actual.zip", zip_bytes, "application/zip")]

    # Intento 1: PATCH al mensaje existente
    try:
        await discord_multipart_request("PATCH", f"/channels/{ADMIN_PANEL_CHANNEL_ID}/messages/{msg_id}", payload, files)
        log.info("Mensaje de ZIP en vivo actualizado con éxito (ID: %s)", msg_id)
        return
    except DiscordAPIError as exc:
        log.warning("Fallo al actualizar mensaje existente (%s): %s. Se creará uno nuevo.", msg_id, exc)

    # Intento 2: POST nuevo mensaje si no existe
    try:
        res = await discord_multipart_request("POST", f"/channels/{ADMIN_PANEL_CHANNEL_ID}/messages", payload, files)
        new_id = res.get("id")
        if new_id:
            _save_current_zip_msg_id(new_id)
            log.info("Nuevo mensaje de ZIP en vivo publicado (ID: %s)", new_id)
    except Exception as exc:
        log.error("No se pudo publicar el mensaje de ZIP en vivo: %s", exc)


async def _send_deploy_compilation_error(rel_file: str, lineno: Any, err_trace: str, prompt: str) -> None:
    trace_trimmed = err_trace[-600:] if len(err_trace) > 600 else err_trace
    prompt_trimmed = prompt[:1000] if len(prompt) > 1000 else prompt
    embed = {
        "title": "❌ Despliegue Rechazado — Error de Compilación",
        "description": (
            "Se ha bloqueado la actualización porque uno o más scripts Python contienen errores "
            "de sintaxis o compilación. **El entorno de producción se mantiene intacto y operativo.**"
        ),
        "color": 15548997,  # #ED4245
        "fields": [
            {
                "name": f"🔍 Archivo Afectado: `{rel_file}` (Línea {lineno})",
                "value": f"```python\n{trace_trimmed}\n```",
                "inline": False,
            },
            {
                "name": "🤖 Prompt de Reparación (Copia y entrega a tu IA)",
                "value": f"```markdown\n{prompt_trimmed}\n```",
                "inline": False,
            },
            {
                "name": "💡 Recomendaciones",
                "value": (
                    "• Copia el prompt anterior y entrégalo a tu IA para corregir la sintaxis.\n"
                    "• Vuelve a empaquetar el código corregido en formato ZIP y súbelo a `#admin-panel`.\n"
                    "• La versión anterior de Fabio sigue atendiendo a los usuarios con total normalidad."
                ),
                "inline": False,
            },
        ],
        "footer": {
            "text": "ThunderMC • Auto-Deploy Safety Shield",
        },
    }
    try:
        await post_message(DEPLOY_LOG_CHANNEL_ID, {"embeds": [embed]})
    except Exception as exc:
        log.error("No se pudo enviar log de compilación a %s: %s", DEPLOY_LOG_CHANNEL_ID, exc)


async def _send_deploy_error(title: str, detail: str, recommendation: str) -> None:
    embed = {
        "title": f"❌ Despliegue Rechazado — {title}",
        "description": detail,
        "color": 15548997,
        "fields": [
            {
                "name": "💡 Recomendación",
                "value": recommendation,
                "inline": False,
            }
        ],
        "footer": {
            "text": "ThunderMC • Auto-Deploy Safety Shield",
        },
    }
    try:
        await post_message(DEPLOY_LOG_CHANNEL_ID, {"embeds": [embed]})
    except Exception as exc:
        log.error("No se pudo enviar log de error a %s: %s", DEPLOY_LOG_CHANNEL_ID, exc)


async def _send_deploy_notice(title: str, detail: str) -> None:
    embed = {
        "title": f"ℹ️ Despliegue Omitido — {title}",
        "description": detail,
        "color": 16776960,  # Amarillo
        "footer": {
            "text": "ThunderMC • Auto-Deploy Engine",
        },
    }
    try:
        await post_message(DEPLOY_LOG_CHANNEL_ID, {"embeds": [embed]})
    except Exception as exc:
        log.error("No se pudo enviar log de aviso a %s: %s", DEPLOY_LOG_CHANNEL_ID, exc)


async def _send_deploy_success(
    modified_files: list[dict[str, Any]],
    skipped_protected: list[str],
    backup_filename: str,
    backup_bytes: bytes,
) -> None:
    lines = []
    for item in modified_files[:10]:
        action_emoji = "✨" if item["action"] == "NUEVO" else "📝"
        diff_info = f" ({item['diff_size']} B)" if "diff_size" in item else f" ({item['size']} B)"
        lines.append(f"> {action_emoji} `{item['rel_path']}` — {item['action'].lower()}{diff_info} [`{item['hash']}`]")
    if len(modified_files) > 10:
        lines.append(f"> ... y {len(modified_files) - 10} archivo(s) más.")

    embed = {
        "title": "✅ Despliegue Exitoso — Código Actualizado en Producción",
        "description": (
            "El nuevo paquete de código ha sido verificado, compilado y aplicado correctamente.\n"
            "Fabio ha reiniciado en caliente su proceso y se encuentra plenamente operativo."
        ),
        "color": 5763719,  # #57F287 Verde
        "fields": [
            {
                "name": f"📋 Archivos Procesados ({len(modified_files)})",
                "value": "\n".join(lines) if lines else "Ninguno",
                "inline": False,
            },
            {
                "name": "🛡️ Respaldo Previo Adjunto (Rollback)",
                "value": (
                    f"Se ha archivado el estado anterior en `{backup_filename}` (adjunto en este mensaje).\n"
                    "Si detectas cualquier anomalía en runtime, descarga este archivo y vuelve a subirlo para restaurar."
                ),
                "inline": False,
            },
            {
                "name": "💡 Recomendaciones",
                "value": (
                    "• Verifica que los botones y menús sigan respondiendo con normalidad.\n"
                    "• Consulta `#admin-panel` para descargar siempre el código más reciente.\n"
                    "• Para futuras modificaciones, utiliza el ZIP actualizado como base."
                ),
                "inline": False,
            },
        ],
        "footer": {
            "text": "ThunderMC • Auto-Deploy Engine • Producción Vultam",
        },
    }
    if skipped_protected:
        embed["fields"].insert(1, {
            "name": "🔒 Archivos Protegidos (Omitidos por Seguridad)",
            "value": ", ".join(f"`{f}`" for f in skipped_protected),
            "inline": False,
        })

    payload = {"embeds": [embed]}
    files = [("files[0]", backup_filename, backup_bytes, "application/zip")]
    try:
        await discord_multipart_request("POST", f"/channels/{DEPLOY_LOG_CHANNEL_ID}/messages", payload, files)
        log.info("Log de despliegue exitoso publicado en #cambios-log con backup adjunto: %s", backup_filename)
    except Exception as exc:
        log.error("No se pudo enviar log de éxito a %s: %s", DEPLOY_LOG_CHANNEL_ID, exc)


async def handle_message_create(data: dict[str, Any]) -> None:
    channel_id = str(data.get("channel_id") or "")
    if channel_id != ADMIN_PANEL_CHANNEL_ID:
        return
    author = data.get("author") or {}
    if author.get("bot"):
        return
    if str(author.get("id") or "") != RAMOS_USER_ID:
        log.warning("Mensaje en admin-panel ignorado (no es el Sr Ramos): %s (%s)", author.get("username"), author.get("id"))
        return

    attachments = data.get("attachments") or []
    zip_att = next((a for a in attachments if str(a.get("filename", "")).lower().endswith(".zip")), None)
    if not zip_att:
        return

    asyncio.create_task(process_deployment_zip(data, zip_att))


async def process_deployment_zip(msg: dict[str, Any], att: dict[str, Any]) -> None:
    if _deploy_lock.locked():
        log.warning("Despliegue ignorado: ya hay un despliegue en curso.")
        return

    async with _deploy_lock:
        msg_id = str(msg["id"])
        channel_id = str(msg["channel_id"])
        url = att["url"]
        filename = att.get("filename") or "update.zip"
        size = att.get("size", 0)

        log.info("Iniciando procesamiento de despliegue desde mensaje %s (%s, %d bytes)", msg_id, filename, size)
        await add_reaction(channel_id, msg_id, "⏳")

        if size > 25 * 1024 * 1024:
            await remove_reaction(channel_id, msg_id, "⏳")
            await add_reaction(channel_id, msg_id, "❌")
            await _send_deploy_error(
                "Archivo Demasiado Grande",
                f"El archivo `{filename}` supera el límite permitido de 25 MB ({size} bytes).",
                "Reduce el tamaño del ZIP excluyendo archivos innecesarios."
            )
            return

        # 1. Descarga del ZIP
        try:
            zip_bytes = await asyncio.to_thread(_download_url, url)
        except Exception as exc:
            await remove_reaction(channel_id, msg_id, "⏳")
            await add_reaction(channel_id, msg_id, "❌")
            await _send_deploy_error(
                "Fallo en la Descarga",
                f"No se pudo descargar el archivo desde Discord CDN: {exc}",
                "Verifica la conexión e inténtalo de nuevo."
            )
            return

        if not zipfile.is_zipfile(io.BytesIO(zip_bytes)):
            await remove_reaction(channel_id, msg_id, "⏳")
            await add_reaction(channel_id, msg_id, "❌")
            await _send_deploy_error(
                "Archivo Inválido",
                f"El archivo `{filename}` no tiene un formato ZIP válido o está dañado.",
                "Asegúrate de comprimir en formato .zip estándar (ZIP_DEFLATED)."
            )
            return

        # 2. Extracción en Sandbox temporal
        temp_dir = tempfile.mkdtemp(prefix="fabio_deploy_")
        try:
            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
                for member in zf.infolist():
                    if member.is_dir():
                        continue
                    clean_name = os.path.normpath(member.filename)
                    if clean_name.startswith("..") or os.path.isabs(clean_name):
                        raise ValueError(f"Intento de path traversal detectado en {member.filename}")
                    target = os.path.join(temp_dir, clean_name)
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    with zf.open(member) as src, open(target, "wb") as dst:
                        shutil.copyfileobj(src, dst)

            # Detectar si viene envuelto en una subcarpeta
            source_root = temp_dir
            entries = [e for e in os.listdir(temp_dir) if not e.startswith(".")]
            if len(entries) == 1 and os.path.isdir(os.path.join(temp_dir, entries[0])):
                candidate = os.path.join(temp_dir, entries[0])
                if os.path.exists(os.path.join(candidate, "gateway_bot.py")):
                    source_root = candidate

            # 3. Verificación de compilación de todos los scripts .py
            for root, _, files in os.walk(source_root):
                for f in files:
                    if f.endswith(".py"):
                        py_file = os.path.join(root, f)
                        rel_file = os.path.relpath(py_file, source_root).replace("\\", "/")
                        try:
                            py_compile.compile(py_file, doraise=True)
                        except py_compile.PyCompileError as c_exc:
                            await remove_reaction(channel_id, msg_id, "⏳")
                            await add_reaction(channel_id, msg_id, "❌")

                            err_trace = (c_exc.msg or str(c_exc)).strip()
                            exc_val = c_exc.exc_value
                            lineno = getattr(exc_val, "lineno", "?")
                            line_text = getattr(exc_val, "text", "") or ""
                            clean_err = str(exc_val)

                            prompt = (
                                "### 🚨 INCIDENCIA DETECTADA EN DESPLIEGUE - THUNDERMC FABIO\n"
                                f"**Archivo:** `{rel_file}`\n"
                                f"**Línea:** {lineno}\n"
                                f"**Error de Sintaxis:** {clean_err}\n\n"
                                f"**Fragmento problemático:**\n```python\n{line_text.strip()}\n```\n\n"
                                "**Instrucción para la IA:**\n"
                                f"Corrige el error de sintaxis anterior en `{rel_file}`. "
                                "Mantén la estructura asíncrona (asyncio/websockets), compatibilidad con Python 3.10+, "
                                "y no agregues dependencias externas innecesarias. Devuelve el código corregido listo para desplegar."
                            )

                            await _send_deploy_compilation_error(rel_file, lineno, err_trace, prompt)
                            return

            # 4. Análisis de cambios respecto a producción
            modified_files: list[dict[str, Any]] = []
            skipped_protected: list[str] = []

            for root, _, files in os.walk(source_root):
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if f in PROTECTED_FILES or f.endswith("_db.json"):
                        skipped_protected.append(f)
                        continue
                    if ext not in ALLOWED_EXTENSIONS and f not in CORE_FILES_TO_PACK:
                        continue

                    src_path = os.path.join(root, f)
                    rel_path = os.path.relpath(src_path, source_root)
                    dest_path = os.path.join(BASE_DIR, rel_path)

                    with open(src_path, "rb") as fh:
                        new_content = fh.read()
                    new_hash = _sha256_bytes(new_content)

                    is_new = not os.path.exists(dest_path)
                    if is_new:
                        modified_files.append({
                            "rel_path": rel_path.replace("\\", "/"),
                            "action": "NUEVO",
                            "size": len(new_content),
                            "hash": new_hash[:10],
                            "src_path": src_path,
                            "dest_path": dest_path,
                        })
                    else:
                        old_hash = _sha256_file(dest_path)
                        if old_hash != new_hash:
                            old_size = os.path.getsize(dest_path)
                            diff_size = len(new_content) - old_size
                            diff_sign = f"+{diff_size}" if diff_size >= 0 else str(diff_size)
                            modified_files.append({
                                "rel_path": rel_path.replace("\\", "/"),
                                "action": "MODIFICADO",
                                "size": len(new_content),
                                "diff_size": diff_sign,
                                "hash": new_hash[:10],
                                "src_path": src_path,
                                "dest_path": dest_path,
                            })

            if not modified_files:
                await remove_reaction(channel_id, msg_id, "⏳")
                await add_reaction(channel_id, msg_id, "⚠️")
                await _send_deploy_notice(
                    "Sin cambios detectados",
                    "El contenido del ZIP es idéntico al código que ya está en ejecución.\n"
                    + (f"Archivos protegidos omitidos: {', '.join(skipped_protected)}" if skipped_protected else "")
                )
                return

            # 5. Generar backup previo del estado actual
            now_ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_previo_{now_ts}.zip"
            pre_backup_bytes = build_current_bot_zip_bytes()

            backup_dir = os.path.join(BASE_DIR, "backups")
            os.makedirs(backup_dir, exist_ok=True)
            with open(os.path.join(backup_dir, backup_filename), "wb") as bfh:
                bfh.write(pre_backup_bytes)

            # 6. Aplicar cambios atómicamente a producción
            for item in modified_files:
                dpath = item["dest_path"]
                os.makedirs(os.path.dirname(dpath), exist_ok=True)
                if os.path.exists(dpath):
                    shutil.copy2(dpath, dpath + ".bak")

                tmp_dest = dpath + ".tmp"
                shutil.copy2(item["src_path"], tmp_dest)
                os.replace(tmp_dest, dpath)
                log.info("Archivo aplicado en producción: %s (%s)", item["rel_path"], item["action"])

            # 7. Actualizar el paquete en vivo en #admin-panel
            new_live_zip = build_current_bot_zip_bytes()
            output_dir = os.path.join(BASE_DIR, "output")
            os.makedirs(output_dir, exist_ok=True)
            with open(os.path.join(output_dir, "fabio_codigo_actual.zip"), "wb") as ofh:
                ofh.write(new_live_zip)

            await update_live_zip_message(new_live_zip)

            # 8. Notificar éxito en #cambios-log con backup adjunto
            await _send_deploy_success(modified_files, skipped_protected, backup_filename, pre_backup_bytes)

            # 9. Concluir reacción y reiniciar proceso en caliente
            await remove_reaction(channel_id, msg_id, "⏳")
            await add_reaction(channel_id, msg_id, "✅")

            log.info("Despliegue completado con éxito. Reiniciando proceso en 2 segundos...")
            await asyncio.sleep(2.0)
            os.execv(sys.executable, [sys.executable] + sys.argv)

        except Exception as exc:
            log.exception("Error crítico durante el despliegue: %s", exc)
            await remove_reaction(channel_id, msg_id, "⏳")
            await add_reaction(channel_id, msg_id, "❌")
            await _send_deploy_error("Error Interno en Despliegue", str(exc), "Revisa los registros del contenedor de Vultam.")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


# =============================================================================
# GATEWAY
# =============================================================================


class FatalGatewayError(RuntimeError):
    pass


class GatewayClient:
    """Cliente del Gateway v10 con heartbeat, detección de conexiones zombi,
    RESUME de sesión y reconexión con backoff exponencial."""

    def __init__(self, token: str, *, intents: int = 512, url: str = GATEWAY_URL):
        self.token = token
        self.intents = intents
        self.default_url = url
        self.session_id: Optional[str] = None
        self.resume_url: Optional[str] = None
        self.seq: Optional[int] = None
        self._acked = True
        self._ready = False
        self._tasks: set[asyncio.Task[Any]] = set()

    # --- Ciclo de vida ----------------------------------------------------------

    async def run_forever(self) -> None:
        backoff = 1.0
        while True:
            self._ready = False
            try:
                code = await self._run_session()
                if code in FATAL_CLOSE_CODES:
                    raise FatalGatewayError(f"Discord cerró la conexión con código fatal {code} (token/intents inválidos).")
                if code in NON_RESUMABLE_CLOSE_CODES:
                    self._reset_session()
                log.warning("Conexión con el Gateway cerrada (código %s).", code)
            except FatalGatewayError:
                raise
            except (OSError, asyncio.TimeoutError, WebSocketException, ValueError, KeyError) as exc:
                log.warning("Error de conexión con el Gateway: %r", exc)

            if self._ready:
                backoff = 1.0
            delay = backoff + random.uniform(0, 1)
            log.info("Reconectando en %.1fs...", delay)
            await asyncio.sleep(delay)
            backoff = min(backoff * 2, 60.0)

    def _reset_session(self) -> None:
        self.session_id = None
        self.resume_url = None
        self.seq = None

    def _can_resume(self) -> bool:
        return bool(self.session_id and self.resume_url and self.seq is not None)

    async def _run_session(self) -> Optional[int]:
        resuming = self._can_resume()
        url = self.resume_url if resuming else self.default_url
        log.info("Conectando al Gateway (%s)...", "RESUME" if resuming else "IDENTIFY")
        async with websockets.connect(
            url, max_size=10_000_000, open_timeout=20, close_timeout=5, ping_interval=None
        ) as ws:
            hello = json.loads(await asyncio.wait_for(ws.recv(), timeout=30))
            if hello.get("op") != 10:
                raise ValueError(f"Se esperaba HELLO y se recibió op={hello.get('op')}")
            interval = hello["d"]["heartbeat_interval"] / 1000.0
            self._acked = True
            heartbeat = asyncio.create_task(self._heartbeat_loop(ws, interval))
            try:
                await self._send(ws, self._resume_payload() if resuming else self._identify_payload())
                try:
                    async for raw in ws:
                        await self._on_payload(ws, json.loads(raw))
                except ConnectionClosed:
                    pass
            finally:
                heartbeat.cancel()
                with suppress(asyncio.CancelledError, Exception):
                    await heartbeat
            return ws.close_code

    # --- Envío ------------------------------------------------------------------

    @staticmethod
    async def _send(ws: Any, payload: dict[str, Any]) -> None:
        await ws.send(json.dumps(payload))

    def _identify_payload(self) -> dict[str, Any]:
        return {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": self.intents,
                "properties": {"os": sys.platform, "browser": "thundermc_bot", "device": "thundermc_bot"},
                "presence": {
                    "status": "online",
                    "since": None,
                    "afk": False,
                    "activities": [{"name": "thundermc.es", "type": 0, "state": "thundermc.es"}],
                },
            },
        }

    def _resume_payload(self) -> dict[str, Any]:
        return {"op": 6, "d": {"token": self.token, "session_id": self.session_id, "seq": self.seq}}

    async def _heartbeat_loop(self, ws: Any, interval: float) -> None:
        try:
            await asyncio.sleep(interval * random.random())
            while True:
                if not self._acked:
                    log.warning("Heartbeat sin ACK: conexión zombi. Forzando reconexión.")
                    await ws.close(code=4000)
                    return
                self._acked = False
                await self._send(ws, {"op": 1, "d": self.seq})
                await asyncio.sleep(interval)
        except ConnectionClosed:
            return

    # --- Recepción --------------------------------------------------------------

    async def _on_payload(self, ws: Any, payload: dict[str, Any]) -> None:
        op = payload.get("op")
        if payload.get("s") is not None:
            self.seq = payload["s"]

        if op == 0:
            self._on_dispatch(payload.get("t"), payload.get("d") or {})
        elif op == 1:
            await self._send(ws, {"op": 1, "d": self.seq})
        elif op == 7:
            log.info("Discord solicita reconexión (op 7).")
            await ws.close(code=4000)
        elif op == 9:
            resumable = bool(payload.get("d"))
            log.warning("Sesión inválida (op 9, reanudable=%s).", resumable)
            if not resumable:
                self._reset_session()
            await asyncio.sleep(random.uniform(1, 5))
            await ws.close(code=4000)
        elif op == 11:
            self._acked = True

    def _on_dispatch(self, event: Optional[str], data: dict[str, Any]) -> None:
        if event == "READY":
            self.session_id = data.get("session_id")
            resume = (data.get("resume_gateway_url") or "").rstrip("/")
            self.resume_url = f"{resume}{GATEWAY_QUERY}" if resume else None
            self._ready = True
            user = data.get("user") or {}
            log.info("BOT CONECTADO Y OPERATIVO: %s (%s)", user.get("username"), user.get("id"))
        elif event == "RESUMED":
            self._ready = True
            log.info("Sesión reanudada correctamente.")
        elif event == "INTERACTION_CREATE":
            task = asyncio.create_task(dispatch_interaction(data))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)
        elif event == "MESSAGE_CREATE":
            task = asyncio.create_task(handle_message_create(data))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)


# =============================================================================
# ARRANQUE
# =============================================================================


def _configure_logging() -> None:
    root = logging.getLogger()
    if root.handlers:
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
    root.addHandler(handler)
    root.setLevel(logging.INFO)


async def gateway_runner() -> None:
    _configure_logging()
    log.info("=" * 60)
    log.info("  THUNDERMC - GATEWAY FABIO v2 (POSTULACIONES + INTERACCIONES)")
    log.info("=" * 60)
    if not TOKEN:
        raise FatalGatewayError("Falta DISCORD_BOT_TOKEN (.env o variable de entorno).")
    log.info("Canal de administracion: %s | Hilo de postulaciones: %s", ADMIN_CHANNEL_ID, POSTULACIONES_THREAD_ID)
    log.info("Revisores: %s", ", ".join(sorted(REVIEWER_ROLE_IDS)) or "solo administradores del servidor")
    try:
        _normalize_db(await STORE_POSTULACIONES.read())
        _normalize_sorteos(await STORE_SORTEOS.read())
    except StoreCorruptedError as exc:
        log.critical("Detenido para proteger los datos: %s", exc)
        raise FatalGatewayError("Base de datos inválida. Revisa el archivo original y su copia.") from exc

    await GatewayClient(TOKEN, intents=512).run_forever()


if __name__ == "__main__":
    try:
        asyncio.run(gateway_runner())
    except KeyboardInterrupt:
        print("\nGateway detenido por el usuario.")
