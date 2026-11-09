package com.thundermc.crops;

import net.md_5.bungee.api.ChatMessageType;
import net.md_5.bungee.api.chat.TextComponent;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.block.Block;
import org.bukkit.block.data.Ageable;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitTask;

import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class ThunderCrops extends JavaPlugin {

    private final Map<String, CropZone> zones = new HashMap<>();
    private final Set<Location> growingBlocks = Collections.synchronizedSet(new HashSet<>());
    private BukkitTask actionBarTask;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        loadZones();

        getServer().getPluginManager().registerEvents(new CropListener(this), this);

        CropCommand cmd = new CropCommand(this);
        if (getCommand("crops") != null) {
            getCommand("crops").setExecutor(cmd);
            getCommand("crops").setTabCompleter(cmd);
        }

        startActionBarTask();

        getLogger().info("ThunderCrops v" + getDescription().getVersion() + " habilitado con " + zones.size() + " zonas cargadas.");
    }

    @Override
    public void onDisable() {
        if (actionBarTask != null) {
            actionBarTask.cancel();
            actionBarTask = null;
        }

        // Finalizar todos los cultivos en crecimiento antes de apagar
        synchronized (growingBlocks) {
            for (Location loc : growingBlocks) {
                if (loc.getWorld() != null) {
                    Block block = loc.getBlock();
                    if (block.getBlockData() instanceof Ageable ageable) {
                        ageable.setAge(ageable.getMaximumAge());
                        block.setBlockData(ageable, false);
                    }
                }
            }
            growingBlocks.clear();
        }

        zones.clear();
        getLogger().info("ThunderCrops deshabilitado.");
    }

    public void reloadPluginConfig() {
        reloadConfig();
        loadZones();
        startActionBarTask();
    }

    private void startActionBarTask() {
        if (actionBarTask != null) {
            actionBarTask.cancel();
            actionBarTask = null;
        }

        if (!getConfig().getBoolean("actionbar.enabled", true)) {
            return;
        }

        // Chequeo periódico cada 20 ticks (1s) para los jugadores dentro de las zonas
        actionBarTask = Bukkit.getScheduler().runTaskTimer(this, () -> {
            String msg = getActionBarMessage();
            if (msg == null || msg.isEmpty()) return;

            for (Player player : Bukkit.getOnlinePlayers()) {
                CropZone zone = getZoneAt(player.getLocation());
                if (zone != null) {
                    sendActionBar(player, msg);
                }
            }
        }, 20L, 20L);
    }

    public void sendActionBar(Player player, String message) {
        if (player == null || !player.isOnline() || message == null || message.isEmpty()) return;
        player.spigot().sendMessage(ChatMessageType.ACTION_BAR, TextComponent.fromLegacyText(message));
    }

    public String getActionBarMessage() {
        String raw = getConfig().getString("actionbar.text", "&aVende los cultivos en &e/venta");
        return ChatColor.translateAlternateColorCodes('&', raw);
    }

    public void loadZones() {
        zones.clear();
        ConfigurationSection section = getConfig().getConfigurationSection("zones");
        if (section == null) return;

        for (String key : section.getKeys(false)) {
            ConfigurationSection zSec = section.getConfigurationSection(key);
            if (zSec == null) continue;

            String world = zSec.getString("world", "world");
            int minX = zSec.getInt("min.x");
            int minY = zSec.getInt("min.y");
            int minZ = zSec.getInt("min.z");
            int maxX = zSec.getInt("max.x");
            int maxY = zSec.getInt("max.y");
            int maxZ = zSec.getInt("max.z");

            Material soil = Material.getMaterial(zSec.getString("soil", "FARMLAND"));
            Material crop = Material.getMaterial(zSec.getString("crop", "WHEAT"));
            Material drop = Material.getMaterial(zSec.getString("drop-item", "WHEAT"));
            List<String> targets = zSec.getStringList("targets");
            int minDrop = zSec.getInt("min-drop", 1);
            int maxDrop = zSec.getInt("max-drop", 2);
            int regenDelay = zSec.getInt("regen-delay-seconds", 3);
            boolean giveInv = zSec.getBoolean("give-to-inventory", true);

            CropZone zone = new CropZone(key, world, minX, minY, minZ, maxX, maxY, maxZ,
                    soil, crop, drop, targets, minDrop, maxDrop, regenDelay, giveInv);
            zones.put(key.toLowerCase(), zone);
        }
    }

    public void saveZone(String name, Location p1, Location p2) {
        String key = name.toLowerCase();
        int minX = Math.min(p1.getBlockX(), p2.getBlockX());
        int minY = Math.min(p1.getBlockY(), p2.getBlockY());
        int minZ = Math.min(p1.getBlockZ(), p2.getBlockZ());
        int maxX = Math.max(p1.getBlockX(), p2.getBlockX());
        int maxY = Math.max(p1.getBlockY(), p2.getBlockY());
        int maxZ = Math.max(p1.getBlockZ(), p2.getBlockZ());

        String path = "zones." + key;
        getConfig().set(path + ".world", p1.getWorld().getName());
        getConfig().set(path + ".min.x", minX);
        getConfig().set(path + ".min.y", minY);
        getConfig().set(path + ".min.z", minZ);
        getConfig().set(path + ".max.x", maxX);
        getConfig().set(path + ".max.y", maxY);
        getConfig().set(path + ".max.z", maxZ);
        getConfig().set(path + ".soil", "FARMLAND");
        getConfig().set(path + ".crop", "WHEAT");
        getConfig().set(path + ".drop-item", "WHEAT");
        getConfig().set(path + ".targets", List.of("GRASS_BLOCK", "DIRT"));
        getConfig().set(path + ".min-drop", 1);
        getConfig().set(path + ".max-drop", 2);
        getConfig().set(path + ".regen-delay-seconds", 3);
        getConfig().set(path + ".give-to-inventory", true);

        saveConfig();
        loadZones();
    }

    public boolean removeZone(String name) {
        String key = name.toLowerCase();
        if (!getConfig().contains("zones." + key)) return false;

        getConfig().set("zones." + key, null);
        saveConfig();
        zones.remove(key);
        return true;
    }

    public CropZone getZoneAt(Location loc) {
        for (CropZone zone : zones.values()) {
            if (zone.contains(loc)) {
                return zone;
            }
        }
        return null;
    }

    public boolean isSoilProtected(Location loc) {
        for (CropZone zone : zones.values()) {
            if (zone.containsOrSoil(loc)) {
                return true;
            }
        }
        return false;
    }

    public CropZone getZone(String name) {
        return zones.get(name.toLowerCase());
    }

    public Collection<CropZone> getZones() {
        return Collections.unmodifiableCollection(zones.values());
    }

    public Set<String> getZoneNames() {
        return Collections.unmodifiableSet(zones.keySet());
    }

    public Set<Location> getGrowingBlocks() {
        return growingBlocks;
    }

    public String getMessage(String key) {
        String prefix = getConfig().getString("messages.prefix", "&8[&6&lThunderCrops&8] &r");
        String msg = getConfig().getString("messages." + key, "");
        return ChatColor.translateAlternateColorCodes('&', prefix + msg);
    }
}
