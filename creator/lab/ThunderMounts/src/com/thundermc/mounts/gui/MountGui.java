package com.thundermc.mounts.gui;

import com.thundermc.mounts.ThunderMounts;
import com.thundermc.mounts.manager.MountManager;
import com.thundermc.mounts.model.ActiveMount;
import com.thundermc.mounts.model.HorseArmor;
import com.thundermc.mounts.model.HorseStyle;
import com.thundermc.mounts.model.MountData;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Material;
import org.bukkit.enchantments.Enchantment;
import org.bukkit.entity.Player;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemFlag;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;

import java.util.ArrayList;
import java.util.List;

public class MountGui {

    public static final String GUI_TITLE = ChatColor.translateAlternateColorCodes('&', "&0&l| &0Dash &0▶ &8Caballos y Estilos");
    public static final int GUI_SIZE = 54;

    public static void open(Player player, ThunderMounts plugin) {
        Inventory inv = Bukkit.createInventory(null, GUI_SIZE, GUI_TITLE);
        MountManager manager = plugin.getMountManager();
        MountData data = manager.getMountData(player);
        ActiveMount active = manager.getActiveMount(player);

        // 1. Añadir los 23 Estilos de Caballo
        for (HorseStyle style : HorseStyle.values()) {
            ItemStack item = new ItemStack(style.getIcon());
            ItemMeta meta = item.getItemMeta();
            if (meta != null) {
                meta.setDisplayName(ChatColor.translateAlternateColorCodes('&', style.getDisplayName()));

                List<String> lore = new ArrayList<>();
                for (String line : style.getLore()) {
                    lore.add(ChatColor.translateAlternateColorCodes('&', line));
                }

                // Si este estilo es el que el jugador tiene actualmente invocado
                if (active != null && active.getStyle() == style) {
                    lore.add("");
                    lore.add(ChatColor.translateAlternateColorCodes('&', "&a&l✔ ACTIVAMENTE MONTADO"));
                    meta.addEnchant(Enchantment.UNBREAKING, 1, true);
                    meta.addItemFlags(ItemFlag.HIDE_ENCHANTS);
                }

                meta.setLore(lore);
                meta.addItemFlags(ItemFlag.HIDE_ATTRIBUTES);
                item.setItemMeta(meta);
            }
            inv.setItem(style.getSlot(), item);
        }

        // 2. Selector de Armadura (Slot 42)
        HorseArmor currentArmor = data.getSelectedArmor();
        ItemStack armorItem = new ItemStack(currentArmor.getIcon());
        ItemMeta armorMeta = armorItem.getItemMeta();
        if (armorMeta != null) {
            armorMeta.setDisplayName(ChatColor.translateAlternateColorCodes('&', "&b&lArmadura Equina: &f" + currentArmor.getDisplayName()));
            List<String> lore = new ArrayList<>();
            lore.add(ChatColor.translateAlternateColorCodes('&', "&7Selecciona la armadura para tus corceles."));
            lore.add("");
            lore.add(ChatColor.translateAlternateColorCodes('&', "&eEquipada: &f" + currentArmor.getDisplayName()));
            lore.add("");
            lore.add(ChatColor.translateAlternateColorCodes('&', "&e▶ Click para ciclar armadura"));
            lore.add(ChatColor.translateAlternateColorCodes('&', "&8(&7Sin Armadura &8▶ &6Cuero &8▶ &fHierro &8▶ &eOro &8▶ &bDiamante&8)"));
            armorMeta.setLore(lore);
            armorMeta.addItemFlags(ItemFlag.HIDE_ATTRIBUTES);
            armorItem.setItemMeta(armorMeta);
        }
        inv.setItem(42, armorItem);

        // 3. Navbar inferior (Fila 5: Slots 45 a 53)
        // Llenar slots intermedios de navbar con paneles grises oscuros
        ItemStack navGlass = new ItemStack(Material.GRAY_STAINED_GLASS_PANE);
        ItemMeta glassMeta = navGlass.getItemMeta();
        if (glassMeta != null) {
            glassMeta.setDisplayName(ChatColor.translateAlternateColorCodes('&', "&7"));
            navGlass.setItemMeta(glassMeta);
        }
        int[] navSlots = {46, 47, 48, 50, 51, 52};
        for (int s : navSlots) {
            inv.setItem(s, navGlass);
        }

        // Slot 45: Brujula (Estadísticas y Guía)
        ItemStack compass = new ItemStack(Material.COMPASS);
        ItemMeta compMeta = compass.getItemMeta();
        if (compMeta != null) {
            compMeta.setDisplayName(ChatColor.translateAlternateColorCodes('&', "&e&lEstadísticas & Información"));
            List<String> lore = new ArrayList<>();
            lore.add(ChatColor.translateAlternateColorCodes('&', "&7Información sobre tu montura equina:"));
            lore.add("");

            if (data.isInCooldown()) {
                long remaining = data.getRemainingCooldownSeconds();
                lore.add(ChatColor.translateAlternateColorCodes('&', "&cEstado: &eEn descanso &8(" + MountManager.formatTime(remaining) + "&8)"));
            } else {
                int stam = data.getRemainingStaminaSeconds();
                lore.add(ChatColor.translateAlternateColorCodes('&', "&aEstamina: &f" + MountManager.formatTime(stam) + " &7/ 01h 00m"));
                lore.add(ChatColor.translateAlternateColorCodes('&', " " + getStaminaLine(stam, 3600)));
            }

            lore.add("");
            lore.add(ChatColor.translateAlternateColorCodes('&', "&8• &7Al bajarte del corcel se guarda solo."));
            lore.add(ChatColor.translateAlternateColorCodes('&', "&8• &7Ningún otro jugador puede montar tu caballo."));
            lore.add(ChatColor.translateAlternateColorCodes('&', "&8• &7Inmune al daño y caídas."));
            compMeta.setLore(lore);
            compass.setItemMeta(compMeta);
        }
        inv.setItem(45, compass);

        // Slot 49: Acción central (Desmontar o Guía)
        if (active != null) {
            ItemStack barrier = new ItemStack(Material.BARRIER);
            ItemMeta bMeta = barrier.getItemMeta();
            if (bMeta != null) {
                bMeta.setDisplayName(ChatColor.translateAlternateColorCodes('&', "&c&lDesmontar y Guardar"));
                List<String> lore = new ArrayList<>();
                lore.add(ChatColor.translateAlternateColorCodes('&', "&7Tienes un corcel activo en el mundo."));
                lore.add("");
                lore.add(ChatColor.translateAlternateColorCodes('&', "&e▶ Click para guardarlo de inmediato"));
                bMeta.setLore(lore);
                barrier.setItemMeta(bMeta);
            }
            inv.setItem(49, barrier);
        } else {
            ItemStack saddle = new ItemStack(Material.SADDLE);
            ItemMeta sMeta = saddle.getItemMeta();
            if (sMeta != null) {
                sMeta.setDisplayName(ChatColor.translateAlternateColorCodes('&', "&a&lSelecciona un Estilo"));
                List<String> lore = new ArrayList<>();
                lore.add(ChatColor.translateAlternateColorCodes('&', "&7Elige cualquiera de los 23 corceles"));
                lore.add(ChatColor.translateAlternateColorCodes('&', "&7superiores para cabalgar de inmediato."));
                sMeta.setLore(lore);
                saddle.setItemMeta(sMeta);
            }
            inv.setItem(49, saddle);
        }

        // Slot 53: Puerta Dark Oak (Cerrar Menú)
        ItemStack door = new ItemStack(Material.DARK_OAK_DOOR);
        ItemMeta doorMeta = door.getItemMeta();
        if (doorMeta != null) {
            doorMeta.setDisplayName(ChatColor.translateAlternateColorCodes('&', "&c&lCerrar Menú"));
            List<String> lore = new ArrayList<>();
            lore.add(ChatColor.translateAlternateColorCodes('&', "&7Click para volver al juego."));
            doorMeta.setLore(lore);
            door.setItemMeta(doorMeta);
        }
        inv.setItem(53, door);

        player.openInventory(inv);
    }

    public static String getStaminaLine(int current, int max) {
        int totalUnits = 14;
        float percent = max > 0 ? Math.min(1.0f, Math.max(0.0f, (float) current / (float) max)) : 0.0f;
        int filled = (int) (totalUnits * percent);
        int empty = totalUnits - filled;

        StringBuilder sb = new StringBuilder("&8[");
        if (filled > 0) {
            sb.append("&a&m").append(" ".repeat(filled));
        }
        if (empty > 0) {
            sb.append("&7&m").append(" ".repeat(empty));
        }
        sb.append("&8]");
        return sb.toString();
    }
}
