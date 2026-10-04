package com.thunderstudios.headanimator;

import com.github.retrooper.packetevents.event.PacketListenerAbstract;
import com.github.retrooper.packetevents.event.PacketListenerPriority;
import com.github.retrooper.packetevents.event.PacketSendEvent;
import com.github.retrooper.packetevents.protocol.packettype.PacketType;
import com.github.retrooper.packetevents.protocol.player.Equipment;
import com.github.retrooper.packetevents.protocol.player.EquipmentSlot;
import com.github.retrooper.packetevents.wrapper.play.server.WrapperPlayServerEntityEquipment;
import io.github.retrooper.packetevents.util.SpigotConversionUtil;
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.SkullMeta;
import org.bukkit.persistence.PersistentDataType;
import org.bukkit.scheduler.BukkitTask;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public class AnimationManager extends PacketListenerAbstract {

    private final HeadAnimatorPlugin plugin;
    private final NamespacedKey headKey;
    private final Map<String, HeadAnimation> animations = new HashMap<>();

    public static class WearerState {
        final Player player;
        final HeadAnimation animation;
        volatile int currentFrameIndex = 0;
        volatile com.github.retrooper.packetevents.protocol.item.ItemStack cachedPEFrame;
        volatile ItemStack cachedBukkitFrame;

        WearerState(Player player, HeadAnimation animation) {
            this.player = player;
            this.animation = animation;
        }
    }

    private final Map<UUID, WearerState> activeWearers = new ConcurrentHashMap<>();
    private final Map<Integer, WearerState> entityWearers = new ConcurrentHashMap<>();

    private BukkitTask tickerTask;
    private long currentTick = 0;

    public AnimationManager(HeadAnimatorPlugin plugin) {
        super(PacketListenerPriority.NORMAL);
        this.plugin = plugin;
        this.headKey = new NamespacedKey(plugin, "animated_head");
    }

    public void registerAnimation(HeadAnimation animation) {
        animations.put(animation.getId().toLowerCase(Locale.ROOT), animation);
    }

    public void clearAnimations() {
        animations.clear();
        activeWearers.clear();
        entityWearers.clear();
    }

    public HeadAnimation getAnimation(String id) {
        if (id == null) return null;
        return animations.get(id.toLowerCase(Locale.ROOT));
    }

    public Collection<HeadAnimation> getAllAnimations() {
        return animations.values();
    }

    public boolean isWearerActive(Player player) {
        return activeWearers.containsKey(player.getUniqueId());
    }

    public int getCurrentFrameIndex(Player player) {
        WearerState state = activeWearers.get(player.getUniqueId());
        return state != null ? state.currentFrameIndex : -1;
    }

    public void start() {
        stop();
        tickerTask = Bukkit.getScheduler().runTaskTimer(plugin, this::tick, 1L, 1L);
    }

    public void stop() {
        if (tickerTask != null) {
            tickerTask.cancel();
            tickerTask = null;
        }
        for (WearerState state : activeWearers.values()) {
            restoreRealHelmet(state.player);
        }
        activeWearers.clear();
        entityWearers.clear();
    }

    @Override
    public void onPacketSend(PacketSendEvent event) {
        if (event.getPacketType() == PacketType.Play.Server.ENTITY_EQUIPMENT) {
            WrapperPlayServerEntityEquipment packet = new WrapperPlayServerEntityEquipment(event);
            int entityId = packet.getEntityId();
            WearerState state = entityWearers.get(entityId);
            if (state != null && state.cachedPEFrame != null) {
                List<Equipment> equipmentList = new ArrayList<>(packet.getEquipment());
                boolean modified = false;
                for (int i = 0; i < equipmentList.size(); i++) {
                    if (equipmentList.get(i).getSlot() == EquipmentSlot.HELMET) {
                        equipmentList.set(i, new Equipment(EquipmentSlot.HELMET, state.cachedPEFrame));
                        modified = true;
                    }
                }
                if (modified) {
                    packet.setEquipment(equipmentList);
                    event.markForReEncode(true);
                }
            }
        }
    }

    private void tick() {
        currentTick++;
        if (animations.isEmpty()) return;

        // 1. Scan online players for animated helmets
        Set<UUID> currentOnlineWearers = new HashSet<>();

        for (Player player : Bukkit.getOnlinePlayers()) {
            ItemStack helmet = player.getInventory().getHelmet();
            HeadAnimation anim = getAnimationFromItem(helmet);

            if (anim != null && anim.getFrameCount() > 0) {
                currentOnlineWearers.add(player.getUniqueId());
                WearerState state = activeWearers.get(player.getUniqueId());
                if (state == null || !state.animation.getId().equalsIgnoreCase(anim.getId())) {
                    state = new WearerState(player, anim);
                    activeWearers.put(player.getUniqueId(), state);
                    entityWearers.put(player.getEntityId(), state);
                    updateFrame(state, 0);
                    broadcastHelmet(state);
                }
            }
        }

        // 2. Cleanup unequipped or logged-off players
        Iterator<Map.Entry<UUID, WearerState>> it = activeWearers.entrySet().iterator();
        while (it.hasNext()) {
            Map.Entry<UUID, WearerState> entry = it.next();
            if (!currentOnlineWearers.contains(entry.getKey())) {
                WearerState removed = entry.getValue();
                entityWearers.remove(removed.player.getEntityId());
                it.remove();
                restoreRealHelmet(removed.player);
            }
        }

        // 3. Step animation frames based on intervals
        for (WearerState state : activeWearers.values()) {
            HeadAnimation anim = state.animation;
            if (currentTick % anim.getIntervalTicks() == 0) {
                int nextFrame = (state.currentFrameIndex + 1) % anim.getFrameCount();
                updateFrame(state, nextFrame);
                broadcastHelmet(state);
            }
        }
    }

    private void updateFrame(WearerState state, int frameIndex) {
        state.currentFrameIndex = frameIndex;
        state.cachedBukkitFrame = state.animation.getFrameItem(frameIndex);
        try {
            state.cachedPEFrame = SpigotConversionUtil.fromBukkitItemStack(state.cachedBukkitFrame);
        } catch (Exception e) {
            state.cachedPEFrame = null;
        }
    }

    private void broadcastHelmet(WearerState state) {
        Player wearer = state.player;
        ItemStack frame = state.cachedBukkitFrame;
        if (frame == null || !wearer.isOnline()) return;

        // Visual update for the wearer themselves (F5 3rd person)
        wearer.sendEquipmentChange(wearer, org.bukkit.inventory.EquipmentSlot.HEAD, frame);

        // Visual update for nearby observers
        double maxDistSq = 48.0 * 48.0;
        for (Player viewer : wearer.getWorld().getPlayers()) {
            if (viewer.equals(wearer)) continue;
            if (viewer.getLocation().distanceSquared(wearer.getLocation()) <= maxDistSq) {
                viewer.sendEquipmentChange(wearer, org.bukkit.inventory.EquipmentSlot.HEAD, frame);
            }
        }
    }

    private void restoreRealHelmet(Player player) {
        if (!player.isOnline()) return;
        ItemStack real = player.getInventory().getHelmet();
        ItemStack restored = real != null ? real : new ItemStack(Material.AIR);
        for (Player viewer : player.getWorld().getPlayers()) {
            viewer.sendEquipmentChange(player, org.bukkit.inventory.EquipmentSlot.HEAD, restored);
        }
    }

    public HeadAnimation getAnimationFromItem(ItemStack item) {
        if (item == null || item.getType() != Material.PLAYER_HEAD) return null;
        if (!item.hasItemMeta()) return null;
        if (!(item.getItemMeta() instanceof SkullMeta)) return null;

        SkullMeta meta = (SkullMeta) item.getItemMeta();
        String animId = meta.getPersistentDataContainer().get(headKey, PersistentDataType.STRING);
        if (animId == null) return null;

        return animations.get(animId.toLowerCase(Locale.ROOT));
    }
}
