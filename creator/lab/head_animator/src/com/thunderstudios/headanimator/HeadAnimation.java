package com.thunderstudios.headanimator;

import com.destroystokyo.paper.profile.PlayerProfile;
import com.destroystokyo.paper.profile.ProfileProperty;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.SkullMeta;
import org.bukkit.persistence.PersistentDataType;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.logging.Level;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class HeadAnimation {

    private static final Pattern HEX_PATTERN = Pattern.compile("&#([A-Fa-f0-9]{6})");

    private final HeadAnimatorPlugin plugin;
    private final String id;
    private final String displayName;
    private final List<String> lore;
    private final int intervalTicks;
    private final List<String> pingPongSequence = new ArrayList<>();
    private final ItemStack[] cachedFrameItems;

    public HeadAnimation(HeadAnimatorPlugin plugin, String id, String displayName, List<String> lore, int intervalTicks, List<String> frames, boolean pingPong) {
        this.plugin = plugin;
        this.id = id;
        this.displayName = colorize(displayName);
        this.lore = new ArrayList<>();
        if (lore != null) {
            for (String line : lore) {
                this.lore.add(colorize(line));
            }
        }
        this.intervalTicks = Math.max(1, intervalTicks);
        List<String> rawFrames = frames != null ? frames : new ArrayList<>();

        if (pingPong && rawFrames.size() > 2) {
            for (int i = 0; i < rawFrames.size(); i++) {
                pingPongSequence.add(rawFrames.get(i));
            }
            for (int i = rawFrames.size() - 2; i > 0; i--) {
                pingPongSequence.add(rawFrames.get(i));
            }
        } else {
            pingPongSequence.addAll(rawFrames);
        }

        this.cachedFrameItems = new ItemStack[this.pingPongSequence.size()];
        for (int i = 0; i < this.pingPongSequence.size(); i++) {
            UUID deterministicUUID = UUID.nameUUIDFromBytes(("headanimator:" + id + ":" + i).getBytes(StandardCharsets.UTF_8));
            this.cachedFrameItems[i] = createSkull(this.pingPongSequence.get(i), this.displayName, this.lore, deterministicUUID, i);
        }
    }

    public String getId() {
        return id;
    }

    public int getIntervalTicks() {
        return intervalTicks;
    }

    public int getFrameCount() {
        return cachedFrameItems.length;
    }

    public ItemStack getFrameItem(int index) {
        if (cachedFrameItems.length == 0) return new ItemStack(Material.PLAYER_HEAD);
        int safeIndex = Math.abs(index % cachedFrameItems.length);
        return cachedFrameItems[safeIndex].clone();
    }

    public ItemStack createGivenItem() {
        return getFrameItem(0);
    }

    public boolean normalizeToBase(ItemStack item) {
        if (item == null || item.getType() != Material.PLAYER_HEAD) return false;
        if (!item.hasItemMeta()) return false;
        if (!(item.getItemMeta() instanceof SkullMeta meta)) return false;

        PlayerProfile currentProfile = meta.getPlayerProfile();
        UUID baseUUID = UUID.nameUUIDFromBytes(("headanimator:" + id + ":0").getBytes(StandardCharsets.UTF_8));
        if (currentProfile != null && baseUUID.equals(currentProfile.getId())) {
            return false;
        }

        ItemStack base = getFrameItem(0);
        SkullMeta baseMeta = (SkullMeta) base.getItemMeta();
        if (baseMeta != null && baseMeta.getPlayerProfile() != null) {
            meta.setPlayerProfile(baseMeta.getPlayerProfile());
            meta.setDisplayName(this.displayName);
            meta.setLore(this.lore);
            item.setItemMeta(meta);
            return true;
        }
        return false;
    }

    private ItemStack createSkull(String base64, String name, List<String> lore, UUID deterministicUUID, int frameIndex) {
        ItemStack item = new ItemStack(Material.PLAYER_HEAD);
        SkullMeta meta = (SkullMeta) item.getItemMeta();
        if (meta != null) {
            meta.setDisplayName(name);
            meta.setLore(lore);
            NamespacedKey key = new NamespacedKey(plugin, "animated_head");
            meta.getPersistentDataContainer().set(key, PersistentDataType.STRING, id);
            try {
                PlayerProfile profile = Bukkit.createProfile(deterministicUUID, "Anim_" + id + "_" + frameIndex);
                profile.setProperty(new ProfileProperty("textures", base64));
                meta.setPlayerProfile(profile);
            } catch (Exception e) {
                plugin.getLogger().log(Level.SEVERE, "Error configurando textura en frame " + frameIndex + " para " + id, e);
            }
            item.setItemMeta(meta);
        }
        return item;
    }

    public static String colorize(String message) {
        if (message == null) return "";
        Matcher matcher = HEX_PATTERN.matcher(message);
        StringBuffer buffer = new StringBuffer();
        while (matcher.find()) {
            String hexCode = matcher.group(1);
            StringBuilder replacement = new StringBuilder("§x");
            for (char c : hexCode.toCharArray()) {
                replacement.append('§').append(c);
            }
            matcher.appendReplacement(buffer, replacement.toString());
        }
        matcher.appendTail(buffer);
        return ChatColor.translateAlternateColorCodes('&', buffer.toString());
    }
}
