import zipfile, re

z = zipfile.ZipFile("creator/lib/paper-1.21.11.jar")
data = z.read("org/bukkit/craftbukkit/CraftParticle.class")

# Find all occurrences of Particle enum names or minecraft particle names
matches = re.findall(rb'([a-z0-9_]+:[a-z0-9_]+)', data)
print("NamespacedKeys in CraftParticle:", len(matches))
print(matches[:30])
