package com.thundermc.fancyanimations.engine;

import com.thundermc.fancyanimations.config.ConfigManager;
import com.thundermc.fancyanimations.display.DisplayNameManager;
import com.thundermc.fancyanimations.model.NpcAnimationProfile;
import com.thundermc.fancyanimations.model.NpcAnimationState;
import com.thundermc.fancyanimations.network.PacketUtil;
import de.oliver.fancynpcs.api.FancyNpcsPlugin;
import de.oliver.fancynpcs.api.Npc;
import net.kyori.adventure.text.Component;
import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.Sound;
import org.bukkit.SoundCategory;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.util.BoundingBox;
import org.bukkit.util.RayTraceResult;
import org.bukkit.util.Vector;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Motor central de cálculo cinemático e inyección de movimiento procedural en NPCs.
 * Incorpora:
 * - Movimiento orgánico completo (respiración, balanceo, ladeo, cabeceo, micro-rotaciones).
 * - Seguimiento suave custom de mirada desacoplado de FancyNpcs.
 * - Resplandor verde (Glow) per-player al apuntar con la mira (Cursor Hover vía RayTrace AABB).
 * - Display Names dinámicos e interactivos bicapa con interpolación de color y escala.
 * - Action Bar interactivo individualizado.
 * - Efectos de sonido ambientales periódicos e inmersivos.
 */
public class AnimationEngine {

    private final JavaPlugin plugin;
    private final ConfigManager configManager;
    private final DisplayNameManager displayNameManager;
    private final Map<String, NpcAnimationState> states = new ConcurrentHashMap<>();
    private final Map<UUID, Set<String>> playerHoveredNpcs = new ConcurrentHashMap<>();
    private static final Random RANDOM = new Random();

    public AnimationEngine(JavaPlugin plugin, ConfigManager configManager) {
        this.plugin = plugin;
        this.configManager = configManager;
        this.displayNameManager = new DisplayNameManager(plugin, configManager);
    }

    public DisplayNameManager getDisplayNameManager() {
        return displayNameManager;
    }

    /**
     * Ciclo de actualización cinemática llamado por el scheduler del servidor.
     */
    public void tick() {
        if (FancyNpcsPlugin.get() == null || FancyNpcsPlugin.get().getNpcManager() == null) {
            return;
        }

        Collection<Npc> allNpcs = FancyNpcsPlugin.get().getNpcManager().getAllNpcs();
        if (allNpcs == null || allNpcs.isEmpty()) {
            return;
        }

        for (Npc npc : allNpcs) {
            try {
                processNpc(npc);
            } catch (Exception ignored) {
            }
        }
    }

    private void processNpc(Npc npc) {
        if (npc == null || npc.getData() == null || npc.getData().getLocation() == null) {
            return;
        }

        // DESACTIVAR el turnToPlayer interno de FancyNpcs para evitar colisiones de paquetes de cabeza
        if (npc.getData().isTurnToPlayer()) {
            npc.getData().setTurnToPlayer(false);
            npc.getData().setDirty(false);
        }

        String npcName = npc.getData().getName();
        String npcId = npc.getData().getId();
        String stateKey = npcId != null ? npcId : (npcName != null ? npcName : "unknown");
        NpcAnimationProfile profile = configManager.getProfile(npcName != null ? npcName : npcId);

        Location baseLocation = npc.getData().getLocation();
        int rawVis = npc.getData().getVisibilityDistance();
        double effectiveVisDist;
        if (rawVis > 0) {
            effectiveVisDist = rawVis;
        } else {
            try {
                effectiveVisDist = FancyNpcsPlugin.get().getFancyNpcConfig().getVisibilityDistance();
            } catch (Throwable ignored) {
                effectiveVisDist = 20.0;
            }
            if (effectiveVisDist <= 0) {
                effectiveVisDist = 20.0;
            }
        }
        double visibilityDistSq = effectiveVisDist * effectiveVisDist;

        double trackDist = configManager.getTrackPlayerDistance();
        double trackDistSq = trackDist * trackDist;

        // Detección de jugadores en rango, cálculo de hover y jugador más cercano para mirada
        boolean hasNearbyPlayers = false;
        Player targetPlayer = null;
        double closestDistSq = Double.MAX_VALUE;
        List<Player> nearbyPlayers = new ArrayList<>();
        Set<UUID> aimingPlayerIds = new HashSet<>();

        for (Player player : Bukkit.getOnlinePlayers()) {
            if (player.getWorld().equals(baseLocation.getWorld())) {
                double distSq = player.getLocation().distanceSquared(baseLocation);
                // El jugador solo puede ver el holograma si está dentro de la distancia de visibilidad Y FancyNpcs lo tiene visible
                boolean canSeeNpc = (distSq <= visibilityDistSq) && npc.isShownFor(player);

                if (canSeeNpc) {
                    hasNearbyPlayers = true;
                    nearbyPlayers.add(player);

                    if (distSq <= trackDistSq && distSq < closestDistSq) {
                        closestDistSq = distSq;
                        targetPlayer = player;
                    }

                    // Chequeo de Cursor Hover (Glow individual y Display Name reactivo)
                    boolean aiming = checkCursorHover(player, npc, stateKey, profile);
                    if (aiming) {
                        aimingPlayerIds.add(player.getUniqueId());
                    }
                } else {
                    clearPlayerGlow(player, npc, stateKey);
                }
            } else {
                clearPlayerGlow(player, npc, stateKey);
            }
        }

        if (!hasNearbyPlayers) {
            // Destruye los TextDisplays en los clientes de cualquier jugador que se haya alejado del rango del NPC
            displayNameManager.tickNpc(npc, stateKey, baseLocation, Collections.emptyList(), Collections.emptySet());
            return;
        }

        // Obtener o registrar estado cinemático
        NpcAnimationState state = states.computeIfAbsent(stateKey, k -> new NpcAnimationState(baseLocation));
        state.incrementTick();

        Location animLoc = state.getBaseLocation().clone();
        long t = state.getTick();

        // 1. Respiración (Breathing): Micro-oscilación vertical senoidal suave
        double dy = 0.0;
        if (profile.isBreathing()) {
            dy = Math.sin(t * configManager.getBreathingSpeed()) * configManager.getBreathingAmplitude();
            animLoc.add(0, dy, 0);
        }

        // 2. Balanceo de Torso / Hombros (Swaying): Leve rotación horizontal de peso
        float dYaw = 0.0f;
        if (profile.isSwaying()) {
            dYaw = (float) (Math.sin(t * configManager.getSwayingSpeed()) * configManager.getSwayingAmplitude());
        }

        // 3. Ladeo de Cabeza (Head Tilt): Inclinación angular suave en eje de mirada
        float dPitch = 0.0f;
        if (profile.isHeadTilt()) {
            float tilt = (float) (Math.cos(t * configManager.getHeadTiltSpeed() + state.getTiltPhase()) * configManager.getHeadTiltAmplitude());
            dPitch += tilt;
        }

        // 4. Cabeceo / Asentimiento orgánico (Nodding)
        if (profile.isNodding()) {
            if (state.isNodding()) {
                int progress = state.getNodProgress();
                if (progress <= 20) {
                    double factor = Math.sin((progress / 20.0) * Math.PI);
                    dPitch += (float) (factor * configManager.getNodAmplitude());
                    state.incrementNodProgress();
                } else {
                    state.setNodding(false);
                    state.setNextNodTick(t + 80 + RANDOM.nextInt(150));
                }
            } else if (t >= state.getNextNodTick()) {
                state.triggerNodNow();
            }
        }

        // 5. Micro-rotación (Mirar a su entorno de forma independiente cuando nadie interactúa)
        if (profile.isMicroRotation()) {
            if (t >= state.getNextMicroRotationTick()) {
                float maxAngle = (float) configManager.getMicroRotationMaxAngle();
                state.setTargetYawOffset((RANDOM.nextFloat() * 2.0f - 1.0f) * maxAngle);
                state.setNextMicroRotationTick(t + 100 + RANDOM.nextInt(160));
            }
            float cur = state.getCurrentYawOffset();
            float tgt = state.getTargetYawOffset();
            state.setCurrentYawOffset(cur + (tgt - cur) * 0.04f);
        }

        // 6. Seguimiento de Mirada Custom (Turn-To-Player Desacoplado y Suave)
        if (profile.isLookAtPlayer() && targetPlayer != null) {
            Location npcEye = baseLocation.clone().add(0, 1.62, 0);
            Location playerEye = targetPlayer.getEyeLocation();
            Vector dir = playerEye.toVector().subtract(npcEye.toVector()).normalize();

            float targetYaw = (float) Math.toDegrees(Math.atan2(-dir.getX(), dir.getZ()));
            float targetPitch = (float) Math.toDegrees(-Math.asin(Math.max(-1.0, Math.min(1.0, dir.getY()))));

            float diffYaw = ((targetYaw - state.getCurrentLookYaw() + 180) % 360 + 360) % 360 - 180;
            state.setCurrentLookYaw(state.getCurrentLookYaw() + diffYaw * (float) configManager.getTrackPlayerSpeed());

            float diffPitch = targetPitch - state.getCurrentLookPitch();
            state.setCurrentLookPitch(state.getCurrentLookPitch() + diffPitch * (float) configManager.getTrackPlayerSpeed());
        } else {
            float targetYaw = baseLocation.getYaw() + state.getCurrentYawOffset();
            float targetPitch = baseLocation.getPitch();

            float diffYaw = ((targetYaw - state.getCurrentLookYaw() + 180) % 360 + 360) % 360 - 180;
            state.setCurrentLookYaw(state.getCurrentLookYaw() + diffYaw * 0.08f);

            float diffPitch = targetPitch - state.getCurrentLookPitch();
            state.setCurrentLookPitch(state.getCurrentLookPitch() + diffPitch * 0.08f);
        }

        // Integrar capas cinemáticas finales
        float finalYaw = state.getCurrentLookYaw() + dYaw;
        float finalPitch = Math.max(-89.0f, Math.min(89.0f, state.getCurrentLookPitch() + dPitch));

        animLoc.setYaw(finalYaw);
        animLoc.setPitch(finalPitch);

        // 7. Gestos aleatorios (Random Arm Swings)
        if (profile.isRandomGestures() && t >= state.getNextGestureTick()) {
            PacketUtil.playArmSwing(npc, 0);
            state.setNextGestureTick(t + 160 + RANDOM.nextInt(250));
        }

        // 8. Sonidos ambientales periódicos (Villager Ambient)
        if (configManager.isAmbientSoundEnabled() && t >= state.getNextAmbientSoundTick()) {
            playAmbientSound(animLoc);
            int minInt = configManager.getAmbientSoundMinInterval();
            int maxInt = Math.max(minInt + 1, configManager.getAmbientSoundMaxInterval());
            state.setNextAmbientSoundTick(t + minInt + RANDOM.nextInt(maxInt - minInt));
        }

        // 9. Cinemática de Display Names Dinámicos (Dual TextDisplays virtuales sincronizados)
        displayNameManager.tickNpc(npc, stateKey, animLoc, nearbyPlayers, aimingPlayerIds);

        // 10. Aplicación de orientación al pipeline de red para todos los jugadores en rango
        Location original = state.getBaseLocation();
        npc.getData().setLocation(animLoc);

        for (Player p : nearbyPlayers) {
            npc.lookAt(p, animLoc);
        }

        // Restaurar anclaje inmutable para asegurar la persistencia en disco de FancyNpcs
        npc.getData().setLocation(original);
        npc.getData().setDirty(false);
    }

    private void playAmbientSound(Location loc) {
        try {
            Sound sound = Sound.valueOf(configManager.getAmbientSoundName());
            float vol = (float) configManager.getAmbientSoundVolume();
            float pitch = (float) (0.9 + RANDOM.nextDouble() * 0.25);
            if (loc.getWorld() != null) {
                loc.getWorld().playSound(loc, sound, SoundCategory.VOICE, vol, pitch);
            }
        } catch (Exception ignored) {
        }
    }

    /**
     * Algoritmo de Ray-Tracing AABB exacto para detectar si el jugador está apuntando su cursor al NPC
     * o a sus display names superiores.
     */
    private boolean checkCursorHover(Player player, Npc npc, String npcKey, NpcAnimationProfile profile) {
        Location eye = player.getEyeLocation();
        Location baseLoc = npc.getData().getLocation();
        double maxGlowDist = configManager.getCursorGlowDistance();

        // Hitbox AABB del NPC incluyendo pies, torso, cabeza y los hologramas flotantes superiores
        BoundingBox box = new BoundingBox(
                baseLoc.getX() - 0.55,
                baseLoc.getY() - 0.1,
                baseLoc.getZ() - 0.55,
                baseLoc.getX() + 0.55,
                baseLoc.getY() + 2.65,
                baseLoc.getZ() + 0.55
        );

        RayTraceResult hit = box.rayTrace(eye.toVector(), eye.getDirection(), maxGlowDist);
        boolean isAiming = (hit != null);

        Set<String> activeGlows = playerHoveredNpcs.computeIfAbsent(player.getUniqueId(), k -> ConcurrentHashMap.newKeySet());
        boolean wasAiming = activeGlows.contains(npcKey);

        if (isAiming && !wasAiming) {
            activeGlows.add(npcKey);
            boolean isBedrock = DisplayNameManager.isBedrockPlayer(player);
            if (isBedrock) {
                if (configManager.isBedrockAdaptationEnabled()) {
                    triggerBedrockHoverStart(player, npc);
                }
            } else if (profile.isCursorGlow()) {
                PacketUtil.sendGlow(player, npc, true);
            }
            displayNameManager.updateHover(player, npc, npcKey, true);
            sendHoverActionBar(player, npcKey, npc);
        } else if (!isAiming && wasAiming) {
            activeGlows.remove(npcKey);
            boolean isBedrock = DisplayNameManager.isBedrockPlayer(player);
            if (!isBedrock && profile.isCursorGlow()) {
                PacketUtil.sendGlow(player, npc, false);
            }
            displayNameManager.updateHover(player, npc, npcKey, false);
            clearHoverActionBar(player);
        } else if (isAiming && wasAiming) {
            // Refresco periódico del action bar mientras se mantiene la mira fija (cada 10 ticks = 2 veces por segundo)
            if (Bukkit.getCurrentTick() % 10 == 0) {
                sendHoverActionBar(player, npcKey, npc);
            }
        }

        return isAiming;
    }

    private void sendHoverActionBar(Player player, String npcKey, Npc npc) {
        if (!configManager.isHoverActionBarEnabled()) return;
        try {
            String desc = configManager.getNpcDescription(npcKey);
            if (desc == null && npc != null && npc.getData() != null) {
                if (npc.getData().getName() != null) {
                    desc = configManager.getNpcDescription(npc.getData().getName());
                }
                if (desc == null && npc.getData().getId() != null) {
                    desc = configManager.getNpcDescription(npc.getData().getId());
                }
            }
            if (desc == null || desc.trim().isEmpty()) {
                desc = configManager.getDefaultDescription();
            }

            Component msg = DisplayNameManager.parseText(desc);
            player.sendActionBar(msg);
        } catch (Exception e) {
            player.sendActionBar(Component.text("Npc clickeable"));
        }
    }

    private void clearHoverActionBar(Player player) {
        if (!configManager.isHoverActionBarEnabled()) return;
        player.sendActionBar(Component.empty());
    }

    private void clearPlayerGlow(Player player, Npc npc, String npcKey) {
        Set<String> activeGlows = playerHoveredNpcs.get(player.getUniqueId());
        if (activeGlows != null && activeGlows.remove(npcKey)) {
            if (!DisplayNameManager.isBedrockPlayer(player)) {
                PacketUtil.sendGlow(player, npc, false);
            }
            displayNameManager.updateHover(player, npc, npcKey, false);
            clearHoverActionBar(player);
        }
    }

    private void triggerBedrockHoverStart(Player player, Npc npc) {
        if (configManager.isBedrockHoverSoundEnabled()) {
            try {
                player.playSound(player.getLocation(), Sound.UI_BUTTON_CLICK, SoundCategory.PLAYERS, 0.25f, 1.8f);
            } catch (Exception ignored) {
            }
        }
    }

    public void clearPlayer(UUID playerId) {
        playerHoveredNpcs.remove(playerId);
        displayNameManager.removePlayer(playerId);
    }

    public void triggerGesture(Npc npc, String gesture) {
        if (npc == null) return;
        switch (gesture.toLowerCase()) {
            case "wave", "saludo", "saludar" -> PacketUtil.playArmSwing(npc, 0);
            case "nod", "cabeceo", "asentir" -> {
                String key = npc.getData().getId() != null ? npc.getData().getId() : npc.getData().getName();
                NpcAnimationState state = states.computeIfAbsent(key, k -> new NpcAnimationState(npc.getData().getLocation()));
                state.triggerNodNow();
            }
            case "offhand", "secundaria" -> PacketUtil.playArmSwing(npc, 3);
            default -> PacketUtil.playArmSwing(npc, 0);
        }
    }

    public void removeState(String key) {
        states.remove(key.toLowerCase());
        displayNameManager.removeNpc(key);
        for (Set<String> set : playerHoveredNpcs.values()) {
            set.remove(key.toLowerCase());
        }
    }

    public void clearAll() {
        states.clear();
        playerHoveredNpcs.clear();
        displayNameManager.destroyAll();
    }
}
