package com.thundermc.mounts.model;

import org.bukkit.Location;
import org.bukkit.Particle;
import org.bukkit.Sound;
import org.bukkit.entity.AbstractHorse;
import org.bukkit.entity.Entity;

import java.util.UUID;

public class ActiveMount {

    private final UUID playerUuid;
    private final AbstractHorse entity;
    private final HorseStyle style;
    private HorseArmor armor;

    public ActiveMount(UUID playerUuid, AbstractHorse entity, HorseStyle style, HorseArmor armor) {
        this.playerUuid = playerUuid;
        this.entity = entity;
        this.style = style;
        this.armor = armor;
    }

    public UUID getPlayerUuid() { return playerUuid; }
    public AbstractHorse getEntity() { return entity; }
    public HorseStyle getStyle() { return style; }
    public HorseArmor getArmor() { return armor; }
    public void setArmor(HorseArmor armor) { this.armor = armor; }

    public void despawn() {
        if (entity != null && entity.isValid()) {
            Location loc = entity.getLocation();
            entity.remove();
            try {
                if (loc.getWorld() != null) {
                    loc.getWorld().spawnParticle(Particle.POOF, loc.add(0, 0.5, 0), 15, 0.3, 0.3, 0.3, 0.05);
                    loc.getWorld().playSound(loc, Sound.ENTITY_HORSE_ARMOR, 0.8f, 1.2f);
                }
            } catch (Throwable ignored) {}
        }
    }
}
