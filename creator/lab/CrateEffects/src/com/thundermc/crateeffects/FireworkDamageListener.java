package com.thundermc.crateeffects;

import org.bukkit.entity.Firework;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityDamageByEntityEvent;

/**
 * Previene cualquier tipo de daño de entidades o jugadores producido por los
 * fuegos artificiales celebratorios generados por CrateEffects.
 */
public class FireworkDamageListener implements Listener {

    public static final String METADATA_KEY = "crate_effects_safe";

    private final CrateEffects plugin;

    public FireworkDamageListener(CrateEffects plugin) {
        this.plugin = plugin;
    }

    @EventHandler(priority = EventPriority.LOWEST, ignoreCancelled = true)
    public void onFireworkDamage(EntityDamageByEntityEvent event) {
        if (!plugin.getEffectConfig().isFireworksPreventDamage()) {
            return;
        }

        if (event.getDamager() instanceof Firework firework) {
            if (firework.hasMetadata(METADATA_KEY)) {
                event.setCancelled(true);
                event.setDamage(0.0);
            }
        }
    }
}
