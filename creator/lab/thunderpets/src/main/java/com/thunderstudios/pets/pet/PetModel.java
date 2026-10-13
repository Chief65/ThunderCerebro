package com.thunderstudios.pets.pet;

import org.bukkit.Material;
import org.bukkit.Particle;
import org.bukkit.inventory.meta.trim.TrimMaterial;
import org.bukkit.inventory.meta.trim.TrimPattern;

import java.util.List;

public class PetModel {

    private final String id;
    private final String name;
    private final PetQuality quality;
    private final int phase;
    private final int requiredLevel;
    private final String permission;
    private final int guiSlot;
    private final List<String> guiLore;

    private final boolean halfBody;
    private final String headTexture;

    private final Material chestplateMaterial;
    private final TrimPattern trimPattern;
    private final TrimMaterial trimMaterial;

    private final Material mainHandMaterial;

    private final double offsetRight;
    private final double offsetBehind;
    private final double offsetHeight;

    private final boolean bobbingEnabled;
    private final double bobbingAmplitude;
    private final double bobbingSpeed;

    private final boolean particlesEnabled;
    private final Particle particle;
    private final int particleCount;
    private final int particleInterval;

    public PetModel(String id, String name, PetQuality quality, int phase, int requiredLevel,
                    String permission, int guiSlot, List<String> guiLore,
                    boolean halfBody, String headTexture,
                    Material chestplateMaterial, TrimPattern trimPattern, TrimMaterial trimMaterial,
                    Material mainHandMaterial,
                    double offsetRight, double offsetBehind, double offsetHeight,
                    boolean bobbingEnabled, double bobbingAmplitude, double bobbingSpeed,
                    boolean particlesEnabled, Particle particle, int particleCount, int particleInterval) {
        this.id = id;
        this.name = name;
        this.quality = quality;
        this.phase = phase;
        this.requiredLevel = requiredLevel;
        this.permission = permission;
        this.guiSlot = guiSlot;
        this.guiLore = guiLore;
        this.halfBody = halfBody;
        this.headTexture = headTexture;
        this.chestplateMaterial = chestplateMaterial;
        this.trimPattern = trimPattern;
        this.trimMaterial = trimMaterial;
        this.mainHandMaterial = mainHandMaterial;
        this.offsetRight = offsetRight;
        this.offsetBehind = offsetBehind;
        this.offsetHeight = offsetHeight;
        this.bobbingEnabled = bobbingEnabled;
        this.bobbingAmplitude = bobbingAmplitude;
        this.bobbingSpeed = bobbingSpeed;
        this.particlesEnabled = particlesEnabled;
        this.particle = particle;
        this.particleCount = particleCount;
        this.particleInterval = particleInterval;
    }

    public String getId() { return id; }
    public String getName() { return name; }
    public PetQuality getQuality() { return quality; }
    public int getPhase() { return phase; }
    public int getRequiredLevel() { return requiredLevel; }
    public String getPermission() { return permission; }
    public int getGuiSlot() { return guiSlot; }
    public List<String> getGuiLore() { return guiLore; }
    public boolean isHalfBody() { return halfBody; }
    public String getHeadTexture() { return headTexture; }
    public Material getChestplateMaterial() { return chestplateMaterial; }
    public TrimPattern getTrimPattern() { return trimPattern; }
    public TrimMaterial getTrimMaterial() { return trimMaterial; }
    public Material getMainHandMaterial() { return mainHandMaterial; }
    public double getOffsetRight() { return offsetRight; }
    public double getOffsetBehind() { return offsetBehind; }
    public double getOffsetHeight() { return offsetHeight; }
    public boolean isBobbingEnabled() { return bobbingEnabled; }
    public double getBobbingAmplitude() { return bobbingAmplitude; }
    public double getBobbingSpeed() { return bobbingSpeed; }
    public boolean isParticlesEnabled() { return particlesEnabled; }
    public Particle getParticle() { return particle; }
    public int getParticleCount() { return particleCount; }
    public int getParticleInterval() { return particleInterval; }
}
