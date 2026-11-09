package com.thundermc.crateeffects.opening;

import com.thundermc.crateeffects.AnimationRunner;
import com.thundermc.crateeffects.CrateEffects;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.minimessage.MiniMessage;
import net.kyori.adventure.text.serializer.legacy.LegacyComponentSerializer;
import org.bukkit.Bukkit;
import org.bukkit.Color;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.Particle;
import org.bukkit.Sound;
import org.bukkit.block.Block;
import org.bukkit.block.data.BlockData;
import org.bukkit.entity.BlockDisplay;
import org.bukkit.entity.Display;
import org.bukkit.entity.ItemDisplay;
import org.bukkit.entity.Player;
import org.bukkit.entity.TextDisplay;
import org.bukkit.inventory.ItemStack;
import org.bukkit.util.Transformation;
import org.bukkit.util.Vector;
import org.joml.Quaternionf;
import org.joml.Vector3f;
import su.nightexpress.excellentcrates.CratesPlugin;
import su.nightexpress.excellentcrates.api.crate.Reward;
import su.nightexpress.excellentcrates.crate.cost.Cost;
import su.nightexpress.excellentcrates.crate.impl.CrateSource;
import su.nightexpress.excellentcrates.crate.reward.impl.ItemReward;
import su.nightexpress.excellentcrates.opening.world.WorldOpening;
import su.nightexpress.excellentcrates.util.ItemHelper;
import su.nightexpress.excellentcrates.util.pos.WorldPos;
import su.nightexpress.nightcore.bridge.item.AdaptedItem;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.ThreadLocalRandom;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ShulkerOpening extends WorldOpening {

    private final CrateEffects effectsPlugin;
    private final Reward winningReward;
    private final List<Reward> spinRewards = new ArrayList<>();

    private Block crateBlock;
    private BlockData originalBlockData;
    private Location displayLocation;
    private BlockDisplay bottomBase;
    private BlockDisplay topLid;
    private ItemDisplay rewardDisplay;
    private ItemDisplay leftDisplay;
    private ItemDisplay rightDisplay;
    private TextDisplay nameDisplay;
    private TextDisplay subtitleDisplay;

    private boolean completed = false;

    // Estados de animación
    private static final int STATE_OPENING = 0;
    private static final int STATE_SPINNING = 1;
    private static final int STATE_WINNER_DISPLAY = 2;
    private static final int STATE_CLOSING = 3;

    private int state = STATE_OPENING;
    private int stateTicks = 0;

    // Curva de desaceleración CS:GO (ticks de espera por cada giro)
    private static final int[] SPIN_DELAYS = new int[]{
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 0..9: giros rápidos iniciales
            3, 3, 3, 4, 4, 4,             // 10..15: transición media
            5, 5, 6, 7, 8, 10, 13         // 16..22: desaceleración final
    };
    private int currentSpin = 0;
    private int spinDelayCounter = 0;

    // Ruleta CS:GO de 3 ítems simultáneos (Izquierda - Centro - Derecha)
    private Reward leftReward;
    private Reward centerReward;
    private Reward rightReward;

    public ShulkerOpening(CrateEffects effectsPlugin, CratesPlugin plugin, Player player, CrateSource source, Cost cost) {
        super(plugin, player, source, cost);
        this.effectsPlugin = effectsPlugin;
        this.winningReward = this.crate.rollReward(player);

        List<Reward> available = new ArrayList<>(this.crate.getRewards(player));
        if (available.isEmpty()) {
            this.spinRewards.add(this.winningReward);
        } else {
            this.spinRewards.addAll(available);
        }
    }

    @Override
    public long getInterval() {
        return 1L;
    }

    @Override
    public boolean isCompleted() {
        return completed;
    }

    @Override
    public void instaRoll() {
        this.completed = true;
    }

    @Override
    protected void onStart() {
        setupEntities();
        this.setRefundable(false);
    }

    private void setupEntities() {
        try {
            crateBlock = this.source.getBlock();

            // Si source no tiene bloque directo, buscar bloque cercano registrado para esta crate
            if (crateBlock == null) {
                Location playerLoc = this.player.getLocation();
                if (this.crate.getBlockPositions() != null) {
                    double closestDist = Double.MAX_VALUE;
                    for (WorldPos wp : this.crate.getBlockPositions()) {
                        Location loc = wp.toLocation();
                        if (loc != null && loc.getWorld() != null && loc.getWorld().equals(playerLoc.getWorld())) {
                            double distSq = loc.distanceSquared(playerLoc);
                            if (distSq < closestDist && distSq < 400.0) { // dentro de 20 bloques
                                closestDist = distSq;
                                crateBlock = loc.getBlock();
                            }
                        }
                    }
                }
            }

            if (crateBlock != null) {
                originalBlockData = crateBlock.getBlockData();
                // Epicentro: anclado exactamente en la base del bloque físico (Y=0 del bloque)
                displayLocation = crateBlock.getLocation().clone().add(0.5, 0.0, 0.5);
                this.hideHologram(WorldPos.from(crateBlock));

                // Ocultar el bloque físico de inmediato
                setFakeBlock(Material.AIR);

                // Reforzar a los ticks 1 y 2 para neutralizar el ACK de interacción de Paper
                Bukkit.getScheduler().runTaskLater(effectsPlugin, () -> {
                    if (!completed && state != STATE_CLOSING) {
                        setFakeBlock(Material.AIR);
                    }
                }, 1L);
                Bukkit.getScheduler().runTaskLater(effectsPlugin, () -> {
                    if (!completed && state != STATE_CLOSING) {
                        setFakeBlock(Material.AIR);
                    }
                }, 2L);
            } else {
                // Apertura virtual en el aire frente a la mirada del jugador
                Location eye = this.player.getEyeLocation().clone();
                displayLocation = eye.add(this.player.getLocation().getDirection().multiply(2.2)).subtract(0.0, 0.5, 0.0);
            }

            Material shulkerMat = resolveShulkerMaterial(this.winningReward);

            // 1. Spawneo de Base Inferior (Ocupa la mitad inferior Y=0.0 a 0.5 del bloque)
            bottomBase = displayLocation.getWorld().spawn(displayLocation, BlockDisplay.class, d -> {
                d.setBlock(shulkerMat.createBlockData());
                d.setTransformation(new Transformation(
                        new Vector3f(-0.5f, 0.0f, -0.5f),
                        new Quaternionf(),
                        new Vector3f(1.0f, 0.5f, 1.0f),
                        new Quaternionf()
                ));
            });

            // 2. Spawneo de Tapa Superior (Inicia cerrada sobre la base Y=0.5 a 1.0 del bloque)
            topLid = displayLocation.getWorld().spawn(displayLocation, BlockDisplay.class, d -> {
                d.setBlock(shulkerMat.createBlockData());
                d.setTransformation(new Transformation(
                        new Vector3f(-0.5f, 0.5f, -0.5f),
                        new Quaternionf(),
                        new Vector3f(1.0f, 0.5f, 1.0f),
                        new Quaternionf()
                ));
            });

            // 3. Cálculo de vectores laterales para la tira CS:GO respecto a la vista del jugador
            Vector lookAtCrate = displayLocation.toVector().subtract(player.getLocation().toVector()).setY(0);
            if (lookAtCrate.lengthSquared() < 0.001) {
                lookAtCrate = new Vector(0, 0, 1);
            } else {
                lookAtCrate.normalize();
            }
            Vector rightVec = lookAtCrate.clone().crossProduct(new Vector(0, 1, 0)).normalize();
            Vector leftVec = rightVec.clone().multiply(-1);
            Vector recessVec = lookAtCrate.clone().multiply(0.12); // Ligeramente retrasados en profundidad

            Location centerLoc = displayLocation.clone().add(0.0, 1.05, 0.0);
            Location leftLoc = centerLoc.clone().add(leftVec.clone().multiply(0.55)).add(recessVec);
            Location rightLoc = centerLoc.clone().add(rightVec.clone().multiply(0.55)).add(recessVec);

            // Inicializar recompensas de la tira CS:GO
            centerReward = getRandomReward();
            leftReward = getRandomReward();
            rightReward = getRandomReward();

            // 4. Spawneo del Ítem Central (Limpio sin glow durante el giro)
            rewardDisplay = displayLocation.getWorld().spawn(centerLoc, ItemDisplay.class, d -> {
                d.setBillboard(Display.Billboard.CENTER);
                d.setItemDisplayTransform(ItemDisplay.ItemDisplayTransform.FIXED);
                d.setItemStack(resolveDisplayItem(centerReward));
                d.setTransformation(new Transformation(
                        new Vector3f(0.0f, 0.0f, 0.0f),
                        new Quaternionf(),
                        new Vector3f(0.85f, 0.85f, 0.85f),
                        new Quaternionf()
                ));
            });

            // 5. Spawneo de Ítem Izquierdo (Objeto previo CS:GO, escala sutil 0.38 y luz atenuada)
            leftDisplay = displayLocation.getWorld().spawn(leftLoc, ItemDisplay.class, d -> {
                d.setBillboard(Display.Billboard.CENTER);
                d.setItemDisplayTransform(ItemDisplay.ItemDisplayTransform.FIXED);
                d.setItemStack(resolveDisplayItem(leftReward));
                d.setBrightness(new Display.Brightness(4, 4)); // Atenuado / baja opacidad
                d.setTransformation(new Transformation(
                        new Vector3f(0.0f, 0.0f, 0.0f),
                        new Quaternionf(),
                        new Vector3f(0.38f, 0.38f, 0.38f),
                        new Quaternionf()
                ));
            });

            // 6. Spawneo de Ítem Derecho (Objeto siguiente CS:GO, escala sutil 0.38 y luz atenuada)
            rightDisplay = displayLocation.getWorld().spawn(rightLoc, ItemDisplay.class, d -> {
                d.setBillboard(Display.Billboard.CENTER);
                d.setItemDisplayTransform(ItemDisplay.ItemDisplayTransform.FIXED);
                d.setItemStack(resolveDisplayItem(rightReward));
                d.setBrightness(new Display.Brightness(4, 4)); // Atenuado / baja opacidad
                d.setTransformation(new Transformation(
                        new Vector3f(0.0f, 0.0f, 0.0f),
                        new Quaternionf(),
                        new Vector3f(0.38f, 0.38f, 0.38f),
                        new Quaternionf()
                ));
            });

            // 7. Spawneo de Textos (Con altura elevada holgada por encima de la tapa superior a Y=2.10)
            // Línea 1: Nombre del Ítem (Mayor tamaño, escala 1.30, sin background, a Y=2.75)
            nameDisplay = displayLocation.getWorld().spawn(displayLocation.clone().add(0.0, 2.75, 0.0), TextDisplay.class, d -> {
                d.setBillboard(Display.Billboard.CENTER);
                d.setBackgroundColor(Color.fromARGB(0, 0, 0, 0)); // Totalmente transparente
                d.setTransformation(new Transformation(
                        new Vector3f(0.0f, 0.0f, 0.0f),
                        new Quaternionf(),
                        new Vector3f(1.30f, 1.30f, 1.30f),
                        new Quaternionf()
                ));
                d.text(formatRewardTitle(centerReward));
            });

            // Línea 2: Únicamente Probabilidad (Con background negro bajado de opacidad, a Y=2.38)
            subtitleDisplay = displayLocation.getWorld().spawn(displayLocation.clone().add(0.0, 2.38, 0.0), TextDisplay.class, d -> {
                d.setBillboard(Display.Billboard.CENTER);
                d.setBackgroundColor(Color.fromARGB(140, 20, 20, 25)); // Negro con opacidad reducida
                d.setTransformation(new Transformation(
                        new Vector3f(0.0f, 0.0f, 0.0f),
                        new Quaternionf(),
                        new Vector3f(0.85f, 0.85f, 0.85f),
                        new Quaternionf()
                ));
                d.text(formatRewardSubtitle(centerReward));
            });

            // Sonido de apertura del Shulker Box
            displayLocation.getWorld().playSound(displayLocation, Sound.BLOCK_SHULKER_BOX_OPEN, 1.0f, 1.0f);
            displayLocation.getWorld().spawnParticle(Particle.PORTAL, displayLocation.clone().add(0.0, 0.7, 0.0), 8, 0.2, 0.2, 0.2, 0.1);

            // Interpolación: elevación suave de la tapa en 14 ticks (de Y=0.5 a Y=1.60, 1.1 bloques de hueco)
            topLid.setInterpolationDelay(0);
            topLid.setInterpolationDuration(14);
            topLid.setTransformation(new Transformation(
                    new Vector3f(-0.5f, 1.60f, -0.5f),
                    new Quaternionf(),
                    new Vector3f(1.0f, 0.5f, 1.0f),
                    new Quaternionf()
            ));

            effectsPlugin.getLogger().info("[ShulkerOpening] Setup exitoso para " + player.getName() + " en " + displayLocation);
        } catch (Throwable t) {
            effectsPlugin.getLogger().warning("Error al iniciar ShulkerOpening: " + t.getMessage());
            t.printStackTrace();
        }
    }

    @Override
    protected void onTick() {
        if (this.completed || displayLocation == null || displayLocation.getWorld() == null) {
            return;
        }

        // Mantener el bloque invisible en el cliente durante toda la fase de apertura y giro
        if (crateBlock != null && state != STATE_CLOSING) {
            if (this.stateTicks <= 5 || this.stateTicks % 5 == 0) {
                setFakeBlock(Material.AIR);
            }
        }

        stateTicks++;

        switch (state) {
            case STATE_OPENING -> {
                if (stateTicks >= 14) {
                    state = STATE_SPINNING;
                    stateTicks = 0;
                    currentSpin = 0;
                    spinDelayCounter = 0;
                }
            }
            case STATE_SPINNING -> {
                spinDelayCounter++;
                int targetDelay = (currentSpin < SPIN_DELAYS.length) ? SPIN_DELAYS[currentSpin] : 14;

                if (spinDelayCounter >= targetDelay) {
                    spinDelayCounter = 0;

                    if (currentSpin < SPIN_DELAYS.length) {
                        // Desplazamiento de ruleta CS:GO: izquierda <- centro <- derecha <- nuevo
                        leftReward = centerReward;
                        centerReward = rightReward;

                        // Si en el próximo giro aterrizamos en el final, cargar el ganador en la derecha
                        if (currentSpin + 1 == SPIN_DELAYS.length) {
                            rightReward = winningReward;
                        } else {
                            rightReward = getRandomReward();
                        }

                        updateDisplays(leftReward, centerReward, rightReward);

                        float progress = (float) currentSpin / (float) SPIN_DELAYS.length;
                        float pitch = 1.0f + (progress * 0.5f);
                        displayLocation.getWorld().playSound(displayLocation, Sound.UI_BUTTON_CLICK, 0.6f, pitch);

                        currentSpin++;
                    } else {
                        // Giro final: el ítem ganador aterriza exactamente en el centro
                        displayWinner();
                        state = STATE_WINNER_DISPLAY;
                        stateTicks = 0;
                    }
                }
            }
            case STATE_WINNER_DISPLAY -> {
                // Muestra al ganador con celebración durante 35 ticks (~1.75 segundos)
                if (stateTicks >= 35) {
                    // Iniciamos el cierre del Shulker
                    displayLocation.getWorld().playSound(displayLocation, Sound.BLOCK_SHULKER_BOX_CLOSE, 1.0f, 1.0f);

                    topLid.setInterpolationDelay(0);
                    topLid.setInterpolationDuration(12);
                    topLid.setTransformation(new Transformation(
                            new Vector3f(-0.5f, 0.5f, -0.5f), // Vuelve a cerrar sobre la base
                            new Quaternionf(),
                            new Vector3f(1.0f, 0.5f, 1.0f),
                            new Quaternionf()
                    ));

                    rewardDisplay.setInterpolationDelay(0);
                    rewardDisplay.setInterpolationDuration(10);
                    rewardDisplay.setTransformation(new Transformation(
                            new Vector3f(0.0f, 0.0f, 0.0f),
                            new Quaternionf(),
                            new Vector3f(0.0f, 0.0f, 0.0f),
                            new Quaternionf()
                    ));

                    if (leftDisplay != null) {
                        leftDisplay.remove();
                        leftDisplay = null;
                    }
                    if (rightDisplay != null) {
                        rightDisplay.remove();
                        rightDisplay = null;
                    }
                    if (nameDisplay != null) {
                        nameDisplay.text(Component.empty());
                    }
                    if (subtitleDisplay != null) {
                        subtitleDisplay.text(Component.empty());
                    }

                    state = STATE_CLOSING;
                    stateTicks = 0;
                }
            }
            case STATE_CLOSING -> {
                if (stateTicks >= 14) {
                    this.completed = true;
                }
            }
        }
    }

    private void updateDisplays(Reward left, Reward center, Reward right) {
        if (leftDisplay != null && left != null) {
            leftDisplay.setItemStack(resolveDisplayItem(left));
        }
        if (rewardDisplay != null && center != null) {
            rewardDisplay.setItemStack(resolveDisplayItem(center));
        }
        if (rightDisplay != null && right != null) {
            rightDisplay.setItemStack(resolveDisplayItem(right));
        }
        if (nameDisplay != null && center != null) {
            nameDisplay.text(formatRewardTitle(center));
        }
        if (subtitleDisplay != null && center != null) {
            subtitleDisplay.text(formatRewardSubtitle(center));
        }
    }

    private void displayWinner() {
        // En el ganador, los laterales se desvanecen contrayéndose
        if (leftDisplay != null) {
            leftDisplay.setInterpolationDelay(0);
            leftDisplay.setInterpolationDuration(6);
            leftDisplay.setTransformation(new Transformation(
                    new Vector3f(0.0f, 0.0f, 0.0f),
                    new Quaternionf(),
                    new Vector3f(0.0f, 0.0f, 0.0f),
                    new Quaternionf()
            ));
        }
        if (rightDisplay != null) {
            rightDisplay.setInterpolationDelay(0);
            rightDisplay.setInterpolationDuration(6);
            rightDisplay.setTransformation(new Transformation(
                    new Vector3f(0.0f, 0.0f, 0.0f),
                    new Quaternionf(),
                    new Vector3f(0.0f, 0.0f, 0.0f),
                    new Quaternionf()
            ));
        }

        ItemStack item = resolveDisplayItem(winningReward);
        if (rewardDisplay != null && item != null) {
            rewardDisplay.setItemStack(item);
            rewardDisplay.setGlowing(true);

            String rarityId = winningReward.getRarity() != null ? winningReward.getRarity().getId() : "default";
            Color glowColor = resolveGlowColor(rarityId);
            try {
                rewardDisplay.setGlowColorOverride(glowColor);
            } catch (Throwable ignored) {}

            // Pop de tamaño al aterrizar en el ganador
            rewardDisplay.setInterpolationDelay(0);
            rewardDisplay.setInterpolationDuration(4);
            rewardDisplay.setTransformation(new Transformation(
                    new Vector3f(0.0f, 0.0f, 0.0f),
                    new Quaternionf(),
                    new Vector3f(1.18f, 1.18f, 1.18f),
                    new Quaternionf()
            ));
        }

        if (nameDisplay != null) {
            nameDisplay.text(formatRewardTitle(winningReward));
        }
        if (subtitleDisplay != null) {
            subtitleDisplay.text(formatRewardSubtitle(winningReward));
        }

        // Sonidos triunfales
        displayLocation.getWorld().playSound(displayLocation, Sound.BLOCK_AMETHYST_BLOCK_CHIME, 1.0f, 1.2f);
        displayLocation.getWorld().playSound(displayLocation, Sound.BLOCK_NOTE_BLOCK_BELL, 1.0f, 1.4f);

        // Disparo de fuegos artificiales suaves (CrateEffects) - Ejecución ÚNICA en el clímax
        String rarityId = winningReward.getRarity() != null ? winningReward.getRarity().getId() : "default";
        AnimationRunner.playRewardAnimation(effectsPlugin, displayLocation.clone().add(0, 0.4, 0), player, rarityId);
    }

    private Reward getRandomReward() {
        return spinRewards.get(ThreadLocalRandom.current().nextInt(spinRewards.size()));
    }

    /**
     * Resuelve el ítem a mostrar: si el preview es una cabeza genérica, busca el primer ítem real de la recompensa.
     */
    private ItemStack resolveDisplayItem(Reward reward) {
        if (reward == null) return null;
        ItemStack preview = reward.getPreviewItem();

        // Si preview es cabeza/bloque genérico sin nombre y es un ItemReward, extraer el ítem real de contenido
        if (reward instanceof ItemReward itemReward) {
            boolean previewHasName = (preview != null && preview.hasItemMeta() &&
                    (preview.getItemMeta().hasDisplayName() || preview.getItemMeta().hasItemName()));
            if (!previewHasName) {
                List<AdaptedItem> items = itemReward.getItems();
                if (items != null && !items.isEmpty()) {
                    ItemStack realItem = ItemHelper.toItemStack(items.get(0));
                    if (realItem != null) {
                        return realItem;
                    }
                }
            }
        }

        return preview;
    }

    /**
     * Línea 1: Únicamente el nombre del ítem en sus colores nativos, sin prefijos ni background.
     */
    private Component formatRewardTitle(Reward reward) {
        if (reward == null) return Component.empty();

        Component nameComp = null;

        // 1. Intentar obtener el Component nativo desde el ítem a mostrar (1.21 Adventure NBT)
        ItemStack item = resolveDisplayItem(reward);
        if (item != null && item.hasItemMeta()) {
            if (item.getItemMeta().hasDisplayName()) {
                try {
                    nameComp = item.getItemMeta().displayName();
                } catch (Throwable ignored) {}
            } else if (item.getItemMeta().hasItemName()) {
                try {
                    nameComp = item.getItemMeta().itemName();
                } catch (Throwable ignored) {}
            }
        }

        // 2. Si no hay Component en el ítem, intentar desde el preview
        if (nameComp == null) {
            ItemStack preview = reward.getPreviewItem();
            if (preview != null && preview.hasItemMeta()) {
                if (preview.getItemMeta().hasDisplayName()) {
                    try {
                        nameComp = preview.getItemMeta().displayName();
                    } catch (Throwable ignored) {}
                } else if (preview.getItemMeta().hasItemName()) {
                    try {
                        nameComp = preview.getItemMeta().itemName();
                    } catch (Throwable ignored) {}
                }
            }
        }

        // 3. Si aún no hay Component, parsear mediante el nombre serializado de la recompensa
        if (nameComp == null) {
            String rawName = reward.getName();
            if (rawName == null || rawName.isBlank()) {
                rawName = reward.getId();
            }
            nameComp = parseFormattedText(rawName);
        }

        return nameComp;
    }

    /**
     * Línea 2: Únicamente la Probabilidad del objeto.
     * Ejemplo: &7Probabilidad: &e1%
     */
    private Component formatRewardSubtitle(Reward reward) {
        if (reward == null) return Component.empty();

        double chance = reward.getRollChance();
        String probStr;
        if (chance <= 0.0) {
            probStr = "<1%";
        } else if (chance < 0.1) {
            probStr = String.format(Locale.US, "%.2f%%", chance);
        } else if (Math.abs(chance - Math.round(chance)) < 0.01) {
            probStr = String.format(Locale.US, "%.0f%%", chance);
        } else {
            probStr = String.format(Locale.US, "%.1f%%", chance);
        }

        String fullSubtitle = "&7Probabilidad: &e" + probStr;
        return parseFormattedText(fullSubtitle);
    }

    /**
     * Deserializador robusto en 2 capas:
     * 1. MiniMessage moderno con conversión unificada de códigos legacy (& y §)
     * 2. Fallback regex hex con stripping de tags para garantizar cero tags residuales
     */
    public static Component parseFormattedText(String input) {
        if (input == null || input.isBlank()) return Component.empty();

        // Limpiar saltos de línea con sangrías excesivas producidas por YAML multi-line
        String cleanInput = input.replaceAll("\\r?\\n\\s+", " ");

        // 1. Intentar parseo MiniMessage con conversión unificada de códigos legacy
        try {
            String converted = toMiniMessageFormat(cleanInput);
            return MiniMessage.miniMessage().deserialize(converted);
        } catch (Throwable ignored) {}

        // 2. Fallback Infalible: Regex Hex Converter + Legacy Deserializer (Cero tags visibles garantizado)
        try {
            return parseFallbackLegacy(cleanInput);
        } catch (Throwable ignored) {}

        return Component.text(cleanInput);
    }

    /**
     * Convierte códigos de color y formato legacy (& y §) a etiquetas estándar de MiniMessage.
     */
    private static String toMiniMessageFormat(String text) {
        if (text == null) return "";
        String s = text.replace('§', '&');
        return s.replace("&0", "<black>")
                .replace("&1", "<dark_blue>")
                .replace("&2", "<dark_green>")
                .replace("&3", "<dark_aqua>")
                .replace("&4", "<dark_red>")
                .replace("&5", "<dark_purple>")
                .replace("&6", "<gold>")
                .replace("&7", "<gray>")
                .replace("&8", "<dark_gray>")
                .replace("&9", "<blue>")
                .replace("&a", "<green>")
                .replace("&b", "<aqua>")
                .replace("&c", "<red>")
                .replace("&d", "<light_purple>")
                .replace("&e", "<yellow>")
                .replace("&f", "<white>")
                .replace("&k", "<obfuscated>")
                .replace("&l", "<bold>")
                .replace("&m", "<strikethrough>")
                .replace("&n", "<underlined>")
                .replace("&o", "<italic>")
                .replace("&r", "<reset>");
    }

    /**
     * Convierte <#RRGGBB> a formato hex nativo de Minecraft (§x§R§R§G§G§B§B) y elimina cualquier tag de cierre o residual.
     */
    private static Component parseFallbackLegacy(String input) {
        // Eliminar tags de cierre </...>
        String withoutClosing = input.replaceAll("</[^>]+>", "");

        // Convertir tags <#RRGGBB> a §x§R§R§G§G§B§B
        Pattern hexTagPattern = Pattern.compile("<#([A-Fa-f0-9]{6})>");
        Matcher matcher = hexTagPattern.matcher(withoutClosing);
        StringBuilder sb = new StringBuilder();
        while (matcher.find()) {
            String hex = matcher.group(1);
            StringBuilder repl = new StringBuilder("§x");
            for (char c : hex.toCharArray()) {
                repl.append('§').append(c);
            }
            matcher.appendReplacement(sb, repl.toString());
        }
        matcher.appendTail(sb);

        // Convertir códigos simples & a § y limpiar tags residuales
        String stripped = sb.toString().replaceAll("<[^>]+>", "").replace('&', '§');
        return LegacyComponentSerializer.legacySection().deserialize(stripped);
    }

    private void setFakeBlock(Material mat) {
        if (crateBlock == null || crateBlock.getWorld() == null) return;
        try {
            Location loc = crateBlock.getLocation();
            BlockData data = mat.createBlockData();
            if (player != null && player.isOnline()) {
                player.sendBlockChange(loc, data);
            }
            for (Player p : loc.getWorld().getPlayers()) {
                if (p != player && p.getLocation().distanceSquared(loc) < 2304.0) { // 48 bloques
                    p.sendBlockChange(loc, data);
                }
            }
        } catch (Throwable ignored) {}
    }

    private void restoreRealBlock() {
        if (crateBlock == null || crateBlock.getWorld() == null) return;
        try {
            Location loc = crateBlock.getLocation();
            BlockData data = (originalBlockData != null) ? originalBlockData : crateBlock.getBlockData();
            if (player != null && player.isOnline()) {
                player.sendBlockChange(loc, data);
            }
            for (Player p : loc.getWorld().getPlayers()) {
                if (p != player && p.getLocation().distanceSquared(loc) < 2304.0) {
                    p.sendBlockChange(loc, data);
                }
            }
        } catch (Throwable ignored) {}
    }

    /**
     * Resuelve el material del Shulker Box basándose prioritariamente en el Crate Item configurado en la Crate.
     */
    private Material resolveShulkerMaterial(Reward reward) {
        // 1. Prioridad Absoluta: El ítem configurado en la Crate (Crate Item / ItemProvider)
        try {
            ItemStack crateItem = this.crate.getRawItemStack();
            if (crateItem != null && crateItem.getType().name().endsWith("SHULKER_BOX")) {
                return crateItem.getType();
            }
            ItemStack crateItem2 = this.crate.getItemStack();
            if (crateItem2 != null && crateItem2.getType().name().endsWith("SHULKER_BOX")) {
                return crateItem2.getType();
            }
        } catch (Throwable ignored) {}

        // 2. Si el bloque físico asignado en el mundo es un shulker box, usarlo
        if (crateBlock != null && crateBlock.getType().name().endsWith("SHULKER_BOX")) {
            return crateBlock.getType();
        }

        // 3. Fallback por rareza o ID de crate
        String id = (reward != null && reward.getRarity() != null) ? reward.getRarity().getId() : this.crate.getId();
        if (id == null) return Material.RED_SHULKER_BOX;
        return switch (id.toLowerCase(Locale.ROOT)) {
            case "mitica" -> Material.RED_SHULKER_BOX;
            case "epica" -> Material.MAGENTA_SHULKER_BOX;
            case "rara" -> Material.LIGHT_BLUE_SHULKER_BOX;
            case "comun" -> Material.LIME_SHULKER_BOX;
            default -> Material.RED_SHULKER_BOX;
        };
    }

    private Color resolveGlowColor(String rarityId) {
        if (rarityId == null) return Color.YELLOW;
        return switch (rarityId.toLowerCase(Locale.ROOT)) {
            case "mitica" -> Color.fromRGB(163, 53, 238);
            case "epica" -> Color.fromRGB(155, 48, 255);
            case "rara" -> Color.fromRGB(0, 191, 255);
            case "comun" -> Color.fromRGB(50, 205, 50);
            default -> Color.fromRGB(255, 215, 0);
        };
    }

    @Override
    protected void onComplete() {
        // Completado
    }

    @Override
    protected void onStop() {
        // Entrega oficial de la recompensa
        this.addReward(this.winningReward);

        // Despawn de display entities
        if (bottomBase != null) {
            bottomBase.remove();
            bottomBase = null;
        }
        if (topLid != null) {
            topLid.remove();
            topLid = null;
        }
        if (rewardDisplay != null) {
            rewardDisplay.remove();
            rewardDisplay = null;
        }
        if (leftDisplay != null) {
            leftDisplay.remove();
            leftDisplay = null;
        }
        if (rightDisplay != null) {
            rightDisplay.remove();
            rightDisplay = null;
        }
        if (nameDisplay != null) {
            nameDisplay.remove();
            nameDisplay = null;
        }
        if (subtitleDisplay != null) {
            subtitleDisplay.remove();
            subtitleDisplay = null;
        }

        // Restaurar el bloque físico y holograma oficial
        if (crateBlock != null) {
            restoreRealBlock();
            this.showHologram(WorldPos.from(crateBlock));
            crateBlock = null;
        }

        super.onStop();
    }
}
