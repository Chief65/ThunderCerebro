package com.thunderstudios.pets.listener;

import com.thunderstudios.pets.ThunderPetsPlugin;
import com.thunderstudios.pets.gui.PetMenuHolder;
import com.thunderstudios.pets.pet.PetModel;
import org.bukkit.Sound;
import org.bukkit.entity.ArmorStand;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityDamageEvent;
import org.bukkit.event.entity.PlayerDeathEvent;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryDragEvent;
import org.bukkit.event.player.PlayerArmorStandManipulateEvent;
import org.bukkit.event.player.PlayerQuitEvent;

public class PetEventListener implements Listener {

    private final ThunderPetsPlugin plugin;

    public PetEventListener(ThunderPetsPlugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler(priority = EventPriority.HIGHEST)
    public void onInventoryClick(InventoryClickEvent event) {
        if (event.getInventory().getHolder() instanceof PetMenuHolder) {
            event.setCancelled(true);

            if (!(event.getWhoClicked() instanceof Player player)) return;

            int rawSlot = event.getRawSlot();
            if (rawSlot < 0 || rawSlot >= event.getInventory().getSize()) return;

            if (rawSlot == 22) {
                // Desactivar mascota
                plugin.getPetManager().despawnPet(player);
                player.playSound(player.getLocation(), Sound.ENTITY_ENDERMAN_TELEPORT, 0.7f, 1.5f);
                player.closeInventory();
                return;
            }

            for (PetModel model : plugin.getPetManager().getModels().values()) {
                if (model.getGuiSlot() == rawSlot) {
                    plugin.getPetManager().togglePet(player, model.getId());
                    player.playSound(player.getLocation(), Sound.ENTITY_PLAYER_LEVELUP, 0.7f, 1.8f);
                    player.closeInventory();
                    return;
                }
            }
        }
    }

    @EventHandler(priority = EventPriority.HIGHEST)
    public void onInventoryDrag(InventoryDragEvent event) {
        if (event.getInventory().getHolder() instanceof PetMenuHolder) {
            event.setCancelled(true);
        }
    }

    @EventHandler
    public void onPlayerQuit(PlayerQuitEvent event) {
        plugin.getPetManager().despawnSilently(event.getPlayer().getUniqueId());
    }

    @EventHandler
    public void onPlayerDeath(PlayerDeathEvent event) {
        plugin.getPetManager().despawnSilently(event.getEntity().getUniqueId());
    }

    @EventHandler(priority = EventPriority.HIGHEST)
    public void onArmorStandManipulate(PlayerArmorStandManipulateEvent event) {
        if (!event.getRightClicked().isPersistent() && event.getRightClicked().isMarker()) {
            event.setCancelled(true);
        }
    }

    @EventHandler(priority = EventPriority.HIGHEST)
    public void onEntityDamage(EntityDamageEvent event) {
        if (event.getEntity() instanceof ArmorStand stand) {
            if (!stand.isPersistent() && stand.isMarker()) {
                event.setCancelled(true);
            }
        }
    }
}
