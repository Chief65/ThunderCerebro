package com.thundermc.ranks.gui;

import com.thundermc.ranks.ThunderRanks;
import com.thundermc.ranks.model.PlayerData;
import com.thundermc.ranks.model.Rank;
import com.thundermc.ranks.model.RankTier;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Color;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemFlag;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.inventory.meta.LeatherArmorMeta;

import java.util.ArrayList;
import java.util.List;

public class RankConfirmGui {

    public static final String CONFIRM_TITLE = ChatColor.translateAlternateColorCodes('&', "&0&l| &0Dash &0▶ &8Confirmar Ascenso");

    public static void open(Player player, ThunderRanks plugin) {
        Inventory inv = Bukkit.createInventory(null, 27, CONFIRM_TITLE);

        PlayerData pd = plugin.getPlayerDataManager().getPlayerData(player);
        Rank currentRank = plugin.getRankManager().getRank(pd.getCurrentRankId());
        if (currentRank == null) currentRank = plugin.getRankManager().getFirstRank();

        RankTier currentTier = currentRank.getTier(pd.getCurrentTier());

        String targetName;
        double cost;
        Color armorColor;

        if (pd.getCurrentTier() < 5) {
            // Ascensión de sub-etapa
            String nextRoman = switch (pd.getCurrentTier() + 1) {
                case 2 -> "II";
                case 3 -> "III";
                case 4 -> "IV";
                case 5 -> "V";
                default -> "I";
            };
            targetName = currentRank.getDisplayName() + " " + nextRoman;
            cost = currentTier != null ? currentTier.getRankupCost() : 0.0;
            armorColor = getRankColor(currentRank.getId());
        } else {
            // Gran Ascensión
            Rank nextRank = plugin.getRankManager().getNextRank(currentRank.getId());
            if (nextRank == null) {
                player.sendMessage(plugin.getMessage("max-rank"));
                return;
            }
            targetName = nextRank.getDisplayName() + " I";
            cost = currentRank.getMajorRankupCost();
            armorColor = getRankColor(nextRank.getId());
        }

        double balance = plugin.getEconomy() != null ? plugin.getEconomy().getBalance(player) : 0.0;
        boolean hasMoney = balance >= cost;

        // Fondo con cristales oscuros
        ItemStack glass = createItem(Material.BLACK_STAINED_GLASS_PANE, " ", null);
        for (int i = 0; i < 27; i++) {
            if (i != 11 && i != 13 && i != 15) {
                inv.setItem(i, glass);
            }
        }

        // Slot 11: LIME_WOOL (Confirmar)
        List<String> confirmLore = List.of(
                "",
                "&7Estás a punto de ascender a:",
                "&e" + targetName,
                "",
                "&7Coste de la ascensión: &e$" + String.format("%,.0f", cost),
                "&7Tu saldo disponible: " + (hasMoney ? "&a" : "&c") + "$" + String.format("%,.0f", balance),
                "",
                (hasMoney ? "&a&l▶ ¡Haz clic para confirmar el ascenso!" : "&c&l✖ No tienes suficiente dinero.")
        );
        inv.setItem(11, createItem(Material.LIME_WOOL, "&a&l✔ CONFIRMAR ASCENSO", confirmLore));

        // Slot 13: Casco correspondiente
        ItemStack helmet = createLeatherHelmet(armorColor, targetName, List.of("", "&7Rango o etapa destino."));
        inv.setItem(13, helmet);

        // Slot 15: RED_WOOL (Cancelar)
        List<String> cancelLore = List.of(
                "",
                "&7Cancela la operación y regresa",
                "&7al menú principal de rangos.",
                "",
                "&c&l▶ ¡Haz clic para cancelar!"
        );
        inv.setItem(15, createItem(Material.RED_WOOL, "&c&l✖ CANCELAR", cancelLore));

        player.openInventory(inv);
    }

    public static Color getRankColor(String rankId) {
        return switch (rankId.toLowerCase()) {
            case "user" -> Color.fromRGB(240, 240, 240);    // Blanco
            case "knight" -> Color.fromRGB(0, 183, 255);     // Azul
            case "heroe" -> Color.fromRGB(46, 204, 113);     // Verde
            case "legend" -> Color.fromRGB(241, 196, 15);    // Oro / Amarillo
            case "mythic" -> Color.fromRGB(155, 89, 182);    // Púrpura
            case "titan" -> Color.fromRGB(231, 76, 60);      // Rojo
            case "cosmos" -> Color.fromRGB(255, 20, 147);    // Rosa Cósmico
            default -> Color.fromRGB(200, 200, 200);
        };
    }

    private static ItemStack createLeatherHelmet(Color color, String name, List<String> lore) {
        ItemStack item = new ItemStack(Material.LEATHER_HELMET);
        LeatherArmorMeta meta = (LeatherArmorMeta) item.getItemMeta();
        if (meta != null) {
            meta.setColor(color);
            if (name != null) meta.setDisplayName(ChatColor.translateAlternateColorCodes('&', name));
            if (lore != null) {
                List<String> colored = new ArrayList<>();
                for (String l : lore) colored.add(ChatColor.translateAlternateColorCodes('&', l));
                meta.setLore(colored);
            }
            meta.addItemFlags(ItemFlag.HIDE_ATTRIBUTES, ItemFlag.HIDE_DYE);
            item.setItemMeta(meta);
        }
        return item;
    }

    private static ItemStack createItem(Material mat, String name, List<String> lore) {
        ItemStack item = new ItemStack(mat != null ? mat : Material.STONE);
        ItemMeta meta = item.getItemMeta();
        if (meta != null) {
            if (name != null) meta.setDisplayName(ChatColor.translateAlternateColorCodes('&', name));
            if (lore != null) {
                List<String> colored = new ArrayList<>();
                for (String l : lore) colored.add(ChatColor.translateAlternateColorCodes('&', l));
                meta.setLore(colored);
            }
            meta.addItemFlags(ItemFlag.HIDE_ATTRIBUTES);
            item.setItemMeta(meta);
        }
        return item;
    }
}
