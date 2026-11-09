package com.thundermc.crateeffects;

import org.bukkit.Location;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import su.nightexpress.excellentcrates.api.crate.Reward;
import su.nightexpress.excellentcrates.api.event.CrateObtainRewardEvent;
import su.nightexpress.excellentcrates.crate.impl.Crate;
import su.nightexpress.excellentcrates.crate.impl.Rarity;
import su.nightexpress.excellentcrates.util.pos.WorldPos;

public class RewardEffectListener implements Listener {

    private final CrateEffects plugin;

    public RewardEffectListener(CrateEffects plugin) {
        this.plugin = plugin;
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onCrateReward(CrateObtainRewardEvent event) {
        // Envoltura defensiva total: si algo falla en el efecto, jamás interrumpe ExcellentCrates
        try {
            Player player = event.getPlayer();
            if (player == null || !player.isOnline()) {
                return;
            }

            Crate crate = event.getCrate();
            // Si la crate usa la animación custom 'shulker_box', la celebración ya se reproduce
            // exclusivamente en el clímax de ShulkerOpening (displayWinner). Evitar duplicar el efecto al entregar el premio.
            if (crate != null && "shulker_box".equalsIgnoreCase(crate.getOpeningId())) {
                return;
            }

            Reward reward = event.getReward();

            String rarityId = "default";
            if (reward != null && reward.getRarity() != null) {
                Rarity rarity = reward.getRarity();
                if (rarity.getId() != null && !rarity.getId().isBlank()) {
                    rarityId = rarity.getId();
                }
            } else if (crate != null && crate.getId() != null) {
                rarityId = crate.getId();
            }

            Location targetLoc = resolveEffectLocation(player, crate);

            if (plugin.getEffectConfig().isDebug()) {
                plugin.getLogger().info("Disparando efecto de crate para " + player.getName() +
                        " | Rareza/ID: " + rarityId + " en " + targetLoc);
            }

            AnimationRunner.playRewardAnimation(plugin, targetLoc, player, rarityId);
        } catch (Throwable t) {
            plugin.getLogger().warning("Excepcion atrapada en RewardEffectListener (aislamiento seguro): " + t.getMessage());
            if (plugin.getEffectConfig().isDebug()) {
                t.printStackTrace();
            }
        }
    }

    /**
     * Resuelve el epicentro visual del efecto:
     * Si la caja tiene un bloque en el mundo a menos de 7 bloques del jugador, usa ese bloque.
     * Si no (apertura remota o virtual), usa la ubicación del jugador.
     */
    private Location resolveEffectLocation(Player player, Crate crate) {
        Location playerLoc = player.getLocation();
        if (crate != null && crate.getBlockPositions() != null && !crate.getBlockPositions().isEmpty()) {
            Location closestBlock = null;
            double minDistanceSq = 49.0; // 7 bloques de radio

            for (WorldPos pos : crate.getBlockPositions()) {
                if (pos == null) continue;
                Location loc = pos.toLocation();
                if (loc != null && loc.getWorld() != null && loc.getWorld().equals(playerLoc.getWorld())) {
                    double distSq = loc.distanceSquared(playerLoc);
                    if (distSq < minDistanceSq) {
                        minDistanceSq = distSq;
                        closestBlock = loc;
                    }
                }
            }

            if (closestBlock != null) {
                return closestBlock.clone().add(0.5, 1.05, 0.5);
            }
        }

        // Fallback al jugador
        return playerLoc.clone().add(0, 1.0, 0);
    }
}
