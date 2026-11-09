package com.thundermc.crops.event;

import com.thundermc.crops.CropZone;
import org.bukkit.block.Block;
import org.bukkit.entity.Player;
import org.bukkit.event.Event;
import org.bukkit.event.HandlerList;

public class ThunderCropHarvestEvent extends Event {

    private static final HandlerList HANDLERS = new HandlerList();

    private final Player player;
    private final Block block;
    private final CropZone zone;
    private final int dropAmount;

    public ThunderCropHarvestEvent(Player player, Block block, CropZone zone, int dropAmount) {
        this.player = player;
        this.block = block;
        this.zone = zone;
        this.dropAmount = dropAmount;
    }

    public Player getPlayer() {
        return player;
    }

    public Block getBlock() {
        return block;
    }

    public CropZone getZone() {
        return zone;
    }

    public int getDropAmount() {
        return dropAmount;
    }

    @Override
    public HandlerList getHandlers() {
        return HANDLERS;
    }

    public static HandlerList getHandlerList() {
        return HANDLERS;
    }
}
