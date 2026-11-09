package com.thundermc.fancyanimations.display;

import com.thundermc.fancyanimations.config.ConfigManager;
import com.thundermc.fancyanimations.network.PacketUtil;
import de.oliver.fancynpcs.api.Npc;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import net.kyori.adventure.text.minimessage.MiniMessage;
import net.kyori.adventure.text.serializer.legacy.LegacyComponentSerializer;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Location;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Gestor de Display Names fluidos con arquitectura Bicapa (Dual Virtual TextDisplays):
 * - Capa 1 (Título / Nombre): Sin fondo en reposo (transparente: 0), adquiere fondo negro
 *   translúcido (0x40000000), tamaño expandido (1.38) y flechas verdes (&a▶ &a&lNombre &a◀)
 *   ÚNICAMENTE cuando el jugador lo tiene seleccionado con el cursor.
 * - Capa 2 (Subtítulo): Background transparente (0), tamaño estándar (1.0) constante en
 *   ambas situaciones, texto permanente &7ᴄʟɪᴄᴋ ᴘᴀʀᴀ ᴠᴇʀ.
 * Ambas capas flotan sincronizadas milimétricamente con el eje Y de respiración del NPC.
 */
public class DisplayNameManager {

    private final JavaPlugin plugin;
    private final ConfigManager configManager;

    // Entity IDs virtuales duales para cada NPC
    private final AtomicInteger idCounter = new AtomicInteger(1_900_000_000);
    private final Map<String, Integer> npcTitleEntityIds = new ConcurrentHashMap<>();
    private final Map<String, Integer> npcSubtitleEntityIds = new ConcurrentHashMap<>();
    private final Map<String, UUID> npcTitleUuids = new ConcurrentHashMap<>();
    private final Map<String, UUID> npcSubtitleUuids = new ConcurrentHashMap<>();

    // Jugadores que actualmente tienen los TextDisplays spawneados en su cliente
    private final Map<String, Set<UUID>> trackingPlayers = new ConcurrentHashMap<>();

    // Caché de nombres limpios antes de ocultar el nametag nativo de FancyNpcs
    private final Map<String, String> cachedOriginalNames = new ConcurrentHashMap<>();

    private static final LegacyComponentSerializer LEGACY_SECTION = LegacyComponentSerializer.legacySection();

    public DisplayNameManager(JavaPlugin plugin, ConfigManager configManager) {
        this.plugin = plugin;
        this.configManager = configManager;
    }

    public int getOrCreateTitleEntityId(String npcKey) {
        return npcTitleEntityIds.computeIfAbsent(npcKey.toLowerCase(), k -> idCounter.getAndAdd(2));
    }

    public int getOrCreateSubtitleEntityId(String npcKey) {
        return npcSubtitleEntityIds.computeIfAbsent(npcKey.toLowerCase(), k -> getOrCreateTitleEntityId(npcKey) + 1);
    }

    public UUID getOrCreateTitleUuid(String npcKey) {
        return npcTitleUuids.computeIfAbsent(npcKey.toLowerCase(), k -> UUID.randomUUID());
    }

    public UUID getOrCreateSubtitleUuid(String npcKey) {
        return npcSubtitleUuids.computeIfAbsent(npcKey.toLowerCase(), k -> UUID.randomUUID());
    }

    public void setCachedName(String npcKey, String newName) {
        if (newName != null && !newName.isEmpty()) {
            cachedOriginalNames.put(npcKey.toLowerCase(), newName);
        }
    }

    /**
     * Resuelve el nombre base del NPC (priorizando configuración custom, displayname previo o name).
     */
    public String resolveCleanName(Npc npc, String npcKey) {
        String custom = configManager.getNpcDisplayName(npcKey);
        if (custom != null && !custom.isEmpty()) {
            return custom;
        }

        String cached = cachedOriginalNames.get(npcKey.toLowerCase());
        if (cached != null) return cached;

        String dName = npc.getData().getDisplayName();
        if (dName != null && !dName.isEmpty() && !dName.equalsIgnoreCase("<empty>")) {
            cachedOriginalNames.put(npcKey.toLowerCase(), dName);
            return dName;
        }

        String name = npc.getData().getName();
        if (name != null && !name.isEmpty()) {
            cachedOriginalNames.put(npcKey.toLowerCase(), name);
            return name;
        }

        return "NPC";
    }

    /**
     * Oculta el nametag vanilla de FancyNpcs, asegura que el Glowing sea verde
     * y detecta cambios de nombre dinámicos realizados mediante comandos de FancyNpcs.
     */
    public void ensureNpcConfigured(Npc npc, String npcKey) {
        boolean dirty = false;

        String current = npc.getData().getDisplayName();
        if (current != null && !current.equalsIgnoreCase("<empty>")) {
            String old = cachedOriginalNames.put(npcKey.toLowerCase(), current);
            npc.getData().setDisplayName("<empty>");
            dirty = true;
            if (old == null || !old.equals(current)) {
                forceRefreshTitle(npc, npcKey);
            }
        }

        if (npc.getData().getGlowingColor() != NamedTextColor.GREEN) {
            npc.getData().setGlowingColor(NamedTextColor.GREEN);
            dirty = true;
        }

        if (dirty) {
            npc.updateForAll();
        }
    }

    public void forceRefreshTitle(Npc npc, String npcKey) {
        int titleId = getOrCreateTitleEntityId(npcKey);
        Set<UUID> tracking = trackingPlayers.get(npcKey.toLowerCase());
        if (tracking == null || tracking.isEmpty()) return;

        String cleanName = resolveCleanName(npc, npcKey);
        float normalScale = (float) configManager.getTitleNormalScale();

        for (UUID pUuid : tracking) {
            Player p = Bukkit.getPlayer(pUuid);
            if (p != null && p.isOnline()) {
                Component titleComp = createTitleComponent(p, cleanName, false);
                PacketUtil.updateTextDisplay(p, titleId, titleComp, normalScale, 1, 0x40000000);
            }
        }
    }

    /**
     * Sincroniza la cinemática de las dos capas de TextDisplay en cada tick con la respiración del NPC.
     */
    public void tickNpc(Npc npc, String npcKey, Location animLoc, Collection<Player> nearbyPlayers, Set<UUID> aimingPlayerIds) {
        if (!configManager.isDisplayNamesEnabled()) return;

        ensureNpcConfigured(npc, npcKey);

        int titleId = getOrCreateTitleEntityId(npcKey);
        int subtitleId = getOrCreateSubtitleEntityId(npcKey);
        UUID titleUuid = getOrCreateTitleUuid(npcKey);
        UUID subtitleUuid = getOrCreateSubtitleUuid(npcKey);

        String cleanName = resolveCleanName(npc, npcKey);
        String subtitleText = configManager.getNpcSubtitle(npcKey);

        float npcScale = npc.getData().getScale();
        if (npcScale <= 0) npcScale = 1.0f;

        double titleOffset = configManager.getTitleHeightOffset() * npcScale;
        double subtitleOffset = configManager.getSubtitleHeightOffset() * npcScale;

        Location titleLoc = animLoc.clone().add(0, titleOffset, 0);
        Location subtitleLoc = animLoc.clone().add(0, subtitleOffset, 0);

        Set<UUID> tracking = trackingPlayers.computeIfAbsent(npcKey.toLowerCase(), k -> ConcurrentHashMap.newKeySet());
        Set<UUID> currentNearbyUuids = new HashSet<>();

        float normalTitleScale = (float) configManager.getTitleNormalScale();
        float hoverTitleScale = (float) configManager.getTitleHoverScale();
        float subScale = (float) configManager.getSubtitleScale();
        int interpTicks = configManager.getTitleInterpolationTicks();

        Component subComponent = parseText(subtitleText);

        for (Player p : nearbyPlayers) {
            UUID pUuid = p.getUniqueId();
            currentNearbyUuids.add(pUuid);

            boolean isAiming = aimingPlayerIds.contains(pUuid);
            float currentTitleScale = isAiming ? hoverTitleScale : normalTitleScale;
            // El background negro translúcido (0x40000000) en el título tanto en reposo como en selección
            int titleBg = 0x40000000;
            Component titleComponent = createTitleComponent(p, cleanName, isAiming);

            if (!tracking.contains(pUuid)) {
                // 1. Spawnea Capa Título (Background negro translúcido)
                PacketUtil.spawnTextDisplay(p, titleId, titleUuid, titleLoc, titleComponent, currentTitleScale, interpTicks, titleBg);

                // 2. Spawnea Capa Subtítulo (Background 0 = 100% transparente en ambas situaciones, tamaño 1.0)
                PacketUtil.spawnTextDisplay(p, subtitleId, subtitleUuid, subtitleLoc, subComponent, subScale, 1, 0);

                tracking.add(pUuid);
            } else {
                // Teleport sincronizado al eje Y de respiración en ambas capas
                PacketUtil.teleportTextDisplay(p, titleId, titleLoc);
                PacketUtil.teleportTextDisplay(p, subtitleId, subtitleLoc);
            }
        }

        // Jugadores que salieron del rango -> Destruir ambas capas
        Iterator<UUID> it = tracking.iterator();
        while (it.hasNext()) {
            UUID trackedUuid = it.next();
            if (!currentNearbyUuids.contains(trackedUuid)) {
                Player p = Bukkit.getPlayer(trackedUuid);
                if (p != null && p.isOnline()) {
                    PacketUtil.destroyTextDisplay(p, titleId);
                    PacketUtil.destroyTextDisplay(p, subtitleId);
                }
                it.remove();
            }
        }
    }

    /**
     * Notificación instantánea de cambio de hover (apuntar / desapuntar con cursor).
     * El título cambia entre escala normal (1.20) y hover (1.38) y color verde, manteniendo su fondo translúcido.
     */
    public void updateHover(Player player, Npc npc, String npcKey, boolean isAiming) {
        if (!configManager.isDisplayNamesEnabled()) return;

        int titleId = getOrCreateTitleEntityId(npcKey);
        Set<UUID> tracking = trackingPlayers.get(npcKey.toLowerCase());
        if (tracking == null || !tracking.contains(player.getUniqueId())) return;

        String cleanName = resolveCleanName(npc, npcKey);
        float scale = isAiming ? (float) configManager.getTitleHoverScale() : (float) configManager.getTitleNormalScale();
        int interpTicks = configManager.getTitleInterpolationTicks();
        Component text = createTitleComponent(player, cleanName, isAiming);

        PacketUtil.updateTextDisplay(player, titleId, text, scale, interpTicks, 0x40000000);
    }

    public Component createTitleComponent(Player player, String cleanName, boolean isAiming) {
        String plain = ChatColor.stripColor(ChatColor.translateAlternateColorCodes('&', cleanName));
        String format;
        if (isAiming) {
            if (configManager.isBedrockAdaptationEnabled() && isBedrockPlayer(player)) {
                format = configManager.getBedrockTitleHoverFormat();
            } else {
                format = configManager.getTitleHoverFormat();
            }
        } else {
            format = configManager.getTitleNormalFormat();
        }
        String raw = format.replace("%name%", plain);
        return parseText(raw);
    }

    public Component createTitleComponent(String cleanName, boolean isAiming) {
        return createTitleComponent(null, cleanName, isAiming);
    }

    private static Boolean floodgateAvailable = null;

    /**
     * Comprueba si el jugador proviene de Minecraft Bedrock (vía Floodgate API o prefijos).
     */
    public static boolean isBedrockPlayer(Player player) {
        if (player == null) return false;

        if (floodgateAvailable == null) {
            floodgateAvailable = Bukkit.getPluginManager().isPluginEnabled("floodgate");
        }

        if (floodgateAvailable) {
            try {
                return org.geysermc.floodgate.api.FloodgateApi.getInstance().isFloodgatePlayer(player.getUniqueId());
            } catch (Throwable t) {
                floodgateAvailable = false;
            }
        }

        String name = player.getName();
        return name.startsWith(".") || name.startsWith("*");
    }

    /**
     * Parser universal robusto: soporta MiniMessage (<...>) y códigos clásicos (&a, &f, §a, etc.).
     */
    public static Component parseText(String raw) {
        if (raw == null || raw.isEmpty()) return Component.empty();

        // Si contiene tags de MiniMessage (<green>, <white>, etc.)
        if (raw.contains("<") && raw.contains(">")) {
            try {
                return MiniMessage.miniMessage().deserialize(raw);
            } catch (Exception ignored) {
            }
        }

        // Códigos estándar ampersand y sección
        String formatted = ChatColor.translateAlternateColorCodes('&', raw);
        return LEGACY_SECTION.deserialize(formatted);
    }

    public void removePlayer(UUID playerId) {
        Player p = Bukkit.getPlayer(playerId);
        for (Map.Entry<String, Set<UUID>> entry : trackingPlayers.entrySet()) {
            if (entry.getValue().remove(playerId)) {
                if (p != null && p.isOnline()) {
                    Integer titleId = npcTitleEntityIds.get(entry.getKey());
                    Integer subtitleId = npcSubtitleEntityIds.get(entry.getKey());
                    if (titleId != null) PacketUtil.destroyTextDisplay(p, titleId);
                    if (subtitleId != null) PacketUtil.destroyTextDisplay(p, subtitleId);
                }
            }
        }
    }

    public void removeNpc(String npcKey) {
        Integer titleId = npcTitleEntityIds.remove(npcKey.toLowerCase());
        Integer subtitleId = npcSubtitleEntityIds.remove(npcKey.toLowerCase());
        npcTitleUuids.remove(npcKey.toLowerCase());
        npcSubtitleUuids.remove(npcKey.toLowerCase());
        cachedOriginalNames.remove(npcKey.toLowerCase());
        Set<UUID> tracking = trackingPlayers.remove(npcKey.toLowerCase());

        if (tracking != null) {
            for (UUID pUuid : tracking) {
                Player p = Bukkit.getPlayer(pUuid);
                if (p != null && p.isOnline()) {
                    if (titleId != null) PacketUtil.destroyTextDisplay(p, titleId);
                    if (subtitleId != null) PacketUtil.destroyTextDisplay(p, subtitleId);
                }
            }
        }
    }

    public void destroyAll() {
        for (Map.Entry<String, Set<UUID>> entry : trackingPlayers.entrySet()) {
            Integer titleId = npcTitleEntityIds.get(entry.getKey());
            Integer subtitleId = npcSubtitleEntityIds.get(entry.getKey());
            for (UUID pUuid : entry.getValue()) {
                Player p = Bukkit.getPlayer(pUuid);
                if (p != null && p.isOnline()) {
                    if (titleId != null) PacketUtil.destroyTextDisplay(p, titleId);
                    if (subtitleId != null) PacketUtil.destroyTextDisplay(p, subtitleId);
                }
            }
        }
        trackingPlayers.clear();
        npcTitleEntityIds.clear();
        npcSubtitleEntityIds.clear();
        npcTitleUuids.clear();
        npcSubtitleUuids.clear();
        cachedOriginalNames.clear();
    }
}
