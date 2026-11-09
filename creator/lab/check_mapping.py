import subprocess

java_code = """public class CheckParticleMapping {
    public static void main(String[] args) {
        for (org.bukkit.Particle p : new org.bukkit.Particle[]{
            org.bukkit.Particle.FLASH,
            org.bukkit.Particle.END_ROD,
            org.bukkit.Particle.FIREWORK,
            org.bukkit.Particle.ELECTRIC_SPARK,
            org.bukkit.Particle.TOTEM_OF_UNDYING
        }) {
            try {
                net.minecraft.core.particles.ParticleType<?> mc = org.bukkit.craftbukkit.CraftParticle.bukkitToMinecraft(p);
                System.out.println(p.name() + " -> " + mc);
                net.minecraft.core.particles.ParticleOptions opt = org.bukkit.craftbukkit.CraftParticle.createParticleParam(p, null);
                System.out.println(p.name() + " created null param: " + opt);
            } catch (Throwable t) {
                System.out.println(p.name() + " THREW: " + t.getClass().getName() + " - " + t.getMessage());
            }
        }
    }
}
"""

with open("creator/lab/CheckParticleMapping.java", "w", encoding="utf-8") as f:
    f.write(java_code)

import glob

cp = ";".join(glob.glob("creator/lib/*.jar"))

res1 = subprocess.run([r"C:\Program Files\Java\jdk-21\bin\javac.exe", "-proc:none", "-cp", cp, "creator/lab/CheckParticleMapping.java"], capture_output=True, text=True)
if res1.returncode != 0:
    print("javac error:", res1.stderr)
else:
    res2 = subprocess.run([r"C:\Program Files\Java\jdk-21\bin\java.exe", "-cp", "creator/lab;" + cp, "CheckParticleMapping"], capture_output=True, text=True)
    print(res2.stdout)
    print(res2.stderr)
