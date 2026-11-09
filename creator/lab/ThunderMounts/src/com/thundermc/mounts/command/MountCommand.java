package com.thundermc.mounts.command;

import com.thundermc.mounts.ThunderMounts;
import com.thundermc.mounts.gui.MountGui;
import com.thundermc.mounts.model.HorseStyle;
import com.thundermc.mounts.model.MountData;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.entity.Player;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class MountCommand implements CommandExecutor, TabCompleter {

    private final ThunderMounts plugin;

    public MountCommand(ThunderMounts plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!(sender instanceof Player player)) {
            sender.sendMessage(ChatColor.RED + "Este comando solo puede ser ejecutado por un jugador.");
            return true;
        }

        if (args.length == 0) {
            MountGui.open(player, plugin);
            return true;
        }

        String sub = args[0].toLowerCase();

        if (sub.equals("despawn") || sub.equals("guardar") || sub.equals("dismount")) {
            if (plugin.getMountManager().hasActiveMount(player)) {
                plugin.getMountManager().despawnMount(player);
            } else {
                player.sendMessage(ChatColor.RED + "No tienes ningún corcel activo.");
            }
            return true;
        }

        if (sub.equals("spawn")) {
            if (args.length < 2) {
                player.sendMessage(ChatColor.RED + "Uso: /" + label + " spawn <estilo>");
                return true;
            }
            HorseStyle style = HorseStyle.fromId(args[1]);
            if (style == null) {
                player.sendMessage(ChatColor.RED + "Estilo no reconocido. Usa /" + label + " para abrir el catálogo.");
                return true;
            }
            plugin.getMountManager().spawnMount(player, style);
            return true;
        }

        if (sub.equals("admin")) {
            if (!player.hasPermission("thundermounts.admin")) {
                player.sendMessage(ChatColor.RED + "No tienes permiso para comandos de administración.");
                return true;
            }
            if (args.length >= 3 && args[1].equalsIgnoreCase("reset")) {
                Player target = Bukkit.getPlayer(args[2]);
                if (target == null) {
                    player.sendMessage(ChatColor.RED + "Jugador no encontrado.");
                    return true;
                }
                MountData md = plugin.getMountManager().getMountData(target);
                md.reset();
                plugin.getMountManager().saveData();
                player.sendMessage(ChatColor.GREEN + "Estamina y descanso reiniciados para " + target.getName() + ".");
                return true;
            }
            if (args.length >= 2 && args[1].equalsIgnoreCase("reload")) {
                plugin.reloadConfig();
                player.sendMessage(ChatColor.GREEN + "Configuración de ThunderMounts recargada.");
                return true;
            }
        }

        MountGui.open(player, plugin);
        return true;
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        if (args.length == 1) {
            List<String> subs = new ArrayList<>(Arrays.asList("menu", "guardar", "despawn", "spawn"));
            if (sender.hasPermission("thundermounts.admin")) {
                subs.add("admin");
            }
            return filter(subs, args[0]);
        }

        if (args.length == 2 && args[0].equalsIgnoreCase("spawn")) {
            List<String> styles = new ArrayList<>();
            for (HorseStyle s : HorseStyle.values()) {
                styles.add(s.getId());
            }
            return filter(styles, args[1]);
        }

        if (args.length == 2 && args[0].equalsIgnoreCase("admin")) {
            return filter(Arrays.asList("reset", "reload"), args[1]);
        }

        if (args.length == 3 && args[0].equalsIgnoreCase("admin") && args[1].equalsIgnoreCase("reset")) {
            List<String> names = new ArrayList<>();
            for (Player p : Bukkit.getOnlinePlayers()) {
                names.add(p.getName());
            }
            return filter(names, args[2]);
        }

        return Collections.emptyList();
    }

    private List<String> filter(List<String> list, String query) {
        List<String> result = new ArrayList<>();
        String q = query.toLowerCase();
        for (String s : list) {
            if (s.toLowerCase().startsWith(q)) {
                result.add(s);
            }
        }
        return result;
    }
}
