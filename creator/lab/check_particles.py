import subprocess

java_code = """public class TestParticles {
    public static void main(String[] args) {
        for (org.bukkit.Particle p : org.bukkit.Particle.values()) {
            if (p.getDataType() != Void.class) {
                System.out.println(p.name() + " -> " + p.getDataType().getName());
            }
        }
    }
}
"""

with open("creator/lab/TestParticles.java", "w", encoding="utf-8") as f:
    f.write(java_code)

import subprocess, glob

cp = ";".join(glob.glob("creator/lib/*.jar"))

res1 = subprocess.run([r"C:\Program Files\Java\jdk-21\bin\javac.exe", "-proc:none", "-cp", cp, "creator/lab/TestParticles.java"], capture_output=True, text=True)
if res1.returncode != 0:
    print("javac error:", res1.stderr)
else:
    res2 = subprocess.run([r"C:\Program Files\Java\jdk-21\bin\java.exe", "-cp", "creator/lab;" + cp, "TestParticles"], capture_output=True, text=True)
    print(res2.stdout)

