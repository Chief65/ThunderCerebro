package com.thundermc.crateeffects;

import org.bukkit.Color;
import org.bukkit.FireworkEffect;
import org.bukkit.Sound;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.configuration.file.FileConfiguration;

import java.util.*;
import java.util.logging.Logger;

public class EffectConfig {

    public static class RarityPalette {
        private final List<Color> colors;
        private final List<Color> fadeColors;
        private final FireworkEffect.Type shape;
        private final boolean flicker;
        private final boolean trail;

        public RarityPalette(List<Color> colors, List<Color> fadeColors, FireworkEffect.Type shape, boolean flicker, boolean trail) {
            this.colors = colors.isEmpty() ? List.of(Color.YELLOW, Color.ORANGE) : colors;
            this.fadeColors = fadeColors.isEmpty() ? List.of(Color.WHITE) : fadeColors;
            this.shape = shape != null ? shape : FireworkEffect.Type.BALL_LARGE;
            this.flicker = flicker;
            this.trail = trail;
        }

        public List<Color> getColors() { return colors; }
        public List<Color> getFadeColors() { return fadeColors; }
        public FireworkEffect.Type getShape() { return shape; }
        public boolean isFlicker() { return flicker; }
        public boolean isTrail() { return trail; }

        public FireworkEffect buildFireworkEffect() {
            return FireworkEffect.builder()
                    .with(shape)
                    .withColor(colors)
                    .withFade(fadeColors)
                    .flicker(flicker)
                    .trail(trail)
                    .build();
        }
    }

    private final CrateEffects plugin;
    private boolean debug;

    private boolean fireworksEnabled;
    private boolean fireworksPreventDamage;
    private int fireworksAmount;
    private double fireworksHeightOffset;
    private double fireworksSpread;

    private boolean particlesEnabled;
    private boolean particlesInitialFlash;
    private boolean particlesSpiralHelix;
    private boolean particlesTotemConfetti;
    private int particlesBurstCount;

    private boolean soundsEnabled;
    private float soundVolume;
    private Sound startSound;
    private float startPitch;
    private Sound launchSound;
    private float launchPitch;
    private Sound climaxSound;
    private float climaxPitch;

    private final Map<String, RarityPalette> rarityPalettes = new HashMap<>();
    private RarityPalette defaultPalette;

    public EffectConfig(CrateEffects plugin) {
        this.plugin = plugin;
    }

    public void load() {
        plugin.reloadConfig();
        FileConfiguration config = plugin.getConfig();

        this.debug = config.getBoolean("debug", false);

        this.fireworksEnabled = config.getBoolean("fireworks.enabled", true);
        this.fireworksPreventDamage = config.getBoolean("fireworks.prevent_damage", true);
        this.fireworksAmount = Math.max(1, Math.min(6, config.getInt("fireworks.amount", 2)));
        this.fireworksHeightOffset = config.getDouble("fireworks.height_offset", 2.5);
        this.fireworksSpread = config.getDouble("fireworks.spread", 0.6);

        this.particlesEnabled = config.getBoolean("particles.enabled", true);
        this.particlesInitialFlash = config.getBoolean("particles.initial_flash", true);
        this.particlesSpiralHelix = config.getBoolean("particles.spiral_helix", true);
        this.particlesTotemConfetti = config.getBoolean("particles.totem_confetti", true);
        this.particlesBurstCount = Math.max(10, Math.min(150, config.getInt("particles.firework_burst_count", 45)));

        this.soundsEnabled = config.getBoolean("sounds.enabled", true);
        this.soundVolume = (float) config.getDouble("sounds.volume", 1.0);
        this.startSound = parseSound(config.getString("sounds.start_sound", "UI_TOAST_CHALLENGE_COMPLETE"), Sound.UI_TOAST_CHALLENGE_COMPLETE);
        this.startPitch = (float) config.getDouble("sounds.start_pitch", 1.2);
        this.launchSound = parseSound(config.getString("sounds.launch_sound", "ENTITY_FIREWORK_ROCKET_LAUNCH"), Sound.ENTITY_FIREWORK_ROCKET_LAUNCH);
        this.launchPitch = (float) config.getDouble("sounds.launch_pitch", 1.1);
        this.climaxSound = parseSound(config.getString("sounds.climax_sound", "ENTITY_FIREWORK_ROCKET_LARGE_BLAST"), Sound.ENTITY_FIREWORK_ROCKET_LARGE_BLAST);
        this.climaxPitch = (float) config.getDouble("sounds.climax_pitch", 1.0);

        this.rarityPalettes.clear();
        ConfigurationSection palSec = config.getConfigurationSection("rarity_palettes");
        if (palSec != null) {
            for (String key : palSec.getKeys(false)) {
                ConfigurationSection sec = palSec.getConfigurationSection(key);
                if (sec == null) continue;
                RarityPalette pal = parsePalette(sec);
                rarityPalettes.put(key.toLowerCase(Locale.ROOT), pal);
            }
        }

        this.defaultPalette = rarityPalettes.getOrDefault("default", new RarityPalette(
                List.of(Color.YELLOW, Color.ORANGE, Color.WHITE),
                List.of(Color.ORANGE),
                FireworkEffect.Type.BALL_LARGE,
                true,
                true
        ));
    }

    private RarityPalette parsePalette(ConfigurationSection sec) {
        List<Color> colors = parseColorList(sec.getStringList("colors"));
        List<Color> fade = parseColorList(sec.getStringList("fade"));
        FireworkEffect.Type type = FireworkEffect.Type.BALL_LARGE;
        String shapeStr = sec.getString("shape", "BALL_LARGE");
        try {
            type = FireworkEffect.Type.valueOf(shapeStr.toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException ignored) {}

        boolean flicker = sec.getBoolean("flicker", true);
        boolean trail = sec.getBoolean("trail", true);

        return new RarityPalette(colors, fade, type, flicker, trail);
    }

    private List<Color> parseColorList(List<String> list) {
        List<Color> result = new ArrayList<>();
        for (String raw : list) {
            Color c = parseColor(raw);
            if (c != null) result.add(c);
        }
        return result;
    }

    private Color parseColor(String str) {
        if (str == null || str.isBlank()) return null;
        str = str.trim();
        if (str.startsWith("#")) {
            try {
                int rgb = Integer.parseInt(str.substring(1), 16);
                return Color.fromRGB((rgb >> 16) & 0xFF, (rgb >> 8) & 0xFF, rgb & 0xFF);
            } catch (Exception ignored) {}
        }
        return switch (str.toUpperCase(Locale.ROOT)) {
            case "WHITE" -> Color.WHITE;
            case "RED" -> Color.RED;
            case "ORANGE" -> Color.ORANGE;
            case "YELLOW" -> Color.YELLOW;
            case "GREEN" -> Color.GREEN;
            case "LIME" -> Color.LIME;
            case "AQUA" -> Color.AQUA;
            case "BLUE" -> Color.BLUE;
            case "NAVY" -> Color.NAVY;
            case "PURPLE" -> Color.PURPLE;
            case "MAGENTA" -> Color.FUCHSIA;
            case "SILVER" -> Color.SILVER;
            case "GRAY" -> Color.GRAY;
            case "BLACK" -> Color.BLACK;
            default -> null;
        };
    }

    private Sound parseSound(String raw, Sound fallback) {
        if (raw == null) return fallback;
        try {
            return Sound.valueOf(raw.toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException e) {
            plugin.getLogger().warning("Sonido desconocido '" + raw + "', usando fallback " + fallback.name());
            return fallback;
        }
    }

    public RarityPalette getPalette(String key) {
        if (key == null) return defaultPalette;
        return rarityPalettes.getOrDefault(key.toLowerCase(Locale.ROOT), defaultPalette);
    }

    public boolean isDebug() { return debug; }
    public boolean isFireworksEnabled() { return fireworksEnabled; }
    public boolean isFireworksPreventDamage() { return fireworksPreventDamage; }
    public int getFireworksAmount() { return fireworksAmount; }
    public double getFireworksHeightOffset() { return fireworksHeightOffset; }
    public double getFireworksSpread() { return fireworksSpread; }

    public boolean isParticlesEnabled() { return particlesEnabled; }
    public boolean isParticlesInitialFlash() { return particlesInitialFlash; }
    public boolean isParticlesSpiralHelix() { return particlesSpiralHelix; }
    public boolean isParticlesTotemConfetti() { return particlesTotemConfetti; }
    public int getParticlesBurstCount() { return particlesBurstCount; }

    public boolean isSoundsEnabled() { return soundsEnabled; }
    public float getSoundVolume() { return soundVolume; }
    public Sound getStartSound() { return startSound; }
    public float getStartPitch() { return startPitch; }
    public Sound getLaunchSound() { return launchSound; }
    public float getLaunchPitch() { return launchPitch; }
    public Sound getClimaxSound() { return climaxSound; }
    public float getClimaxPitch() { return climaxPitch; }
}
