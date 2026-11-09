import subprocess, glob

java_code = """import org.bukkit.Color;
import org.bukkit.Location;
import org.bukkit.Particle;
import org.bukkit.World;

public class TestSpawnCompile {
    public static void test(World world, Location loc) {
        world.spawnParticle(Particle.FLASH, loc, 1, 0.0, 0.0, 0.0, 0.0, Color.WHITE);
    }
}
"""

with open("creator/lab/TestSpawnCompile.java", "w", encoding="utf-8") as f:
    f.write(java_code)

cp = ";".join(glob.glob("creator/lib/*.jar"))
res = subprocess.run([r"C:\Program Files\Java\jdk-21\bin\javac.exe", "-proc:none", "-cp", cp, "creator/lab/TestSpawnCompile.java"], capture_output=True, text=True)
print("Return code:", res.returncode)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
