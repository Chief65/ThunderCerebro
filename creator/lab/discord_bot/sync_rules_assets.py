import os
import json
import base64
import urllib.request

script_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot"
env_path = os.path.join(script_dir, ".env")
token = [l.split("=", 1)[1].strip() for l in open(env_path) if l.startswith("DISCORD_BOT_TOKEN=")][0]
app_id = "1552716487100342404"
channel_id = "1552723526996336724"
user_agent = "DiscordBot (https://thundermc.es, 1.0.0)"

def api(method, endpoint, body=None):
    url = f"https://discord.com/api/v10{endpoint}"
    headers = {"Authorization": f"Bot {token}", "User-Agent": user_agent}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}

# 1. Subir emojis a la aplicación
icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"
emojis_to_sync = {
    "th_normativa_w": os.path.join(icons_dir, "icon_normativa_w.png"),
    "th_reglas_gen_w": os.path.join(icons_dir, "icon_reglas_gen_w.png"),
    "th_reglas_dc_w": os.path.join(icons_dir, "icon_reglas_dc_w.png"),
}

existing = {e["name"]: e["id"] for e in api("GET", f"/applications/{app_id}/emojis").get("items", [])}
results = {}

for name, path in emojis_to_sync.items():
    if name in existing:
        results[name] = existing[name]
        print(f"Emoji {name} ya existe -> {existing[name]}")
    else:
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        res = api("POST", f"/applications/{app_id}/emojis", {
            "name": name,
            "image": f"data:image/png;base64,{b64}"
        })
        emoji_id = res["id"]
        results[name] = emoji_id
        print(f"Emoji {name} creado -> {emoji_id}")

# 2. Subir imagen del libro verde a Discord para obtener CDN URL
book_path = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\minecraft_knowledge_book.png"
boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
body = bytearray()
body.extend(f"--{boundary}\r\n".encode("utf-8"))
body.extend(f'Content-Disposition: form-data; name="files[0]"; filename="minecraft_knowledge_book.png"\r\n'.encode("utf-8"))
body.extend(b"Content-Type: image/png\r\n\r\n")
with open(book_path, "rb") as f:
    body.extend(f.read())
body.extend(f"\r\n--{boundary}\r\n".encode("utf-8"))
body.extend(b'Content-Disposition: form-data; name="payload_json"\r\n')
body.extend(b"Content-Type: application/json\r\n\r\n")
body.extend(json.dumps({"content": ""}).encode("utf-8"))
body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

req = urllib.request.Request(f"https://discord.com/api/v10/channels/{channel_id}/messages", data=bytes(body), headers={
    "Authorization": f"Bot {token}",
    "User-Agent": user_agent,
    "Content-Type": f"multipart/form-data; boundary={boundary}"
}, method="POST")

with urllib.request.urlopen(req) as resp:
    msg = json.loads(resp.read().decode("utf-8"))
    book_url = msg["attachments"][0]["url"]
    print("Book URL subido exitosamente:", book_url)
    api("DELETE", f"/channels/{channel_id}/messages/{msg['id']}")

meta_path = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot\rules_assets_meta.json"
with open(meta_path, "w", encoding="utf-8") as f:
    json.dump({"emojis": results, "book_url": book_url}, f, indent=2)

print("SUCCESS: Assets sincronizados.")
