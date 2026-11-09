package com.thundermc.ranks.listener;

import com.thundermc.ranks.ThunderRanks;
import org.bukkit.GameMode;
import org.bukkit.Material;
import org.bukkit.block.data.Ageable;
import org.bukkit.entity.EntityType;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.block.BlockBreakEvent;
import org.bukkit.event.entity.EntityDeathEvent;
import org.bukkit.event.player.PlayerQuitEvent;

import java.util.HashMap;
import java.util.Map;

public class XpListener implements Listener {

    private final ThunderRanks plugin;
    private final Map<Material, Integer> blockXp = new HashMap<>();
    private final Map<EntityType, Integer> mobXp = new HashMap<>();

    public XpListener(ThunderRanks plugin) {
        this.plugin = plugin;
        loadXpValues();
    }

    public void loadXpValues() {
        blockXp.clear();
        mobXp.clear();

        if (plugin.getConfig().contains("xp-sources.mining")) {
            for (String key : plugin.getConfig().getConfigurationSection("xp-sources.mining").getKeys(false)) {
                try {
                    Material mat = Material.valueOf(key.toUpperCase());
                    int xp = plugin.getConfig().getInt("xp-sources.mining." + key);
                    blockXp.put(mat, xp);
                } catch (Exception ignored) {}
            }
        }

        if (plugin.getConfig().contains("xp-sources.mobs")) {
            for (String key : plugin.getConfig().getConfigurationSection("xp-sources.mobs").getKeys(false)) {
                try {
                    EntityType type = EntityType.valueOf(key.toUpperCase());
                    int xp = plugin.getConfig().getInt("xp-sources.mobs." + key);
                    mobXp.put(type, xp);
                } catch (Exception ignored) {}
            }
        }
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = false)
    public void onBlockBreak(BlockBreakEvent event) {
        Player player = event.getPlayer();
        if (player.getGameMode() == GameMode.CREATIVE) return;

        Material mat = event.getBlock().getType();

        // Si es cultivo, verificar que esté maduro para dar XP
        if (event.getBlock().getBlockData() instanceof Ageable ageable) {
            if (ageable.getAge() < ageable.getMaximumAge()) return;
        }

        if (blockXp.containsKey(mat)) {
            int amount = blockXp.get(mat);
            plugin.getPlayerDataManager().addXp(player, amount);
        }
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onEntityDeath(EntityDeathEvent event) {
        Player killer = event.getEntity().getKiller();
        if (killer == null) return;
        if (killer.getGameMode() == GameMode.CREATIVE) return;

        EntityType type = event.getEntityType();
        if (mobXp.containsKey(type)) {
            int amount = mobXp.get(type);
            plugin.getPlayerDataManager().addXp(killer, amount);
        }
    }

    @EventHandler
    public void onQuit(PlayerQuitEvent event) {
        plugin.getPlayerDataManager().unloadPlayer(event.getPlayer());
    }
}
