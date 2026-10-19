import os
import sys
import numpy as np
from PIL import Image
from rembg import remove, new_session

input_gif_path = r"C:\Users\PC\OneDrive\Escritorio\descargas\Whats Up Waiting GIF by Minecraft.gif"
output_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\gif_test"
output_gif_full = os.path.join(output_dir, "frog_transparent_full.gif")
output_gif_avatar = os.path.join(output_dir, "frog_transparent_avatar.gif")

print(f"Cargando GIF original: {input_gif_path}")
gif = Image.open(input_gif_path)
n_frames = gif.n_frames
duration = gif.info.get("duration", 70)

print("Inicializando sesion ONNX con silueta...")
session = new_session("silueta")

processed_frames = []
avatar_frames = []

for f in range(n_frames):
    gif.seek(f)
    frame_rgb = gif.convert("RGB")
    
    # 1. AI segmentation
    frame_rgba = remove(frame_rgb, session=session)
    arr = np.array(frame_rgba).copy()
    
    # Dynamic top eye detection
    orange_top = np.where((arr[44:66, 170:310, 0] > 180) & (arr[44:66, 170:310, 1] > 90) & (arr[44:66, 170:310, 2] < 120))
    top_y = orange_top[0].min() + 44 if len(orange_top[0]) > 0 else 48
    
    # 2. Geometric cleanup
    # Above frog head
    arr[:top_y, :, 3] = 0
    
    # Left side
    arr[:98, :163, 3] = 0       # Iron golem arm
    arr[98:148, :138, 3] = 0    # Left background
    arr[:, :64, 3] = 0          # Leftmost foot bound
    
    # Right side
    arr[:145, 325:, 3] = 0      # Eliminates cactus & spider flicker on the right of the head
    arr[145:, 378:, 3] = 0      # Rightmost foot bound
    
    # Belly floor shadow (between front legs x=216..280 below y=205)
    for y in range(205, arr.shape[0]):
        for x in range(216, 280):
            r, g, b = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
            # If it's dark shadow (not orange/light belly)
            if r < 140 or (r - g) < 20:
                arr[y, x, 3] = 0
    
    # Spider removal between/above the eyes (y in top_y .. top_y + 20)
    for y in range(top_y, min(top_y + 22, 70)):
        for x in range(160, 330):
            if arr[y, x, 3] > 0:
                r, g, b = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
                is_frog_orange = (r > 150 and g > 65 and b < 130 and (r - g) > 15)
                is_frog_sclera = (r > 170 and g > 160 and b > 90)
                is_frog_pupil = (y >= (top_y + 11) and (x <= 225 or x >= 290) and r < 70 and g < 70 and b < 70)
                
                if not (is_frog_orange or is_frog_sclera or is_frog_pupil):
                    arr[y, x, 3] = 0

    clean_img = Image.fromarray(arr)
    processed_frames.append(clean_img)
    
    # 3. Square crop (ratio 1:1) for avatar (centered on frog: x=80..360, y=10..250)
    crop_box = (75, 10, 365, 250) # 290x240 -> let's make it square 260x260
    # Frog bounds: x in 64..378 (width ~314), y in 45..226 (height ~181)
    # Center: x = 221, y = 136. Square of 320x320:
    crop_square = (61, 0, 381, 270) # 320x270 -> or 300x300 padded
    
    # Let's create an exact square canvas 320x320 with frog centered
    square_canvas = Image.new("RGBA", (320, 320), (0, 0, 0, 0))
    # Paste frog at offset x = 320 - 480 / 2... wait, frog is at x=64..378.
    # We can crop (60, 0, 380, 270) which is 320x270, and paste in (0, 25)
    cropped_frog = clean_img.crop((60, 0, 380, 270))
    square_canvas.paste(cropped_frog, (0, 25))
    avatar_frames.append(square_canvas)

print("Guardando GIFs animados optimizados con canal alfa y disposal=2...")

# Save full size transparent gif
processed_frames[0].save(
    output_gif_full,
    save_all=True,
    append_images=processed_frames[1:],
    duration=duration,
    loop=0,
    disposal=2,
    transparency=0
)

# Save square avatar transparent gif
avatar_frames[0].save(
    output_gif_avatar,
    save_all=True,
    append_images=avatar_frames[1:],
    duration=duration,
    loop=0,
    disposal=2,
    transparency=0
)

print(f"Perfeccionado con exito!")
print(f"GIF Completo: {output_gif_full} ({os.path.getsize(output_gif_full)} bytes)")
print(f"GIF Avatar 1:1: {output_gif_avatar} ({os.path.getsize(output_gif_avatar)} bytes)")
