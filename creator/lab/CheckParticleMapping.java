public class CheckParticleMapping {
    public static void main(String[] args) {
        for (org.bukkit.Particle p : new org.bukkit.Particle[]{
            org.bukkit.Particle.FLASH,
            org.bukkit.Particle.END_ROD,
            org.bukkit.Particle.FIREWORK,
            org.bukkit.Particle.ELECTRIC_SPARK,
            org.bukkit.Particle.TOTEM_OF_UNDYING
        }) {
            try {
                net.minecraft.core.particles.ParticleType<?> mc = org.bukkit.craftbukkit.CraftParticle.bukkitToMinecraft(p);
                System.out.println(p.name() + " -> " + mc);
                net.minecraft.core.particles.ParticleOptions opt = org.bukkit.craftbukkit.CraftParticle.createParticleParam(p, null);
                System.out.println(p.name() + " created null param: " + opt);
            } catch (Throwable t) {
                System.out.println(p.name() + " THREW: " + t.getClass().getName() + " - " + t.getMessage());
            }
        }
    }
}
