package com.thunderstudios.headanimator;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class HeadCommand implements CommandExecutor, TabCompleter {

    private final HeadAnimatorPlugin plugin;

    public HeadCommand(HeadAnimatorPlugin plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!sender.hasPermission("headanimator.admin")) {
            sender.sendMessage(ChatColor.RED + "No tienes permiso para usar este comando.");
            return true;
        }

        if (args.length == 0) {
            sender.sendMessage(ChatColor.DARK_GRAY + "---------------------------------------------");
            sender.sendMessage(HeadAnimation.colorize("&#78CD23&lHeadAnimator &8v1.2.0 &7por ThunderStudios"));
            sender.sendMessage(ChatColor.YELLOW + "/ha give <jugador> <animacion>" + ChatColor.GRAY + " - Entrega una cabeza animada.");
            sender.sendMessage(ChatColor.YELLOW + "/ha list" + ChatColor.GRAY + " - Lista las animaciones disponibles.");
            sender.sendMessage(ChatColor.YELLOW + "/ha debug" + ChatColor.GRAY + " - Diagnostico en tiempo real del casco y animacion.");
            sender.sendMessage(ChatColor.YELLOW + "/ha reload" + ChatColor.GRAY + " - Recarga la configuracion.");
            sender.sendMessage(ChatColor.DARK_GRAY + "---------------------------------------------");
            return true;
        }

        String sub = args[0].toLowerCase();

        if (sub.equals("reload")) {
            plugin.reload();
            sender.sendMessage(HeadAnimation.colorize("&#78CD23✔ &aConfiguracion de HeadAnimator recargada correctamente."));
            return true;
        }

        if (sub.equals("list")) {
            sender.sendMessage(HeadAnimation.colorize("&#78CD23&lAnimaciones registradas:"));
            for (HeadAnimation anim : plugin.getAnimationManager().getAllAnimations()) {
                sender.sendMessage(ChatColor.GRAY + " - " + ChatColor.GREEN + anim.getId() + 
                        ChatColor.DARK_GRAY + " (" + anim.getFrameCount() + " frames, cada " + anim.getIntervalTicks() + " ticks)");
            }
            return true;
        }

        if (sub.equals("debug")) {
            if (!(sender instanceof Player)) {
                sender.sendMessage(ChatColor.RED + "Este comando solo lo puede usar un jugador.");
                return true;
            }
            Player p = (Player) sender;
            ItemStack helmet = p.getInventory().getHelmet();
            HeadAnimation helmetAnim = plugin.getAnimationManager().getAnimationFromItem(helmet);

            p.sendMessage(ChatColor.DARK_GRAY + "--- [HeadAnimator Debug] ---");
            p.sendMessage(ChatColor.GOLD + "Casco Equipado: " + ChatColor.WHITE + (helmet != null ? helmet.getType() : "VACIO") + 
                    ChatColor.GRAY + " -> Animacion PDC: " + (helmetAnim != null ? ChatColor.GREEN + helmetAnim.getId() + " (" + helmetAnim.getFrameCount() + " frames)" : ChatColor.RED + "Ninguna"));
            p.sendMessage(ChatColor.GOLD + "Activo como Wearer: " + (plugin.getAnimationManager().isWearerActive(p) ? ChatColor.GREEN + "SI (Frame actual: " + plugin.getAnimationManager().getCurrentFrameIndex(p) + ")" : ChatColor.RED + "NO"));
            p.sendMessage(ChatColor.DARK_GRAY + "----------------------------");
            return true;
        }

        if (sub.equals("give")) {
            if (args.length < 3) {
                sender.sendMessage(ChatColor.RED + "Uso: /" + label + " give <jugador> <animacion>");
                return true;
            }

            Player target = Bukkit.getPlayer(args[1]);
            if (target == null || !target.isOnline()) {
                sender.sendMessage(ChatColor.RED + "El jugador '" + args[1] + "' no esta conectado.");
                return true;
            }

            String animId = args[2];
            HeadAnimation anim = plugin.getAnimationManager().getAnimation(animId);
            if (anim == null) {
                sender.sendMessage(ChatColor.RED + "La animacion '" + animId + "' no existe. Usa /" + label + " list.");
                return true;
            }

            ItemStack item = anim.createGivenItem();
            target.getInventory().addItem(item);
            sender.sendMessage(HeadAnimation.colorize("&#78CD23✔ &aCabeza animada &#A8FF3E" + anim.getId() + " &aentregada a &f" + target.getName() + "&a."));
            target.sendMessage(HeadAnimation.colorize("&#78CD23✔ &aHas recibido una cabeza animada: " + anim.createGivenItem().getItemMeta().getDisplayName()));
            return true;
        }

        sender.sendMessage(ChatColor.RED + "Subcomando desconocido. Usa /" + label + " para ayuda.");
        return true;
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        if (!sender.hasPermission("headanimator.admin")) {
            return Collections.emptyList();
        }

        if (args.length == 1) {
            List<String> subs = Arrays.asList("give", "list", "debug", "reload");
            List<String> matches = new ArrayList<>();
            for (String s : subs) {
                if (s.startsWith(args[0].toLowerCase())) matches.add(s);
            }
            return matches;
        }

        if (args.length == 2 && args[0].equalsIgnoreCase("give")) {
            List<String> players = new ArrayList<>();
            for (Player p : Bukkit.getOnlinePlayers()) {
                if (p.getName().toLowerCase().startsWith(args[1].toLowerCase())) {
                    players.add(p.getName());
                }
            }
            return players;
        }

        if (args.length == 3 && args[0].equalsIgnoreCase("give")) {
            List<String> anims = new ArrayList<>();
            for (HeadAnimation anim : plugin.getAnimationManager().getAllAnimations()) {
                if (anim.getId().toLowerCase().startsWith(args[2].toLowerCase())) {
                    anims.add(anim.getId());
                }
            }
            return anims;
        }

        return Collections.emptyList();
    }
}
