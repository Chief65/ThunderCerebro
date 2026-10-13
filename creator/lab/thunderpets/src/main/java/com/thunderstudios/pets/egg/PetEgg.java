package com.thunderstudios.pets.egg;

import com.thunderstudios.pets.ThunderPetsPlugin;
import com.thunderstudios.pets.pet.PetQuality;
import com.thunderstudios.pets.util.TextUtil;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.inventory.ItemFlag;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.persistence.PersistentDataContainer;
import org.bukkit.persistence.PersistentDataType;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class PetEgg {

    public static NamespacedKey getKeyQuality(ThunderPetsPlugin plugin) {
        return new NamespacedKey(plugin, "egg_quality");
    }

    public static NamespacedKey getKeyFed(ThunderPetsPlugin plugin) {
        return new NamespacedKey(plugin, "egg_fed");
    }

    public static NamespacedKey getKeyKills(ThunderPetsPlugin plugin) {
        return new NamespacedKey(plugin, "egg_kills");
    }

    public static NamespacedKey getKeyReqKills(ThunderPetsPlugin plugin) {
        return new NamespacedKey(plugin, "egg_req_kills");
    }

    public static NamespacedKey getKeyMinutes(ThunderPetsPlugin plugin) {
        return new NamespacedKey(plugin, "egg_minutes");
    }

    public static NamespacedKey getKeyReqMinutes(ThunderPetsPlugin plugin) {
        return new NamespacedKey(plugin, "egg_req_minutes");
    }

    public static NamespacedKey getKeyUuid(ThunderPetsPlugin plugin) {
        return new NamespacedKey(plugin, "egg_uuid");
    }

    public static boolean isEgg(ItemStack item, ThunderPetsPlugin plugin) {
        if (item == null || item.getType() == Material.AIR) return false;
        ItemMeta meta = item.getItemMeta();
        if (meta == null) return false;
        return meta.getPersistentDataContainer().has(getKeyQuality(plugin), PersistentDataType.STRING);
    }

    public static ItemStack createEgg(PetQuality quality, int reqKills, int reqMinutes, ThunderPetsPlugin plugin) {
        Material mat = (quality == PetQuality.LIMITED || quality == PetQuality.DIVINA || quality == PetQuality.MITICA)
                ? Material.DRAGON_EGG : Material.SNIFFER_EGG;

        ItemStack egg = new ItemStack(mat);
        ItemMeta meta = egg.getItemMeta();
        if (meta == null) return egg;

        PersistentDataContainer pdc = meta.getPersistentDataContainer();
        pdc.set(getKeyQuality(plugin), PersistentDataType.STRING, quality.name());
        pdc.set(getKeyFed(plugin), PersistentDataType.BYTE, (byte) 0);
        pdc.set(getKeyKills(plugin), PersistentDataType.INTEGER, 0);
        pdc.set(getKeyReqKills(plugin), PersistentDataType.INTEGER, reqKills);
        pdc.set(getKeyMinutes(plugin), PersistentDataType.INTEGER, 0);
        pdc.set(getKeyReqMinutes(plugin), PersistentDataType.INTEGER, reqMinutes);
        pdc.set(getKeyUuid(plugin), PersistentDataType.STRING, UUID.randomUUID().toString());

        egg.setItemMeta(meta);
        updateEggVisuals(egg, plugin);
        return egg;
    }

    public static PetQuality getQuality(ItemStack item, ThunderPetsPlugin plugin) {
        if (!isEgg(item, plugin)) return PetQuality.SUPER;
        ItemMeta meta = item.getItemMeta();
        String qStr = meta.getPersistentDataContainer().get(getKeyQuality(plugin), PersistentDataType.STRING);
        return PetQuality.fromString(qStr);
    }

    public static boolean isReadyToHatch(ItemStack item, ThunderPetsPlugin plugin) {
        if (!isEgg(item, plugin)) return false;
        ItemMeta meta = item.getItemMeta();
        PersistentDataContainer pdc = meta.getPersistentDataContainer();

        byte fed = pdc.getOrDefault(getKeyFed(plugin), PersistentDataType.BYTE, (byte) 0);
        int kills = pdc.getOrDefault(getKeyKills(plugin), PersistentDataType.INTEGER, 0);
        int reqKills = pdc.getOrDefault(getKeyReqKills(plugin), PersistentDataType.INTEGER, 1);
        int minutes = pdc.getOrDefault(getKeyMinutes(plugin), PersistentDataType.INTEGER, 0);
        int reqMinutes = pdc.getOrDefault(getKeyReqMinutes(plugin), PersistentDataType.INTEGER, 1);

        return fed >= 1 && kills >= reqKills && minutes >= reqMinutes;
    }

    public static boolean feedEgg(ItemStack item, ThunderPetsPlugin plugin) {
        if (!isEgg(item, plugin)) return false;
        ItemMeta meta = item.getItemMeta();
        PersistentDataContainer pdc = meta.getPersistentDataContainer();
        byte fed = pdc.getOrDefault(getKeyFed(plugin), PersistentDataType.BYTE, (byte) 0);
        if (fed >= 1) return false;

        pdc.set(getKeyFed(plugin), PersistentDataType.BYTE, (byte) 1);
        item.setItemMeta(meta);
        updateEggVisuals(item, plugin);
        return true;
    }

    public static boolean addKill(ItemStack item, ThunderPetsPlugin plugin) {
        if (!isEgg(item, plugin)) return false;
        ItemMeta meta = item.getItemMeta();
        PersistentDataContainer pdc = meta.getPersistentDataContainer();

        int kills = pdc.getOrDefault(getKeyKills(plugin), PersistentDataType.INTEGER, 0);
        int reqKills = pdc.getOrDefault(getKeyReqKills(plugin), PersistentDataType.INTEGER, 1);
        if (kills >= reqKills) return false;

        pdc.set(getKeyKills(plugin), PersistentDataType.INTEGER, kills + 1);
        item.setItemMeta(meta);
        updateEggVisuals(item, plugin);
        return (kills + 1 >= reqKills);
    }

    public static boolean addMinute(ItemStack item, ThunderPetsPlugin plugin) {
        if (!isEgg(item, plugin)) return false;
        ItemMeta meta = item.getItemMeta();
        PersistentDataContainer pdc = meta.getPersistentDataContainer();

        int minutes = pdc.getOrDefault(getKeyMinutes(plugin), PersistentDataType.INTEGER, 0);
        int reqMinutes = pdc.getOrDefault(getKeyReqMinutes(plugin), PersistentDataType.INTEGER, 1);
        if (minutes >= reqMinutes) return false;

        pdc.set(getKeyMinutes(plugin), PersistentDataType.INTEGER, minutes + 1);
        item.setItemMeta(meta);
        updateEggVisuals(item, plugin);
        return (minutes + 1 >= reqMinutes);
    }

    public static void accelerate(ItemStack item, ThunderPetsPlugin plugin) {
        if (!isEgg(item, plugin)) return;
        ItemMeta meta = item.getItemMeta();
        PersistentDataContainer pdc = meta.getPersistentDataContainer();

        int reqKills = pdc.getOrDefault(getKeyReqKills(plugin), PersistentDataType.INTEGER, 1);
        int reqMinutes = pdc.getOrDefault(getKeyReqMinutes(plugin), PersistentDataType.INTEGER, 1);

        pdc.set(getKeyFed(plugin), PersistentDataType.BYTE, (byte) 1);
        pdc.set(getKeyKills(plugin), PersistentDataType.INTEGER, reqKills);
        pdc.set(getKeyMinutes(plugin), PersistentDataType.INTEGER, reqMinutes);

        item.setItemMeta(meta);
        updateEggVisuals(item, plugin);
    }

    public static void updateEggVisuals(ItemStack item, ThunderPetsPlugin plugin) {
        if (!isEgg(item, plugin)) return;
        ItemMeta meta = item.getItemMeta();
        if (meta == null) return;

        PersistentDataContainer pdc = meta.getPersistentDataContainer();
        PetQuality quality = getQuality(item, plugin);
        byte fed = pdc.getOrDefault(getKeyFed(plugin), PersistentDataType.BYTE, (byte) 0);
        int kills = pdc.getOrDefault(getKeyKills(plugin), PersistentDataType.INTEGER, 0);
        int reqKills = pdc.getOrDefault(getKeyReqKills(plugin), PersistentDataType.INTEGER, 1);
        int minutes = pdc.getOrDefault(getKeyMinutes(plugin), PersistentDataType.INTEGER, 0);
        int reqMinutes = pdc.getOrDefault(getKeyReqMinutes(plugin), PersistentDataType.INTEGER, 1);

        boolean ready = (fed >= 1 && kills >= reqKills && minutes >= reqMinutes);

        meta.setDisplayName(TextUtil.color(quality.getNameColor() + "Huevo de Mascota &7[" + quality.name() + "]"));

        List<String> lore = new ArrayList<>();
        lore.add(TextUtil.color(quality.getCanonTag()));
        lore.add(TextUtil.color("&7"));
        lore.add(TextUtil.color("&fUn huevo místico que requiere cuidados activos"));
        lore.add(TextUtil.color("&fpara eclosionar y revelar a tu nuevo compañero."));
        lore.add(TextUtil.color("&7"));
        lore.add(TextUtil.color("&e&lTAREAS DE CUIDADO:"));

        // 1. Alimentación
        if (fed >= 1) {
            lore.add(TextUtil.color(" &8▸ &fAlimentación: &a✔ ¡Completada! &8(&7Nutrido&8)"));
        } else {
            lore.add(TextUtil.color(" &8▸ &fAlimentación: &c✘ Pendiente &8(&7Clic der. con Comida&8)"));
        }

        // 2. Kills
        if (kills >= reqKills) {
            lore.add(TextUtil.color(" &8▸ &fProtección: &a✔ ¡Completada! &8(&a" + kills + "&7/&a" + reqKills + "&8)"));
        } else {
            lore.add(TextUtil.color(" &8▸ &fProtección: &e" + kills + "&7/" + reqKills + " &7Mobs hostiles"));
        }

        // 3. Minutos
        if (minutes >= reqMinutes) {
            lore.add(TextUtil.color(" &8▸ &fIncubación: &a✔ ¡Completada! &8(&a" + minutes + "&7/&a" + reqMinutes + "m&8)"));
        } else {
            lore.add(TextUtil.color(" &8▸ &fIncubación: &b" + minutes + "&7/" + reqMinutes + " &7Minutos de juego"));
        }

        lore.add(TextUtil.color("&7"));

        if (ready) {
            lore.add(TextUtil.color("&a&l¡HUEVO LISTO PARA ECLOSIONAR!"));
            lore.add(TextUtil.color("&e▶ Haz Clic Derecho para abrirlo."));
            meta.setEnchantmentGlintOverride(true);
        } else {
            lore.add(TextUtil.color("&e▶ Cumple las tareas para que eclosione."));
            meta.setEnchantmentGlintOverride(false);
        }

        meta.addItemFlags(ItemFlag.HIDE_ATTRIBUTES);
        meta.setLore(lore);
        item.setItemMeta(meta);
    }
}
