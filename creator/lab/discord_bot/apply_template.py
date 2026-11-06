import os
import time
import requests

ENV_PATH = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot\.env"
TEMPLATE_CODE = "txxzkw4Cv6Rr"
GUILD_ID = "1552715004669726802"

token = ""
with open(ENV_PATH, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("DISCORD_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()

headers = {
    "Authorization": f"Bot {token}",
    "User-Agent": "ThunderBot (https://thundermc.es, 1.0.0)",
    "Content-Type": "application/json; charset=utf-8"
}

def api_request(method, endpoint, json_data=None):
    url = f"https://discord.com/api/v10{endpoint}"
    while True:
        resp = requests.request(method, url, headers=headers, json=json_data)
        if resp.status_code == 429:
            retry_after = resp.json().get("retry_after", 1.0)
            print(f"[Rate Limit] Esperando {retry_after}s...")
            time.sleep(float(retry_after) + 0.2)
            continue
        return resp

print("--- INICIANDO PROCESO DE APLICACIÓN DE PLANTILLA ---")

# 1. Obtener la plantilla de Discord
print(f"Descargando datos de la plantilla: {TEMPLATE_CODE}...")
tmpl_resp = requests.get(f"https://discord.com/api/v10/guilds/templates/{TEMPLATE_CODE}")
if tmpl_resp.status_code != 200:
    print(f"Error al obtener la plantilla: {tmpl_resp.status_code} {tmpl_resp.text}")
    exit(1)

tmpl_data = tmpl_resp.json()
sg = tmpl_data["serialized_source_guild"]
print(f"Plantilla cargada: '{sg.get('name')}' con {len(sg.get('roles', []))} roles y {len(sg.get('channels', []))} canales.")

# 2. Paso previo: Preservar canales existentes en categoría '📦 BACKUP'
print("\n--- PASO 1: CREANDO CATEGORÍA BACKUP Y MOVIENDO CANALES PREVIOS ---")
curr_channels = api_request("GET", f"/guilds/{GUILD_ID}/channels").json()

# Crear categoría BACKUP
backup_cat_resp = api_request("POST", f"/guilds/{GUILD_ID}/channels", {
    "name": "📦 BACKUP",
    "type": 4,
    "position": 999
})
backup_cat_id = backup_cat_resp.json()["id"]
print(f"Categoría '📦 BACKUP' creada con ID: {backup_cat_id}")

old_categories = []
for ch in curr_channels:
    ch_id = ch["id"]
    ch_type = ch.get("type")
    ch_name = ch.get("name")
    if ch_type == 4:
        old_categories.append(ch_id)
    else:
        # Mover canal a la categoría de BACKUP
        patch_r = api_request("PATCH", f"/channels/{ch_id}", {
            "parent_id": backup_cat_id
        })
        if patch_r.status_code in (200, 201):
            print(f"Canal '{ch_name}' movido a '📦 BACKUP'")
        else:
            print(f"Error moviendo '{ch_name}': {patch_r.status_code}")
        time.sleep(0.3)

# Eliminar categorías vacías anteriores para limpiar la interfaz
for cat_id in old_categories:
    del_r = api_request("DELETE", f"/channels/{cat_id}")
    print(f"Categoría antigua {cat_id} eliminada ({del_r.status_code})")
    time.sleep(0.3)

# 3. Crear / mapear Roles
print("\n--- PASO 2: CLONANDO ROLES DE LA PLANTILLA ---")
existing_roles = api_request("GET", f"/guilds/{GUILD_ID}/roles").json()
existing_roles_by_name = {r["name"]: r for r in existing_roles}
everyone_role = next(r for r in existing_roles if r["name"] == "@everyone")

role_map = {0: everyone_role["id"]}

# Actualizar permisos del rol @everyone si viene en la plantilla
for r in sg.get("roles", []):
    if r.get("id") == 0:
        patch_ev = api_request("PATCH", f"/guilds/{GUILD_ID}/roles/{everyone_role['id']}", {
            "permissions": r.get("permissions", "0")
        })
        print(f"Rol @everyone actualizado con permisos base ({patch_ev.status_code})")
        break

# Crear el resto de roles
for r in sg.get("roles", []):
    t_id = r["id"]
    if t_id == 0:
        continue
    r_name = r["name"]
    # Si ya existe un rol con ese nombre, reusarlo
    if r_name in existing_roles_by_name:
        role_map[t_id] = existing_roles_by_name[r_name]["id"]
        print(f"Rol '{r_name}' ya existente -> Reusado (ID: {role_map[t_id]})")
        continue

    payload = {
        "name": r_name,
        "permissions": r.get("permissions", "0"),
        "color": r.get("color", 0),
        "hoist": r.get("hoist", False),
        "mentionable": r.get("mentionable", False)
    }
    create_r = api_request("POST", f"/guilds/{GUILD_ID}/roles", payload)
    if create_r.status_code in (200, 201):
        new_role = create_r.json()
        role_map[t_id] = new_role["id"]
        print(f"Rol creado: '{r_name}' (ID: {new_role['id']})")
    else:
        print(f"Error creando rol '{r_name}': {create_r.status_code} {create_r.text}")
    time.sleep(0.35)

print(f"Total roles mapeados: {len(role_map)}")

# 4. Crear Categorías y Canales
print("\n--- PASO 3: CLONANDO CATEGORÍAS Y CANALES ---")
channel_map = {}

# Primero: Categorías (type == 4)
for ch in sg.get("channels", []):
    if ch.get("type") == 4:
        t_id = ch["id"]
        name = ch["name"]
        
        # Mapear permisos
        overwrites = []
        for ow in ch.get("permission_overwrites", []):
            mapped_role_id = role_map.get(ow["id"])
            if mapped_role_id:
                overwrites.append({
                    "id": mapped_role_id,
                    "type": ow.get("type", 0),
                    "allow": ow.get("allow", "0"),
                    "deny": ow.get("deny", "0")
                })
        
        payload = {
            "name": name,
            "type": 4,
            "position": ch.get("position", 0),
            "permission_overwrites": overwrites
        }
        create_c = api_request("POST", f"/guilds/{GUILD_ID}/channels", payload)
        if create_c.status_code in (200, 201):
            new_cat = create_c.json()
            channel_map[t_id] = new_cat["id"]
            print(f"Categoría creada: '{name}' (ID: {new_cat['id']})")
        else:
            print(f"Error creando categoría '{name}': {create_c.status_code} {create_c.text}")
        time.sleep(0.4)

# Segundo: Canales no categoría
for ch in sg.get("channels", []):
    ch_type = ch.get("type")
    if ch_type == 4:
        continue
    
    t_id = ch["id"]
    name = ch["name"]
    
    # Omitir canales de tickets residuales
    if name.lower().startswith("ticket-"):
        print(f"Omitiendo canal residual de ticket: '{name}'")
        continue

    parent_id = channel_map.get(ch.get("parent_id"))
    
    overwrites = []
    for ow in ch.get("permission_overwrites", []):
        mapped_role_id = role_map.get(ow["id"])
        if mapped_role_id:
            overwrites.append({
                "id": mapped_role_id,
                "type": ow.get("type", 0),
                "allow": ow.get("allow", "0"),
                "deny": ow.get("deny", "0")
            })
    
    payload = {
        "name": name,
        "type": ch_type,
        "position": ch.get("position", 0),
        "permission_overwrites": overwrites
    }
    if parent_id:
        payload["parent_id"] = parent_id
    if ch.get("topic"):
        payload["topic"] = ch["topic"]
    if ch_type == 2:
        if ch.get("bitrate"):
            payload["bitrate"] = min(ch["bitrate"], 96000)
        if ch.get("user_limit"):
            payload["user_limit"] = ch["user_limit"]
    if ch.get("rate_limit_per_user"):
        payload["rate_limit_per_user"] = ch["rate_limit_per_user"]

    create_c = api_request("POST", f"/guilds/{GUILD_ID}/channels", payload)
    
    # Si falla por ser tipo foro (15) en un servidor sin Comunidad, degradar a texto (0)
    if create_c.status_code == 400 and ch_type == 15:
        print(f"Canal foro '{name}' no soportado (requiere Comunidad). Creando como canal de texto...")
        payload["type"] = 0
        create_c = api_request("POST", f"/guilds/{GUILD_ID}/channels", payload)

    if create_c.status_code in (200, 201):
        new_ch = create_c.json()
        channel_map[t_id] = new_ch["id"]
        print(f"Canal creado [{payload['type']}]: '{name}' (ID: {new_ch['id']})")
    else:
        print(f"Error creando canal '{name}': {create_c.status_code} {create_c.text}")
    time.sleep(0.4)

# Asegurar que BACKUP quede al final absoluto
api_request("PATCH", f"/channels/{backup_cat_id}", {"position": 999})

print("\n--- IMPORTACIÓN COMPLETADA CON ÉXITO ---")
