package com.thunderstudios.pets.listener;

import com.thunderstudios.pets.ThunderPetsPlugin;
import com.thunderstudios.pets.egg.PetEgg;
import com.thunderstudios.pets.util.TextUtil;
import org.bukkit.Material;
import org.bukkit.Particle;
import org.bukkit.Sound;
import org.bukkit.entity.Monster;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.block.Action;
import org.bukkit.event.block.BlockPlaceEvent;
import org.bukkit.event.entity.EntityDeathEvent;
import org.bukkit.event.player.PlayerInteractEvent;
import org.bukkit.inventory.EquipmentSlot;
import org.bukkit.inventory.ItemStack;

public class EggListener implements Listener {

    private final ThunderPetsPlugin plugin;

    public EggListener(ThunderPetsPlugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler(priority = EventPriority.HIGH)
    public void onPlayerInteract(PlayerInteractEvent event) {
        if (event.getAction() != Action.RIGHT_CLICK_AIR && event.getAction() != Action.RIGHT_CLICK_BLOCK) {
            return;
        }

        Player player = event.getPlayer();
        ItemStack mainItem = player.getInventory().getItemInMainHand();
        ItemStack offItem = player.getInventory().getItemInOffHand();

        // 1. Prevención estricta: No permitir colocar el huevo como bloque físico en el mundo
        if (PetEgg.isEgg(mainItem, plugin) || PetEgg.isEgg(offItem, plugin)) {
            if (event.getAction() == Action.RIGHT_CLICK_BLOCK) {
                event.setCancelled(true);
            }
        }

        // 2. Uso de Poción Aceleradora
        if (plugin.getEggManager().isAccelerator(mainItem)) {
            event.setCancelled(true);
            if (event.getHand() != EquipmentSlot.HAND) return;

            ItemStack targetEgg = null;
            if (PetEgg.isEgg(offItem, plugin)) {
                targetEgg = offItem;
            } else {
                for (ItemStack item : player.getInventory().getContents()) {
                    if (PetEgg.isEgg(item, plugin) && !PetEgg.isReadyToHatch(item, plugin)) {
                        targetEgg = item;
                        break;
                    }
                }
            }

            if (targetEgg != null) {
                PetEgg.accelerate(targetEgg, plugin);
                mainItem.setAmount(mainItem.getAmount() - 1);
                player.playSound(player.getLocation(), Sound.BLOCK_ENCHANTMENT_TABLE_USE, 1.0f, 1.2f);
                player.playSound(player.getLocation(), Sound.ENTITY_PLAYER_LEVELUP, 0.8f, 1.5f);
                player.getWorld().spawnParticle(Particle.ENCHANT, player.getLocation().add(0, 1.2, 0), 30, 0.3, 0.3, 0.3, 0.5);
                player.sendMessage(TextUtil.color("&a¡Has aplicado la Poción de Incubación Rápida! El huevo está listo para eclosionar."));
            } else {
                player.sendMessage(TextUtil.color("&cNo tienes ningún Huevo de Mascota en incubación para acelerar."));
            }
            return;
        }

        // 3. Interacción con el Huevo en mano principal
        if (PetEgg.isEgg(mainItem, plugin)) {
            event.setCancelled(true);
            if (event.getHand() != EquipmentSlot.HAND) return;

            // Comprobar si ya está listo para eclosionar
            if (PetEgg.isReadyToHatch(mainItem, plugin)) {
                plugin.getEggManager().hatch(player, mainItem);
                return;
            }

            // Tarea de Alimentación / Cariño
            ItemStack foodFound = null;
            if (offItem != null && offItem.getType().isEdible()) {
                foodFound = offItem;
            } else {
                for (ItemStack invItem : player.getInventory().getContents()) {
                    if (invItem != null && invItem.getType().isEdible() && !PetEgg.isEgg(invItem, plugin)) {
                        foodFound = invItem;
                        break;
                    }
                }
            }

            if (foodFound != null) {
                boolean fed = PetEgg.feedEgg(mainItem, plugin);
                if (fed) {
                    foodFound.setAmount(foodFound.getAmount() - 1);
                    player.playSound(player.getLocation(), Sound.ENTITY_GENERIC_EAT, 1.0f, 1.1f);
                    player.playSound(player.getLocation(), Sound.ENTITY_EXPERIENCE_ORB_PICKUP, 0.8f, 1.5f);
                    player.getWorld().spawnParticle(Particle.HEART, player.getLocation().add(0, 1.5, 0), 6, 0.2, 0.2, 0.2, 0.01);
                    player.sendMessage(TextUtil.color("&a¡Has alimentado a tu huevo con cariño! &7(Tarea de alimentación completada)"));
                    return;
                }
            }

            player.sendMessage(TextUtil.color("&eEste huevo ya está bien alimentado. Revisa tu lore para completar las tareas restantes."));
        }
    }

    @EventHandler(priority = EventPriority.LOWEST)
    public void onBlockPlace(BlockPlaceEvent event) {
        if (PetEgg.isEgg(event.getItemInHand(), plugin)) {
            event.setCancelled(true);
        }
    }

    @EventHandler
    public void onEntityDeath(EntityDeathEvent event) {
        if (event.getEntity() instanceof Monster) {
            Player killer = event.getEntity().getKiller();
            if (killer == null) return;

            for (ItemStack item : killer.getInventory().getContents()) {
                if (PetEgg.isEgg(item, plugin)) {
                    boolean completed = PetEgg.addKill(item, plugin);
                    if (completed) {
                        killer.playSound(killer.getLocation(), Sound.BLOCK_NOTE_BLOCK_BELL, 0.8f, 1.6f);
                        killer.sendActionBar(TextUtil.color("&a✔ ¡Tarea de Protección completada en tu Huevo de Mascota!"));
                    }
                    break;
                }
            }
        }
    }
}
