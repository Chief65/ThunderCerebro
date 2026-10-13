package com.thunderstudios.pets.command;

import com.thunderstudios.pets.ThunderPetsPlugin;
import com.thunderstudios.pets.egg.PetEgg;
import com.thunderstudios.pets.gui.PetMenu;
import com.thunderstudios.pets.pet.PetQuality;
import com.thunderstudios.pets.util.TextUtil;
import org.bukkit.Bukkit;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class PetCommand implements CommandExecutor, TabCompleter {

    private final ThunderPetsPlugin plugin;
    private final PetMenu petMenu;

    public PetCommand(ThunderPetsPlugin plugin) {
        this.plugin = plugin;
        this.petMenu = new PetMenu(plugin);
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        String prefix = plugin.getConfig().getString("messages.prefix", "&6&lMASCOTAS &8▸ ");

        if (args.length > 0) {
            String sub = args[0].toLowerCase();

            if (sub.equals("reload")) {
                if (!sender.hasPermission("thunderpets.admin")) {
                    sender.sendMessage(TextUtil.color(prefix + "&cNo tienes permisos para ejecutar este comando."));
                    return true;
                }
                plugin.reloadConfig();
                plugin.getPetManager().loadConfig();
                String reloadMsg = plugin.getConfig().getString("messages.reload-success", "&aConfiguración recargada correctamente.");
                sender.sendMessage(TextUtil.color(prefix + reloadMsg));
                return true;
            }

            if (sub.equals("giveegg")) {
                if (!sender.hasPermission("thunderpets.admin")) {
                    sender.sendMessage(TextUtil.color(prefix + "&cNo tienes permisos para ejecutar este comando."));
                    return true;
                }
                if (args.length < 3) {
                    sender.sendMessage(TextUtil.color(prefix + "&cUso: /pets giveegg <jugador> <calidad> [kills] [minutos]"));
                    return true;
                }

                Player target = Bukkit.getPlayer(args[1]);
                if (target == null || !target.isOnline()) {
                    sender.sendMessage(TextUtil.color(prefix + "&cJugador no encontrado o desconectado."));
                    return true;
                }

                PetQuality quality = PetQuality.fromString(args[2]);
                int defKills = plugin.getConfig().getInt("eggs.default-kills." + quality.name(), 15);
                int defMins = plugin.getConfig().getInt("eggs.default-minutes." + quality.name(), 10);

                if (args.length >= 4) {
                    try { defKills = Integer.parseInt(args[3]); } catch (NumberFormatException ignored) {}
                }
                if (args.length >= 5) {
                    try { defMins = Integer.parseInt(args[4]); } catch (NumberFormatException ignored) {}
                }

                ItemStack egg = PetEgg.createEgg(quality, defKills, defMins, plugin);
                target.getInventory().addItem(egg);
                sender.sendMessage(TextUtil.color(prefix + "&aHuevo de calidad " + quality.name() + " entregado a " + target.getName() + "."));
                target.sendMessage(TextUtil.color(prefix + "&a¡Has recibido un " + quality.getNameColor() + "Huevo de Mascota &7[" + quality.name() + "]&a! Cuídalo para que eclosione."));
                return true;
            }

            if (sub.equals("giveaccelerator")) {
                if (!sender.hasPermission("thunderpets.admin")) {
                    sender.sendMessage(TextUtil.color(prefix + "&cNo tienes permisos para ejecutar este comando."));
                    return true;
                }
                if (args.length < 2) {
                    sender.sendMessage(TextUtil.color(prefix + "&cUso: /pets giveaccelerator <jugador>"));
                    return true;
                }

                Player target = Bukkit.getPlayer(args[1]);
                if (target == null || !target.isOnline()) {
                    sender.sendMessage(TextUtil.color(prefix + "&cJugador no encontrado o desconectado."));
                    return true;
                }

                ItemStack acc = plugin.getEggManager().createAccelerator();
                target.getInventory().addItem(acc);
                sender.sendMessage(TextUtil.color(prefix + "&aPoción de Incubación Rápida entregada a " + target.getName() + "."));
                target.sendMessage(TextUtil.color(prefix + "&a¡Has recibido una &#FD9A00Poción de Incubación Rápida&a!"));
                return true;
            }
        }

        if (!(sender instanceof Player player)) {
            sender.sendMessage(TextUtil.color(prefix + "&cEste comando solo puede ser ejecutado por jugadores en el servidor."));
            return true;
        }

        petMenu.open(player);
        return true;
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        if (!sender.hasPermission("thunderpets.admin")) {
            return Collections.emptyList();
        }

        if (args.length == 1) {
            List<String> list = new ArrayList<>();
            for (String s : List.of("reload", "giveegg", "giveaccelerator")) {
                if (s.startsWith(args[0].toLowerCase())) list.add(s);
            }
            return list;
        }

        if (args.length == 2 && (args[0].equalsIgnoreCase("giveegg") || args[0].equalsIgnoreCase("giveaccelerator"))) {
            List<String> players = new ArrayList<>();
            for (Player p : Bukkit.getOnlinePlayers()) {
                if (p.getName().toLowerCase().startsWith(args[1].toLowerCase())) {
                    players.add(p.getName());
                }
            }
            return players;
        }

        if (args.length == 3 && args[0].equalsIgnoreCase("giveegg")) {
            List<String> qualities = new ArrayList<>();
            for (PetQuality q : PetQuality.values()) {
                if (q.name().toLowerCase().startsWith(args[2].toLowerCase())) {
                    qualities.add(q.name());
                }
            }
            return qualities;
        }

        return Collections.emptyList();
    }
}
