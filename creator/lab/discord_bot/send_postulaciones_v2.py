import os
import json
import urllib.request

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")

token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("DISCORD_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()

thread_post_id = "1568202156090073101"
user_agent = "DiscordBot (https://thundermc.es, 1.0.0)"

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
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}

# 1. Limpiar mensajes antiguos dentro del hilo de postulaciones
print(f"Limpiando mensajes en hilo {thread_post_id}...")
msgs = discord_api("GET", f"/channels/{thread_post_id}/messages?limit=10")
for m in msgs:
    if m.get("type") == 0:
        try:
            discord_api("DELETE", f"/channels/{thread_post_id}/messages/{m['id']}")
            print(f"Eliminado mensaje {m['id']} del hilo de postulaciones")
        except Exception as e:
            print(f"Aviso al borrar: {e}")

# 2. Cargar y enviar el payload Components v2
v2_file = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\menu_postulaciones_v2.json"
with open(v2_file, "r", encoding="utf-8") as f:
    payload = json.load(f)

res = discord_api("POST", f"/channels/{thread_post_id}/messages", payload)
print(f"Enviado Components v2 de Postulaciones al hilo {thread_post_id} con ID: {res['id']}")
