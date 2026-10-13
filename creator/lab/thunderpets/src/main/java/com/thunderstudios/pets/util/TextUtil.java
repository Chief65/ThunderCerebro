package com.thunderstudios.pets.util;

import com.destroystokyo.paper.profile.PlayerProfile;
import com.destroystokyo.paper.profile.ProfileProperty;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Material;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.SkullMeta;
import org.bukkit.profile.PlayerTextures;

import java.net.URI;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TextUtil {

    private static final Pattern HEX_PATTERN = Pattern.compile("&#([a-fA-F0-9]{6})");

    public static String color(String text) {
        if (text == null) return "";
        Matcher matcher = HEX_PATTERN.matcher(text);
        StringBuilder sb = new StringBuilder();
        while (matcher.find()) {
            String hex = matcher.group(1);
            matcher.appendReplacement(sb, net.md_5.bungee.api.ChatColor.of("#" + hex).toString());
        }
        matcher.appendTail(sb);
        return ChatColor.translateAlternateColorCodes('&', sb.toString());
    }

    public static List<String> color(List<String> list) {
        List<String> colored = new ArrayList<>();
        if (list == null) return colored;
        for (String s : list) {
            colored.add(color(s));
        }
        return colored;
    }

    public static ItemStack createCustomHead(String base64) {
        ItemStack head = new ItemStack(Material.PLAYER_HEAD);
        if (base64 == null || base64.trim().isEmpty()) {
            return head;
        }

        SkullMeta meta = (SkullMeta) head.getItemMeta();
        if (meta == null) return head;

        String cleanBase64 = base64.trim();
        UUID uuid = UUID.nameUUIDFromBytes(cleanBase64.getBytes(StandardCharsets.UTF_8));
        PlayerProfile profile = Bukkit.createProfile(uuid, "BabyYoda");

        try {
            String decoded = new String(Base64.getDecoder().decode(cleanBase64), StandardCharsets.UTF_8);
            String urlPrefix = "textures.minecraft.net/texture/";
            int idx = decoded.indexOf(urlPrefix);
            if (idx != -1) {
                int endIdx = decoded.indexOf('"', idx);
                if (endIdx != -1) {
                    String hash = decoded.substring(idx + urlPrefix.length(), endIdx);
                    URL skinUrl = URI.create("http://textures.minecraft.net/texture/" + hash).toURL();
                    PlayerTextures textures = profile.getTextures();
                    textures.setSkin(skinUrl);
                    profile.setTextures(textures);
                }
            }
        } catch (Exception ignored) {
        }

        profile.setProperty(new ProfileProperty("textures", cleanBase64));
        meta.setPlayerProfile(profile);
        head.setItemMeta(meta);
        return head;
    }
}
