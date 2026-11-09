package com.thundermc.mounts.listener;

import com.thundermc.mounts.ThunderMounts;
import com.thundermc.mounts.gui.MountGui;
import com.thundermc.mounts.model.ActiveMount;
import com.thundermc.mounts.model.HorseArmor;
import com.thundermc.mounts.model.HorseStyle;
import com.thundermc.mounts.model.MountData;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Sound;
import org.bukkit.entity.Entity;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityDamageEvent;
import org.bukkit.event.entity.EntityDismountEvent;
import org.bukkit.event.entity.EntityMountEvent;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.player.PlayerInteractEntityEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.event.vehicle.VehicleEnterEvent;

public class MountListener implements Listener {

    private final ThunderMounts plugin;

    public MountListener(ThunderMounts plugin) {
        this.plugin = plugin;
    }

    @EventHandler
    public void onInventoryClick(InventoryClickEvent event) {
        String title = event.getView().getTitle();

        if (!title.equals(MountGui.GUI_TITLE)) {
            return;
        }

        event.setCancelled(true);
        if (!(event.getWhoClicked() instanceof Player player)) return;

        int slot = event.getRawSlot();
        if (slot < 0 || slot >= MountGui.GUI_SIZE) return;

        // Slot 53: Cerrar menú
        if (slot == 53) {
            player.closeInventory();
            player.playSound(player.getLocation(), Sound.BLOCK_WOODEN_DOOR_CLOSE, 0.7f, 1.0f);
            return;
        }

        // Slot 45: Brujula (Info)
        if (slot == 45) {
            player.playSound(player.getLocation(), Sound.UI_BUTTON_CLICK, 0.7f, 1.2f);
            return;
        }

        // Slot 42: Selector de Armadura
        if (slot == 42) {
            MountData data = plugin.getMountManager().getMountData(player);
            HorseArmor nextArmor = data.getSelectedArmor().next();
            data.setSelectedArmor(nextArmor);
            plugin.getMountManager().updateActiveMountArmor(player, nextArmor);
            player.playSound(player.getLocation(), Sound.ITEM_ARMOR_EQUIP_DIAMOND, 0.8f, 1.2f);
            MountGui.open(player, plugin);
            return;
        }

        // Slot 49: Desmontar / Guardar montura activa
        if (slot == 49) {
            if (plugin.getMountManager().hasActiveMount(player)) {
                plugin.getMountManager().despawnMount(player);
                player.playSound(player.getLocation(), Sound.ENTITY_HORSE_ARMOR, 0.8f, 1.0f);
                MountGui.open(player, plugin);
            }
            return;
        }

        // Selección directa de estilo de corcel
        HorseStyle clickedStyle = HorseStyle.fromSlot(slot);
        if (clickedStyle != null) {
            player.closeInventory();
            plugin.getMountManager().spawnMount(player, clickedStyle);
        }
    }

    /**
     * Al bajarse del caballo, despawnearlo inmediatamente
     */
    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onEntityDismount(EntityDismountEvent event) {
        if (event.getEntity() instanceof Player player) {
            ActiveMount am = plugin.getMountManager().getActiveMount(player);
            if (am != null && am.getEntity().equals(event.getDismounted())) {
                Bukkit.getScheduler().runTask(plugin, () -> {
                    if (plugin.getMountManager().hasActiveMount(player)) {
                        plugin.getMountManager().despawnMount(player);
                        player.sendMessage(ChatColor.translateAlternateColorCodes('&',
                            "&e[Montura] &7Has desmontado de tu corcel. Usa &6/montura &7para volver a cabalgar."));
                    }
                });
            }
        }
    }

    /**
     * Prohibición absoluta de que cualquier otro jugador monte el corcel
     */
    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = true)
    public void onEntityMount(EntityMountEvent event) {
        Entity mount = event.getMount();
        for (ActiveMount am : plugin.getMountManager().getPlayerMounts()) {
            if (am.getEntity().equals(mount)) {
                if (!event.getEntity().getUniqueId().equals(am.getPlayerUuid())) {
                    event.setCancelled(true);
                    if (event.getEntity() instanceof Player intruder) {
                        intruder.sendMessage(ChatColor.translateAlternateColorCodes('&',
                            "&c&l¡ALTO! &7Este corcel no te pertenece."));
                        intruder.playSound(intruder.getLocation(), Sound.ENTITY_VILLAGER_NO, 1.0f, 1.0f);
                    }
                }
                return;
            }
        }
    }

    /**
     * Doble verificación anti-robo al intentar subirse al vehículo
     */
    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = true)
    public void onVehicleEnter(VehicleEnterEvent event) {
        Entity vehicle = event.getVehicle();
        for (ActiveMount am : plugin.getMountManager().getPlayerMounts()) {
            if (am.getEntity().equals(vehicle)) {
                if (!event.getEntered().getUniqueId().equals(am.getPlayerUuid())) {
                    event.setCancelled(true);
                    if (event.getEntered() instanceof Player intruder) {
                        intruder.sendMessage(ChatColor.translateAlternateColorCodes('&',
                            "&c&l¡ALTO! &7Este corcel no te pertenece."));
                        intruder.playSound(intruder.getLocation(), Sound.ENTITY_VILLAGER_NO, 1.0f, 1.0f);
                    }
                }
                return;
            }
        }
    }

    /**
     * Evitar que otros jugadores abran el inventario o interactúen con el caballo
     */
    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = true)
    public void onPlayerInteractEntity(PlayerInteractEntityEvent event) {
        Entity clicked = event.getRightClicked();
        for (ActiveMount am : plugin.getMountManager().getPlayerMounts()) {
            if (am.getEntity().equals(clicked)) {
                Player clicker = event.getPlayer();
                if (!clicker.getUniqueId().equals(am.getPlayerUuid())) {
                    event.setCancelled(true);
                    clicker.sendMessage(ChatColor.translateAlternateColorCodes('&',
                        "&c&l¡ALTO! &7Este corcel no te pertenece."));
                    clicker.playSound(clicker.getLocation(), Sound.ENTITY_VILLAGER_NO, 1.0f, 1.0f);
                }
                return;
            }
        }
    }

    /**
     * Proteger al corcel de cualquier tipo de daño
     */
    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = true)
    public void onEntityDamage(EntityDamageEvent event) {
        Entity entity = event.getEntity();
        for (ActiveMount am : plugin.getMountManager().getPlayerMounts()) {
            if (am.getEntity().equals(entity)) {
                event.setCancelled(true);
                return;
            }
        }
    }

    @EventHandler
    public void onPlayerQuit(PlayerQuitEvent event) {
        plugin.getMountManager().despawnMount(event.getPlayer());
    }
}
