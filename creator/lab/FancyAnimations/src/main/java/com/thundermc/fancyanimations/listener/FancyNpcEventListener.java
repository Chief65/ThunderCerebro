package com.thundermc.fancyanimations.listener;

import com.thundermc.fancyanimations.command.FancyAnimCommand;
import com.thundermc.fancyanimations.config.ConfigManager;
import com.thundermc.fancyanimations.engine.AnimationEngine;
import com.thundermc.fancyanimations.model.NpcAnimationProfile;
import de.oliver.fancynpcs.api.Npc;
import de.oliver.fancynpcs.api.events.NpcCreateEvent;
import de.oliver.fancynpcs.api.events.NpcInteractEvent;
import de.oliver.fancynpcs.api.events.NpcRemoveEvent;
import org.bukkit.ChatColor;
import org.bukkit.Location;
import org.bukkit.Sound;
import org.bukkit.SoundCategory;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerCommandPreprocessEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.event.server.ServerCommandEvent;

import java.util.Arrays;

/**
 * Escucha los eventos oficiales de FancyNpcs para gestionar el ciclo de vida, la interactividad,
 * el feedback auditivo y la limpieza de estados de red.
 * Además intercepta comandos /npcs desc y /npc desc con máxima prioridad para evitar colisiones.
 */
public class FancyNpcEventListener implements Listener {

    private final ConfigManager configManager;
    private final AnimationEngine animationEngine;
    private final FancyAnimCommand cmdHandler;

    public FancyNpcEventListener(ConfigManager configManager, AnimationEngine animationEngine, FancyAnimCommand cmdHandler) {
        this.configManager = configManager;
        this.animationEngine = animationEngine;
        this.cmdHandler = cmdHandler;
    }

    public FancyNpcEventListener(ConfigManager configManager, AnimationEngine animationEngine) {
        this(configManager, animationEngine, null);
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onNpcCreate(NpcCreateEvent event) {
        Npc npc = event.getNpc();
        if (npc == null || npc.getData() == null) return;

        String name = npc.getData().getName();
        if ("ambient".equalsIgnoreCase(configManager.getDefaultProfile())) {
            NpcAnimationProfile profile = configManager.getAmbientPreset().clone();
            configManager.setProfile(name, profile);
        }
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onNpcModify(de.oliver.fancynpcs.api.events.NpcModifyEvent event) {
        Npc npc = event.getNpc();
        if (npc == null || npc.getData() == null) return;

        if (event.getModification() == de.oliver.fancynpcs.api.events.NpcModifyEvent.NpcModification.DISPLAY_NAME) {
            String newDisplayName = String.valueOf(event.getNewValue());
            String key = npc.getData().getId() != null ? npc.getData().getId() : npc.getData().getName();
            if (newDisplayName != null) {
                if (newDisplayName.equalsIgnoreCase("@none") || newDisplayName.equalsIgnoreCase("<empty>")) {
                    animationEngine.getDisplayNameManager().setCachedName(key, npc.getData().getName());
                } else {
                    animationEngine.getDisplayNameManager().setCachedName(key, newDisplayName);
                }
                animationEngine.getDisplayNameManager().forceRefreshTitle(npc, key);
            }
        }
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onNpcRemove(NpcRemoveEvent event) {
        Npc npc = event.getNpc();
        if (npc == null || npc.getData() == null) return;

        String name = npc.getData().getName();
        String id = npc.getData().getId();
        if (name != null) animationEngine.removeState(name);
        if (id != null) animationEngine.removeState(id);
    }

    @EventHandler(priority = EventPriority.NORMAL, ignoreCancelled = true)
    public void onNpcInteract(NpcInteractEvent event) {
        Npc npc = event.getNpc();
        if (npc == null || npc.getData() == null) return;

        Player player = event.getPlayer();

        // 1. Efecto de Sonido: Villager YES al interactuar (dar click)
        if (configManager.isClickSoundEnabled() && player != null) {
            try {
                Sound clickSound = Sound.valueOf(configManager.getClickSoundName());
                Location loc = npc.getData().getLocation();
                player.playSound(loc, clickSound, SoundCategory.VOICE,
                        (float) configManager.getClickSoundVolume(),
                        (float) configManager.getClickSoundPitch());
            } catch (Exception ignored) {
            }
        }

        // 2. Gesto de saludo con brazo al interactuar
        String name = npc.getData().getName();
        NpcAnimationProfile profile = configManager.getProfile(name);
        if (profile.isAmbientActive()) {
            animationEngine.triggerGesture(npc, "wave");
        }
    }

    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = false)
    public void onPlayerCommandPreprocess(PlayerCommandPreprocessEvent event) {
        if (cmdHandler == null) return;
        String message = event.getMessage().trim();
        String lower = message.toLowerCase();

        if (lower.startsWith("/npcs desc") || lower.startsWith("/npc desc") || lower.startsWith("/fanim desc") || lower.startsWith("/npcdesc")) {
            event.setCancelled(true);
            Player player = event.getPlayer();
            if (!player.hasPermission("fancyanimations.admin")) {
                player.sendMessage(ChatColor.RED + "No tienes permiso para ejecutar este comando.");
                return;
            }

            String rawWithoutSlash = message.substring(1).trim();
            String[] parts = rawWithoutSlash.split("\\s+");
            if (parts.length > 0) {
                // Si invocó con /npcdesc ... el subcomando ya es directo; si invocó con /npcs desc ... quitamos 'npcs'
                String[] subArgs;
                if (parts[0].equalsIgnoreCase("npcdesc")) {
                    subArgs = parts;
                } else {
                    subArgs = Arrays.copyOfRange(parts, 1, parts.length);
                }
                cmdHandler.handleDescDirect(player, subArgs, parts[0]);
            }
        }
    }

    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = false)
    public void onServerCommand(ServerCommandEvent event) {
        if (cmdHandler == null) return;
        String message = event.getCommand().trim();
        String lower = message.toLowerCase();

        if (lower.startsWith("npcs desc") || lower.startsWith("npc desc") || lower.startsWith("fanim desc") || lower.startsWith("npcdesc")) {
            event.setCancelled(true);
            String[] parts = message.split("\\s+");
            if (parts.length > 0) {
                String[] subArgs;
                if (parts[0].equalsIgnoreCase("npcdesc")) {
                    subArgs = parts;
                } else {
                    subArgs = Arrays.copyOfRange(parts, 1, parts.length);
                }
                cmdHandler.handleDescDirect(event.getSender(), subArgs, parts[0]);
            }
        }
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onPlayerQuit(PlayerQuitEvent event) {
        animationEngine.clearPlayer(event.getPlayer().getUniqueId());
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onPlayerChangedWorld(org.bukkit.event.player.PlayerChangedWorldEvent event) {
        animationEngine.clearPlayer(event.getPlayer().getUniqueId());
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onPlayerTeleport(org.bukkit.event.player.PlayerTeleportEvent event) {
        if (event.getFrom().getWorld() != null && event.getTo() != null && !event.getFrom().getWorld().equals(event.getTo().getWorld())) {
            animationEngine.clearPlayer(event.getPlayer().getUniqueId());
        }
    }
}
