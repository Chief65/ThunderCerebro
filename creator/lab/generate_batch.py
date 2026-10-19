import glob

files = glob.glob('creator/lab/glow/*.yml')
with open('creator/lab/upload_glow.txt', 'w', encoding='utf-8') as out:
    for f in sorted(files):
        clean_path = f.replace('\\', '/')
        name = clean_path.split('/')[-1]
        out.write(f"put {clean_path} plugins/ExecutableItems/items/ThunderMC/{name}\n")
    out.write("exit\n")

print(f"Generated upload_glow.txt with {len(files)} entries.")
