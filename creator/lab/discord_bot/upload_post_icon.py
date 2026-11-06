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

def upload_attachment(channel_id, file_path, file_name):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    boundary = "----ThunderBoundary7MA4YWxkTrZu0gW"
    with open(file_path, "rb") as f:
        img_bytes = f.read()

    parts = [
        f"--{boundary}\r\n".encode("utf-8"),
        f'Content-Disposition: form-data; name="files[0]"; filename="{file_name}"\r\n'.encode("utf-8"),
        b"Content-Type: image/png\r\n\r\n",
        img_bytes,
        f"\r\n--{boundary}--\r\n".encode("utf-8"),
    ]
    data = b"".join(parts)
    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": user_agent,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw)

# Subir roles_bell_thumbnail para obtener su URL de CDN permanente
img_file = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\roles_bell_thumbnail.png"
res_up = upload_attachment(thread_post_id, img_file, "roles_bell_thumbnail.png")
cdn_url = res_up["attachments"][0]["url"]
temp_msg_id = res_up["id"]
print("CDN URL obtenida:", cdn_url)

# Borramos el mensaje temporal con la imagen suelta
discord_api("DELETE", f"/channels/{thread_post_id}/messages/{temp_msg_id}")
print("Mensaje temporal borrado.")

# Guardamos la URL
with open(os.path.join(script_dir, "post_icon_url.txt"), "w", encoding="utf-8") as f:
    f.write(cdn_url)
