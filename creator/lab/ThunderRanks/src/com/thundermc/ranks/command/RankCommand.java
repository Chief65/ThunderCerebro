package com.thundermc.ranks.command;

import com.thundermc.ranks.ThunderRanks;
import com.thundermc.ranks.gui.RankGui;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

public class RankCommand implements CommandExecutor {

    private final ThunderRanks plugin;

    public RankCommand(ThunderRanks plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!(sender instanceof Player player)) {
            sender.sendMessage(ChatColor.RED + "Este comando solo puede ser ejecutado por un jugador.");
            return true;
        }

        if (label.equalsIgnoreCase("rankup")) {
            if (plugin.getPlayerDataManager().canRankup(player)) {
                com.thundermc.ranks.gui.RankConfirmGui.open(player, plugin);
            } else {
                // Si no puede, abrir GUI para que vea qué le falta
                RankGui.open(player, plugin);
            }
            return true;
        }

        // /rangos /rank /ranks
        RankGui.open(player, plugin);
        return true;
    }
}
