import zipfile

z = zipfile.ZipFile("creator/lib/mojang_1.21.11.jar")
# Check all particle types in ParticleTypes.class
import subprocess

res = subprocess.run([
    r"C:\Program Files\Java\jdk-21\bin\javap.exe",
    "-c", "-p",
    "-cp", "creator/lib/mojang_1.21.11.jar",
    "net.minecraft.core.particles.ParticleTypes"
], capture_output=True, text=True)

for line in res.stdout.splitlines():
    if "flash" in line.lower() or "instant" in line.lower() or "effect" in line.lower():
        print(line)
