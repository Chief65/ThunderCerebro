package com.thundermc.ranks.command;

import com.thundermc.ranks.ThunderRanks;
import com.thundermc.ranks.model.PlayerData;
import com.thundermc.ranks.model.Rank;
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

public class AdminCommand implements CommandExecutor, TabCompleter {

    private final ThunderRanks plugin;

    public AdminCommand(ThunderRanks plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!sender.hasPermission("thunderranks.admin")) {
            sender.sendMessage(ChatColor.RED + "No tienes permiso para usar este comando.");
            return true;
        }

        if (args.length == 0 || args[0].equalsIgnoreCase("help")) {
            sendHelp(sender, label);
            return true;
        }

        String sub = args[0].toLowerCase();

        if (sub.equals("reload")) {
            plugin.reloadPlugin();
            sender.sendMessage(ChatColor.GREEN + "[ThunderRanks] Configuración, rangos y valores de XP recargados.");
            return true;
        }

        if (sub.equals("addxp")) {
            if (args.length < 3) {
                sender.sendMessage(ChatColor.RED + "Uso: /" + label + " addxp <jugador> <cantidad>");
                return true;
            }
            Player target = Bukkit.getPlayer(args[1]);
            if (target == null) {
                sender.sendMessage(ChatColor.RED + "Jugador no encontrado o desconectado.");
                return true;
            }
            int amount;
            try {
                amount = Integer.parseInt(args[2]);
            } catch (NumberFormatException e) {
                sender.sendMessage(ChatColor.RED + "Cantidad inválida.");
                return true;
            }

            plugin.getPlayerDataManager().addXp(target, amount);
            sender.sendMessage(ChatColor.GREEN + "Se añadieron " + amount + " XP a " + target.getName() + ".");
            return true;
        }

        if (sub.equals("setrank")) {
            if (args.length < 3) {
                sender.sendMessage(ChatColor.RED + "Uso: /" + label + " setrank <jugador> <rango> [etapa_1_a_5]");
                return true;
            }
            Player target = Bukkit.getPlayer(args[1]);
            if (target == null) {
                sender.sendMessage(ChatColor.RED + "Jugador no encontrado.");
                return true;
            }
            String rankId = args[2].toLowerCase();
            Rank rank = plugin.getRankManager().getRank(rankId);
            if (rank == null) {
                sender.sendMessage(ChatColor.RED + "El rango " + rankId + " no existe.");
                return true;
            }

            int tier = 1;
            if (args.length >= 4) {
                try {
                    tier = Math.max(1, Math.min(5, Integer.parseInt(args[3])));
                } catch (NumberFormatException ignored) {}
            }

            PlayerData pd = plugin.getPlayerDataManager().getPlayerData(target);
            pd.setCurrentRankId(rank.getId());
            pd.setCurrentTier(tier);
            plugin.getPlayerDataManager().updateAndShowBossBar(target, pd, rank, rank.getTier(tier));
            plugin.getPlayerDataManager().saveData();
            sender.sendMessage(ChatColor.GREEN + "Rango de " + target.getName() + " establecido a " + rank.getDisplayName() + " " + rank.getTier(tier).getRomanNumeral() + ".");
            return true;
        }

        if (sub.equals("reset")) {
            if (args.length < 2) {
                sender.sendMessage(ChatColor.RED + "Uso: /" + label + " reset <jugador>");
                return true;
            }
            Player target = Bukkit.getPlayer(args[1]);
            if (target == null) {
                sender.sendMessage(ChatColor.RED + "Jugador no encontrado.");
                return true;
            }
            PlayerData pd = plugin.getPlayerDataManager().getPlayerData(target);
            pd.setCurrentRankId("user");
            pd.setCurrentTier(1);
            Rank rank = plugin.getRankManager().getRank("user");
            if (rank != null) {
                plugin.getPlayerDataManager().updateAndShowBossBar(target, pd, rank, rank.getTier(1));
            }
            plugin.getPlayerDataManager().saveData();
            sender.sendMessage(ChatColor.GREEN + "Progreso de " + target.getName() + " reiniciado a USER I.");
            return true;
        }

        sendHelp(sender, label);
        return true;
    }

    private void sendHelp(CommandSender sender, String label) {
        sender.sendMessage(ChatColor.GOLD + "=== ThunderRanks Admin ===");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " addxp <jugador> <cantidad>" + ChatColor.GRAY + " - Añade XP de rango.");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " setrank <jugador> <rango>" + ChatColor.GRAY + " - Asigna un rango directamente.");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " reset <jugador>" + ChatColor.GRAY + " - Reinicia el progreso del jugador.");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " reload" + ChatColor.GRAY + " - Recarga la configuración.");
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        if (!sender.hasPermission("thunderranks.admin")) return Collections.emptyList();

        if (args.length == 1) {
            List<String> list = Arrays.asList("addxp", "setrank", "reset", "reload");
            return list.stream().filter(s -> s.startsWith(args[0].toLowerCase())).toList();
        }

        if (args.length == 2 && (args[0].equalsIgnoreCase("addxp") || args[0].equalsIgnoreCase("setrank") || args[0].equalsIgnoreCase("reset"))) {
            return null; // Jugadores online
        }

        if (args.length == 3 && args[0].equalsIgnoreCase("setrank")) {
            List<String> ranks = new ArrayList<>();
            for (Rank r : plugin.getRankManager().getRanks()) {
                ranks.add(r.getId());
            }
            return ranks.stream().filter(s -> s.startsWith(args[2].toLowerCase())).toList();
        }

        return Collections.emptyList();
    }
}
