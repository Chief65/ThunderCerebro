import subprocess, glob

java_code = """public class CheckFlash {
    public static void main(String[] args) {
        for (org.bukkit.Particle p : org.bukkit.Particle.values()) {
            if (p.name().contains("FLASH") || p.name().contains("FIREWORK") || p.name().contains("END_ROD") || p.name().contains("EFFECT") || p.getDataType() == org.bukkit.Color.class) {
                System.out.println(p.name() + " -> dataType: " + p.getDataType().getName());
            }
        }
    }
}
"""

with open("creator/lab/CheckFlash.java", "w", encoding="utf-8") as f:
    f.write(java_code)

cp = ";".join(glob.glob("creator/lib/*.jar"))
subprocess.run([r"C:\Program Files\Java\jdk-21\bin\javac.exe", "-proc:none", "-cp", cp, "creator/lab/CheckFlash.java"])
res = subprocess.run([r"C:\Program Files\Java\jdk-21\bin\java.exe", "-cp", "creator/lab;" + cp, "CheckFlash"], capture_output=True, text=True)
print(res.stdout)
