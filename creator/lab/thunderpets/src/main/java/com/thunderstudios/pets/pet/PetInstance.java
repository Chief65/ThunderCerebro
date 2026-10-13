package com.thunderstudios.pets.pet;

import com.thunderstudios.pets.util.TextUtil;
import org.bukkit.GameMode;
import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.entity.ArmorStand;
import org.bukkit.entity.Player;
import org.bukkit.inventory.EntityEquipment;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ArmorMeta;
import org.bukkit.inventory.meta.trim.ArmorTrim;

public class PetInstance {

    private final Player player;
    private final PetModel model;
    private final double smoothFactor;
    private final double maxFollowDistanceSq;
    private final boolean hideInSpectator;

    private ArmorStand armorStand;
    private Location lastPlayerLoc;
    private long tickCount = 0;
    private boolean valid = true;

    public PetInstance(Player player, PetModel model, double smoothFactor, double maxFollowDistance, boolean hideInSpectator) {
        this.player = player;
        this.model = model;
        this.smoothFactor = Math.max(0.05, Math.min(1.0, smoothFactor));
        this.maxFollowDistanceSq = maxFollowDistance * maxFollowDistance;
        this.hideInSpectator = hideInSpectator;
        spawn();
    }

    private void spawn() {
        Location spawnLoc = calculateTargetLocation(player.getLocation(), 0.0);
        World world = player.getWorld();

        armorStand = world.spawn(spawnLoc, ArmorStand.class, entity -> {
            entity.setInvisible(true);
            entity.setSmall(true);
            entity.setMarker(true);
            entity.setGravity(false);
            entity.setBasePlate(false);
            entity.setPersistent(false);
            entity.setCanPickupItems(false);
            entity.setCollidable(false);
            entity.setInvulnerable(true);

            entity.setCustomName(null);
            entity.setCustomNameVisible(false);

            EntityEquipment eq = entity.getEquipment();
            if (eq != null) {
                eq.setHelmet(TextUtil.createCustomHead(model.getHeadTexture()));

                if (model.isHalfBody()) {
                    entity.setArms(true);

                    if (model.getChestplateMaterial() != null) {
                        ItemStack chest = new ItemStack(model.getChestplateMaterial());
                        if (model.getTrimPattern() != null && model.getTrimMaterial() != null) {
                            if (chest.getItemMeta() instanceof ArmorMeta armorMeta) {
                                armorMeta.setTrim(new ArmorTrim(model.getTrimMaterial(), model.getTrimPattern()));
                                chest.setItemMeta(armorMeta);
                            }
                        }
                        eq.setChestplate(chest);
                    }

                    if (model.getMainHandMaterial() != null) {
                        eq.setItemInMainHand(new ItemStack(model.getMainHandMaterial()));
                    }
                } else {
                    entity.setArms(false);
                }
            }
        });
    }

    private boolean hiddenInSpectator = false;

    public void tick() {
        if (!valid) return;

        if (armorStand == null || !armorStand.isValid() || armorStand.isDead()) {
            if (player.isOnline() && player.isValid()) {
                spawn();
            } else {
                despawn();
                return;
            }
        }

        if (!player.isOnline() || !player.isValid()) {
            despawn();
            return;
        }

        tickCount++;

        // Modo espectador: ocultar o visibilizar equipamiento
        if (hideInSpectator && player.getGameMode() == GameMode.SPECTATOR) {
            if (!hiddenInSpectator) {
                hiddenInSpectator = true;
                EntityEquipment eq = armorStand.getEquipment();
                if (eq != null) eq.clear();
            }
            return;
        } else if (hiddenInSpectator) {
            hiddenInSpectator = false;
            EntityEquipment eq = armorStand.getEquipment();
            if (eq != null) {
                eq.setHelmet(TextUtil.createCustomHead(model.getHeadTexture()));
                if (model.isHalfBody()) {
                    if (model.getChestplateMaterial() != null) {
                        ItemStack chest = new ItemStack(model.getChestplateMaterial());
                        if (model.getTrimPattern() != null && model.getTrimMaterial() != null) {
                            if (chest.getItemMeta() instanceof ArmorMeta armorMeta) {
                                armorMeta.setTrim(new ArmorTrim(model.getTrimMaterial(), model.getTrimPattern()));
                                chest.setItemMeta(armorMeta);
                            }
                        }
                        eq.setChestplate(chest);
                    }
                    if (model.getMainHandMaterial() != null) {
                        eq.setItemInMainHand(new ItemStack(model.getMainHandMaterial()));
                    }
                }
            }
        }

        Location playerLoc = player.getLocation();
        Location currentLoc = armorStand.getLocation();

        // Si el jugador cambió de mundo
        if (!currentLoc.getWorld().equals(playerLoc.getWorld())) {
            armorStand.remove();
            spawn();
            lastPlayerLoc = playerLoc.clone();
            return;
        }

        boolean playerMoved = (lastPlayerLoc == null)
                || lastPlayerLoc.distanceSquared(playerLoc) > 0.0004
                || Math.abs(lastPlayerLoc.getYaw() - playerLoc.getYaw()) > 1.0f;

        double bobOffset = 0.0;
        if (model.isBobbingEnabled()) {
            bobOffset = Math.sin(tickCount * model.getBobbingSpeed()) * model.getBobbingAmplitude();
        }

        Location targetLoc = calculateTargetLocation(playerLoc, bobOffset);
        double distSq = currentLoc.distanceSquared(targetLoc);

        // DIRTY CHECKING: Si el jugador no se ha movido y la mascota ya está en posición
        if (!playerMoved && distSq < 0.002 && Math.abs(currentLoc.getYaw() - playerLoc.getYaw()) < 1.5f) {
            // No teletransportar si no hay oscilación o si ya está perfectamente sincronizada
            if (!model.isBobbingEnabled()) {
                // Totalmente quieto, omitir paquete de red
            } else if (tickCount % 2 == 0) {
                // Bobbing suave throttled a la mitad de paquetes en reposo
                double ny = currentLoc.getY() + (targetLoc.getY() - currentLoc.getY()) * smoothFactor;
                armorStand.teleport(new Location(player.getWorld(), currentLoc.getX(), ny, currentLoc.getZ(), currentLoc.getYaw(), 0));
            }
        } else {
            if (distSq > maxFollowDistanceSq) {
                armorStand.teleport(targetLoc);
            } else {
                double nx = currentLoc.getX() + (targetLoc.getX() - currentLoc.getX()) * smoothFactor;
                double ny = currentLoc.getY() + (targetLoc.getY() - currentLoc.getY()) * smoothFactor;
                double nz = currentLoc.getZ() + (targetLoc.getZ() - currentLoc.getZ()) * smoothFactor;

                float curYaw = currentLoc.getYaw();
                float targetYaw = playerLoc.getYaw();
                float diff = (targetYaw - curYaw + 540) % 360 - 180;
                float newYaw = curYaw + diff * (float) Math.min(1.0, smoothFactor * 1.5);

                armorStand.teleport(new Location(player.getWorld(), nx, ny, nz, newYaw, 0));
            }
        }

        lastPlayerLoc = playerLoc.clone();

        // Partículas sutiles
        if (model.isParticlesEnabled() && model.getParticle() != null) {
            if (tickCount % Math.max(1, model.getParticleInterval()) == 0) {
                Location partLoc = armorStand.getLocation().clone().add(0, model.isHalfBody() ? 0.6 : 0.75, 0);
                armorStand.getWorld().spawnParticle(
                        model.getParticle(),
                        partLoc,
                        model.getParticleCount(),
                        0.1, 0.08, 0.1,
                        0.01
                );
            }
        }
    }

    private Location calculateTargetLocation(Location pLoc, double bobOffset) {
        double yawRad = Math.toRadians(pLoc.getYaw());
        // Vector lateral derecho
        double rightX = Math.cos(yawRad) * model.getOffsetRight();
        double rightZ = Math.sin(yawRad) * model.getOffsetRight();
        // Vector hacia atrás
        double behindX = Math.sin(yawRad) * model.getOffsetBehind();
        double behindZ = -Math.cos(yawRad) * model.getOffsetBehind();

        double tx = pLoc.getX() + rightX + behindX;
        double ty = pLoc.getY() + model.getOffsetHeight() + bobOffset;
        double tz = pLoc.getZ() + rightZ + behindZ;

        return new Location(pLoc.getWorld(), tx, ty, tz, pLoc.getYaw(), 0);
    }

    public void despawn() {
        valid = false;
        if (armorStand != null) {
            if (armorStand.isValid()) {
                armorStand.remove();
            }
            armorStand = null;
        }
    }

    public Player getPlayer() { return player; }
    public PetModel getModel() { return model; }
    public boolean isValid() { return valid; }
}
