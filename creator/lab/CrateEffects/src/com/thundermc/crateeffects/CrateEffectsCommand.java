package com.thundermc.crateeffects;

import com.thundermc.crateeffects.opening.ShulkerOpening;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import org.bukkit.Location;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.entity.Player;
import su.nightexpress.excellentcrates.CratesAPI;
import su.nightexpress.excellentcrates.crate.cost.Cost;
import su.nightexpress.excellentcrates.crate.impl.Crate;
import su.nightexpress.excellentcrates.crate.impl.CrateSource;

import java.util.ArrayList;
import java.util.List;

public class CrateEffectsCommand implements CommandExecutor, TabCompleter {

    private final CrateEffects plugin;

    public CrateEffectsCommand(CrateEffects plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!sender.hasPermission("crateeffects.admin")) {
            sender.sendMessage(Component.text("No tienes permiso para ejecutar este comando.", NamedTextColor.RED));
            return true;
        }

        if (args.length == 0) {
            sender.sendMessage(Component.text("--- CrateEffects Addon v1.1.0 ---", NamedTextColor.GOLD));
            sender.sendMessage(Component.text("/" + label + " reload - Recarga la configuracion", NamedTextColor.YELLOW));
            sender.sendMessage(Component.text("/" + label + " test [rareza] - Prueba los fuegos artificiales suaves en tu posicion", NamedTextColor.YELLOW));
            sender.sendMessage(Component.text("/" + label + " testshulker [crate_id] - Prueba la animacion de Shulker CS:GO", NamedTextColor.YELLOW));
            return true;
        }

        if (args[0].equalsIgnoreCase("reload")) {
            plugin.getEffectConfig().load();
            sender.sendMessage(Component.text("[CrateEffects] Configuracion recargada correctamente.", NamedTextColor.GREEN));
            return true;
        }

        if (args[0].equalsIgnoreCase("test")) {
            if (!(sender instanceof Player player)) {
                sender.sendMessage(Component.text("Este comando solo puede ser ejecutado por un jugador.", NamedTextColor.RED));
                return true;
            }

            String rarity = args.length > 1 ? args[1].toLowerCase() : "default";
            Location loc = player.getLocation().add(0, 0.5, 0);

            sender.sendMessage(Component.text("[CrateEffects] Probando fuegos artificiales sutiles con paleta: " + rarity, NamedTextColor.AQUA));
            AnimationRunner.playRewardAnimation(plugin, loc, player, rarity);
            return true;
        }

        if (args[0].equalsIgnoreCase("testshulker")) {
            if (!(sender instanceof Player player)) {
                sender.sendMessage(Component.text("Este comando solo puede ser ejecutado por un jugador.", NamedTextColor.RED));
                return true;
            }

            String crateId = args.length > 1 ? args[1].toLowerCase() : "mitica";
            Crate crate = CratesAPI.getCrateManager().getCrateById(crateId);
            if (crate == null) {
                sender.sendMessage(Component.text("[CrateEffects] Crate '" + crateId + "' no encontrada. Crates disponibles: " +
                        CratesAPI.getCrateManager().getCrateIds(), NamedTextColor.RED));
                return true;
            }

            org.bukkit.block.Block targetBlock = player.getTargetBlockExact(6);
            org.bukkit.block.Block crateBlock = null;
            if (targetBlock != null && !targetBlock.isEmpty()) {
                crateBlock = targetBlock;
            } else if (crate.getBlockPositions() != null) {
                for (su.nightexpress.excellentcrates.util.pos.WorldPos wp : crate.getBlockPositions()) {
                    Location loc = wp.toLocation();
                    if (loc != null && loc.getWorld() != null && loc.getWorld().equals(player.getWorld())) {
                        if (loc.distanceSquared(player.getLocation()) < 400.0) {
                            crateBlock = loc.getBlock();
                            break;
                        }
                    }
                }
            }

            CrateSource source = (crateBlock != null)
                    ? new CrateSource(crate, null, crateBlock)
                    : new CrateSource(crate);
            Cost cost = crate.getFirstCost().orElse(null);
            ShulkerOpening opening = new ShulkerOpening(plugin, CratesAPI.getPlugin(), player, source, cost);
            // CRÍTICO: pasar false para ejecutar la animación normal sin insta-roll!
            CratesAPI.getPlugin().getOpeningManager().startOpening(player, opening, false);

            sender.sendMessage(Component.text("[CrateEffects] Iniciando animacion de prueba Shulker CS:GO para la crate: " + crateId, NamedTextColor.GREEN));
            return true;
        }

        sender.sendMessage(Component.text("Subcomando desconocido. Usa /" + label + " para ver la ayuda.", NamedTextColor.RED));
        return true;
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        if (!sender.hasPermission("crateeffects.admin")) {
            return List.of();
        }

        if (args.length == 1) {
            List<String> list = new ArrayList<>(List.of("reload", "test", "testshulker"));
            list.removeIf(s -> !s.startsWith(args[0].toLowerCase()));
            return list;
        }

        if (args.length == 2 && args[0].equalsIgnoreCase("test")) {
            List<String> rarities = new ArrayList<>(List.of("mitica", "epica", "rara", "comun", "default"));
            rarities.removeIf(s -> !s.startsWith(args[1].toLowerCase()));
            return rarities;
        }

        if (args.length == 2 && args[0].equalsIgnoreCase("testshulker")) {
            List<String> crateIds = new ArrayList<>(CratesAPI.getCrateManager().getCrateIds());
            crateIds.removeIf(s -> !s.startsWith(args[1].toLowerCase()));
            return crateIds;
        }

        return List.of();
    }
}
