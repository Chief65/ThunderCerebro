import subprocess, glob

java_code = """public class CheckKeys {
    public static void main(String[] args) {
        for (org.bukkit.Particle p : new org.bukkit.Particle[]{
            org.bukkit.Particle.FLASH,
            org.bukkit.Particle.END_ROD,
            org.bukkit.Particle.FIREWORK,
            org.bukkit.Particle.ELECTRIC_SPARK,
            org.bukkit.Particle.TOTEM_OF_UNDYING,
            org.bukkit.Particle.ENTITY_EFFECT
        }) {
            System.out.println(p.name() + " -> Key: " + p.getKey() + " | DataType: " + p.getDataType());
        }
    }
}
"""

with open("creator/lab/CheckKeys.java", "w", encoding="utf-8") as f:
    f.write(java_code)

cp = ";".join(glob.glob("creator/lib/*.jar"))
subprocess.run([r"C:\Program Files\Java\jdk-21\bin\javac.exe", "-proc:none", "-cp", cp, "creator/lab/CheckKeys.java"])
res = subprocess.run([r"C:\Program Files\Java\jdk-21\bin\java.exe", "-cp", "creator/lab;" + cp, "CheckKeys"], capture_output=True, text=True)
print(res.stdout)
