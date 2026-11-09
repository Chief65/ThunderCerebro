package com.thundermc.crops;

import org.bukkit.ChatColor;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.World;
import org.bukkit.block.Block;
import org.bukkit.block.BlockFace;
import org.bukkit.block.data.Ageable;
import org.bukkit.block.data.type.Farmland;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.entity.Player;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

public class CropCommand implements CommandExecutor, TabCompleter {

    private final ThunderCrops plugin;
    private final Map<UUID, Location> pos1Map = new HashMap<>();
    private final Map<UUID, Location> pos2Map = new HashMap<>();

    public CropCommand(ThunderCrops plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!sender.hasPermission("thundercrops.admin")) {
            sender.sendMessage(plugin.getMessage("no-permission"));
            return true;
        }

        if (args.length == 0 || args[0].equalsIgnoreCase("help")) {
            sendHelp(sender, label);
            return true;
        }

        String sub = args[0].toLowerCase();

        if (sub.equals("reload")) {
            plugin.reloadPluginConfig();
            sender.sendMessage(plugin.getMessage("reloaded"));
            return true;
        }

        if (sub.equals("list")) {
            sender.sendMessage(ChatColor.GOLD + "=== Zonas Activas de ThunderCrops ===");
            for (CropZone zone : plugin.getZones()) {
                sender.sendMessage(ChatColor.YELLOW + "- " + ChatColor.AQUA + zone.getId() +
                        ChatColor.GRAY + " [" + zone.getWorldName() + " (" +
                        zone.getMinX() + "," + zone.getMinY() + "," + zone.getMinZ() + " a " +
                        zone.getMaxX() + "," + zone.getMaxY() + "," + zone.getMaxZ() + ")] Cultivo: " +
                        ChatColor.GREEN + zone.getCropMaterial() + " Drop: " + zone.getMinDrop() + "-" + zone.getMaxDrop() + " " + zone.getDropMaterial());
            }
            return true;
        }

        if (!(sender instanceof Player player)) {
            sender.sendMessage(ChatColor.RED + "Este comando solo puede ser ejecutado por un jugador.");
            return true;
        }

        UUID uuid = player.getUniqueId();

        if (sub.equals("pos1")) {
            Location loc = getTargetOrPlayerLoc(player);
            pos1Map.put(uuid, loc);
            sender.sendMessage(plugin.getMessage("pos1-set")
                    .replace("%x%", String.valueOf(loc.getBlockX()))
                    .replace("%y%", String.valueOf(loc.getBlockY()))
                    .replace("%z%", String.valueOf(loc.getBlockZ())));
            return true;
        }

        if (sub.equals("pos2")) {
            Location loc = getTargetOrPlayerLoc(player);
            pos2Map.put(uuid, loc);
            sender.sendMessage(plugin.getMessage("pos2-set")
                    .replace("%x%", String.valueOf(loc.getBlockX()))
                    .replace("%y%", String.valueOf(loc.getBlockY()))
                    .replace("%z%", String.valueOf(loc.getBlockZ())));
            return true;
        }

        if (sub.equals("create")) {
            if (args.length < 2) {
                sender.sendMessage(ChatColor.RED + "Uso: /" + label + " create <nombre_zona>");
                return true;
            }
            String zoneName = args[1].toLowerCase();
            Location p1 = pos1Map.get(uuid);
            Location p2 = pos2Map.get(uuid);

            if (p1 == null || p2 == null || p1.getWorld() == null || p2.getWorld() == null ||
                    !p1.getWorld().getName().equals(p2.getWorld().getName())) {
                sender.sendMessage(plugin.getMessage("select-both-points"));
                return true;
            }

            plugin.saveZone(zoneName, p1, p2);
            sender.sendMessage(plugin.getMessage("zone-created").replace("%zone%", zoneName));
            sender.sendMessage(ChatColor.GRAY + "Ejecuta " + ChatColor.YELLOW + "/" + label + " setup " + zoneName +
                    ChatColor.GRAY + " para convertir automáticamente los bloques en cultivos.");
            return true;
        }

        if (sub.equals("remove") || sub.equals("delete")) {
            if (args.length < 2) {
                sender.sendMessage(ChatColor.RED + "Uso: /" + label + " remove <nombre_zona>");
                return true;
            }
            String zoneName = args[1].toLowerCase();
            if (plugin.removeZone(zoneName)) {
                sender.sendMessage(plugin.getMessage("zone-removed").replace("%zone%", zoneName));
            } else {
                sender.sendMessage(plugin.getMessage("zone-not-found").replace("%zone%", zoneName));
            }
            return true;
        }

        if (sub.equals("setup")) {
            if (args.length < 2) {
                sender.sendMessage(ChatColor.RED + "Uso: /" + label + " setup <nombre_zona>");
                return true;
            }
            String zoneName = args[1].toLowerCase();
            CropZone zone = plugin.getZone(zoneName);
            if (zone == null) {
                sender.sendMessage(plugin.getMessage("zone-not-found").replace("%zone%", zoneName));
                return true;
            }

            World world = player.getServer().getWorld(zone.getWorldName());
            if (world == null) {
                sender.sendMessage(ChatColor.RED + "El mundo " + zone.getWorldName() + " no está cargado.");
                return true;
            }

            int count = 0;
            for (int x = zone.getMinX(); x <= zone.getMaxX(); x++) {
                for (int y = zone.getMinY(); y <= zone.getMaxY(); y++) {
                    for (int z = zone.getMinZ(); z <= zone.getMaxZ(); z++) {
                        Block block = world.getBlockAt(x, y, z);
                        if (zone.getTargetMaterials().contains(block.getType())) {
                            // Convertir bloque base en FARMLAND
                            block.setType(zone.getSoilMaterial(), false);
                            if (block.getBlockData() instanceof Farmland f) {
                                f.setMoisture(f.getMaximumMoisture());
                                block.setBlockData(f, false);
                            }

                            // Colocar cultivo maduro justo encima
                            Block above = block.getRelative(BlockFace.UP);
                            if (above.getType() == Material.AIR || above.getType() == zone.getCropMaterial()) {
                                above.setType(zone.getCropMaterial(), false);
                                if (above.getBlockData() instanceof Ageable a) {
                                    a.setAge(a.getMaximumAge());
                                    above.setBlockData(a, false);
                                }
                            }
                            count++;
                        } else if (block.getType() == zone.getSoilMaterial()) {
                            // Si ya es farmland, asegurar hidratación y cultivo encima
                            if (block.getBlockData() instanceof Farmland f) {
                                f.setMoisture(f.getMaximumMoisture());
                                block.setBlockData(f, false);
                            }
                            Block above = block.getRelative(BlockFace.UP);
                            if (above.getType() == Material.AIR || above.getType() == zone.getCropMaterial()) {
                                above.setType(zone.getCropMaterial(), false);
                                if (above.getBlockData() instanceof Ageable a) {
                                    a.setAge(a.getMaximumAge());
                                    above.setBlockData(a, false);
                                }
                            }
                            count++;
                        }
                    }
                }
            }

            sender.sendMessage(plugin.getMessage("setup-complete").replace("%count%", String.valueOf(count)));
            return true;
        }

        sendHelp(sender, label);
        return true;
    }

    private Location getTargetOrPlayerLoc(Player player) {
        Block target = player.getTargetBlockExact(5);
        if (target != null) {
            return target.getLocation();
        }
        return player.getLocation().getBlock().getLocation();
    }

    private void sendHelp(CommandSender sender, String label) {
        sender.sendMessage(ChatColor.GOLD + "=== Comandos de ThunderCrops ===");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " pos1" + ChatColor.GRAY + " - Marca la esquina 1.");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " pos2" + ChatColor.GRAY + " - Marca la esquina 2.");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " create <nombre>" + ChatColor.GRAY + " - Crea la zona con las esquinas.");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " setup <nombre>" + ChatColor.GRAY + " - Convierte césped/tierra en cultivos maduros.");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " remove <nombre>" + ChatColor.GRAY + " - Elimina una zona.");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " list" + ChatColor.GRAY + " - Lista todas las zonas activas.");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " reload" + ChatColor.GRAY + " - Recarga la configuración.");
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        if (!sender.hasPermission("thundercrops.admin")) return Collections.emptyList();

        if (args.length == 1) {
            List<String> list = Arrays.asList("pos1", "pos2", "create", "setup", "remove", "list", "reload");
            return list.stream().filter(s -> s.startsWith(args[0].toLowerCase())).toList();
        }

        if (args.length == 2 && (args[0].equalsIgnoreCase("setup") || args[0].equalsIgnoreCase("remove"))) {
            return plugin.getZoneNames().stream().filter(s -> s.startsWith(args[1].toLowerCase())).toList();
        }

        return Collections.emptyList();
    }
}
