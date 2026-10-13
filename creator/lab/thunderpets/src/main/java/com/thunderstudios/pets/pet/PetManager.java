package com.thunderstudios.pets.pet;

import com.thunderstudios.pets.ThunderPetsPlugin;
import com.thunderstudios.pets.util.TextUtil;
import org.bukkit.Material;
import org.bukkit.Particle;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.entity.Player;
import org.bukkit.inventory.meta.trim.TrimMaterial;
import org.bukkit.inventory.meta.trim.TrimPattern;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public class PetManager {

    private final ThunderPetsPlugin plugin;
    private final Map<String, PetModel> models = new LinkedHashMap<>();
    private final Map<UUID, PetInstance> activePets = new ConcurrentHashMap<>();

    private double smoothFactor = 0.25;
    private double maxFollowDistance = 20.0;
    private boolean hideInSpectator = true;

    public PetManager(ThunderPetsPlugin plugin) {
        this.plugin = plugin;
    }

    public void loadConfig() {
        despawnAll();
        models.clear();

        FileConfiguration config = plugin.getConfig();

        smoothFactor = config.getDouble("settings.smooth-factor", 0.25);
        maxFollowDistance = config.getDouble("settings.max-follow-distance", 20.0);
        hideInSpectator = config.getBoolean("settings.hide-in-spectator", true);

        ConfigurationSection petsSection = config.getConfigurationSection("pets");
        if (petsSection != null) {
            for (String key : petsSection.getKeys(false)) {
                ConfigurationSection sec = petsSection.getConfigurationSection(key);
                if (sec == null) continue;

                String name = sec.getString("name", "&eMascota");
                String permission = sec.getString("permission", "thunderpets.use");
                int slot = sec.getInt("gui.slot", 10);
                List<String> lore = sec.getStringList("gui.lore");

                String typeStr = sec.getString("type", "HEAD_ONLY");
                boolean halfBody = "HALF_BODY".equalsIgnoreCase(typeStr);
                String headTexture = sec.getString("head-texture", "");

                Material chestplateMat = null;
                TrimPattern pattern = null;
                TrimMaterial trimMat = null;
                if (halfBody && sec.isConfigurationSection("chestplate")) {
                    String chestMatStr = sec.getString("chestplate.material", "NETHERITE_CHESTPLATE");
                    chestplateMat = Material.matchMaterial(chestMatStr);
                    if (chestplateMat == null) chestplateMat = Material.NETHERITE_CHESTPLATE;

                    String patStr = sec.getString("chestplate.trim-pattern", "SILENCE");
                    pattern = parseTrimPattern(patStr);

                    String tmatStr = sec.getString("chestplate.trim-material", "GOLD");
                    trimMat = parseTrimMaterial(tmatStr);
                }

                Material mainHandMat = null;
                if (halfBody && sec.isString("main-hand")) {
                    mainHandMat = Material.matchMaterial(sec.getString("main-hand", "TOTEM_OF_UNDYING"));
                }

                double right = sec.getDouble("offset.right", 1.1);
                double behind = sec.getDouble("offset.behind", 0.5);
                double height = sec.getDouble("offset.height", 0.9);

                boolean bobbing = sec.getBoolean("bobbing.enabled", false);
                double amplitude = sec.getDouble("bobbing.amplitude", 0.1);
                double speed = sec.getDouble("bobbing.speed", 0.08);

                boolean particles = sec.getBoolean("particles.enabled", false);
                Particle particle = null;
                if (particles) {
                    try {
                        particle = Particle.valueOf(sec.getString("particles.type", "CHERRY_LEAVES"));
                    } catch (Exception e) {
                        particle = Particle.CHERRY_LEAVES;
                    }
                }
                int particleCount = sec.getInt("particles.count", 1);
                int particleInterval = sec.getInt("particles.interval-ticks", 3);

                String qualityStr = sec.getString("quality", "SUPER");
                PetQuality quality = PetQuality.fromString(qualityStr);
                int phase = sec.getInt("phase", 1);
                int requiredLevel = sec.getInt("required-level", 1);

                PetModel model = new PetModel(
                        key, name, quality, phase, requiredLevel,
                        permission, slot, lore,
                        halfBody, headTexture,
                        chestplateMat, pattern, trimMat,
                        mainHandMat,
                        right, behind, height,
                        bobbing, amplitude, speed,
                        particles, particle, particleCount, particleInterval
                );

                models.put(key, model);
            }
        }
        plugin.getLogger().info("Se han cargado " + models.size() + " mascotas cosmeticas.");
    }

    private TrimPattern parseTrimPattern(String pattern) {
        if (pattern == null) return TrimPattern.SILENCE;
        return switch (pattern.toUpperCase()) {
            case "SENTRY" -> TrimPattern.SENTRY;
            case "DUNE" -> TrimPattern.DUNE;
            case "COAST" -> TrimPattern.COAST;
            case "WILD" -> TrimPattern.WILD;
            case "WARD" -> TrimPattern.WARD;
            case "EYE" -> TrimPattern.EYE;
            case "VEX" -> TrimPattern.VEX;
            case "TIDE" -> TrimPattern.TIDE;
            case "SNOUT" -> TrimPattern.SNOUT;
            case "RIB" -> TrimPattern.RIB;
            case "SPIRE" -> TrimPattern.SPIRE;
            case "WAYFINDER" -> TrimPattern.WAYFINDER;
            case "SHAPER" -> TrimPattern.SHAPER;
            case "RAISER" -> TrimPattern.RAISER;
            case "HOST" -> TrimPattern.HOST;
            case "FLOW" -> TrimPattern.FLOW;
            case "BOLT" -> TrimPattern.BOLT;
            default -> TrimPattern.SILENCE;
        };
    }

    private TrimMaterial parseTrimMaterial(String mat) {
        if (mat == null) return TrimMaterial.GOLD;
        return switch (mat.toUpperCase()) {
            case "QUARTZ" -> TrimMaterial.QUARTZ;
            case "IRON" -> TrimMaterial.IRON;
            case "NETHERITE" -> TrimMaterial.NETHERITE;
            case "REDSTONE" -> TrimMaterial.REDSTONE;
            case "COPPER" -> TrimMaterial.COPPER;
            case "EMERALD" -> TrimMaterial.EMERALD;
            case "DIAMOND" -> TrimMaterial.DIAMOND;
            case "LAPIS" -> TrimMaterial.LAPIS;
            case "AMETHYST" -> TrimMaterial.AMETHYST;
            default -> TrimMaterial.GOLD;
        };
    }

    public void togglePet(Player player, String petId) {
        PetModel model = models.get(petId);
        if (model == null) return;

        if (!player.hasPermission(model.getPermission()) && !player.hasPermission("thunderpets.pet.*")) {
            String prefix = plugin.getConfig().getString("messages.prefix", "&6&lMASCOTAS &8▸ ");
            String noPerm = plugin.getConfig().getString("messages.no-permission", "&cNo tienes permiso.");
            player.sendMessage(TextUtil.color(prefix + noPerm));
            return;
        }

        PetInstance current = activePets.get(player.getUniqueId());
        if (current != null) {
            current.despawn();
            activePets.remove(player.getUniqueId());

            if (current.getModel().getId().equals(petId)) {
                String prefix = plugin.getConfig().getString("messages.prefix", "&6&lMASCOTAS &8▸ ");
                String msg = plugin.getConfig().getString("messages.pet-despawned", "&eHas guardado a tu mascota.");
                player.sendMessage(TextUtil.color(prefix + msg));
                return;
            }
        }

        PetInstance newPet = new PetInstance(player, model, smoothFactor, maxFollowDistance, hideInSpectator);
        activePets.put(player.getUniqueId(), newPet);

        String prefix = plugin.getConfig().getString("messages.prefix", "&6&lMASCOTAS &8▸ ");
        String msg = plugin.getConfig().getString("messages.pet-summoned", "&aHas invocado a tu mascota %pet%&a.")
                .replace("%pet%", model.getName());
        player.sendMessage(TextUtil.color(prefix + msg));
    }

    public void despawnPet(Player player) {
        PetInstance instance = activePets.remove(player.getUniqueId());
        if (instance != null) {
            instance.despawn();
            String prefix = plugin.getConfig().getString("messages.prefix", "&6&lMASCOTAS &8▸ ");
            String msg = plugin.getConfig().getString("messages.pet-despawned", "&eHas guardado a tu mascota.");
            player.sendMessage(TextUtil.color(prefix + msg));
        }
    }

    public void despawnSilently(UUID uuid) {
        PetInstance instance = activePets.remove(uuid);
        if (instance != null) {
            instance.despawn();
        }
    }

    public PetInstance getActivePet(Player player) {
        return activePets.get(player.getUniqueId());
    }

    public Map<String, PetModel> getModels() {
        return Collections.unmodifiableMap(models);
    }

    public void tickAll() {
        Iterator<Map.Entry<UUID, PetInstance>> it = activePets.entrySet().iterator();
        while (it.hasNext()) {
            Map.Entry<UUID, PetInstance> entry = it.next();
            PetInstance pet = entry.getValue();
            if (!pet.isValid() || !pet.getPlayer().isOnline()) {
                pet.despawn();
                it.remove();
                continue;
            }
            pet.tick();
        }
    }

    public void despawnAll() {
        for (PetInstance pet : activePets.values()) {
            pet.despawn();
        }
        activePets.clear();
    }
}
