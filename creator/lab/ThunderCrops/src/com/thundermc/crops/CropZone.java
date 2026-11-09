package com.thundermc.crops;

import org.bukkit.Location;
import org.bukkit.Material;

import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class CropZone {

    private final String id;
    private final String worldName;
    private final int minX;
    private final int minY;
    private final int minZ;
    private final int maxX;
    private final int maxY;
    private final int maxZ;

    private final Material soilMaterial;
    private final Material cropMaterial;
    private final Material dropMaterial;
    private final Set<Material> targetMaterials;
    private final int minDrop;
    private final int maxDrop;
    private final int regenDelaySeconds;
    private final boolean giveToInventory;

    public CropZone(String id, String worldName, int x1, int y1, int z1, int x2, int y2, int z2,
                    Material soilMaterial, Material cropMaterial, Material dropMaterial,
                    List<String> targets, int minDrop, int maxDrop, int regenDelaySeconds,
                    boolean giveToInventory) {
        this.id = id;
        this.worldName = worldName;
        this.minX = Math.min(x1, x2);
        this.minY = Math.min(y1, y2);
        this.minZ = Math.min(z1, z2);
        this.maxX = Math.max(x1, x2);
        this.maxY = Math.max(y1, y2);
        this.maxZ = Math.max(z1, z2);

        this.soilMaterial = soilMaterial != null ? soilMaterial : Material.FARMLAND;
        this.cropMaterial = cropMaterial != null ? cropMaterial : Material.WHEAT;
        this.dropMaterial = dropMaterial != null ? dropMaterial : Material.WHEAT;

        Set<Material> set = new HashSet<>();
        if (targets != null && !targets.isEmpty()) {
            for (String s : targets) {
                try {
                    set.add(Material.valueOf(s.toUpperCase()));
                } catch (IllegalArgumentException ignored) {}
            }
        }
        if (set.isEmpty()) {
            set.add(Material.GRASS_BLOCK);
            set.add(Material.DIRT);
        }
        this.targetMaterials = Collections.unmodifiableSet(set);

        this.minDrop = Math.max(1, minDrop);
        this.maxDrop = Math.max(this.minDrop, maxDrop);
        this.regenDelaySeconds = Math.max(1, regenDelaySeconds);
        this.giveToInventory = giveToInventory;
    }

    public boolean contains(Location loc) {
        if (loc == null || loc.getWorld() == null) return false;
        if (!loc.getWorld().getName().equalsIgnoreCase(worldName)) return false;

        int x = loc.getBlockX();
        int y = loc.getBlockY();
        int z = loc.getBlockZ();

        return x >= minX && x <= maxX &&
               y >= minY && y <= maxY &&
               z >= minZ && z <= maxZ;
    }

    public boolean containsOrSoil(Location loc) {
        if (loc == null || loc.getWorld() == null) return false;
        if (!loc.getWorld().getName().equalsIgnoreCase(worldName)) return false;

        int x = loc.getBlockX();
        int y = loc.getBlockY();
        int z = loc.getBlockZ();

        // 1 bloque por debajo para proteger y verificar el suelo
        return x >= minX && x <= maxX &&
               y >= (minY - 1) && y <= maxY &&
               z >= minZ && z <= maxZ;
    }

    public long getGrowthIntervalTicks(int maxAge) {
        int steps = Math.max(1, maxAge);
        return Math.max(1L, (regenDelaySeconds * 20L) / steps);
    }

    public String getId() { return id; }
    public String getWorldName() { return worldName; }
    public int getMinX() { return minX; }
    public int getMinY() { return minY; }
    public int getMinZ() { return minZ; }
    public int getMaxX() { return maxX; }
    public int maxY() { return maxY; }
    public int getMaxY() { return maxY; }
    public int getMaxZ() { return maxZ; }

    public Material getSoilMaterial() { return soilMaterial; }
    public Material getCropMaterial() { return cropMaterial; }
    public Material getDropMaterial() { return dropMaterial; }
    public Set<Material> getTargetMaterials() { return targetMaterials; }
    public int getMinDrop() { return minDrop; }
    public int getMaxDrop() { return maxDrop; }
    public int getRegenDelaySeconds() { return regenDelaySeconds; }
    public boolean isGiveToInventory() { return giveToInventory; }
}
