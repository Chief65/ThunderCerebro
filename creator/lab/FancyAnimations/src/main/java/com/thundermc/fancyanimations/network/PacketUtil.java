package com.thundermc.fancyanimations.network;

import com.github.retrooper.packetevents.PacketEvents;
import com.github.retrooper.packetevents.protocol.entity.data.EntityData;
import com.github.retrooper.packetevents.protocol.entity.data.EntityDataTypes;
import com.github.retrooper.packetevents.protocol.entity.type.EntityTypes;
import com.github.retrooper.packetevents.util.Vector3d;
import com.github.retrooper.packetevents.util.Vector3f;
import com.github.retrooper.packetevents.wrapper.play.server.WrapperPlayServerDestroyEntities;
import com.github.retrooper.packetevents.wrapper.play.server.WrapperPlayServerEntityMetadata;
import com.github.retrooper.packetevents.wrapper.play.server.WrapperPlayServerEntityTeleport;
import com.github.retrooper.packetevents.wrapper.play.server.WrapperPlayServerSpawnEntity;
import de.oliver.fancynpcs.api.Npc;
import net.kyori.adventure.text.Component;
import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.entity.Player;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Utilidad de bajo nivel para despachar paquetes de animación, hologramas virtuales y metadata vanilla a clientes.
 */
public class PacketUtil {

    private static final Logger LOGGER = Bukkit.getLogger();
    private static boolean initialized = false;
    private static boolean packetEventsAvailable = false;

    // NMS Reflection cached handles
    private static Field npcEntityField = null;
    private static Constructor<?> animatePacketConstructor = null;
    private static Method craftPlayerGetHandle = null;
    private static Field serverPlayerConnection = null;
    private static Method connectionSend = null;

    public static synchronized void init() {
        if (initialized) return;
        initialized = true;

        // Comprobar PacketEvents
        try {
            Class.forName("com.github.retrooper.packetevents.PacketEvents");
            packetEventsAvailable = true;
            LOGGER.info("[FancyAnimations] PacketEvents vinculado exitosamente para TextDisplays y EntityMetadata.");
        } catch (ClassNotFoundException e) {
            packetEventsAvailable = false;
        }

        // Inicializar NMS Reflection para animaciones vanilla (arm swing)
        try {
            Class<?> craftPlayerClass = Class.forName("org.bukkit.craftbukkit.entity.CraftPlayer");
            craftPlayerGetHandle = craftPlayerClass.getMethod("getHandle");

            Class<?> serverPlayerClass = Class.forName("net.minecraft.server.level.ServerPlayer");
            for (Field f : serverPlayerClass.getFields()) {
                if (f.getType().getName().endsWith("ServerGamePacketListenerImpl")) {
                    serverPlayerConnection = f;
                    break;
                }
            }
            if (serverPlayerConnection == null) {
                serverPlayerConnection = serverPlayerClass.getField("connection");
            }

            Class<?> connectionClass = serverPlayerConnection.getType();
            for (Method m : connectionClass.getMethods()) {
                if (m.getName().equals("send") && m.getParameterCount() == 1) {
                    connectionSend = m;
                    break;
                }
            }

            Class<?> entityClass = Class.forName("net.minecraft.world.entity.Entity");
            Class<?> animateClass = Class.forName("net.minecraft.network.protocol.game.ClientboundAnimatePacket");
            animatePacketConstructor = animateClass.getConstructor(entityClass, int.class);

            LOGGER.info("[FancyAnimations] Pipeline NMS de animación inicializado correctamente.");
        } catch (Exception e) {
            LOGGER.log(Level.WARNING, "[FancyAnimations] Error al inicializar pipeline NMS de animaciones: " + e.getMessage());
        }
    }

    /**
     * Envía el paquete de Glowing (Bit 6 de Metadata Byte 0) EXCLUSIVAMENTE al jugador especificado.
     * Los demás jugadores no ven el glow.
     */
    public static void sendGlow(Player player, Npc npc, boolean glow) {
        if (!initialized) init();
        if (player == null || npc == null) return;

        if (packetEventsAvailable) {
            try {
                int entityId = npc.getEntityId();
                byte flag = glow ? (byte) 0x40 : (byte) 0x00;
                EntityData<Byte> data = new EntityData<>(0, EntityDataTypes.BYTE, flag);
                WrapperPlayServerEntityMetadata packet = new WrapperPlayServerEntityMetadata(entityId, List.of(data));
                PacketEvents.getAPI().getPlayerManager().sendPacket(player, packet);
            } catch (Exception ignored) {
            }
        }
    }

    /**
     * Spawnea un TextDisplay virtual para el jugador especificado con soporte de color de fondo y escala.
     */
    public static void spawnTextDisplay(Player player, int entityId, UUID uuid, Location loc, Component text, float scale, int interpolationTicks, int backgroundColor) {
        if (!initialized) init();
        if (!packetEventsAvailable || player == null || !player.isOnline()) return;

        try {
            Vector3d pos = new Vector3d(loc.getX(), loc.getY(), loc.getZ());
            WrapperPlayServerSpawnEntity spawnPacket = new WrapperPlayServerSpawnEntity(
                    entityId,
                    Optional.of(uuid),
                    EntityTypes.TEXT_DISPLAY,
                    pos,
                    0.0f, 0.0f, 0.0f,
                    0,
                    Optional.empty()
            );
            PacketEvents.getAPI().getPlayerManager().sendPacket(player, spawnPacket);

            List<EntityData<?>> metadataList = new ArrayList<>();
            // Index 0: Flags generales
            metadataList.add(new EntityData<>(0, EntityDataTypes.BYTE, (byte) 0));
            // Index 8: Retraso de inicio de interpolación
            metadataList.add(new EntityData<>(8, EntityDataTypes.INT, 0));
            // Index 9: Duración de interpolación de transformación (ticks)
            metadataList.add(new EntityData<>(9, EntityDataTypes.INT, Math.max(1, interpolationTicks)));
            // Index 10: Duración de interpolación de posición/rotación para suavidad de respiración
            metadataList.add(new EntityData<>(10, EntityDataTypes.INT, 1));
            // Index 11: Traslación (0, 0, 0)
            metadataList.add(new EntityData<>(11, EntityDataTypes.VECTOR3F, new Vector3f(0.0f, 0.0f, 0.0f)));
            // Index 12: Escala
            metadataList.add(new EntityData<>(12, EntityDataTypes.VECTOR3F, new Vector3f(scale, scale, scale)));
            // Index 15: Billboard CENTER (mira siempre hacia la cámara del jugador)
            metadataList.add(new EntityData<>(15, EntityDataTypes.BYTE, (byte) 3));
            // Index 23: Componente de Texto
            metadataList.add(new EntityData<>(23, EntityDataTypes.ADV_COMPONENT, text));
            // Index 25: Color de fondo (0 = transparente, 0x40000000 = negro semitransparente)
            metadataList.add(new EntityData<>(25, EntityDataTypes.INT, backgroundColor));
            // Index 27: Flags de texto: Sombra activada (0x01)
            metadataList.add(new EntityData<>(27, EntityDataTypes.BYTE, (byte) 0x01));

            WrapperPlayServerEntityMetadata metaPacket = new WrapperPlayServerEntityMetadata(entityId, metadataList);
            PacketEvents.getAPI().getPlayerManager().sendPacket(player, metaPacket);
        } catch (Exception ignored) {
        }
    }

    /**
     * Actualiza el texto, la escala y el color de fondo del TextDisplay virtual.
     */
    public static void updateTextDisplay(Player player, int entityId, Component text, float scale, int interpolationTicks, int backgroundColor) {
        if (!initialized) init();
        if (!packetEventsAvailable || player == null || !player.isOnline()) return;

        try {
            List<EntityData<?>> metadataList = new ArrayList<>();
            metadataList.add(new EntityData<>(9, EntityDataTypes.INT, Math.max(1, interpolationTicks)));
            metadataList.add(new EntityData<>(12, EntityDataTypes.VECTOR3F, new Vector3f(scale, scale, scale)));
            metadataList.add(new EntityData<>(23, EntityDataTypes.ADV_COMPONENT, text));
            metadataList.add(new EntityData<>(25, EntityDataTypes.INT, backgroundColor));

            WrapperPlayServerEntityMetadata metaPacket = new WrapperPlayServerEntityMetadata(entityId, metadataList);
            PacketEvents.getAPI().getPlayerManager().sendPacket(player, metaPacket);
        } catch (Exception ignored) {
        }
    }

    public static void updateTextDisplay(Player player, int entityId, Component text, float scale, int interpolationTicks) {
        updateTextDisplay(player, entityId, text, scale, interpolationTicks, 0);
    }

    /**
     * Mueve verticalmente el TextDisplay sincronizado con la respiración del NPC.
     */
    public static void teleportTextDisplay(Player player, int entityId, Location loc) {
        if (!initialized) init();
        if (!packetEventsAvailable || player == null || !player.isOnline()) return;

        try {
            Vector3d pos = new Vector3d(loc.getX(), loc.getY(), loc.getZ());
            WrapperPlayServerEntityTeleport tpPacket = new WrapperPlayServerEntityTeleport(
                    entityId,
                    pos,
                    0.0f, 0.0f,
                    false
            );
            PacketEvents.getAPI().getPlayerManager().sendPacket(player, tpPacket);
        } catch (Exception ignored) {
        }
    }

    /**
     * Destruye el TextDisplay virtual para el jugador especificado.
     */
    public static void destroyTextDisplay(Player player, int entityId) {
        if (!initialized) init();
        if (!packetEventsAvailable || player == null || !player.isOnline()) return;

        try {
            WrapperPlayServerDestroyEntities destroyPacket = new WrapperPlayServerDestroyEntities(entityId);
            PacketEvents.getAPI().getPlayerManager().sendPacket(player, destroyPacket);
        } catch (Exception ignored) {
        }
    }

    /**
     * Envía un swing de brazo (gesto / saludo) a todos los jugadores en un radio de 48 bloques.
     * action: 0 = Swing brazo principal, 3 = Swing brazo secundario
     */
    public static void playArmSwing(Npc npc, int action) {
        if (!initialized) init();
        if (npc == null || npc.getData() == null || npc.getData().getLocation() == null) return;

        Location loc = npc.getData().getLocation();
        double radiusSq = 48.0 * 48.0;

        for (Player player : Bukkit.getOnlinePlayers()) {
            if (player.getWorld().equals(loc.getWorld()) && player.getLocation().distanceSquared(loc) <= radiusSq) {
                sendAnimationPacket(player, npc, action);
            }
        }
    }

    public static void playArmSwing(Player player, Npc npc, int action) {
        if (!initialized) init();
        sendAnimationPacket(player, npc, action);
    }

    private static void sendAnimationPacket(Player player, Npc npc, int action) {
        try {
            if (npcEntityField == null) {
                Class<?> current = npc.getClass();
                while (current != null && current != Object.class) {
                    try {
                        npcEntityField = current.getDeclaredField("npc");
                        npcEntityField.setAccessible(true);
                        break;
                    } catch (NoSuchFieldException e) {
                        current = current.getSuperclass();
                    }
                }
            }

            if (npcEntityField == null) return;
            Object nmsEntity = npcEntityField.get(npc);
            if (nmsEntity == null) return;

            if (animatePacketConstructor != null && craftPlayerGetHandle != null && connectionSend != null) {
                Object packet = animatePacketConstructor.newInstance(nmsEntity, action);
                Object serverPlayer = craftPlayerGetHandle.invoke(player);
                Object connection = serverPlayerConnection.get(serverPlayer);
                connectionSend.invoke(connection, packet);
            }
        } catch (Exception ignored) {
        }
    }
}
