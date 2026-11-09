public class CheckKeys {
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
