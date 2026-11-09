package com.thundermc.fancyanimations.command;

import com.thundermc.fancyanimations.config.ConfigManager;
import com.thundermc.fancyanimations.display.DisplayNameManager;
import com.thundermc.fancyanimations.engine.AnimationEngine;
import com.thundermc.fancyanimations.model.NpcAnimationProfile;
import de.oliver.fancynpcs.api.FancyNpcsPlugin;
import de.oliver.fancynpcs.api.Npc;
import org.bukkit.ChatColor;
import org.bukkit.Location;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.entity.Player;
import org.bukkit.util.BoundingBox;
import org.bukkit.util.RayTraceResult;
import org.bukkit.util.StringUtil;
import org.bukkit.util.Vector;

import java.util.*;

/**
 * Gestor de comandos y autocompletado para /fanim, /npcs, /npcdesc y /ambient.
 * Proporciona control de animaciones, presets y asignación dinámica de descripciones
 * interactivas para el Action Bar al apuntar a NPCs.
 */
public class FancyAnimCommand implements CommandExecutor, TabCompleter {

    private final ConfigManager configManager;
    private final AnimationEngine animationEngine;

    private static final List<String> ROOT_SUBCOMMANDS = Arrays.asList(
            "desc", "ambient", "animate", "play", "preset", "list", "info", "default", "reload"
    );

    private static final List<String> DESC_SUBCOMMANDS = Arrays.asList(
            "add", "set", "remove", "clear", "list", "info", "default"
    );

    private static final List<String> ANIMATION_TYPES = Arrays.asList(
            "breathing", "swaying", "headtilt", "nodding", "microrotation", "lookat", "cursorglow", "randomgestures"
    );

    private static final List<String> GESTURE_TYPES = Arrays.asList(
            "wave", "nod", "offhand"
    );

    private static final List<String> BOOLEAN_VALUES = Arrays.asList(
            "on", "off"
    );

    private static final List<String> PRESETS = Arrays.asList(
            "ambient", "none"
    );

    public FancyAnimCommand(ConfigManager configManager, AnimationEngine animationEngine) {
        this.configManager = configManager;
        this.animationEngine = animationEngine;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!sender.hasPermission("fancyanimations.admin")) {
            sender.sendMessage(ChatColor.RED + "No tienes permiso para ejecutar este comando.");
            return true;
        }

        if (args.length == 0) {
            sendHelp(sender, label);
            return true;
        }

        String sub = args[0].toLowerCase();
        switch (sub) {
            case "desc", "descripcion", "description" -> handleDesc(sender, args, label);
            case "ambient", "ambiental" -> handleAmbient(sender, args, label);
            case "animate", "animar" -> handleAnimate(sender, args, label);
            case "play", "gesto" -> handlePlay(sender, args, label);
            case "preset" -> handlePreset(sender, args, label);
            case "list", "listar" -> handleList(sender);
            case "info" -> handleInfo(sender, args, label);
            case "default", "defecto" -> handleDefault(sender, args, label);
            case "reload", "recargar" -> handleReload(sender);
            default -> sendHelp(sender, label);
        }
        return true;
    }

    /**
     * Intercepta y despacha comandos directos como /npcs desc ... o /npc desc ...
     */
    public void handleDescDirect(CommandSender sender, String[] args, String label) {
        if (!sender.hasPermission("fancyanimations.admin")) {
            sender.sendMessage(ChatColor.RED + "No tienes permiso para ejecutar este comando.");
            return;
        }
        handleDesc(sender, args, label);
    }

    public void handleDesc(CommandSender sender, String[] args, String label) {
        String[] cleanArgs;
        if (args.length > 0 && (args[0].equalsIgnoreCase("desc") || args[0].equalsIgnoreCase("descripcion") || args[0].equalsIgnoreCase("description"))) {
            cleanArgs = Arrays.copyOfRange(args, 1, args.length);
        } else {
            cleanArgs = args;
        }

        if (cleanArgs.length == 0) {
            sendDescHelp(sender, label);
            return;
        }

        String action = cleanArgs[0].toLowerCase();
        switch (action) {
            case "add", "set", "crear", "poner" -> handleDescAdd(sender, cleanArgs, label);
            case "remove", "rem", "delete", "del", "clear", "quitar", "borrar" -> handleDescRemove(sender, cleanArgs, label);
            case "list", "listar" -> handleDescList(sender);
            case "default", "defecto" -> handleDescDefault(sender, cleanArgs, label);
            case "info", "get", "ver" -> handleDescInfo(sender, cleanArgs, label);
            default -> sendDescHelp(sender, label);
        }
    }

    private void handleDescAdd(CommandSender sender, String[] args, String label) {
        if (args.length < 2) {
            sender.sendMessage(ChatColor.YELLOW + "Uso: /" + label + " desc add [npc] <texto de descripción>");
            return;
        }

        Npc targetNpc = findNpc(args[1]);
        String descriptionText;

        if (targetNpc != null && args.length >= 3) {
            // Caso explícito: /npcs desc add <npc> <texto...>
            descriptionText = String.join(" ", Arrays.copyOfRange(args, 2, args.length));
        } else {
            // Caso contextual: /npcs desc add <texto...> mirando a un NPC
            if (sender instanceof Player player) {
                targetNpc = getTargetNpc(player, 10.0);
                if (targetNpc != null) {
                    descriptionText = String.join(" ", Arrays.copyOfRange(args, 1, args.length));
                } else {
                    if (findNpc(args[1]) != null) {
                        sender.sendMessage(ChatColor.YELLOW + "Falta el texto de la descripción. Uso: /" + label + " desc add " + args[1] + " <texto>");
                        return;
                    }
                    sender.sendMessage(ChatColor.RED + "No estás apuntando a ningún NPC y no se encontró el NPC '" + args[1] + "'.");
                    sender.sendMessage(ChatColor.YELLOW + "Apunta a un NPC con la mira o indica su nombre: /" + label + " desc add [npc] <texto>");
                    return;
                }
            } else {
                if (targetNpc == null) {
                    sender.sendMessage(ChatColor.RED + "NPC no encontrado: " + args[1]);
                    return;
                }
                sender.sendMessage(ChatColor.YELLOW + "Uso desde consola: /" + label + " desc add <npc> <texto>");
                return;
            }
        }

        String npcKey = targetNpc.getData().getName();
        configManager.setNpcDescription(npcKey, descriptionText);
        if (targetNpc.getData().getId() != null) {
            configManager.setNpcDescription(targetNpc.getData().getId(), descriptionText);
        }

        sender.sendMessage(ChatColor.GREEN + "Descripción asignada al NPC " + ChatColor.AQUA + npcKey + ChatColor.GREEN + ":");
        sender.sendMessage(DisplayNameManager.parseText("  " + descriptionText));
    }

    private void handleDescRemove(CommandSender sender, String[] args, String label) {
        Npc targetNpc = null;
        if (args.length >= 2) {
            targetNpc = findNpc(args[1]);
            if (targetNpc == null) {
                sender.sendMessage(ChatColor.RED + "NPC no encontrado: " + args[1]);
                return;
            }
        } else if (sender instanceof Player player) {
            targetNpc = getTargetNpc(player, 10.0);
            if (targetNpc == null) {
                sender.sendMessage(ChatColor.RED + "No estás apuntando a ningún NPC. Especifica el nombre: /" + label + " desc remove <npc>");
                return;
            }
        } else {
            sender.sendMessage(ChatColor.YELLOW + "Uso desde consola: /" + label + " desc remove <npc>");
            return;
        }

        String npcKey = targetNpc.getData().getName();
        configManager.removeNpcDescription(npcKey);
        if (targetNpc.getData().getId() != null) {
            configManager.removeNpcDescription(targetNpc.getData().getId());
        }

        sender.sendMessage(ChatColor.GREEN + "Descripción personalizada eliminada para el NPC " + ChatColor.AQUA + npcKey + ChatColor.GREEN + ".");
        sender.sendMessage(ChatColor.GRAY + "Ahora mostrará la descripción por defecto: " + ChatColor.WHITE + configManager.getDefaultDescription());
    }

    private void handleDescDefault(CommandSender sender, String[] args, String label) {
        if (args.length < 2) {
            sender.sendMessage(ChatColor.GRAY + "Descripción por defecto actual: ");
            sender.sendMessage(DisplayNameManager.parseText("  " + configManager.getDefaultDescription()));
            sender.sendMessage(ChatColor.YELLOW + "Para cambiarla: /" + label + " desc default <texto...>");
            return;
        }

        String newDefault = String.join(" ", Arrays.copyOfRange(args, 1, args.length));
        configManager.setDefaultDescription(newDefault);
        sender.sendMessage(ChatColor.GREEN + "Descripción por defecto para NPCs actualizada a:");
        sender.sendMessage(DisplayNameManager.parseText("  " + newDefault));
    }

    private void handleDescList(CommandSender sender) {
        Map<String, String> descs = configManager.getNpcDescriptions();
        sender.sendMessage(ChatColor.GOLD + "=== Descripciones de NPCs (" + descs.size() + ") ===");
        sender.sendMessage(ChatColor.GRAY + "Por defecto: " + ChatColor.RESET);
        sender.sendMessage(DisplayNameManager.parseText("  " + configManager.getDefaultDescription()));
        if (descs.isEmpty()) {
            sender.sendMessage(ChatColor.YELLOW + "No hay descripciones personalizadas asignadas a NPCs.");
            return;
        }
        for (Map.Entry<String, String> entry : descs.entrySet()) {
            sender.sendMessage(ChatColor.AQUA + "- " + entry.getKey() + ChatColor.GRAY + ":");
            sender.sendMessage(DisplayNameManager.parseText("    " + entry.getValue()));
        }
    }

    private void handleDescInfo(CommandSender sender, String[] args, String label) {
        Npc targetNpc = null;
        if (args.length >= 2) {
            targetNpc = findNpc(args[1]);
            if (targetNpc == null) {
                sender.sendMessage(ChatColor.RED + "NPC no encontrado: " + args[1]);
                return;
            }
        } else if (sender instanceof Player player) {
            targetNpc = getTargetNpc(player, 10.0);
            if (targetNpc == null) {
                sender.sendMessage(ChatColor.RED + "No estás apuntando a ningún NPC. Uso: /" + label + " desc info [npc]");
                return;
            }
        } else {
            sender.sendMessage(ChatColor.YELLOW + "Uso desde consola: /" + label + " desc info <npc>");
            return;
        }

        String name = targetNpc.getData().getName();
        String custom = configManager.getNpcDescription(name);
        sender.sendMessage(ChatColor.GOLD + "=== Descripción del NPC: " + ChatColor.AQUA + name + ChatColor.GOLD + " ===");
        if (custom != null && !custom.trim().isEmpty()) {
            sender.sendMessage(ChatColor.GRAY + "Tipo: " + ChatColor.GREEN + "Personalizada");
            sender.sendMessage(ChatColor.GRAY + "Texto: ");
            sender.sendMessage(DisplayNameManager.parseText("  " + custom));
        } else {
            sender.sendMessage(ChatColor.GRAY + "Tipo: " + ChatColor.DARK_AQUA + "Por defecto");
            sender.sendMessage(ChatColor.GRAY + "Texto: ");
            sender.sendMessage(DisplayNameManager.parseText("  " + configManager.getDefaultDescription()));
        }
    }

    private void sendDescHelp(CommandSender sender, String label) {
        sender.sendMessage(ChatColor.GOLD + "=== Gestión de Descripciones de NPCs ===");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " desc add [npc] <texto...> " + ChatColor.GRAY + "- Asigna una descripción al NPC (apuntando o por nombre)");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " desc remove [npc] " + ChatColor.GRAY + "- Elimina la descripción personalizada");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " desc list " + ChatColor.GRAY + "- Lista los NPCs con descripción personalizada");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " desc info [npc] " + ChatColor.GRAY + "- Muestra la descripción del NPC");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " desc default <texto...> " + ChatColor.GRAY + "- Modifica el texto por defecto");
    }

    private void handleAmbient(CommandSender sender, String[] args, String label) {
        if (args.length < 3) {
            sender.sendMessage(ChatColor.YELLOW + "Uso: /" + label + " ambient <npc> <on|off>");
            return;
        }
        String npcName = args[1];
        Npc npc = findNpc(npcName);
        if (npc == null) {
            sender.sendMessage(ChatColor.RED + "NPC no encontrado: " + npcName);
            return;
        }

        boolean enable = args[2].equalsIgnoreCase("on") || args[2].equalsIgnoreCase("true");
        NpcAnimationProfile profile = configManager.getProfile(npc.getData().getName());
        profile.setAmbient(enable, configManager.getAmbientPreset());
        configManager.setProfile(npc.getData().getName(), profile);

        if (enable) {
            sender.sendMessage(ChatColor.GREEN + "Conjunto ambiental activado para el NPC: " + ChatColor.AQUA + npc.getData().getName());
        } else {
            sender.sendMessage(ChatColor.YELLOW + "Conjunto ambiental desactivado para el NPC: " + ChatColor.AQUA + npc.getData().getName());
        }
    }

    private void handleAnimate(CommandSender sender, String[] args, String label) {
        if (args.length < 4) {
            sender.sendMessage(ChatColor.YELLOW + "Uso: /" + label + " animate <npc> <tipo> <on|off>");
            return;
        }
        String npcName = args[1];
        Npc npc = findNpc(npcName);
        if (npc == null) {
            sender.sendMessage(ChatColor.RED + "NPC no encontrado: " + npcName);
            return;
        }

        String animType = args[2];
        boolean enable = args[3].equalsIgnoreCase("on") || args[3].equalsIgnoreCase("true");
        NpcAnimationProfile profile = configManager.getProfile(npc.getData().getName());

        if (!profile.setByName(animType, enable)) {
            sender.sendMessage(ChatColor.RED + "Tipo de animación no válido. Opciones: " + String.join(", ", ANIMATION_TYPES));
            return;
        }

        configManager.setProfile(npc.getData().getName(), profile);
        sender.sendMessage(ChatColor.GREEN + "Animación " + ChatColor.YELLOW + animType +
                (enable ? ChatColor.GREEN + " activada" : ChatColor.RED + " desactivada") +
                ChatColor.GREEN + " para " + ChatColor.AQUA + npc.getData().getName());
    }

    private void handlePlay(CommandSender sender, String[] args, String label) {
        if (args.length < 3) {
            sender.sendMessage(ChatColor.YELLOW + "Uso: /" + label + " play <npc> <wave|nod|offhand>");
            return;
        }
        String npcName = args[1];
        Npc npc = findNpc(npcName);
        if (npc == null) {
            sender.sendMessage(ChatColor.RED + "NPC no encontrado: " + npcName);
            return;
        }

        String gesture = args[2];
        animationEngine.triggerGesture(npc, gesture);
        sender.sendMessage(ChatColor.GREEN + "Gesto " + ChatColor.YELLOW + gesture + ChatColor.GREEN + " reproducido en " + ChatColor.AQUA + npc.getData().getName());
    }

    private void handlePreset(CommandSender sender, String[] args, String label) {
        if (args.length < 3) {
            sender.sendMessage(ChatColor.YELLOW + "Uso: /" + label + " preset <npc> <ambient|none>");
            return;
        }
        String npcName = args[1];
        Npc npc = findNpc(npcName);
        if (npc == null) {
            sender.sendMessage(ChatColor.RED + "NPC no encontrado: " + npcName);
            return;
        }

        String preset = args[2].toLowerCase();
        NpcAnimationProfile profile = configManager.getProfile(npc.getData().getName());
        if ("ambient".equals(preset)) {
            profile.setAmbient(true, configManager.getAmbientPreset());
            configManager.setProfile(npc.getData().getName(), profile);
            sender.sendMessage(ChatColor.GREEN + "Preset 'ambient' aplicado a " + ChatColor.AQUA + npc.getData().getName());
        } else if ("none".equals(preset)) {
            profile.setAmbient(false, configManager.getAmbientPreset());
            configManager.setProfile(npc.getData().getName(), profile);
            sender.sendMessage(ChatColor.YELLOW + "Todas las animaciones desactivadas para " + ChatColor.AQUA + npc.getData().getName());
        } else {
            sender.sendMessage(ChatColor.RED + "Preset no reconocido. Usa 'ambient' o 'none'.");
        }
    }

    private void handleList(CommandSender sender) {
        if (FancyNpcsPlugin.get() == null || FancyNpcsPlugin.get().getNpcManager() == null) {
            sender.sendMessage(ChatColor.RED + "FancyNpcs no está cargado.");
            return;
        }
        Collection<Npc> npcs = FancyNpcsPlugin.get().getNpcManager().getAllNpcs();
        if (npcs.isEmpty()) {
            sender.sendMessage(ChatColor.YELLOW + "No hay NPCs registrados en FancyNpcs.");
            return;
        }

        sender.sendMessage(ChatColor.GOLD + "=== NPCs y Perfiles de Animación (" + npcs.size() + ") ===");
        for (Npc npc : npcs) {
            String name = npc.getData().getName();
            NpcAnimationProfile profile = configManager.getProfile(name);
            boolean custom = configManager.hasCustomProfile(name);
            String status = profile.isAmbientActive() ? ChatColor.GREEN + "[AMBIENTAL ACTIVO]" : ChatColor.GRAY + "[INACTIVO]";
            String origin = custom ? ChatColor.YELLOW + "(Personalizado)" : ChatColor.DARK_AQUA + "(Por defecto: " + configManager.getDefaultProfile() + ")";
            sender.sendMessage(ChatColor.GRAY + "- " + ChatColor.AQUA + name + " " + status + " " + origin);
        }
    }

    private void handleInfo(CommandSender sender, String[] args, String label) {
        if (args.length < 2) {
            sender.sendMessage(ChatColor.YELLOW + "Uso: /" + label + " info <npc>");
            return;
        }
        String npcName = args[1];
        Npc npc = findNpc(npcName);
        if (npc == null) {
            sender.sendMessage(ChatColor.RED + "NPC no encontrado: " + npcName);
            return;
        }

        String name = npc.getData().getName();
        NpcAnimationProfile p = configManager.getProfile(name);
        boolean custom = configManager.hasCustomProfile(name);

        sender.sendMessage(ChatColor.GOLD + "=== Estado de Animación: " + ChatColor.AQUA + name + ChatColor.GOLD + " ===");
        sender.sendMessage(ChatColor.GRAY + "Origen: " + (custom ? ChatColor.YELLOW + "Configuración propia" : ChatColor.DARK_AQUA + "Heredado de default-profile"));
        sender.sendMessage(ChatColor.GRAY + "Respiración (Breathing): " + formatBool(p.isBreathing()));
        sender.sendMessage(ChatColor.GRAY + "Balanceo (Swaying): " + formatBool(p.isSwaying()));
        sender.sendMessage(ChatColor.GRAY + "Ladeo de Cabeza (Head Tilt): " + formatBool(p.isHeadTilt()));
        sender.sendMessage(ChatColor.GRAY + "Cabeceo / Asentimiento (Nodding): " + formatBool(p.isNodding()));
        sender.sendMessage(ChatColor.GRAY + "Micro-rotación (Mirada viva): " + formatBool(p.isMicroRotation()));
        sender.sendMessage(ChatColor.GRAY + "Seguimiento de Mirada (Look-At): " + formatBool(p.isLookAtPlayer()));
        sender.sendMessage(ChatColor.GRAY + "Cursor Glow (Resplandor al apuntar): " + formatBool(p.isCursorGlow()));
        sender.sendMessage(ChatColor.GRAY + "Gestos aleatorios (Brazos): " + formatBool(p.isRandomGestures()));
    }

    private void handleDefault(CommandSender sender, String[] args, String label) {
        if (args.length < 2) {
            sender.sendMessage(ChatColor.GRAY + "Perfil por defecto actual: " + ChatColor.AQUA + configManager.getDefaultProfile());
            sender.sendMessage(ChatColor.YELLOW + "Uso para cambiar: /" + label + " default <ambient|none>");
            return;
        }
        String val = args[1].toLowerCase();
        if ("ambient".equals(val) || "none".equals(val)) {
            configManager.setDefaultProfile(val);
            sender.sendMessage(ChatColor.GREEN + "Perfil por defecto para NPCs nuevos y no configurados cambiado a: " + ChatColor.AQUA + val);
        } else {
            sender.sendMessage(ChatColor.RED + "Opciones válidas: 'ambient' o 'none'");
        }
    }

    private void handleReload(CommandSender sender) {
        configManager.load();
        sender.sendMessage(ChatColor.GREEN + "[FancyAnimations] Configuración recargada correctamente.");
    }

    private String formatBool(boolean b) {
        return b ? ChatColor.GREEN + "ON" : ChatColor.RED + "OFF";
    }

    public Npc findNpc(String name) {
        if (FancyNpcsPlugin.get() == null || FancyNpcsPlugin.get().getNpcManager() == null) return null;
        Npc byName = FancyNpcsPlugin.get().getNpcManager().getNpc(name);
        if (byName != null) return byName;
        return FancyNpcsPlugin.get().getNpcManager().getNpcById(name);
    }

    public static Npc getTargetNpc(Player player, double maxDist) {
        if (FancyNpcsPlugin.get() == null || FancyNpcsPlugin.get().getNpcManager() == null) {
            return null;
        }
        Location eye = player.getEyeLocation();
        Vector dir = eye.getDirection().normalize();

        Npc closestHitNpc = null;
        double closestHitDist = Double.MAX_VALUE;

        Collection<Npc> all = FancyNpcsPlugin.get().getNpcManager().getAllNpcs();
        if (all == null || all.isEmpty()) return null;

        for (Npc npc : all) {
            if (npc == null || npc.getData() == null || npc.getData().getLocation() == null) continue;
            Location loc = npc.getData().getLocation();
            if (loc.getWorld() == null || !loc.getWorld().equals(player.getWorld())) continue;

            double d = loc.distance(eye);
            if (d > maxDist) continue;

            BoundingBox box = new BoundingBox(
                    loc.getX() - 0.6,
                    loc.getY() - 0.2,
                    loc.getZ() - 0.6,
                    loc.getX() + 0.6,
                    loc.getY() + 2.7,
                    loc.getZ() + 0.6
            );

            RayTraceResult hit = box.rayTrace(eye.toVector(), dir, maxDist);
            if (hit != null) {
                double hitDist = eye.toVector().distance(hit.getHitPosition());
                if (hitDist < closestHitDist) {
                    closestHitDist = hitDist;
                    closestHitNpc = npc;
                }
            }
        }

        if (closestHitNpc != null) return closestHitNpc;

        // Fallback: cono de visión para detección cercana suave
        Npc closestConeNpc = null;
        double bestDot = 0.70;
        for (Npc npc : all) {
            if (npc == null || npc.getData() == null || npc.getData().getLocation() == null) continue;
            Location loc = npc.getData().getLocation();
            if (loc.getWorld() == null || !loc.getWorld().equals(player.getWorld())) continue;

            double d = loc.distance(eye);
            if (d > 6.0) continue;

            Vector toNpc = loc.clone().add(0, 1.2, 0).toVector().subtract(eye.toVector()).normalize();
            double dot = dir.dot(toNpc);
            if (dot > bestDot) {
                bestDot = dot;
                closestConeNpc = npc;
            }
        }
        return closestConeNpc;
    }

    private void sendHelp(CommandSender sender, String label) {
        sender.sendMessage(ChatColor.GOLD + "=== FancyAnimations (Addon Oficial ThunderMC) ===");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " desc add [npc] <texto...> " + ChatColor.GRAY + "- Asigna una descripción interactiva al Action Bar");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " desc remove [npc] " + ChatColor.GRAY + "- Elimina la descripción personalizada del NPC");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " desc list " + ChatColor.GRAY + "- Lista los NPCs con descripción personalizada");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " desc default <texto...> " + ChatColor.GRAY + "- Cambia el texto por defecto ('Npc clickeable')");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " ambient <npc> <on|off> " + ChatColor.GRAY + "- Activa/desactiva el paquete ambiental");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " animate <npc> <tipo> <on|off> " + ChatColor.GRAY + "- Controla una animación específica");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " play <npc> <gesto> " + ChatColor.GRAY + "- Reproduce un gesto inmediato");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " list " + ChatColor.GRAY + "- Lista los NPCs y su estado");
        sender.sendMessage(ChatColor.YELLOW + "/" + label + " reload " + ChatColor.GRAY + "- Recarga la configuración");
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        if (!sender.hasPermission("fancyanimations.admin")) return Collections.emptyList();

        List<String> completions = new ArrayList<>();
        if (args.length == 1) {
            StringUtil.copyPartialMatches(args[0], ROOT_SUBCOMMANDS, completions);
            Collections.sort(completions);
            return completions;
        }

        if (args.length == 2) {
            String sub = args[0].toLowerCase();
            if ("desc".equals(sub)) {
                StringUtil.copyPartialMatches(args[1], DESC_SUBCOMMANDS, completions);
                Collections.sort(completions);
                return completions;
            } else if (Arrays.asList("ambient", "animate", "play", "preset", "info").contains(sub)) {
                List<String> npcNames = getNpcNames();
                StringUtil.copyPartialMatches(args[1], npcNames, completions);
                Collections.sort(completions);
                return completions;
            } else if ("default".equals(sub)) {
                StringUtil.copyPartialMatches(args[1], PRESETS, completions);
                return completions;
            }
        }

        if (args.length == 3) {
            String sub = args[0].toLowerCase();
            if ("desc".equals(sub)) {
                String descSub = args[1].toLowerCase();
                if (Arrays.asList("add", "set", "remove", "clear", "info").contains(descSub)) {
                    List<String> npcNames = getNpcNames();
                    StringUtil.copyPartialMatches(args[2], npcNames, completions);
                    Collections.sort(completions);
                    return completions;
                }
            } else if ("ambient".equals(sub)) {
                StringUtil.copyPartialMatches(args[2], BOOLEAN_VALUES, completions);
            } else if ("animate".equals(sub)) {
                StringUtil.copyPartialMatches(args[2], ANIMATION_TYPES, completions);
            } else if ("play".equals(sub)) {
                StringUtil.copyPartialMatches(args[2], GESTURE_TYPES, completions);
            } else if ("preset".equals(sub)) {
                StringUtil.copyPartialMatches(args[2], PRESETS, completions);
            }
            Collections.sort(completions);
            return completions;
        }

        if (args.length == 4) {
            if ("animate".equalsIgnoreCase(args[0])) {
                StringUtil.copyPartialMatches(args[3], BOOLEAN_VALUES, completions);
                Collections.sort(completions);
                return completions;
            }
        }

        return Collections.emptyList();
    }

    private List<String> getNpcNames() {
        if (FancyNpcsPlugin.get() == null || FancyNpcsPlugin.get().getNpcManager() == null) {
            return Collections.emptyList();
        }
        List<String> names = new ArrayList<>();
        for (Npc npc : FancyNpcsPlugin.get().getNpcManager().getAllNpcs()) {
            if (npc.getData() != null && npc.getData().getName() != null) {
                names.add(npc.getData().getName());
            }
        }
        return names;
    }
}
