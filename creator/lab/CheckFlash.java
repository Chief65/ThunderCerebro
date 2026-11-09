public class CheckFlash {
    public static void main(String[] args) {
        for (org.bukkit.Particle p : org.bukkit.Particle.values()) {
            if (p.name().contains("FLASH") || p.name().contains("FIREWORK") || p.name().contains("END_ROD") || p.name().contains("EFFECT") || p.getDataType() == org.bukkit.Color.class) {
                System.out.println(p.name() + " -> dataType: " + p.getDataType().getName());
            }
        }
    }
}
