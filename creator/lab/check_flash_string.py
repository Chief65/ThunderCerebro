import zipfile

z = zipfile.ZipFile("creator/lib/paper-1.21.11.jar")
data = z.read("org/bukkit/craftbukkit/CraftParticle.class")

# Let's search for "flash" in CraftParticle constants
import re
print("Occurrences of flash:", [m.group(0) for m in re.finditer(rb'[a-zA-Z0-9_/]*flash[a-zA-Z0-9_/]*', data, re.I)])
