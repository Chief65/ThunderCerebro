import subprocess

res = subprocess.run([
    r"C:\Program Files\Java\jdk-21\bin\javap.exe",
    "-c", "-v",
    r"creator\lab\CrateEffects\bin\com\thundermc\crateeffects\AnimationRunner$1.class"
], capture_output=True, text=True)

with open("creator/lab/disasm.txt", "w", encoding="utf-8") as f:
    f.write(res.stdout)

print("Saved to creator/lab/disasm.txt, lines:", len(res.stdout.splitlines()))
for line in res.stdout.splitlines():
    if "spawnParticle" in line:
        print(line)
