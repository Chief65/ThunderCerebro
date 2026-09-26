import os

dir_path = "creator/lab"
for tier in range(1, 6):
    file_name = "bolsadedinero.yml" if tier == 1 else f"bolsadedinero_{tier}.yml"
    full_path = os.path.join(dir_path, file_name)
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Reemplazar subtitulos verdes por blancos en animacion
    content = content.replace('&2&o\u0274\u1d07\ua731\u1d04\u026a\ua730\u0280\u1d00\u0274\u1d05\u1d0f...', '&f&o\u0274\u1d07\ua731\u1d04\u026a\ua730\u0280\u1d00\u0274\u1d05\u1d0f...')
    content = content.replace('&a&o\u0274\u1d07\ua731\u1d04\u026a\ua730\u0280\u1d00\u0274\u1d05\u1d0f...', '&f&o\u0274\u1d07\ua731\u1d04\u026a\ua730\u0280\u1d00\u0274\u1d05\u1d0f...')
    content = content.replace('&a&o\u00a1\u0274\u1d07\ua731\u1d04\u026a\ua730\u0280\u1d00\u1d05\u1d0f!', '&f&o\u00a1\u0274\u1d07\ua731\u1d04\u026a\ua730\u0280\u1d00\u1d05\u1d0f!')

    # Reemplazar subtitulos verdes de recompensa por blancos
    content = content.replace('&a\u00a1\u0280\u1d07\u1d04\u1d0f\u1d0d\u1d18\u1d07\u0274\ua731\u1d00 \u1d0f\u0299\u1d1b\u1d07\u0274\u026a\u1d05\u1d00!', '&f\u00a1\u0280\u1d07\u1d04\u1d0f\u1d0d\u1d18\u1d07\u0274\ua731\u1d00 \u1d0f\u0299\u1d1b\u1d07\u0274\u026a\u1d05\u1d00!')
    content = content.replace('&a\u00a1\u1d18\u0280\u1d07\u1d0d\u026a\u1d0f \u1d0d\u1d00\u0278\u026a\u1d0d\u1d0f!', '&f\u00a1\u1d18\u0280\u1d07\u1d0d\u026a\u1d0f \u1d0d\u1d00\u0278\u026a\u1d0d\u1d0f!')
    content = content.replace('&a\u00a1\u1d18\u0280\u1d07\u1d0d\u026a\u1d0f \ua731\u1d18\u0280\u1d07\u1d0d\u1d0f!', '&f\u00a1\u1d18\u0280\u1d07\u1d0d\u026a\u1d0f \ua731\u1d18\u0280\u1d07\u1d0d\u1d0f!')

    # Insertar sonido saddle si no existe
    saddle_cmd = "execute at %player% run playsound minecraft:entity.horse.saddle master %player% ~ ~ ~ 0.9 1.1"
    if saddle_cmd not in content:
        target_amethyst = "execute at %player% run playsound minecraft:block.amethyst_block.hit master %player% ~ ~ ~ 0.8 1.0"
        replacement_sound = f"{target_amethyst}\n    - {saddle_cmd}"
        content = content.replace(target_amethyst, replacement_sound)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Procesado: {file_name}")
