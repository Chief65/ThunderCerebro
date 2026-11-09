import os
import json
import time
import asyncio
import urllib.request
import urllib.error
import websockets

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")

token = None
channel_id = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("DISCORD_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()
        elif line.startswith("DISCORD_CHANNEL_ID="):
            channel_id = line.split("=", 1)[1].strip()

app_id = "1552716487100342404"
guild_id = "1552715004669726802"
admin_channel_id = "1568307337859436716"  # Canal privado postu-media
postulaciones_thread_id = "1568202156090073101"
user_agent = "DiscordBot (https://thundermc.es, 1.0.0)"

db_postulaciones_file = os.path.join(script_dir, "postulaciones_db.json")
if not os.path.exists(db_postulaciones_file):
    with open(db_postulaciones_file, "w", encoding="utf-8") as f:
        json.dump({"counter": 100, "applications": {}}, f, indent=2, ensure_ascii=False)

db_sorteos_file = os.path.join(script_dir, "sorteos_db.json")
if not os.path.exists(db_sorteos_file):
    with open(db_sorteos_file, "w", encoding="utf-8") as f:
        json.dump({"entries": []}, f, indent=2, ensure_ascii=False)

cfg_sorteo_file = os.path.join(script_dir, "sorteo_config.json")
cfg_sorteo = None
if os.path.exists(cfg_sorteo_file):
    try:
        with open(cfg_sorteo_file, "r", encoding="utf-8") as f:
            cfg_sorteo = json.load(f)
    except Exception:
        pass

rg_file = os.path.join(script_dir, "reglas_generales.json")
if not os.path.exists(rg_file):
    rg_file = r"C:\Users\PC\OneDrive\Escritorio\descargas\reglas\reglas generales.json"

rd_file = os.path.join(script_dir, "reglas_discord.json")
if not os.path.exists(rd_file):
    rd_file = r"C:\Users\PC\OneDrive\Escritorio\descargas\reglas\reglas discord.json"

def discord_api(method, endpoint, body=None):
    url = f"https://discord.com/api/v10{endpoint}"
    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": user_agent,
    }
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"[API Error] {method} {endpoint} -> HTTP {e.code}: {err_body}")
        raise

def send_interaction_response(inter_id, inter_token, body_obj):
    url = f"https://discord.com/api/v10/interactions/{inter_id}/{inter_token}/callback"
    headers = {
        "User-Agent": user_agent,
        "Content-Type": "application/json; charset=utf-8"
    }
    data = json.dumps(body_obj, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read()
    except Exception as e:
        print(f"[Callback Error] Interacción {inter_id}: {e}")

def send_dm_to_user(user_id, body_obj):
    try:
        # 1. Abrir canal de DM
        dm_channel = discord_api("POST", "/users/@me/channels", {"recipient_id": str(user_id)})
        dm_channel_id = dm_channel["id"]
        # 2. Enviar mensaje al DM
        res = discord_api("POST", f"/channels/{dm_channel_id}/messages", body_obj)
        return res
    except Exception as e:
        print(f"[DM Warning] No se pudo enviar DM a usuario {user_id}: {e}")
        return None

def create_single_use_invite():
    try:
        # Generar invitación de un solo uso en el canal general de bienvenida
        res = discord_api("POST", f"/channels/{channel_id}/invites", {
            "max_age": 86400,
            "max_uses": 1,
            "unique": True
        })
        return f"https://discord.gg/{res.get('code')}"
    except Exception as e:
        print(f"[Invite Error] Falló al crear invite: {e}")
        return "https://discord.gg/thundermc"

def load_postulaciones():
    try:
        with open(db_postulaciones_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"counter": 100, "applications": {}}

def save_postulaciones(db):
    with open(db_postulaciones_file, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

def get_sorteo_entries():
    try:
        with open(db_sorteos_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("entries", [])
    except Exception:
        return []

def save_sorteo_entries(entries):
    with open(db_sorteos_file, "w", encoding="utf-8") as f:
        json.dump({"entries": entries}, f, indent=2, ensure_ascii=False)

print("=" * 60)
print("  THUNDERMC - GATEWAY INTEGRADO (POSTULACIONES + INTERACCIONES)")
print("=" * 60)
print(f"Canal de Administración (Postulaciones): {admin_channel_id}")
print(f"Hilo de Postulaciones: {postulaciones_thread_id}")

async def handle_interaction(interaction):
    inter_id = interaction.get("id")
    inter_token = interaction.get("token")
    inter_type = interaction.get("type")
    data = interaction.get("data", {})
    custom_id = data.get("custom_id", "")
    
    user = interaction.get("member", {}).get("user") or interaction.get("user") or {}
    user_id = user.get("id")
    user_name = user.get("username", "Desconocido")
    
    print(f"\n[INTERACTION] Usuario: {user_name} ({user_id}) | Tipo: {inter_type} | CustomID: {custom_id}")

    # =========================================================================
    # 1. SELECT MENU: TIPO DE POSTULACIÓN (Components V2)
    # =========================================================================
    if custom_id == "select_postulacion_tipo":
        selected_val = data.get("values", [""])[0]
        print(f"   -> Selección de tipo de postulación: {selected_val}")
        
        info_map = {
            "postulacion_staff": {
                "name": "Staff / Moderación",
                "emoji": "🛡️",
                "reqs": (
                    "`✅` Edad mínima requerida: **16 años** cumplidos.\n"
                    "`✅` Micrófono funcional y presencia activa en Discord y Minecraft.\n"
                    "`✅` Cero historial de sanciones graves o toxicidad en la red.\n"
                    "`✅` Madurez, objetividad y respeto estricto del criterio del staff."
                )
            },
            "postulacion_media": {
                "name": "Media / Creador de Contenido",
                "emoji": "🎥",
                "reqs": (
                    "`✅` Canales activos en Twitch, YouTube o TikTok.\n"
                    "`✅` Compromiso para realizar directos o vídeos recurrentes en ThunderMC.\n"
                    "`✅` Contenido respetuoso acorde a la imagen de marca de la network.\n"
                    "`✅` Comunidad afín a Minecraft y videojuegos."
                )
            },
            "postulacion_contribuidor": {
                "name": "Contribuidor Oficial",
                "emoji": "🛠️",
                "reqs": (
                    "`✅` Especialidades: Donación, Diseñador Gráfico, Builder o Developer.\n"
                    "`✅` Portafolio o demostración tangible de trabajos previos.\n"
                    "`✅` Capacidad para trabajar en equipo y cumplir plazos fijados.\n"
                    "`✅` Compromiso con los estándares de calidad de ThunderMC."
                )
            }
        }
        
        cat = info_map.get(selected_val, info_map["postulacion_staff"])
        
        terms_embed = {
            "title": f"{cat['emoji']} Términos, Requisitos & Seguridad | {cat['name']}",
            "description": (
                f"Has iniciado el proceso de postulación para el área de **{cat['name']}**.\n"
                "-# ʟᴇᴇ ᴄᴏɴ ᴀᴛᴇɴᴄɪᴏ́ɴ ʟᴀꜱ ꜱɪɢᴜɪᴇɴᴛᴇꜱ ᴄᴏɴᴅɪᴄɪᴏɴᴇꜱ ᴀɴᴛᴇꜱ ᴅᴇ ᴄᴏɴᴛɪɴᴜᴀʀ\n\n"
                "**Requisitos Indispensables:**\n"
                f"{cat['reqs']}\n\n"
                "**🔒 Cláusula de Seguridad y Protección de Datos:**\n"
                "> La información aportada será tratada de manera estrictamente confidencial y exclusivamente por la directiva de ThunderMC.\n"
                "> Al continuar, declaras formalmente que todos los datos suministrados son reales y verídicos. Falsear edad, nick o experiencia supondrá la **expulsión inmediata y veto permanente** de cualquier convocatoria futura.\n\n"
                "**⏱️ Tiempos de Evaluación:**\n"
                "> Tras enviar el formulario, el equipo revisará tu ficha. Recibirás respuesta por mensaje directo (DM) en un plazo estimado de hasta **3 días hábiles**."
            ),
            "color": 16762880,
            "footer": {
                "text": "ThunderMC Convocatorias • Pulsa el botón inferior para abrir tu formulario"
            }
        }
        
        resp = {
            "type": 4,
            "data": {
                "flags": 64,  # Efímero
                "embeds": [terms_embed],
                "components": [
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 2,
                                "style": 3,  # Verde / Success
                                "label": "Acepto los Términos y Requisitos",
                                "emoji": {"name": "✅"},
                                "custom_id": f"btn_accept_terms_{selected_val}"
                            }
                        ]
                    }
                ]
            }
        }
        send_interaction_response(inter_id, inter_token, resp)
        print("   -> Embed efímero de Términos y Condiciones enviado.")
        return

    # =========================================================================
    # 2. CLICK EN EL TICK (BOTÓN VERDE): APERTURA DEL MODAL
    # =========================================================================
    if custom_id.startswith("btn_accept_terms_"):
        post_type = custom_id.replace("btn_accept_terms_", "")
        print(f"   -> Usuario aceptó términos. Desplegando modal para: {post_type}")
        
        modal_payload = None
        
        if post_type == "postulacion_staff":
            modal_payload = {
                "type": 9,
                "data": {
                    "custom_id": "modal_submit_staff",
                    "title": "Postulación Staff | ThunderMC",
                    "components": [
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_nombre_real",
                                    "label": "Nombre Real",
                                    "style": 1,
                                    "placeholder": "Tu nombre y apellido real",
                                    "min_length": 2,
                                    "max_length": 80,
                                    "required": True
                                }
                            ]
                        },
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_nick_edad",
                                    "label": "Nick de Minecraft y Edad (Mínimo 16)",
                                    "style": 1,
                                    "placeholder": "Ej: Steve_Thunder | 17 años",
                                    "min_length": 3,
                                    "max_length": 60,
                                    "required": True
                                }
                            ]
                        },
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_pais",
                                    "label": "País de Nacimiento",
                                    "style": 1,
                                    "placeholder": "Ej: España, México, Colombia, Argentina, Chile...",
                                    "min_length": 2,
                                    "max_length": 50,
                                    "required": True
                                }
                            ]
                        },
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_horas_exp",
                                    "label": "Horas Jugadas y Experiencia como Staff",
                                    "style": 2,
                                    "placeholder": "Horas en el servidor y detalles de servidores previos donde fuiste staff...",
                                    "min_length": 10,
                                    "max_length": 1000,
                                    "required": True
                                }
                            ]
                        },
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_motivo",
                                    "label": "¿Por qué quieres ser Staff en ThunderMC?",
                                    "style": 2,
                                    "placeholder": "¿Qué cualidades aportarías y qué te motiva a unirte a nuestro equipo?",
                                    "min_length": 15,
                                    "max_length": 1000,
                                    "required": True
                                }
                            ]
                        }
                    ]
                }
            }
            
        elif post_type == "postulacion_media":
            modal_payload = {
                "type": 9,
                "data": {
                    "custom_id": "modal_submit_media",
                    "title": "Postulación Media | ThunderMC",
                    "components": [
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_nombre_nick",
                                    "label": "Nombre Real y Nick de Minecraft",
                                    "style": 1,
                                    "placeholder": "Ej: Carlos Gómez / CarlosGamer99",
                                    "min_length": 3,
                                    "max_length": 80,
                                    "required": True
                                }
                            ]
                        },
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_pais_edad",
                                    "label": "País de Nacimiento y Edad (Mínimo 16)",
                                    "style": 1,
                                    "placeholder": "Ej: México | 18 años",
                                    "min_length": 3,
                                    "max_length": 50,
                                    "required": True
                                }
                            ]
                        },
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_twitch",
                                    "label": "Enlace de Twitch",
                                    "style": 1,
                                    "placeholder": "https://twitch.tv/tu_canal (o Deja vacío si no tienes)",
                                    "required": False
                                }
                            ]
                        },
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_youtube",
                                    "label": "Enlace de YouTube",
                                    "style": 1,
                                    "placeholder": "https://youtube.com/@tu_canal (o Deja vacío si no tienes)",
                                    "required": False
                                }
                            ]
                        },
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_tiktok",
                                    "label": "Enlace de TikTok u otras redes",
                                    "style": 1,
                                    "placeholder": "https://tiktok.com/@tu_usuario (o Deja vacío si no tienes)",
                                    "required": False
                                }
                            ]
                        }
                    ]
                }
            }

        elif post_type == "postulacion_contribuidor":
            modal_payload = {
                "type": 9,
                "data": {
                    "custom_id": "modal_submit_contribuidor",
                    "title": "Postulación Contribuidor | ThunderMC",
                    "components": [
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_nombre_nick",
                                    "label": "Nombre Real y Nick de Minecraft",
                                    "style": 1,
                                    "placeholder": "Ej: Alejandro / AlexDev",
                                    "min_length": 3,
                                    "max_length": 80,
                                    "required": True
                                }
                            ]
                        },
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_pais_edad",
                                    "label": "País de Nacimiento y Edad",
                                    "style": 1,
                                    "placeholder": "Ej: España | 19 años",
                                    "min_length": 3,
                                    "max_length": 50,
                                    "required": True
                                }
                            ]
                        },
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_rol_contribucion",
                                    "label": "Área (Donación, Diseñador, Builder, Dev)",
                                    "style": 1,
                                    "placeholder": "Donación Monetaria, Diseñador Gráfico, Builder, Developer...",
                                    "min_length": 3,
                                    "max_length": 80,
                                    "required": True
                                }
                            ]
                        },
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_portafolio",
                                    "label": "Experiencia y Portafolio / Enlaces de trabajo",
                                    "style": 2,
                                    "placeholder": "Indica enlaces a proyectos, Behance, GitHub, capturas de builds, etc...",
                                    "min_length": 10,
                                    "max_length": 1000,
                                    "required": True
                                }
                            ]
                        },
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 4,
                                    "custom_id": "field_propuesta",
                                    "label": "Propuesta de colaboración y disponibilidad",
                                    "style": 2,
                                    "placeholder": "¿En qué área te gustaría apoyar al servidor y cuántas horas puedes aportar?",
                                    "min_length": 10,
                                    "max_length": 1000,
                                    "required": True
                                }
                            ]
                        }
                    ]
                }
            }

        if modal_payload:
            send_interaction_response(inter_id, inter_token, modal_payload)
            print(f"   -> Modal {post_type} enviado exitosamente.")
        return

    # =========================================================================
    # 3. ENVÍO DEL FORMULARIO (MODAL SUBMIT)
    # =========================================================================
    if inter_type == 5:  # APPLICATION_MODAL_SUBMIT
        values = {}
        for row in data.get("components", []):
            for comp in row.get("components", []):
                values[comp.get("custom_id")] = comp.get("value", "").strip()

        db = load_postulaciones()
        db["counter"] += 1
        post_id = f"TH-{db['counter']}"
        now_ts = int(time.time())

        tipo_display = "Desconocido"
        resumen_fields = []

        if custom_id == "modal_submit_staff":
            tipo_display = "Staff / Moderación"
            resumen_fields = [
                {"name": "👤 Nombre Real", "value": values.get("field_nombre_real", "N/A"), "inline": True},
                {"name": "🎮 Nick & Edad", "value": values.get("field_nick_edad", "N/A"), "inline": True},
                {"name": "🌎 País", "value": values.get("field_pais", "N/A"), "inline": True},
                {"name": "⏱️ Horas Jugadas & Experiencia", "value": values.get("field_horas_exp", "N/A"), "inline": False},
                {"name": "💡 ¿Por qué quiere ser Staff?", "value": values.get("field_motivo", "N/A"), "inline": False},
            ]
        elif custom_id == "modal_submit_media":
            tipo_display = "Media / Creador"
            resumen_fields = [
                {"name": "👤 Nombre & Nick", "value": values.get("field_nombre_nick", "N/A"), "inline": True},
                {"name": "🌎 País & Edad", "value": values.get("field_pais_edad", "N/A"), "inline": True},
                {"name": "🟣 Twitch", "value": values.get("field_twitch") or "No indicado", "inline": True},
                {"name": "🔴 YouTube", "value": values.get("field_youtube") or "No indicado", "inline": True},
                {"name": "⚫ TikTok", "value": values.get("field_tiktok") or "No indicado", "inline": True},
            ]
        elif custom_id == "modal_submit_contribuidor":
            tipo_display = "Contribuidor Oficial"
            resumen_fields = [
                {"name": "👤 Nombre & Nick", "value": values.get("field_nombre_nick", "N/A"), "inline": True},
                {"name": "🌎 País & Edad", "value": values.get("field_pais_edad", "N/A"), "inline": True},
                {"name": "🛠️ Área Solicitada", "value": values.get("field_rol_contribucion", "N/A"), "inline": True},
                {"name": "📁 Portafolio / Experiencia", "value": values.get("field_portafolio", "N/A"), "inline": False},
                {"name": "📝 Propuesta & Disponibilidad", "value": values.get("field_propuesta", "N/A"), "inline": False},
            ]

        # Guardar en base de datos
        db["applications"][post_id] = {
            "id": post_id,
            "user_id": user_id,
            "username": user_name,
            "tipo": tipo_display,
            "submitted_at": now_ts,
            "status": "En revision",
            "values": values,
            "resumen_fields": resumen_fields
        }
        save_postulaciones(db)

        # 1. Responder inmediatamente al modal (efímero)
        resp = {
            "type": 4,
            "data": {
                "flags": 64,
                "content": (
                    f"✅ **¡Postulación enviada correctamente!** (ID: `{post_id}`)\n"
                    f"Tu ficha ha sido remitida a la directiva de ThunderMC. Hemos enviado un comprobante a tus mensajes directos (DM).\n"
                    f"Estado actual: **🟡 En revisión** *(puede tardar hasta 3 días hábiles en obtener una respuesta)*."
                )
            }
        }
        send_interaction_response(inter_id, inter_token, resp)
        print(f"   -> Formulario {post_id} registrado en DB. Notificando por DM...")

        # 2. Enviar DM al candidato con comprobante de recepción
        dm_embed = {
            "title": "📨 Postulación Recibida | ThunderMC",
            "description": (
                f"Hola **{user_name}**, hemos recibido con éxito tu solicitud para el área de **{tipo_display}**.\n\n"
                f"**Información de tu expediente:**\n"
                f"> `📌` **ID de Solicitud:** `{post_id}`\n"
                f"> `⏳` **Estado:** `🟡 En revisión` *(puede tardar hasta 3d en obtener una respuesta)*\n"
                f"> `📅` **Fecha de Envío:** <t:{now_ts}:F>\n\n"
                "Nuestro equipo directivo analizará tu perfil. Te mantendremos informado en este mismo chat privado en cuanto se emita una resolución."
            ),
            "color": 16762880,
            "footer": {
                "text": "ThunderMC Network • Sistema Oficial de Selección"
            }
        }
        send_dm_to_user(user_id, {"embeds": [dm_embed]})

        # 3. Enviar ficha completa al canal privado de administración
        admin_embed = {
            "title": f"📥 Nueva Postulación: {tipo_display} | {post_id}",
            "description": (
                f"**Candidato:** <@{user_id}> (`{user_name}`)\n"
                f"**ID de Usuario:** `{user_id}`\n"
                f"**Fecha:** <t:{now_ts}:F> (<t:{now_ts}:R>)\n"
                f"**Estado:** `🟡 En revisión`\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ),
            "fields": resumen_fields,
            "color": 3447003,
            "footer": {
                "text": f"ThunderMC Admin Panel • Ref: {post_id}"
            }
        }
        
        admin_buttons = {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "style": 3,  # Verde / Success
                    "label": "Aceptar Postulación",
                    "emoji": {"name": "✅"},
                    "custom_id": f"admin_accept_{post_id}"
                },
                {
                    "type": 2,
                    "style": 4,  # Rojo / Danger
                    "label": "Rechazar Postulación",
                    "emoji": {"name": "❌"},
                    "custom_id": f"admin_reject_{post_id}"
                },
                {
                    "type": 2,
                    "style": 2,  # Gris / Secondary
                    "label": "Poner en Revisión",
                    "emoji": {"name": "🔍"},
                    "custom_id": f"admin_review_{post_id}"
                }
            ]
        }

        try:
            admin_msg = discord_api("POST", f"/channels/{admin_channel_id}/messages", {
                "embeds": [admin_embed],
                "components": [admin_buttons]
            })
            db["applications"][post_id]["admin_msg_id"] = admin_msg.get("id")
            save_postulaciones(db)
            print(f"   -> Ficha {post_id} enviada al canal privado de admins ({admin_channel_id}).")
        except Exception as e:
            print(f"   -> [Error] No se pudo enviar ficha al canal admin: {e}")
        return

    # =========================================================================
    # 4. ACCIÓN ADMIN: ACEPTAR POSTULACIÓN -> ENVIAR CONTRATO
    # =========================================================================
    if custom_id.startswith("admin_accept_"):
        post_id = custom_id.replace("admin_accept_", "")
        db = load_postulaciones()
        app = db.get("applications", {}).get(post_id)
        
        if not app:
            send_interaction_response(inter_id, inter_token, {
                "type": 4, "data": {"flags": 64, "content": "❌ No se encontró la postulación en la base de datos."}
            })
            return

        cand_id = app["user_id"]
        cand_name = app["username"]
        tipo = app["tipo"]
        
        # Enviar Embed en forma de Contrato Oficial por DM al jugador
        contract_embed = {
            "title": "📜 CONTRATO OFICIAL DE INCORPORACIÓN | THUNDERMC",
            "description": (
                f"Estimado/a **{cand_name}**,\n\n"
                f"Nos complace comunicarte que tu solicitud para formar parte del equipo de **{tipo}** ha sido **APROBADA** por la directiva de ThunderMC.\n\n"
                "Para formalizar tu incorporación y activar tus accesos oficiales, es requisito indispensable leer y aceptar las siguientes cláusulas contractuales:"
            ),
            "color": 3066993,  # Verde esmeralda
            "fields": [
                {
                    "name": "⚖️ Cláusula 1: Compromiso, Conducta y Confidencialidad",
                    "value": (
                        "> • Cumplir y hacer cumplir la normativa de ThunderMC sin favoritismos.\n"
                        "> • Absoluta confidencialidad respecto a canales internos, directrices y herramientas del equipo.\n"
                        "> • Trato impecable, respetuoso y profesional hacia todos los jugadores de la comunidad."
                    ),
                    "inline": False
                },
                {
                    "name": "🎁 Cláusula 2: Recompensas y Beneficios por tu Contribución",
                    "value": (
                        "> `⭐` **Rango y Rol Exclusivo:** Asignación inmediata del rango correspondiente en Discord y Minecraft.\n"
                        "> `🗝️` **Beneficios In-Game Mensuales:** Paquete de llaves exclusivas, perks cosméticos y pase de temporada.\n"
                        "> `💎` **Comisiones & Tienda:** Para Media y Desarrolladores, porcentaje de comisiones y código de creador oficial en la tienda Tebex.\n"
                        "> `🏛️` **Voz y Voto:** Acceso directo a las reuniones de coordinación y planificación estratégica de la network."
                    ),
                    "inline": False
                },
                {
                    "name": "📌 Cláusula 3: Periodo de Prueba",
                    "value": (
                        "> Tu incorporación contará con un periodo de adaptación supervisado por directores para garantizar tu correcta integración al flujo de trabajo."
                    ),
                    "inline": False
                }
            ],
            "footer": {
                "text": f"ThunderMC Team • Contrato ID: {post_id} • Pulsa el botón inferior para firmar"
            }
        }

        sign_buttons = {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "style": 3,
                    "label": "✍️ Firmar y Aceptar Contrato",
                    "custom_id": f"user_sign_contract_{post_id}"
                },
                {
                    "type": 2,
                    "style": 4,
                    "label": "Declinar Propuesta",
                    "custom_id": f"user_decline_contract_{post_id}"
                }
            ]
        }

        dm_res = send_dm_to_user(cand_id, {
            "embeds": [contract_embed],
            "components": [sign_buttons]
        })

        # Actualizar embed en canal admin
        app["status"] = "Contrato Enviado"
        save_postulaciones(db)

        # Modificar mensaje en canal admin para reflejar que se envió el contrato
        if interaction.get("message"):
            msg_embeds = interaction["message"].get("embeds", [])
            if msg_embeds:
                emb = msg_embeds[0]
                emb["color"] = 15844367  # Dorado
                emb["description"] = emb.get("description", "").replace("`🟡 En revisión`", f"`📨 Contrato Enviado por <@{user_id}>`")
                resp = {
                    "type": 7,  # UPDATE_MESSAGE
                    "data": {
                        "embeds": [emb],
                        "components": [
                            {
                                "type": 1,
                                "components": [
                                    {
                                        "type": 2,
                                        "style": 3,
                                        "label": "Contrato Enviado (Esperando Firma)",
                                        "disabled": True,
                                        "custom_id": "dummy_sent"
                                    }
                                ]
                            }
                        ]
                    }
                }
                send_interaction_response(inter_id, inter_token, resp)
                print(f"   -> Contrato enviado por DM al candidato {cand_name} ({cand_id}).")
                return

    # =========================================================================
    # 5. ACCIÓN CANDIDATO: FIRMAR CONTRATO -> BIENVENIDA + INVITACIÓN + ROL
    # =========================================================================
    if custom_id.startswith("user_sign_contract_"):
        post_id = custom_id.replace("user_sign_contract_", "")
        db = load_postulaciones()
        app = db.get("applications", {}).get(post_id)

        if not app:
            send_interaction_response(inter_id, inter_token, {
                "type": 4, "data": {"flags": 64, "content": "❌ Contrato no localizado."}
            })
            return

        cand_id = app["user_id"]
        tipo = app["tipo"]
        
        # Generar invitación de un solo uso
        invite_link = create_single_use_invite()
        
        # Asignar rol en el servidor si existe
        role_assigned = False
        try:
            # Buscar rol por coincidencia de nombre o asignar rol base
            roles = discord_api("GET", f"/guilds/{guild_id}/roles")
            target_role = None
            for r in roles:
                rname = r["name"].lower()
                if "staff" in tipo.lower() and "staff" in rname:
                    target_role = r["id"]
                    break
                elif "media" in tipo.lower() and ("media" in rname or "creador" in rname):
                    target_role = r["id"]
                    break
                elif "contribuidor" in tipo.lower() and ("builder" in rname or "dev" in rname or "team" in rname):
                    target_role = r["id"]
                    break
            
            if target_role:
                discord_api("PUT", f"/guilds/{guild_id}/members/{cand_id}/roles/{target_role}")
                role_assigned = True
        except Exception as e:
            print(f"[Role Warning] No se pudo asignar rol automáticamente: {e}")

        welcome_embed = {
            "title": "🎉 ¡Felicidades! Ahora eres parte del Team Thunder",
            "description": (
                f"**¡Tu contrato ha quedado formalmente firmado y registrado!**\n\n"
                f"Te damos la bienvenida al equipo oficial de ThunderMC como **{tipo}**.\n\n"
                f"**🔗 Tu invitación privada y exclusiva (de un solo uso):**\n"
                f"> {invite_link}\n\n"
                "**Próximos Pasos:**\n"
                "`1️⃣` Accede al Discord mediante el enlace proporcionado.\n"
                "`2️⃣` Dirígete al canal de coordinación interna para sincronizarte con el resto del equipo.\n"
                "`3️⃣` ¡Mucho éxito en esta nueva etapa junto a la familia Thunder!"
            ),
            "color": 3066993,
            "footer": {
                "text": "ThunderMC Network • ¡Bienvenid@ al Equipo!"
            }
        }

        # Actualizar el DM del usuario
        send_interaction_response(inter_id, inter_token, {
            "type": 7,  # UPDATE_MESSAGE
            "data": {
                "embeds": [welcome_embed],
                "components": []  # Retirar botones tras firmar
            }
        })

        # Notificar en canal admin que el usuario ya firmó
        app["status"] = "Aceptado y Firmado"
        save_postulaciones(db)

        try:
            discord_api("POST", f"/channels/{admin_channel_id}/messages", {
                "content": (
                    f"🎉 **¡INCORPORACIÓN COMPLETADA!** <@{cand_id}> (`{app['username']}`) ha **firmado su contrato** "
                    f"para `{tipo}`. Invitación de un solo uso generada y enviada por DM."
                )
            })
        except Exception as e:
            print(f"Error al notificar firma en canal admin: {e}")
        return

    # =========================================================================
    # 6. ACCIÓN ADMIN: RECHAZAR POSTULACIÓN -> ABRIR MODAL DE MOTIVO
    # =========================================================================
    if custom_id.startswith("admin_reject_"):
        post_id = custom_id.replace("admin_reject_", "")
        print(f"   -> Admin inició rechazo para: {post_id}. Desplegando modal de motivo...")
        
        modal_reject = {
            "type": 9,
            "data": {
                "custom_id": f"modal_reason_reject_{post_id}",
                "title": f"Rechazar Postulación {post_id}",
                "components": [
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 4,
                                "custom_id": "field_reject_reason",
                                "label": "Motivo del Rechazo (Se enviará al usuario)",
                                "style": 2,
                                "placeholder": "Explica con respeto y criterio qué aspectos no se ajustaron al perfil requerido...",
                                "min_length": 10,
                                "max_length": 1000,
                                "required": True
                            }
                        ]
                    }
                ]
            }
        }
        send_interaction_response(inter_id, inter_token, modal_reject)
        return

    # =========================================================================
    # 7. SUBMIT DEL MOTIVO DE RECHAZO (ADMIN MODAL SUBMIT)
    # =========================================================================
    if inter_type == 5 and custom_id.startswith("modal_reason_reject_"):
        post_id = custom_id.replace("modal_reason_reject_", "")
        reason = ""
        for row in data.get("components", []):
            for comp in row.get("components", []):
                if comp.get("custom_id") == "field_reject_reason":
                    reason = comp.get("value", "").strip()

        db = load_postulaciones()
        app = db.get("applications", {}).get(post_id)
        
        if not app:
            send_interaction_response(inter_id, inter_token, {
                "type": 4, "data": {"flags": 64, "content": "❌ Solicitud no encontrada."}
            })
            return

        cand_id = app["user_id"]
        cand_name = app["username"]
        tipo = app["tipo"]

        # Enviar DM al usuario con la resolución y motivo
        reject_embed = {
            "title": "Resolución de tu Postulación | ThunderMC",
            "description": (
                f"Estimado/a **{cand_name}**,\n\n"
                f"Queremos agradecerte sinceramente el tiempo, interés y entusiasmo dedicado al postularte para el área de **{tipo}** en ThunderMC.\n\n"
                "Tras revisar minuciosamente tu perfil, lamentamos informarte de que en esta ocasión **tu solicitud no ha sido seleccionada**.\n\n"
                "**📋 Motivo de la Decisión:**\n"
                f"> {reason}\n\n"
                "**🌱 Futuras Convocatorias:**\n"
                "Nuestros procesos de selección son altamente competitivos y rigurosos. Te animamos a continuar disfrutando de la comunidad de ThunderMC y a presentar tu candidatura en futuras aperturas tras acumular mayor experiencia."
            ),
            "color": 15158332,  # Rojo elegante
            "footer": {
                "text": "ThunderMC Network • Gracias por tu interés en formar parte del proyecto"
            }
        }
        send_dm_to_user(cand_id, {"embeds": [reject_embed]})

        # Actualizar DB
        app["status"] = "Rechazada"
        app["reject_reason"] = reason
        save_postulaciones(db)

        # Responder al admin
        send_interaction_response(inter_id, inter_token, {
            "type": 4,
            "data": {
                "flags": 64,
                "content": f"✅ La postulación `{post_id}` ha sido **rechazada** y se le ha notificado por DM a <@{cand_id}> con el motivo especificado."
            }
        })

        # Notificar en canal admin
        try:
            discord_api("POST", f"/channels/{admin_channel_id}/messages", {
                "content": (
                    f"❌ **POSTULACIÓN RECHAZADA:** `{post_id}` (<@{cand_id}>) por <@{user_id}>.\n"
                    f"**Motivo:** *\"{reason}\"*"
                )
            })
        except Exception as e:
            print(f"Error al notificar en canal admin: {e}")
        return

    # =========================================================================
    # 8. ACCIÓN ADMIN: PONER EN REVISIÓN
    # =========================================================================
    if custom_id.startswith("admin_review_"):
        post_id = custom_id.replace("admin_review_", "")
        send_interaction_response(inter_id, inter_token, {
            "type": 4,
            "data": {
                "flags": 64,
                "content": f"🔍 Postulación `{post_id}` marcada como **En Revisión Activa** por tu parte."
            }
        })
        try:
            discord_api("POST", f"/channels/{admin_channel_id}/messages", {
                "content": f"🔍 La postulación `{post_id}` está siendo evaluada activamente por <@{user_id}>."
            })
        except Exception as e:
            pass
        return

    # =========================================================================
    # 9. NORMATIVA EFÍMERA (Compatibilidad con el menú de reglas)
    # =========================================================================
    if custom_id == "select_reglas_normativa":
        selected_val = data.get("values", [""])[0]
        target_embed = None
        if selected_val == "reglas_generales" and os.path.exists(rg_file):
            with open(rg_file, "r", encoding="utf-8") as f:
                target_embed = json.load(f).get("embeds", [None])[0]
        elif selected_val == "reglas_discord" and os.path.exists(rd_file):
            with open(rd_file, "r", encoding="utf-8") as f:
                target_embed = json.load(f).get("embeds", [None])[0]

        if target_embed:
            send_interaction_response(inter_id, inter_token, {
                "type": 4,
                "data": {
                    "flags": 64,
                    "embeds": [target_embed]
                }
            })
            print(f"   -> Normativa efímera ({selected_val}) enviada a {user_name}.")
        return

    # =========================================================================
    # 10. SORTEOS (Compatibilidad)
    # =========================================================================
    if custom_id == "sorteo_participar":
        entries = get_sorteo_entries()
        already = any(e.get("userId") == user_id for e in entries)
        if already:
            msg = (cfg_sorteo or {}).get("already_registered", "¡Ya estás participando en el sorteo!")
        else:
            entries.append({"userId": user_id, "username": user_name, "joinedAt": int(time.time())})
            save_sorteo_entries(entries)
            msg = (cfg_sorteo or {}).get("success_registration", "¡Te has registrado con éxito en el sorteo!")
        send_interaction_response(inter_id, inter_token, {
            "type": 4, "data": {"flags": 64, "content": msg}
        })
        return

async def gateway_runner():
    gateway_url = "wss://gateway.discord.gg/?v=10&encoding=json"
    
    while True:
        try:
            print("\nConectando al Gateway de Discord en tiempo real...")
            async with websockets.connect(gateway_url, max_size=10_000_000) as ws:
                heartbeat_task = None
                seq = None
                
                async for message in ws:
                    payload = json.loads(message)
                    op = payload.get("op")
                    t = payload.get("t")
                    d = payload.get("d")
                    s = payload.get("s")
                    if s is not None:
                        seq = s

                    # Op 10: Hello -> Iniciar Heartbeat e Identificar
                    if op == 10:
                        interval = d["heartbeat_interval"] / 1000.0
                        print(f"Gateway Hello recibido. Heartbeat: {interval}s")
                        
                        async def heartbeat_loop(interval):
                            try:
                                while True:
                                    await asyncio.sleep(interval)
                                    await ws.send(json.dumps({"op": 1, "d": seq}))
                            except asyncio.CancelledError:
                                pass

                        heartbeat_task = asyncio.create_task(heartbeat_loop(interval))
                        
                        # Op 2: Identify
                        identify_payload = {
                            "op": 2,
                            "d": {
                                "token": token,
                                "intents": 0,
                                "properties": {
                                    "os": "windows",
                                    "browser": "thundermc_bot",
                                    "device": "thundermc_bot"
                                },
                                "presence": {
                                    "status": "online",
                                    "activities": [
                                        {
                                            "name": "thundermc.es",
                                            "type": 0,
                                            "state": "thundermc.es"
                                        }
                                    ]
                                }
                            }
                        }
                        await ws.send(json.dumps(identify_payload))
                        print("Identificación enviada. Bot escuchando eventos...")

                    # Op 11: Heartbeat ACK
                    elif op == 11:
                        pass

                    # Op 0: Dispatch
                    elif op == 0:
                        if t == "READY":
                            bot_user = d.get("user", {}).get("username")
                            print(f"BOT CONECTADO Y OPERATIVO: {bot_user}")
                            print("Esperando postulaciones e interacciones de usuarios...")
                        elif t == "INTERACTION_CREATE":
                            asyncio.create_task(handle_interaction(d))

        except Exception as e:
            print(f"[Gateway Error] Desconexión: {e}. Reconectando en 5 segundos...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(gateway_runner())
    except KeyboardInterrupt:
        print("\nGateway detenido por el usuario.")
