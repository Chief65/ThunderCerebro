package com.thundermc.crops;

import org.bukkit.GameMode;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.Particle;
import org.bukkit.Sound;
import org.bukkit.SoundCategory;
import org.bukkit.block.Block;
import org.bukkit.block.BlockFace;
import org.bukkit.block.data.Ageable;
import org.bukkit.block.data.type.Farmland;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.block.Action;
import org.bukkit.event.block.BlockBreakEvent;
import org.bukkit.event.block.BlockFadeEvent;
import org.bukkit.event.block.BlockFromToEvent;
import org.bukkit.event.block.BlockPlaceEvent;
import org.bukkit.event.block.MoistureChangeEvent;
import org.bukkit.event.player.PlayerInteractEvent;
import org.bukkit.inventory.EquipmentSlot;
import org.bukkit.inventory.ItemStack;
import org.bukkit.scheduler.BukkitRunnable;

import java.util.HashMap;
import java.util.concurrent.ThreadLocalRandom;

public class CropListener implements Listener {

    private final ThunderCrops plugin;

    public CropListener(ThunderCrops plugin) {
        this.plugin = plugin;
    }

    @EventHandler(priority = EventPriority.LOWEST, ignoreCancelled = false)
    public void onBlockBreak(BlockBreakEvent event) {
        Block block = event.getBlock();
        CropZone zone = plugin.getZoneAt(block.getLocation());

        if (zone == null) {
            if (plugin.isSoilProtected(block.getLocation())) {
                Player p = event.getPlayer();
                if (!(p.hasPermission("thundercrops.admin") && p.getGameMode() == GameMode.CREATIVE && p.isSneaking())) {
                    event.setCancelled(true);
                }
            }
            return;
        }

        Player player = event.getPlayer();

        // Bypass para administradores en Creativo agachados para editar el mapa
        if (player.hasPermission("thundercrops.admin") && player.getGameMode() == GameMode.CREATIVE && player.isSneaking()) {
            return;
        }

        // Siempre cancelar para asegurar BYPASS limpio de WorldGuard
        event.setCancelled(true);

        processHarvest(player, block, zone);
    }

    @EventHandler(priority = EventPriority.LOWEST, ignoreCancelled = false)
    public void onPlayerInteract(PlayerInteractEvent event) {
        // Antipisoteo de tierra arada
        if (event.getAction() == Action.PHYSICAL) {
            Block clicked = event.getClickedBlock();
            if (clicked != null && clicked.getType() == Material.FARMLAND) {
                if (plugin.isSoilProtected(clicked.getLocation())) {
                    event.setCancelled(true);
                }
            }
            return;
        }

        // Cosecha opcional con click derecho en mano principal
        if (event.getAction() == Action.RIGHT_CLICK_BLOCK && event.getHand() == EquipmentSlot.HAND) {
            Block clicked = event.getClickedBlock();
            if (clicked == null) return;

            CropZone zone = plugin.getZoneAt(clicked.getLocation());
            if (zone != null && clicked.getType() == zone.getCropMaterial()) {
                event.setCancelled(true);
                processHarvest(event.getPlayer(), clicked, zone);
            }
        }
    }

    private void processHarvest(Player player, Block block, CropZone zone) {
        if (block.getType() != zone.getCropMaterial()) {
            return;
        }

        Location loc = block.getLocation();

        // Evitar procesar si ya está en proceso de animación/crecimiento
        if (plugin.getGrowingBlocks().contains(loc)) {
            return;
        }

        // Verificar si el cultivo está en su etapa máxima (maduro)
        if (block.getBlockData() instanceof Ageable ageable) {
            if (ageable.getAge() < ageable.getMaximumAge()) {
                return;
            }
        }

        // 1. Entregar drop (1-2 de trigo)
        int min = zone.getMinDrop();
        int max = zone.getMaxDrop();
        int amount = (min == max) ? min : ThreadLocalRandom.current().nextInt(min, max + 1);

        if (amount > 0) {
            ItemStack dropItem = new ItemStack(zone.getDropMaterial(), amount);
            if (zone.isGiveToInventory()) {
                HashMap<Integer, ItemStack> leftover = player.getInventory().addItem(dropItem);
                for (ItemStack rem : leftover.values()) {
                    player.getWorld().dropItemNaturally(player.getLocation(), rem);
                }
            } else {
                player.getWorld().dropItemNaturally(loc.clone().add(0.5, 0.3, 0.5), dropItem);
            }

            // Disparar evento para plugins como ThunderRanks
            org.bukkit.Bukkit.getPluginManager().callEvent(
                new com.thundermc.crops.event.ThunderCropHarvestEvent(player, block, zone, amount)
            );
        }

        // 2. Sonido compuesto altamente satisfactorio (recolección crujiente + tintineo)
        player.playSound(loc, Sound.BLOCK_CROP_BREAK, SoundCategory.BLOCKS, 0.8f, 1.0f);
        player.playSound(loc, Sound.ENTITY_EXPERIENCE_ORB_PICKUP, SoundCategory.PLAYERS, 0.5f, 1.45f);
        player.playSound(loc, Sound.BLOCK_SWEET_BERRY_BUSH_PICK_BERRIES, SoundCategory.BLOCKS, 0.6f, 1.25f);

        // 3. Partículas de rotura
        try {
            player.getWorld().spawnParticle(
                Particle.BLOCK,
                loc.clone().add(0.5, 0.3, 0.5),
                10,
                0.2, 0.2, 0.2,
                zone.getCropMaterial().createBlockData()
            );
        } catch (Throwable ignored) {}

        // 4. Enviar ActionBar al jugador
        plugin.sendActionBar(player, plugin.getActionBarMessage());

        // 5. Instaplantar semilla / brote (age = 0)
        Block soil = block.getRelative(BlockFace.DOWN);
        if (soil.getType() != zone.getSoilMaterial()) {
            soil.setType(zone.getSoilMaterial(), false);
        }
        if (soil.getBlockData() instanceof Farmland f) {
            if (f.getMoisture() < f.getMaximumMoisture()) {
                f.setMoisture(f.getMaximumMoisture());
                soil.setBlockData(f, false);
            }
        }

        block.setType(zone.getCropMaterial(), false);
        if (block.getBlockData() instanceof Ageable a) {
            a.setAge(0);
            block.setBlockData(a, false);
        }

        // 6. Iniciar animación secuencial de crecimiento
        plugin.getGrowingBlocks().add(loc);

        int maxAge = (block.getBlockData() instanceof Ageable a) ? a.getMaximumAge() : 7;
        long intervalTicks = zone.getGrowthIntervalTicks(maxAge);

        new BukkitRunnable() {
            int currentAge = 0;

            @Override
            public void run() {
                // Si el bloque ya no es el cultivo (ej. destruido por admin), abortar
                if (block.getType() != zone.getCropMaterial()) {
                    plugin.getGrowingBlocks().remove(loc);
                    cancel();
                    return;
                }

                currentAge++;

                if (block.getBlockData() instanceof Ageable a) {
                    int targetAge = Math.min(currentAge, a.getMaximumAge());
                    a.setAge(targetAge);
                    block.setBlockData(a, false);

                    // Etapa final: emisión de partícula verde sutil de aldeano
                    if (targetAge >= a.getMaximumAge()) {
                        try {
                            block.getWorld().spawnParticle(
                                Particle.HAPPY_VILLAGER,
                                loc.clone().add(0.5, 0.45, 0.5),
                                2,
                                0.12, 0.12, 0.12,
                                0
                            );
                        } catch (Throwable ignored) {}

                        plugin.getGrowingBlocks().remove(loc);
                        cancel();
                    }
                } else {
                    plugin.getGrowingBlocks().remove(loc);
                    cancel();
                }
            }
        }.runTaskTimer(plugin, intervalTicks, intervalTicks);
    }

    @EventHandler(priority = EventPriority.LOWEST, ignoreCancelled = true)
    public void onMoistureChange(MoistureChangeEvent event) {
        Block block = event.getBlock();
        if (plugin.isSoilProtected(block.getLocation())) {
            event.setCancelled(true);
        }
    }

    @EventHandler(priority = EventPriority.LOWEST, ignoreCancelled = true)
    public void onBlockFade(BlockFadeEvent event) {
        Block block = event.getBlock();
        if (plugin.isSoilProtected(block.getLocation()) || plugin.getZoneAt(block.getLocation()) != null) {
            event.setCancelled(true);
        }
    }

    @EventHandler(priority = EventPriority.LOWEST, ignoreCancelled = true)
    public void onBlockPlace(BlockPlaceEvent event) {
        Player player = event.getPlayer();
        if (player.hasPermission("thundercrops.admin") && player.getGameMode() == GameMode.CREATIVE) {
            return;
        }

        if (plugin.getZoneAt(event.getBlock().getLocation()) != null ||
            plugin.isSoilProtected(event.getBlock().getLocation())) {
            event.setCancelled(true);
        }
    }

    @EventHandler(priority = EventPriority.LOWEST, ignoreCancelled = true)
    public void onWaterFlow(BlockFromToEvent event) {
        Block toBlock = event.getToBlock();
        if (plugin.getZoneAt(toBlock.getLocation()) != null || plugin.isSoilProtected(toBlock.getLocation())) {
            event.setCancelled(true);
        }
    }
}
