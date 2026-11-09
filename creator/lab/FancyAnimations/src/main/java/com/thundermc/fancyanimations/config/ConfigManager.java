package com.thundermc.fancyanimations.config;

import com.thundermc.fancyanimations.model.NpcAnimationProfile;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.HashMap;
import java.util.Map;

/**
 * Gestiona la configuración global, los presets ambientales, los hologramas virtuales bicapa y sonidos.
 */
public class ConfigManager {

    private final JavaPlugin plugin;
    private String defaultProfile = "ambient";
    private NpcAnimationProfile ambientPreset = NpcAnimationProfile.createAmbientDefault();

    // Cinemática
    private double breathingSpeed = 0.08;
    private double breathingAmplitude = 0.05;
    private double swayingSpeed = 0.04;
    private double swayingAmplitude = 3.5;
    private double headTiltSpeed = 0.05;
    private double headTiltAmplitude = 5.0;
    private double nodAmplitude = 12.0;
    private double microRotationMaxAngle = 20.0;
    private double trackPlayerDistance = 8.0;
    private double trackPlayerSpeed = 0.18;
    private double cursorGlowDistance = 6.0;
    private int updateInterval = 1;

    // Display Names dinámicos (Bicapa independiente)
    private boolean displayNamesEnabled = true;

    // Capa 1: Título / Nombre (Fondo negro translúcido, tamaño grande)
    private String titleNormalFormat = "&f%name%";
    private String titleHoverFormat = "&a&l%name%";
    private String bedrockTitleHoverFormat = "&a▶ &a&l%name% &a◀";
    private boolean bedrockAdaptationEnabled = true;
    private boolean bedrockParticlesEnabled = false;
    private boolean bedrockHoverSoundEnabled = true;
    private double titleHeightOffset = 2.32;
    private double titleNormalScale = 1.40;
    private double titleHoverScale = 1.65;
    private int titleInterpolationTicks = 3;

    // Capa 2: Subtítulo (Fondo negro semitransparente, tamaño estándar constante)
    private String subtitleFormat = "&7ᴄʟɪᴄᴋ ᴘᴀʀᴀ ᴠᴇʀ";
    private double subtitleHeightOffset = 2.02;
    private double subtitleScale = 1.0;

    // Action Bar al apuntar
    private boolean hoverActionBarEnabled = true;
    private String defaultDescription = "&fNpc clickeable";
    private String hoverActionBarText = "&fNpc clickeable";

    // Sonidos
    private boolean ambientSoundEnabled = true;
    private String ambientSoundName = "ENTITY_VILLAGER_AMBIENT";
    private double ambientSoundVolume = 0.5;
    private int ambientSoundMinInterval = 200;
    private int ambientSoundMaxInterval = 500;

    private boolean clickSoundEnabled = true;
    private String clickSoundName = "ENTITY_VILLAGER_YES";
    private double clickSoundVolume = 1.0;
    private double clickSoundPitch = 1.0;

    // Perfiles específicos por NPC
    private final Map<String, NpcAnimationProfile> npcProfiles = new HashMap<>();
    private final Map<String, String> npcCustomDisplayNames = new HashMap<>();
    private final Map<String, String> npcCustomSubtitles = new HashMap<>();
    private final Map<String, String> npcDescriptions = new HashMap<>();

    public ConfigManager(JavaPlugin plugin) {
        this.plugin = plugin;
    }

    public void load() {
        plugin.saveDefaultConfig();
        plugin.reloadConfig();
        FileConfiguration config = plugin.getConfig();

        this.defaultProfile = config.getString("default-profile", "ambient");
        this.updateInterval = Math.max(1, config.getInt("update-interval", 1));

        // Preset ambiental
        ConfigurationSection presetSection = config.getConfigurationSection("ambient-preset");
        if (presetSection != null) {
            this.ambientPreset = new NpcAnimationProfile(
                    presetSection.getBoolean("breathing", true),
                    presetSection.getBoolean("swaying", true),
                    presetSection.getBoolean("head-tilt", true),
                    presetSection.getBoolean("nodding", true),
                    presetSection.getBoolean("micro-rotation", true),
                    presetSection.getBoolean("look-at-player", true),
                    presetSection.getBoolean("cursor-glow", true),
                    presetSection.getBoolean("random-gestures", false)
            );
        } else {
            this.ambientPreset = NpcAnimationProfile.createAmbientDefault();
        }

        // Parámetros cinemáticos
        ConfigurationSection kin = config.getConfigurationSection("kinematics");
        if (kin != null) {
            this.breathingSpeed = kin.getDouble("breathing-speed", 0.08);
            this.breathingAmplitude = kin.getDouble("breathing-amplitude", 0.05);
            this.swayingSpeed = kin.getDouble("swaying-speed", 0.04);
            this.swayingAmplitude = kin.getDouble("swaying-amplitude", 3.5);
            this.headTiltSpeed = kin.getDouble("head-tilt-speed", 0.05);
            this.headTiltAmplitude = kin.getDouble("head-tilt-amplitude", 5.0);
            this.nodAmplitude = kin.getDouble("nod-amplitude", 12.0);
            this.microRotationMaxAngle = kin.getDouble("micro-rotation-max-angle", 20.0);
            this.trackPlayerDistance = kin.getDouble("track-player-distance", 8.0);
            this.trackPlayerSpeed = kin.getDouble("track-player-speed", 0.18);
            this.cursorGlowDistance = kin.getDouble("cursor-glow-distance", 6.0);
        }

        // Display Names dinámicos
        ConfigurationSection dn = config.getConfigurationSection("display-names");
        if (dn != null) {
            this.displayNamesEnabled = dn.getBoolean("enabled", true);
            this.titleNormalFormat = dn.getString("title-normal-format", "&f%name%");
            String rawHover = dn.getString("title-hover-format", "&a&l%name%");
            if (rawHover == null || rawHover.contains("▶") || rawHover.contains("◀")) {
                this.titleHoverFormat = "&a&l%name%";
            } else {
                this.titleHoverFormat = rawHover;
            }
            this.titleHeightOffset = dn.getDouble("title-height-offset", 2.32);
            this.titleNormalScale = dn.getDouble("title-normal-scale", 1.40);
            this.titleHoverScale = dn.getDouble("title-hover-scale", 1.65);
            this.titleInterpolationTicks = dn.getInt("title-interpolation-ticks", 3);

            this.subtitleFormat = dn.getString("subtitle-format", "&7ᴄʟɪᴄᴋ ᴘᴀʀᴀ ᴠᴇʀ");
            this.subtitleHeightOffset = dn.getDouble("subtitle-height-offset", 2.02);
            this.subtitleScale = dn.getDouble("subtitle-scale", 1.0);

            // Adaptación para Bedrock
            this.bedrockTitleHoverFormat = dn.getString("bedrock-title-hover-format", "&a▶ &a&l%name% &a◀");
            ConfigurationSection bed = dn.getConfigurationSection("bedrock-adaptation");
            if (bed != null) {
                this.bedrockAdaptationEnabled = bed.getBoolean("enabled", true);
                this.bedrockParticlesEnabled = bed.getBoolean("particles", false);
                this.bedrockHoverSoundEnabled = bed.getBoolean("hover-sound", true);
            }
        }

        // Action Bar al apuntar
        ConfigurationSection bar = config.getConfigurationSection("hover-action-bar");
        if (bar != null) {
            this.hoverActionBarEnabled = bar.getBoolean("enabled", true);
            this.defaultDescription = bar.getString("default-description", "&fNpc clickeable");
            String rawText = bar.getString("text", "&fNpc clickeable");
            this.hoverActionBarText = (rawText != null) ? rawText : "&fNpc clickeable";
        }

        // Sonidos
        ConfigurationSection snd = config.getConfigurationSection("sounds");
        if (snd != null) {
            ConfigurationSection amb = snd.getConfigurationSection("ambient");
            if (amb != null) {
                this.ambientSoundEnabled = amb.getBoolean("enabled", true);
                this.ambientSoundName = amb.getString("sound", "ENTITY_VILLAGER_AMBIENT");
                this.ambientSoundVolume = amb.getDouble("volume", 0.5);
                this.ambientSoundMinInterval = amb.getInt("min-interval-ticks", 200);
                this.ambientSoundMaxInterval = amb.getInt("max-interval-ticks", 500);
            }
            ConfigurationSection clk = snd.getConfigurationSection("click");
            if (clk != null) {
                this.clickSoundEnabled = clk.getBoolean("enabled", true);
                this.clickSoundName = clk.getString("sound", "ENTITY_VILLAGER_YES");
                this.clickSoundVolume = clk.getDouble("volume", 1.0);
                this.clickSoundPitch = clk.getDouble("pitch", 1.0);
            }
        }

        // Cargar perfiles específicos
        this.npcProfiles.clear();
        this.npcCustomDisplayNames.clear();
        this.npcCustomSubtitles.clear();
        this.npcDescriptions.clear();

        ConfigurationSection npcsSection = config.getConfigurationSection("npcs");
        if (npcsSection != null) {
            for (String key : npcsSection.getKeys(false)) {
                ConfigurationSection npcSec = npcsSection.getConfigurationSection(key);
                if (npcSec != null) {
                    NpcAnimationProfile profile = new NpcAnimationProfile(
                            npcSec.getBoolean("breathing", ambientPreset.isBreathing()),
                            npcSec.getBoolean("swaying", ambientPreset.isSwaying()),
                            npcSec.getBoolean("head-tilt", ambientPreset.isHeadTilt()),
                            npcSec.getBoolean("nodding", ambientPreset.isNodding()),
                            npcSec.getBoolean("micro-rotation", ambientPreset.isMicroRotation()),
                            npcSec.getBoolean("look-at-player", ambientPreset.isLookAtPlayer()),
                            npcSec.getBoolean("cursor-glow", ambientPreset.isCursorGlow()),
                            npcSec.getBoolean("random-gestures", ambientPreset.isRandomGestures())
                    );
                    this.npcProfiles.put(key.toLowerCase(), profile);

                    if (npcSec.contains("display-name")) {
                        this.npcCustomDisplayNames.put(key.toLowerCase(), npcSec.getString("display-name"));
                    }
                    if (npcSec.contains("subtitle")) {
                        this.npcCustomSubtitles.put(key.toLowerCase(), npcSec.getString("subtitle"));
                    }
                    if (npcSec.contains("description")) {
                        this.npcDescriptions.put(key.toLowerCase(), npcSec.getString("description"));
                    }
                }
            }
        }
    }

    public void save() {
        FileConfiguration config = plugin.getConfig();
        config.set("default-profile", defaultProfile);
        config.set("update-interval", updateInterval);

        // Guardar preset
        config.set("ambient-preset.breathing", ambientPreset.isBreathing());
        config.set("ambient-preset.swaying", ambientPreset.isSwaying());
        config.set("ambient-preset.head-tilt", ambientPreset.isHeadTilt());
        config.set("ambient-preset.nodding", ambientPreset.isNodding());
        config.set("ambient-preset.micro-rotation", ambientPreset.isMicroRotation());
        config.set("ambient-preset.look-at-player", ambientPreset.isLookAtPlayer());
        config.set("ambient-preset.cursor-glow", ambientPreset.isCursorGlow());
        config.set("ambient-preset.random-gestures", ambientPreset.isRandomGestures());

        // Guardar cinemática
        config.set("kinematics.breathing-speed", breathingSpeed);
        config.set("kinematics.breathing-amplitude", breathingAmplitude);
        config.set("kinematics.swaying-speed", swayingSpeed);
        config.set("kinematics.swaying-amplitude", swayingAmplitude);
        config.set("kinematics.head-tilt-speed", headTiltSpeed);
        config.set("kinematics.head-tilt-amplitude", headTiltAmplitude);
        config.set("kinematics.nod-amplitude", nodAmplitude);
        config.set("kinematics.micro-rotation-max-angle", microRotationMaxAngle);
        config.set("kinematics.track-player-distance", trackPlayerDistance);
        config.set("kinematics.track-player-speed", trackPlayerSpeed);
        config.set("kinematics.cursor-glow-distance", cursorGlowDistance);

        // Guardar display names
        config.set("display-names.enabled", displayNamesEnabled);
        config.set("display-names.title-normal-format", titleNormalFormat);
        config.set("display-names.title-hover-format", titleHoverFormat);
        config.set("display-names.title-height-offset", titleHeightOffset);
        config.set("display-names.title-normal-scale", titleNormalScale);
        config.set("display-names.title-hover-scale", titleHoverScale);
        config.set("display-names.title-interpolation-ticks", titleInterpolationTicks);

        config.set("display-names.subtitle-format", subtitleFormat);
        config.set("display-names.subtitle-height-offset", subtitleHeightOffset);
        config.set("display-names.subtitle-scale", subtitleScale);

        // Guardar adaptación para Bedrock
        config.set("display-names.bedrock-title-hover-format", bedrockTitleHoverFormat);
        config.set("display-names.bedrock-adaptation.enabled", bedrockAdaptationEnabled);
        config.set("display-names.bedrock-adaptation.particles", bedrockParticlesEnabled);
        config.set("display-names.bedrock-adaptation.hover-sound", bedrockHoverSoundEnabled);

        // Guardar action bar
        config.set("hover-action-bar.enabled", hoverActionBarEnabled);
        config.set("hover-action-bar.default-description", defaultDescription);
        config.set("hover-action-bar.text", hoverActionBarText);

        // Guardar descripciones
        for (Map.Entry<String, String> entry : npcDescriptions.entrySet()) {
            config.set("npcs." + entry.getKey() + ".description", entry.getValue());
        }

        // Guardar sonidos
        config.set("sounds.ambient.enabled", ambientSoundEnabled);
        config.set("sounds.ambient.sound", ambientSoundName);
        config.set("sounds.ambient.volume", ambientSoundVolume);
        config.set("sounds.ambient.min-interval-ticks", ambientSoundMinInterval);
        config.set("sounds.ambient.max-interval-ticks", ambientSoundMaxInterval);

        config.set("sounds.click.enabled", clickSoundEnabled);
        config.set("sounds.click.sound", clickSoundName);
        config.set("sounds.click.volume", clickSoundVolume);
        config.set("sounds.click.pitch", clickSoundPitch);

        plugin.saveConfig();
    }

    public NpcAnimationProfile getProfile(String npcNameOrId) {
        String key = npcNameOrId.toLowerCase();
        if (npcProfiles.containsKey(key)) {
            return npcProfiles.get(key);
        }
        if ("ambient".equalsIgnoreCase(defaultProfile)) {
            return ambientPreset.clone();
        }
        return NpcAnimationProfile.createEmpty();
    }

    public boolean hasCustomProfile(String npcNameOrId) {
        return npcProfiles.containsKey(npcNameOrId.toLowerCase());
    }

    public void setProfile(String npcNameOrId, NpcAnimationProfile profile) {
        npcProfiles.put(npcNameOrId.toLowerCase(), profile);
        save();
    }

    public void removeCustomProfile(String npcNameOrId) {
        npcProfiles.remove(npcNameOrId.toLowerCase());
        save();
    }

    public String getNpcDisplayName(String npcKey) {
        return npcCustomDisplayNames.get(npcKey.toLowerCase());
    }

    public String getNpcSubtitle(String npcKey) {
        return npcCustomSubtitles.getOrDefault(npcKey.toLowerCase(), subtitleFormat);
    }

    public String getDefaultProfile() {
        return defaultProfile;
    }

    public void setDefaultProfile(String defaultProfile) {
        this.defaultProfile = defaultProfile;
        save();
    }

    public NpcAnimationProfile getAmbientPreset() {
        return ambientPreset;
    }

    public double getBreathingSpeed() {
        return breathingSpeed;
    }

    public double getBreathingAmplitude() {
        return breathingAmplitude;
    }

    public double getSwayingSpeed() {
        return swayingSpeed;
    }

    public double getSwayingAmplitude() {
        return swayingAmplitude;
    }

    public double getHeadTiltSpeed() {
        return headTiltSpeed;
    }

    public double getHeadTiltAmplitude() {
        return headTiltAmplitude;
    }

    public double getNodAmplitude() {
        return nodAmplitude;
    }

    public double getMicroRotationMaxAngle() {
        return microRotationMaxAngle;
    }

    public double getTrackPlayerDistance() {
        return trackPlayerDistance;
    }

    public double getTrackPlayerSpeed() {
        return trackPlayerSpeed;
    }

    public double getCursorGlowDistance() {
        return cursorGlowDistance;
    }

    public int getUpdateInterval() {
        return updateInterval;
    }

    public boolean isDisplayNamesEnabled() {
        return displayNamesEnabled;
    }

    public String getTitleNormalFormat() {
        return titleNormalFormat;
    }

    public String getTitleHoverFormat() {
        return titleHoverFormat;
    }

    public double getTitleHeightOffset() {
        return titleHeightOffset;
    }

    public double getTitleNormalScale() {
        return titleNormalScale;
    }

    public double getTitleHoverScale() {
        return titleHoverScale;
    }

    public int getTitleInterpolationTicks() {
        return titleInterpolationTicks;
    }

    public String getSubtitleFormat() {
        return subtitleFormat;
    }

    public double getSubtitleHeightOffset() {
        return subtitleHeightOffset;
    }

    public double getSubtitleScale() {
        return subtitleScale;
    }

    public boolean isHoverActionBarEnabled() {
        return hoverActionBarEnabled;
    }

    public String getHoverActionBarText() {
        return hoverActionBarText;
    }

    public boolean isAmbientSoundEnabled() {
        return ambientSoundEnabled;
    }

    public String getAmbientSoundName() {
        return ambientSoundName;
    }

    public double getAmbientSoundVolume() {
        return ambientSoundVolume;
    }

    public int getAmbientSoundMinInterval() {
        return ambientSoundMinInterval;
    }

    public int getAmbientSoundMaxInterval() {
        return ambientSoundMaxInterval;
    }

    public boolean isClickSoundEnabled() {
        return clickSoundEnabled;
    }

    public String getClickSoundName() {
        return clickSoundName;
    }

    public double getClickSoundVolume() {
        return clickSoundVolume;
    }

    public double getClickSoundPitch() {
        return clickSoundPitch;
    }

    public String getDefaultDescription() {
        return defaultDescription;
    }

    public void setDefaultDescription(String defaultDescription) {
        this.defaultDescription = defaultDescription;
        save();
    }

    public Map<String, String> getNpcDescriptions() {
        return java.util.Collections.unmodifiableMap(npcDescriptions);
    }

    public String getNpcDescription(String npcNameOrId) {
        if (npcNameOrId == null) return null;
        return npcDescriptions.get(npcNameOrId.toLowerCase());
    }

    public String getEffectiveDescription(String npcNameOrId) {
        String custom = getNpcDescription(npcNameOrId);
        if (custom != null && !custom.trim().isEmpty()) {
            return custom;
        }
        return defaultDescription;
    }

    public void setNpcDescription(String npcNameOrId, String description) {
        if (npcNameOrId == null) return;
        String key = npcNameOrId.toLowerCase();
        npcDescriptions.put(key, description);
        FileConfiguration config = plugin.getConfig();
        config.set("npcs." + key + ".description", description);
        plugin.saveConfig();
    }

    public void removeNpcDescription(String npcNameOrId) {
        if (npcNameOrId == null) return;
        String key = npcNameOrId.toLowerCase();
        npcDescriptions.remove(key);
        FileConfiguration config = plugin.getConfig();
        config.set("npcs." + key + ".description", null);
        plugin.saveConfig();
    }

    public String getBedrockTitleHoverFormat() {
        return bedrockTitleHoverFormat;
    }

    public void setBedrockTitleHoverFormat(String bedrockTitleHoverFormat) {
        this.bedrockTitleHoverFormat = bedrockTitleHoverFormat;
        save();
    }

    public boolean isBedrockAdaptationEnabled() {
        return bedrockAdaptationEnabled;
    }

    public void setBedrockAdaptationEnabled(boolean bedrockAdaptationEnabled) {
        this.bedrockAdaptationEnabled = bedrockAdaptationEnabled;
        save();
    }

    public boolean isBedrockParticlesEnabled() {
        return bedrockParticlesEnabled;
    }

    public void setBedrockParticlesEnabled(boolean bedrockParticlesEnabled) {
        this.bedrockParticlesEnabled = bedrockParticlesEnabled;
        save();
    }

    public boolean isBedrockHoverSoundEnabled() {
        return bedrockHoverSoundEnabled;
    }

    public void setBedrockHoverSoundEnabled(boolean bedrockHoverSoundEnabled) {
        this.bedrockHoverSoundEnabled = bedrockHoverSoundEnabled;
        save();
    }
}
