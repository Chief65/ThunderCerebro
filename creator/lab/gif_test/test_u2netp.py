import os
from PIL import Image
from rembg import remove, new_session

img_path = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\gif_test\frame_0.png"
out_path = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\gif_test\frame_0_u2netp.png"

print("Inicializando sesion con modelo u2netp (ligero)...")
session = new_session("u2netp")

with open(img_path, "rb") as f:
    input_data = f.read()

output_data = remove(input_data, session=session)

with open(out_path, "wb") as f:
    f.write(output_data)

print(f"Resultado guardado en {out_path}")
