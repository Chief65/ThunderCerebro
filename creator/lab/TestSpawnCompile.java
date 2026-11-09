import org.bukkit.Color;
import org.bukkit.Location;
import org.bukkit.Particle;
import org.bukkit.World;

public class TestSpawnCompile {
    public static void test(World world, Location loc) {
        world.spawnParticle(Particle.FLASH, loc, 1, 0.0, 0.0, 0.0, 0.0, Color.WHITE);
    }
}
