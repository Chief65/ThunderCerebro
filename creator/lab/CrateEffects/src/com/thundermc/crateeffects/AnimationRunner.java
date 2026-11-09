package com.thundermc.crateeffects;

import org.bukkit.Color;
import org.bukkit.Location;
import org.bukkit.Particle;
import org.bukkit.World;
import org.bukkit.entity.Firework;
import org.bukkit.entity.Player;
import org.bukkit.inventory.meta.FireworkMeta;
import org.bukkit.metadata.FixedMetadataValue;
import org.bukkit.scheduler.BukkitRunnable;

import java.util.concurrent.ThreadLocalRandom;

public class AnimationRunner {

    public static void playRewardAnimation(CrateEffects plugin, Location origin, Player player, String rarityId) {
        if (origin == null || origin.getWorld() == null) {
            return;
        }

        EffectConfig config = plugin.getEffectConfig();
        EffectConfig.RarityPalette palette = config.getPalette(rarityId);

        new BukkitRunnable() {
            private int tick = 0;
            private final World world = origin.getWorld();
            private final Location center = origin.clone();

            @Override
            public void run() {
                try {
                    if (world == null || !center.isChunkLoaded()) {
                        cancel();
                        return;
                    }

                    // ==========================================
                    // ETAPA 0 (Tick 0): Revelación instantánea
                    // ==========================================
                    if (tick == 0) {
                        if (config.isSoundsEnabled() && config.getStartSound() != null) {
                            try {
                                world.playSound(center, config.getStartSound(), config.getSoundVolume(), config.getStartPitch());
                            } catch (Throwable t) {
                                if (config.isDebug()) t.printStackTrace();
                            }
                        }

                        if (config.isParticlesEnabled() && config.isParticlesInitialFlash()) {
                            // En Paper 1.21+, Particle.FLASH requiere org.bukkit.Color como data
                            Color flashColor = (palette.getColors() != null && !palette.getColors().isEmpty())
                                    ? palette.getColors().get(0)
                                    : Color.WHITE;

                            try {
                                world.spawnParticle(Particle.FLASH, center.clone().add(0.0, 0.5, 0.0), 1, 0.0, 0.0, 0.0, 0.0, flashColor);
                            } catch (Throwable t) {
                                // Fallback seguro si la implementación de Particle no acepta Color
                                try {
                                    world.spawnParticle(Particle.FIREWORK, center.clone().add(0.0, 0.5, 0.0), 8, 0.1, 0.1, 0.1, 0.05);
                                } catch (Throwable ignored) {}
                            }

                            // Chispas adicionales leves
                            try {
                                world.spawnParticle(Particle.END_ROD, center.clone().add(0.0, 0.5, 0.0), 6, 0.15, 0.15, 0.15, 0.05);

                                // Anillo horizontal sutil de chispas
                                double radius = 0.75;
                                int points = 8;
                                for (int i = 0; i < points; i++) {
                                    double angle = (2 * Math.PI * i) / points;
                                    double x = Math.cos(angle) * radius;
                                    double z = Math.sin(angle) * radius;
                                    world.spawnParticle(Particle.FIREWORK, center.clone().add(x, 0.2, z), 1, 0.0, 0.0, 0.0, 0.01);
                                }
                            } catch (Throwable t) {
                                if (config.isDebug()) t.printStackTrace();
                            }
                        }
                    }

                    // ==========================================
                    // ETAPA 1 (Ticks 1 al 8): Espiral ascendente
                    // ==========================================
                    if (tick >= 1 && tick <= 8 && config.isParticlesEnabled() && config.isParticlesSpiralHelix()) {
                        try {
                            double progress = (double) tick / 8.0;
                            double yOffset = progress * 2.2;
                            double radius = 0.75 * (1.0 - progress * 0.3);
                            double angle = tick * 0.85;

                            // Rama 1 del espiral
                            double x1 = Math.cos(angle) * radius;
                            double z1 = Math.sin(angle) * radius;
                            world.spawnParticle(Particle.FIREWORK, center.clone().add(x1, yOffset, z1), 1, 0.0, 0.0, 0.0, 0.02);

                            // Rama 2 del espiral (opuesta)
                            double x2 = Math.cos(angle + Math.PI) * radius;
                            double z2 = Math.sin(angle + Math.PI) * radius;
                            world.spawnParticle(Particle.ELECTRIC_SPARK, center.clone().add(x2, yOffset, z2), 1, 0.0, 0.0, 0.0, 0.02);

                            if (tick == 5 && config.isSoundsEnabled() && config.getLaunchSound() != null) {
                                world.playSound(center, config.getLaunchSound(), config.getSoundVolume() * 0.8f, config.getLaunchPitch());
                            }
                        } catch (Throwable t) {
                            if (config.isDebug()) t.printStackTrace();
                        }
                    }

                    // ==========================================
                    // ETAPA 2 (Tick 10): Clímax de fuegos artificiales (Únicamente Blanco y partículas reducidas)
                    // ==========================================
                    if (tick == 10) {
                        double height = config.getFireworksHeightOffset();
                        Location burstLoc = center.clone().add(0.0, height, 0.0);

                        // Fuegos artificiales físicos protegidos (sin daño)
                        // EXCLUSIVAMENTE COLOR BLANCO y efecto suave
                        if (config.isFireworksEnabled()) {
                            try {
                                Firework fw = world.spawn(burstLoc, Firework.class);
                                FireworkMeta meta = fw.getFireworkMeta();
                                org.bukkit.FireworkEffect whiteEffect = org.bukkit.FireworkEffect.builder()
                                        .with(org.bukkit.FireworkEffect.Type.BALL)
                                        .withColor(Color.WHITE)
                                        .withFade(Color.WHITE)
                                        .trail(false)
                                        .flicker(false)
                                        .build();
                                meta.addEffect(whiteEffect);
                                meta.setPower(0);
                                fw.setFireworkMeta(meta);

                                if (config.isFireworksPreventDamage()) {
                                    fw.setMetadata(FireworkDamageListener.METADATA_KEY, new FixedMetadataValue(plugin, true));
                                }

                                fw.detonate();
                            } catch (Throwable t) {
                                plugin.getLogger().warning("Aviso en detonacion de fuegos artificiales: " + t.getMessage());
                                if (config.isDebug()) t.printStackTrace();
                            }
                        }

                        // Partículas de apoyo muy reducidas (6 chispas blancas leves en lugar de saturación)
                        if (config.isParticlesEnabled()) {
                            try {
                                world.spawnParticle(Particle.FIREWORK, burstLoc, 6, 0.25, 0.25, 0.25, 0.04);
                            } catch (Throwable t) {
                                if (config.isDebug()) t.printStackTrace();
                            }
                        }

                        // Sonido clímax
                        if (config.isSoundsEnabled() && config.getClimaxSound() != null) {
                            try {
                                world.playSound(burstLoc, config.getClimaxSound(), config.getSoundVolume(), config.getClimaxPitch());
                            } catch (Throwable t) {
                                if (config.isDebug()) t.printStackTrace();
                            }
                        }
                    }

                    // ==========================================
                    // ETAPA 3 (Ticks 14 al 20): Chispas residuales
                    // ==========================================
                    if (tick >= 14 && tick <= 20 && config.isParticlesEnabled()) {
                        try {
                            double ox = (ThreadLocalRandom.current().nextDouble() - 0.5) * 1.4;
                            double oy = config.getFireworksHeightOffset() - (tick - 14) * 0.25;
                            double oz = (ThreadLocalRandom.current().nextDouble() - 0.5) * 1.4;
                            world.spawnParticle(Particle.FIREWORK, center.clone().add(ox, oy, oz), 1, 0.0, -0.02, 0.0, 0.01);
                        } catch (Throwable t) {
                            if (config.isDebug()) t.printStackTrace();
                        }
                    }

                    if (tick >= 22) {
                        cancel();
                    }

                    tick++;
                } catch (Throwable t) {
                    plugin.getLogger().warning("Error en ejecucion de animacion: " + t.getMessage());
                    if (config.isDebug()) t.printStackTrace();
                    cancel();
                }
            }
        }.runTaskTimer(plugin, 0L, 1L);
    }
}
