import subprocess, glob

java_code = """public class CheckParticlesInPaper {
    public static void main(String[] args) {
        for (org.bukkit.Particle p : org.bukkit.Particle.values()) {
            if (p.getDataType() == org.bukkit.Color.class) {
                System.out.println("Particle with Color: " + p.name() + " (" + p.getKey() + ")");
            }
        }
    }
}
"""

with open("creator/lab/CheckParticlesInPaper.java", "w", encoding="utf-8") as f:
    f.write(java_code)

cp = ";".join(glob.glob("creator/lib/*.jar"))
subprocess.run([r"C:\Program Files\Java\jdk-21\bin\javac.exe", "-proc:none", "-cp", cp, "creator/lab/CheckParticlesInPaper.java"])
res = subprocess.run([r"C:\Program Files\Java\jdk-21\bin\java.exe", "-cp", "creator/lab;" + cp, "CheckParticlesInPaper"], capture_output=True, text=True)
print(res.stdout)
