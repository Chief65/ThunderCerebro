public class CheckAllEnum {
    public static void main(String[] args) {
        for (org.bukkit.Particle p : org.bukkit.Particle.values()) {
            System.out.println(p.name() + " -> " + p.getDataType().getName());
        }
    }
}
