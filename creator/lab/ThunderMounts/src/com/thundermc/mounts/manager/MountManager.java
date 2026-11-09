package com.thundermc.mounts.manager;

import com.thundermc.mounts.ThunderMounts;
import com.thundermc.mounts.model.ActiveMount;
import com.thundermc.mounts.model.HorseArmor;
import com.thundermc.mounts.model.HorseStyle;
import com.thundermc.mounts.model.MountData;
import net.md_5.bungee.api.ChatMessageType;
import net.md_5.bungee.api.chat.TextComponent;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.Particle;
import org.bukkit.Sound;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.entity.AbstractHorse;
import org.bukkit.entity.EntityType;
import org.bukkit.entity.Horse;
import org.bukkit.entity.Player;
import org.bukkit.entity.SkeletonHorse;
import org.bukkit.entity.ZombieHorse;
import org.bukkit.inventory.ItemStack;
import org.bukkit.scheduler.BukkitTask;

import java.io.File;
import java.io.IOException;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class MountManager {

    private final ThunderMounts plugin;
    private final Map<UUID, MountData> playerData = new HashMap<>();
    private final Map<UUID, ActiveMount> activeMounts = new HashMap<>();
    private final File dataFile;
    private FileConfiguration dataConfig;
    private BukkitTask tickerTask;

    public MountManager(ThunderMounts plugin) {
        this.plugin = plugin;
        this.dataFile = new File(plugin.getDataFolder(), "mounts_data.yml");
        loadData();
        startTicker();
    }

    public void loadData() {
        if (!dataFile.exists()) {
            try {
                dataFile.getParentFile().mkdirs();
                dataFile.createNewFile();
            } catch (IOException ignored) {}
        }
        dataConfig = YamlConfiguration.loadConfiguration(dataFile);
    }

    public void saveData() {
        if (dataConfig == null) return;
        for (Map.Entry<UUID, MountData> entry : playerData.entrySet()) {
            String pUuid = entry.getKey().toString();
            MountData md = entry.getValue();
            dataConfig.set("players." + pUuid + ".stamina", md.getRemainingStaminaSeconds());
            dataConfig.set("players." + pUuid + ".cooldown-end", md.getCooldownEndTimestamp());
            dataConfig.set("players." + pUuid + ".style", md.getSelectedStyle().getId());
            dataConfig.set("players." + pUuid + ".armor", md.getSelectedArmor().getId());
        }
        try {
            dataConfig.save(dataFile);
        } catch (IOException e) {
            plugin.getLogger().warning("Error guardando mounts_data.yml: " + e.getMessage());
        }
    }

    public MountData getMountData(Player player) {
        return getMountData(player.getUniqueId());
    }

    public MountData getMountData(UUID uuid) {
        if (playerData.containsKey(uuid)) {
            return playerData.get(uuid);
        }

        String path = "players." + uuid.toString();
        int stamina = dataConfig.getInt(path + ".stamina", 3600);
        long cooldownEnd = dataConfig.getLong(path + ".cooldown-end", 0L);
        String styleId = dataConfig.getString(path + ".style", "white_pure");
        String armorId = dataConfig.getString(path + ".armor", "diamond");

        HorseStyle style = HorseStyle.fromId(styleId);
        HorseArmor armor = HorseArmor.fromId(armorId);

        MountData md = new MountData(stamina, cooldownEnd, style, armor);
        playerData.put(uuid, md);
        return md;
    }

    public ActiveMount getActiveMount(Player player) {
        return activeMounts.get(player.getUniqueId());
    }

    public Collection<ActiveMount> getPlayerMounts() {
        return activeMounts.values();
    }

    public boolean hasActiveMount(Player player) {
        ActiveMount am = activeMounts.get(player.getUniqueId());
        return am != null && am.getEntity().isValid();
    }

    public void despawnMount(Player player) {
        ActiveMount am = activeMounts.remove(player.getUniqueId());
        if (am != null) {
            am.despawn();
            player.sendMessage(plugin.getMessage("despawned"));
        }
    }

    public boolean spawnMount(Player player, HorseStyle style) {
        // Despawn previa si tenía una
        if (hasActiveMount(player)) {
            despawnMount(player);
        }

        MountData data = getMountData(player);
        if (data.isInCooldown()) {
            long remaining = data.getRemainingCooldownSeconds();
            String formattedTime = formatTime(remaining);
            player.sendMessage(plugin.getMessage("in-cooldown").replace("%time%", formattedTime));
            player.playSound(player.getLocation(), Sound.ENTITY_VILLAGER_NO, 1.0f, 1.0f);
            return false;
        }

        Location loc = player.getLocation();
        AbstractHorse horseEntity = null;

        if (style.getEntityType() == EntityType.HORSE) {
            Horse horse = (Horse) loc.getWorld().spawnEntity(loc, EntityType.HORSE);
            horse.setTamed(true);
            horse.setOwner(player);
            if (style.getColor() != null) horse.setColor(style.getColor());
            if (style.getStyle() != null) horse.setStyle(style.getStyle());
            horse.getInventory().setSaddle(new ItemStack(Material.SADDLE));

            // Aplicar armadura seleccionada
            HorseArmor armor = data.getSelectedArmor();
            if (armor != HorseArmor.NONE && armor.getItemStack() != null) {
                horse.getInventory().setArmor(armor.getItemStack());
            }

            horse.setCustomName(ChatColor.translateAlternateColorCodes('&', "&6Corcel de &f" + player.getName()));
            horse.setCustomNameVisible(true);
            horse.setInvulnerable(true);
            horseEntity = horse;
        } else if (style.getEntityType() == EntityType.SKELETON_HORSE) {
            SkeletonHorse skeleton = (SkeletonHorse) loc.getWorld().spawnEntity(loc, EntityType.SKELETON_HORSE);
            skeleton.setTamed(true);
            skeleton.setOwner(player);
            skeleton.getInventory().setSaddle(new ItemStack(Material.SADDLE));
            skeleton.setCustomName(ChatColor.translateAlternateColorCodes('&', "&f&lEspectral de &f" + player.getName()));
            skeleton.setCustomNameVisible(true);
            skeleton.setInvulnerable(true);
            horseEntity = skeleton;
        } else if (style.getEntityType() == EntityType.ZOMBIE_HORSE) {
            ZombieHorse zombie = (ZombieHorse) loc.getWorld().spawnEntity(loc, EntityType.ZOMBIE_HORSE);
            zombie.setTamed(true);
            zombie.setOwner(player);
            zombie.getInventory().setSaddle(new ItemStack(Material.SADDLE));
            zombie.setCustomName(ChatColor.translateAlternateColorCodes('&', "&2&lNo-Muerto de &f" + player.getName()));
            zombie.setCustomNameVisible(true);
            zombie.setInvulnerable(true);
            horseEntity = zombie;
        }

        if (horseEntity != null) {
            horseEntity.addPassenger(player);
            ActiveMount am = new ActiveMount(player.getUniqueId(), horseEntity, style, data.getSelectedArmor());
            activeMounts.put(player.getUniqueId(), am);
            data.setSelectedStyle(style);

            player.sendMessage(plugin.getMessage("spawned").replace("%mount%", style.getDisplayName()));

            loc.getWorld().spawnParticle(Particle.HAPPY_VILLAGER, loc.clone().add(0, 0.6, 0), 12, 0.4, 0.4, 0.4, 0);
            player.playSound(loc, Sound.ENTITY_HORSE_ARMOR, 1.0f, 1.2f);
            player.playSound(loc, Sound.ENTITY_HORSE_GALLOP, 0.8f, 1.0f);
            return true;
        }

        return false;
    }

    public void updateActiveMountArmor(Player player, HorseArmor newArmor) {
        ActiveMount am = activeMounts.get(player.getUniqueId());
        if (am != null && am.getEntity() instanceof Horse horse && am.getEntity().isValid()) {
            if (newArmor != HorseArmor.NONE && newArmor.getItemStack() != null) {
                horse.getInventory().setArmor(newArmor.getItemStack());
            } else {
                horse.getInventory().setArmor(null);
            }
            am.setArmor(newArmor);
            player.playSound(player.getLocation(), Sound.ITEM_ARMOR_EQUIP_DIAMOND, 1.0f, 1.1f);
        }
    }

    private void startTicker() {
        if (tickerTask != null) {
            tickerTask.cancel();
            tickerTask = null;
        }

        // Corre cada 20 ticks (1s) para consumir estamina y mostrar ActionBar
        tickerTask = Bukkit.getScheduler().runTaskTimer(plugin, () -> {
            for (Map.Entry<UUID, ActiveMount> entry : new HashMap<>(activeMounts).entrySet()) {
                Player player = Bukkit.getPlayer(entry.getKey());
                ActiveMount am = entry.getValue();

                if (player == null || !player.isOnline() || !am.getEntity().isValid()) {
                    am.despawn();
                    activeMounts.remove(entry.getKey());
                    continue;
                }

                // Si el jugador no está montado en el caballo, despawnearlo inmediatamente
                if (!am.getEntity().getPassengers().contains(player)) {
                    am.despawn();
                    activeMounts.remove(entry.getKey());
                    continue;
                }

                // Manejo de Estamina cada segundo
                MountData md = getMountData(player);
                int cooldownSeconds = plugin.getConfig().getInt("settings.cooldown-seconds", 3600);

                md.consumeStamina(1, cooldownSeconds);

                // Enviar ActionBar con la línea delgada
                if (plugin.getConfig().getBoolean("settings.stamina-actionbar", true)) {
                    sendStaminaActionBar(player, md.getRemainingStaminaSeconds(), 3600);
                }

                // Si se agotó la estamina
                if (md.isInCooldown()) {
                    am.despawn();
                    activeMounts.remove(entry.getKey());
                    player.sendMessage(plugin.getMessage("exhausted"));
                    player.playSound(player.getLocation(), Sound.ENTITY_HORSE_BREATHE, 1.0f, 0.8f);
                    player.playSound(player.getLocation(), Sound.ENTITY_VILLAGER_NO, 1.0f, 1.0f);
                }
            }
        }, 20L, 20L);
    }

    private void sendStaminaActionBar(Player player, int current, int max) {
        int totalUnits = 14;
        float percent = max > 0 ? Math.min(1.0f, Math.max(0.0f, (float) current / (float) max)) : 0.0f;
        int filled = (int) (totalUnits * percent);
        int empty = totalUnits - filled;

        StringBuilder sb = new StringBuilder("&e&l⚡ ESTAMINA: &f" + formatTime(current) + " &8[");
        if (filled > 0) {
            sb.append("&a&m").append(" ".repeat(filled));
        }
        if (empty > 0) {
            sb.append("&7&m").append(" ".repeat(empty));
        }
        sb.append("&8]");

        String msg = ChatColor.translateAlternateColorCodes('&', sb.toString());
        player.spigot().sendMessage(ChatMessageType.ACTION_BAR, TextComponent.fromLegacyText(msg));
    }

    public static String formatTime(long totalSeconds) {
        long hours = totalSeconds / 3600;
        long minutes = (totalSeconds % 3600) / 60;
        long seconds = totalSeconds % 60;

        if (hours > 0) {
            return String.format("%02dh %02dm", hours, minutes);
        } else {
            return String.format("%02dm %02ds", minutes, seconds);
        }
    }

    public void cleanup() {
        if (tickerTask != null) {
            tickerTask.cancel();
            tickerTask = null;
        }
        for (ActiveMount am : activeMounts.values()) {
            am.despawn();
        }
        activeMounts.clear();
        saveData();
    }
}
