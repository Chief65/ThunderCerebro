package com.thundermc.ranks.listener;

import com.thundermc.crops.event.ThunderCropHarvestEvent;
import com.thundermc.ranks.ThunderRanks;
import org.bukkit.GameMode;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;

public class ThunderCropsListener implements Listener {

    private final ThunderRanks plugin;

    public ThunderCropsListener(ThunderRanks plugin) {
        this.plugin = plugin;
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onCropHarvest(ThunderCropHarvestEvent event) {
        Player player = event.getPlayer();
        if (player.getGameMode() == GameMode.CREATIVE) return;

        int xp = plugin.getConfig().getInt("xp-sources.custom-crops", 35);
        plugin.getPlayerDataManager().addXp(player, xp);
    }
}
