from PIL import Image
import numpy as np

img = Image.open(r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\gif_test\frame_0_silueta.png")
arr = np.array(img).copy()

# 1. Clean top (y < 46)
arr[:46, :, 3] = 0

# 2. Left of frog:
# y < 90: eye starts at x=163
arr[:90, :163, 3] = 0
# 90 <= y < 148: body starts at x=138
arr[90:148, :138, 3] = 0
# y >= 148: feet extend down to x=65
arr[:, :65, 3] = 0

# 3. Right of frog:
# y < 95: right eye ends at x=325
arr[:95, 325:, 3] = 0
# 95 <= y < 148: right cheek/body ends at x=336
arr[95:148, 336:, 3] = 0
# y >= 148: back foot ends at x=376
arr[:, 376:, 3] = 0

# 4. Spider removal between/above the eyes (y in 46..68)
for y in range(46, 68):
    for x in range(160, 335):
        if arr[y, x, 3] > 0:
            r, g, b = int(arr[y, x, 0]), int(arr[y, x, 1]), int(arr[y, x, 2])
            is_frog_orange = (r > 150 and g > 65 and b < 130 and (r - g) > 15)
            is_frog_sclera = (r > 170 and g > 160 and b > 90) # yellow sclera
            is_frog_pupil = (y >= 62 and (x <= 225 or x >= 290) and r < 70 and g < 70 and b < 70)
            
            if not (is_frog_orange or is_frog_sclera or is_frog_pupil):
                arr[y, x, 3] = 0

cleaned = Image.fromarray(arr)
cleaned.save(r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\gif_test\frame_0_cleaned.png")
print("Saved frame_0_cleaned.png")
