public class CheckParticlesInPaper {
    public static void main(String[] args) {
        for (org.bukkit.Particle p : org.bukkit.Particle.values()) {
            if (p.getDataType() == org.bukkit.Color.class) {
                System.out.println("Particle with Color: " + p.name() + " (" + p.getKey() + ")");
            }
        }
    }
}
