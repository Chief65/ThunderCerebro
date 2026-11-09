public class TestParticles {
    public static void main(String[] args) {
        for (org.bukkit.Particle p : org.bukkit.Particle.values()) {
            if (p.getDataType() != Void.class) {
                System.out.println(p.name() + " -> " + p.getDataType().getName());
            }
        }
    }
}
