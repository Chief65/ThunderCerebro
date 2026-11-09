package com.thundermc.mounts.model;

import org.bukkit.Material;
import org.bukkit.inventory.ItemStack;

public enum HorseArmor {
    NONE("none", "&7Sin Armadura", Material.SADDLE, null),
    LEATHER("leather", "&6Armadura de Cuero", Material.LEATHER_HORSE_ARMOR, new ItemStack(Material.LEATHER_HORSE_ARMOR)),
    IRON("iron", "&fArmadura de Hierro", Material.IRON_HORSE_ARMOR, new ItemStack(Material.IRON_HORSE_ARMOR)),
    GOLD("gold", "&eArmadura de Oro", Material.GOLDEN_HORSE_ARMOR, new ItemStack(Material.GOLDEN_HORSE_ARMOR)),
    DIAMOND("diamond", "&bArmadura de Diamante", Material.DIAMOND_HORSE_ARMOR, new ItemStack(Material.DIAMOND_HORSE_ARMOR));

    private final String id;
    private final String displayName;
    private final Material icon;
    private final ItemStack itemStack;

    HorseArmor(String id, String displayName, Material icon, ItemStack itemStack) {
        this.id = id;
        this.displayName = displayName;
        this.icon = icon;
        this.itemStack = itemStack;
    }

    public String getId() { return id; }
    public String getDisplayName() { return displayName; }
    public Material getIcon() { return icon; }
    public ItemStack getItemStack() { return itemStack != null ? itemStack.clone() : null; }

    public HorseArmor next() {
        HorseArmor[] values = values();
        return values[(this.ordinal() + 1) % values.length];
    }

    public static HorseArmor fromId(String id) {
        if (id == null) return DIAMOND;
        for (HorseArmor armor : values()) {
            if (armor.id.equalsIgnoreCase(id) || armor.name().equalsIgnoreCase(id)) {
                return armor;
            }
        }
        return DIAMOND;
    }
}
