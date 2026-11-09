import subprocess, glob

java_code = """public class CheckAllEnum {
    public static void main(String[] args) {
        for (org.bukkit.Particle p : org.bukkit.Particle.values()) {
            System.out.println(p.name() + " -> " + p.getDataType().getName());
        }
    }
}
"""

with open("creator/lab/CheckAllEnum.java", "w", encoding="utf-8") as f:
    f.write(java_code)

cp = ";".join(glob.glob("creator/lib/*.jar"))
subprocess.run([r"C:\Program Files\Java\jdk-21\bin\javac.exe", "-proc:none", "-cp", cp, "creator/lab/CheckAllEnum.java"])
res = subprocess.run([r"C:\Program Files\Java\jdk-21\bin\java.exe", "-cp", "creator/lab;" + cp, "CheckAllEnum"], capture_output=True, text=True)
with open("creator/lab/all_particles.txt", "w") as out:
    out.write(res.stdout)

for line in res.stdout.splitlines():
    if "Color" in line:
        print(line)
