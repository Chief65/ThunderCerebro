package com.thunderstudios.headanimator;

import com.destroystokyo.paper.event.player.PlayerArmorChangeEvent;
import org.bukkit.Bukkit;
import org.bukkit.entity.ArmorStand;
import org.bukkit.entity.ItemFrame;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.block.BlockPlaceEvent;
import org.bukkit.event.entity.EntityPickupItemEvent;
import org.bukkit.event.entity.PlayerDeathEvent;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryCloseEvent;
import org.bukkit.event.inventory.InventoryCreativeEvent;
import org.bukkit.event.inventory.InventoryDragEvent;
import org.bukkit.event.player.PlayerDropItemEvent;
import org.bukkit.event.player.PlayerInteractEntityEvent;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.inventory.ItemStack;

public class HeadListener implements Listener {

    private final HeadAnimatorPlugin plugin;

    public HeadListener(HeadAnimatorPlugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = false)
    public void onInventoryClick(InventoryClickEvent event) {
        if (!(event.getWhoClicked() instanceof Player player)) return;

        plugin.getAnimationManager().normalizeItem(event.getCurrentItem());
        plugin.getAnimationManager().normalizeItem(event.getCursor());

        Bukkit.getScheduler().runTask(plugin, () -> {
            plugin.getAnimationManager().normalizePlayerInventory(player);
        });
    }

    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = false)
    public void onInventoryCreative(InventoryCreativeEvent event) {
        if (!(event.getWhoClicked() instanceof Player player)) return;

        ItemStack cursor = event.getCursor();
        if (plugin.getAnimationManager().normalizeItem(cursor)) {
            event.setCursor(cursor);
        }
        Bukkit.getScheduler().runTask(plugin, () -> {
            plugin.getAnimationManager().normalizePlayerInventory(player);
        });
    }

    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = false)
    public void onInventoryDrag(InventoryDragEvent event) {
        if (!(event.getWhoClicked() instanceof Player player)) return;

        plugin.getAnimationManager().normalizeItem(event.getOldCursor());
        plugin.getAnimationManager().normalizeItem(event.getCursor());

        Bukkit.getScheduler().runTask(plugin, () -> {
            plugin.getAnimationManager().normalizePlayerInventory(player);
        });
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onInventoryClose(InventoryCloseEvent event) {
        if (event.getPlayer() instanceof Player player) {
            plugin.getAnimationManager().normalizePlayerInventory(player);
        }
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onArmorChange(PlayerArmorChangeEvent event) {
        if (event.getSlotType() == PlayerArmorChangeEvent.SlotType.HEAD) {
            Player player = event.getPlayer();
            Bukkit.getScheduler().runTask(plugin, () -> {
                plugin.getAnimationManager().normalizePlayerInventory(player);
            });
        }
    }

    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = true)
    public void onDrop(PlayerDropItemEvent event) {
        ItemStack dropped = event.getItemDrop().getItemStack();
        if (plugin.getAnimationManager().normalizeItem(dropped)) {
            event.getItemDrop().setItemStack(dropped);
        }
    }

    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = true)
    public void onPickup(EntityPickupItemEvent event) {
        if (event.getEntity() instanceof Player player) {
            ItemStack item = event.getItem().getItemStack();
            if (plugin.getAnimationManager().normalizeItem(item)) {
                event.getItem().setItemStack(item);
            }
            Bukkit.getScheduler().runTask(plugin, () -> {
                plugin.getAnimationManager().normalizePlayerInventory(player);
            });
        }
    }

    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = true)
    public void onBlockPlace(BlockPlaceEvent event) {
        ItemStack item = event.getItemInHand();
        if (plugin.getAnimationManager().getAnimationFromItem(item) != null) {
            event.setCancelled(true);
            event.getPlayer().sendMessage(HeadAnimation.colorize("&c✖ No puedes colocar una cabeza animada como bloque."));
        }
    }

    @EventHandler(priority = EventPriority.HIGHEST)
    public void onDeath(PlayerDeathEvent event) {
        for (ItemStack item : event.getDrops()) {
            plugin.getAnimationManager().normalizeItem(item);
        }
    }

    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = true)
    public void onEntityInteract(PlayerInteractEntityEvent event) {
        if (event.getRightClicked() instanceof ItemFrame || event.getRightClicked() instanceof ArmorStand) {
            ItemStack inHand = event.getPlayer().getInventory().getItem(event.getHand());
            if (plugin.getAnimationManager().getAnimationFromItem(inHand) != null) {
                event.setCancelled(true);
                event.getPlayer().sendMessage(HeadAnimation.colorize("&c✖ No puedes colocar una cabeza animada en este soporte."));
            }
        }
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onQuit(PlayerQuitEvent event) {
        plugin.getAnimationManager().normalizePlayerInventory(event.getPlayer());
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onJoin(PlayerJoinEvent event) {
        plugin.getAnimationManager().normalizePlayerInventory(event.getPlayer());
    }
}
