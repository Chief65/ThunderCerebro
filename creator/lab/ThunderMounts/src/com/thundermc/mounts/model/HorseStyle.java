package com.thundermc.mounts.model;

import org.bukkit.Material;
import org.bukkit.entity.EntityType;
import org.bukkit.entity.Horse;

public enum HorseStyle {

    // ========================================================
    // FILA 1: COLORES BASE PUROS (Slots 10 a 16)
    // ========================================================
    WHITE_PURE("white_pure", "&f&lCorcel Blanco Imperial", EntityType.HORSE, Horse.Color.WHITE, Horse.Style.NONE, Material.WHITE_WOOL, 10,
        new String[]{"&7Pelaje níveo puro de alta nobleza.", "&eColor: &fBlanco &8| &eMarcas: &7Liso", "", "&e▶ Click para montar"}),

    BLACK_PURE("black_pure", "&8&lAzabache Sombrío", EntityType.HORSE, Horse.Color.BLACK, Horse.Style.NONE, Material.BLACK_WOOL, 11,
        new String[]{"&7Corcel de medianoche veloz y sigiloso.", "&eColor: &8Negro &8| &eMarcas: &7Liso", "", "&e▶ Click para montar"}),

    CHESTNUT_PURE("chestnut_pure", "&6&lAlazán de la Corona", EntityType.HORSE, Horse.Color.CHESTNUT, Horse.Style.NONE, Material.ORANGE_WOOL, 12,
        new String[]{"&7Castaño rojizo de linaje real.", "&eColor: &6Castaño &8| &eMarcas: &7Liso", "", "&e▶ Click para montar"}),

    GRAY_PURE("gray_pure", "&7&lNiebla Plateada", EntityType.HORSE, Horse.Color.GRAY, Horse.Style.NONE, Material.LIGHT_GRAY_WOOL, 13,
        new String[]{"&7Tono grisáceo elegante y resistente.", "&eColor: &7Gris &8| &eMarcas: &7Liso", "", "&e▶ Click para montar"}),

    CREAMY_PURE("creamy_pure", "&e&lPalomino Dorado", EntityType.HORSE, Horse.Color.CREAMY, Horse.Style.NONE, Material.YELLOW_WOOL, 14,
        new String[]{"&7Corcel color crema con reflejos áureos.", "&eColor: &eCremoso &8| &eMarcas: &7Liso", "", "&e▶ Click para montar"}),

    BROWN_PURE("brown_pure", "&6&lPardo Roble", EntityType.HORSE, Horse.Color.BROWN, Horse.Style.NONE, Material.BROWN_WOOL, 15,
        new String[]{"&7Pelaje marrón clásico de gran fortaleza.", "&eColor: &6Marrón &8| &eMarcas: &7Liso", "", "&e▶ Click para montar"}),

    DARK_BROWN_PURE("dark_brown_pure", "&4&lCaoba Crepuscular", EntityType.HORSE, Horse.Color.DARK_BROWN, Horse.Style.NONE, Material.TERRACOTTA, 16,
        new String[]{"&7Tono castaño oscuro de presencia imponente.", "&eColor: &4Marrón Oscuro &8| &eMarcas: &7Liso", "", "&e▶ Click para montar"}),

    // ========================================================
    // FILA 2: PELAJES CON LUCERO Y PINTOS (Slots 19 a 25)
    // ========================================================
    WHITE_SOCKS("white_socks", "&f&lBlanco Lucero", EntityType.HORSE, Horse.Color.WHITE, Horse.Style.WHITE, Material.WHITE_CARPET, 19,
        new String[]{"&7Blanco con calcetines y testuz marcada.", "&eColor: &fBlanco &8| &eMarcas: &fCalcetines", "", "&e▶ Click para montar"}),

    BLACK_SOCKS("black_socks", "&8&lMedianoche Lucero", EntityType.HORSE, Horse.Color.BLACK, Horse.Style.WHITE, Material.BLACK_CARPET, 20,
        new String[]{"&7Negro con patas y marcas frontales blancas.", "&eColor: &8Negro &8| &eMarcas: &fCalcetines", "", "&e▶ Click para montar"}),

    CHESTNUT_PAINT("chestnut_paint", "&6&lAlazán Pinto", EntityType.HORSE, Horse.Color.CHESTNUT, Horse.Style.WHITEFIELD, Material.ORANGE_CARPET, 21,
        new String[]{"&7Castaño con amplios mantos blancos.", "&eColor: &6Castaño &8| &eMarcas: &fParche Blanco", "", "&e▶ Click para montar"}),

    BROWN_PAINT("brown_paint", "&6&lOvero Boscoso", EntityType.HORSE, Horse.Color.BROWN, Horse.Style.WHITEFIELD, Material.BROWN_CARPET, 22,
        new String[]{"&7Marrón manchado tipo pinto salvaje.", "&eColor: &6Marrón &8| &eMarcas: &fParche Blanco", "", "&e▶ Click para montar"}),

    CREAMY_SOCKS("creamy_socks", "&e&lPalomino Lucero", EntityType.HORSE, Horse.Color.CREAMY, Horse.Style.WHITE, Material.YELLOW_CARPET, 23,
        new String[]{"&7Cremoso con pezuñas níveas.", "&eColor: &eCremoso &8| &eMarcas: &fCalcetines", "", "&e▶ Click para montar"}),

    GRAY_PAINT("gray_paint", "&7&lTormenta Pintada", EntityType.HORSE, Horse.Color.GRAY, Horse.Style.WHITEFIELD, Material.LIGHT_GRAY_CARPET, 24,
        new String[]{"&7Gris con grandes mantos claros.", "&eColor: &7Gris &8| &eMarcas: &fParche Blanco", "", "&e▶ Click para montar"}),

    DARK_BROWN_PAINT("dark_brown_paint", "&4&lCaoba Salpicado", EntityType.HORSE, Horse.Color.DARK_BROWN, Horse.Style.WHITEFIELD, Material.RED_CARPET, 25,
        new String[]{"&7Marrón oscuro con parches asimétricos.", "&eColor: &4Marrón Oscuro &8| &eMarcas: &fParche Blanco", "", "&e▶ Click para montar"}),

    // ========================================================
    // FILA 3: PELAJES MOTEADOS Y APALOOSA (Slots 28 a 34)
    // ========================================================
    WHITE_APPALOOSA_SNOW("white_appaloosa_snow", "&f&lApaloosa Nevado", EntityType.HORSE, Horse.Color.WHITE, Horse.Style.WHITE_DOTS, Material.SNOWBALL, 28,
        new String[]{"&7Manto con copos blancos como la ventisca.", "&eColor: &fBlanco &8| &eMarcas: &fCopos Blancos", "", "&e▶ Click para montar"}),

    WHITE_APPALOOSA_COAL("white_appaloosa_coal", "&8&lApaloosa Carbón", EntityType.HORSE, Horse.Color.WHITE, Horse.Style.BLACK_DOTS, Material.COAL, 29,
        new String[]{"&7Base blanca con manchas moteadas negras.", "&eColor: &fBlanco &8| &eMarcas: &8Moteado Carbón", "", "&e▶ Click para montar"}),

    BLACK_APPALOOSA_STARS("black_appaloosa_stars", "&5&lÉbano Estrellado", EntityType.HORSE, Horse.Color.BLACK, Horse.Style.WHITE_DOTS, Material.GUNPOWDER, 30,
        new String[]{"&7Pelaje negro con estrellas blancas moteadas.", "&eColor: &8Negro &8| &eMarcas: &fCopos Blancos", "", "&e▶ Click para montar"}),

    GRAY_DAPPLED("gray_dappled", "&7&lTordo Manchado", EntityType.HORSE, Horse.Color.GRAY, Horse.Style.WHITE_DOTS, Material.FLINT, 31,
        new String[]{"&7Gris perla con salpicaduras nevadas.", "&eColor: &7Gris &8| &eMarcas: &fCopos Blancos", "", "&e▶ Click para montar"}),

    CHESTNUT_DAPPLED("chestnut_dappled", "&6&lAlazán Salpicado", EntityType.HORSE, Horse.Color.CHESTNUT, Horse.Style.BLACK_DOTS, Material.COPPER_INGOT, 32,
        new String[]{"&7Castaño con motas oscuras de carbón.", "&eColor: &6Castaño &8| &eMarcas: &8Moteado Carbón", "", "&e▶ Click para montar"}),

    CREAMY_DAPPLED("creamy_dappled", "&e&lMarfil Copos", EntityType.HORSE, Horse.Color.CREAMY, Horse.Style.WHITE_DOTS, Material.GLOWSTONE_DUST, 33,
        new String[]{"&7Palomino dorado con motas brillantes.", "&eColor: &eCremoso &8| &eMarcas: &fCopos Blancos", "", "&e▶ Click para montar"}),

    DARK_BROWN_DAPPLED("dark_brown_dappled", "&4&lNogal Moteado", EntityType.HORSE, Horse.Color.DARK_BROWN, Horse.Style.WHITE_DOTS, Material.COCOA_BEANS, 34,
        new String[]{"&7Madera oscura con salpicaduras claras.", "&eColor: &4Marrón Oscuro &8| &eMarcas: &fCopos Blancos", "", "&e▶ Click para montar"}),

    // ========================================================
    // FILA 4: NO-MUERTOS ESPECIALES (Slots 38 y 40)
    // ========================================================
    SKELETON_HORSE("skeleton_horse", "&f&lCaballo Esquelético &8[&bMítico&8]", EntityType.SKELETON_HORSE, null, null, Material.SKELETON_SKULL, 38,
        new String[]{"&7Corcel espectral forjado por rayos de tormenta.", "&bNo-Muerto &8| &7Inmune al ahogamiento", "", "&e▶ Click para montar"}),

    ZOMBIE_HORSE("zombie_horse", "&2&lCaballo Zombie &8[&aNo-Muerto&8]", EntityType.ZOMBIE_HORSE, null, null, Material.ZOMBIE_HEAD, 40,
        new String[]{"&7Criatura imperecedera de las criptas arcanas.", "&aNo-Muerto &8| &7Resistencia sobrenatural", "", "&e▶ Click para montar"});

    private final String id;
    private final String displayName;
    private final EntityType entityType;
    private final Horse.Color color;
    private final Horse.Style style;
    private final Material icon;
    private final int slot;
    private final String[] lore;

    HorseStyle(String id, String displayName, EntityType entityType, Horse.Color color, Horse.Style style, Material icon, int slot, String[] lore) {
        this.id = id;
        this.displayName = displayName;
        this.entityType = entityType;
        this.color = color;
        this.style = style;
        this.icon = icon;
        this.slot = slot;
        this.lore = lore;
    }

    public String getId() { return id; }
    public String getDisplayName() { return displayName; }
    public EntityType getEntityType() { return entityType; }
    public Horse.Color getColor() { return color; }
    public Horse.Style getStyle() { return style; }
    public Material getIcon() { return icon; }
    public int getSlot() { return slot; }
    public String[] getLore() { return lore; }

    public boolean isUndead() {
        return entityType == EntityType.SKELETON_HORSE || entityType == EntityType.ZOMBIE_HORSE;
    }

    public static HorseStyle fromId(String id) {
        if (id == null) return WHITE_PURE;
        for (HorseStyle style : values()) {
            if (style.id.equalsIgnoreCase(id) || style.name().equalsIgnoreCase(id)) {
                return style;
            }
        }
        return WHITE_PURE;
    }

    public static HorseStyle fromSlot(int slot) {
        for (HorseStyle style : values()) {
            if (style.slot == slot) {
                return style;
            }
        }
        return null;
    }
}
