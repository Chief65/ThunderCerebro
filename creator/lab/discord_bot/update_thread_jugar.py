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

channel_id = "1552723526996336724"
thread_jugar_id = "1568202142278352989"
extra_msg_id = "1568207651719086194"
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

# 1. Eliminar el mensaje extra enviado por error al canal principal #embeds
try:
    discord_api("DELETE", f"/channels/{channel_id}/messages/{extra_msg_id}")
    print(f"1. Eliminado mensaje extra {extra_msg_id} de #embeds")
except Exception as e:
    print(f"1. Aviso al borrar {extra_msg_id}: {e}")

# 2. Limpiar mensajes anteriores dentro del hilo 🕹️・empezar-a-jugar
msgs = discord_api("GET", f"/channels/{thread_jugar_id}/messages?limit=10")
for m in msgs:
    if m.get("type") == 0:
        try:
            discord_api("DELETE", f"/channels/{thread_jugar_id}/messages/{m['id']}")
            print(f"2. Eliminado mensaje antiguo {m['id']} del hilo empezar-a-jugar")
        except Exception as e:
            print(f"2. Aviso: {e}")

# 3. Enviar el nuevo payload Components v2 (sin barra de color, sin imagen grande y con formato intacto) al hilo
json_path = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\entrar_a_jugar_v2.json"
with open(json_path, "r", encoding="utf-8") as f:
    payload = json.load(f)

# Guardar copia también en descargas\reglas
copy_path = r"C:\Users\PC\OneDrive\Escritorio\descargas\reglas\entrar a jugar v2.json"
with open(copy_path, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

res = discord_api("POST", f"/channels/{thread_jugar_id}/messages", payload)
print(f"3. Enviado al hilo {thread_jugar_id} con ID: {res['id']}")
