package com.thundermc.ranks.gui;

import com.thundermc.ranks.ThunderRanks;
import com.thundermc.ranks.model.PlayerData;
import com.thundermc.ranks.model.Rank;
import com.thundermc.ranks.model.RankMilestone;
import com.thundermc.ranks.model.RankTier;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Color;
import org.bukkit.Material;
import org.bukkit.Sound;
import org.bukkit.enchantments.Enchantment;
import org.bukkit.entity.Player;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemFlag;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.inventory.meta.LeatherArmorMeta;

import java.util.ArrayList;
import java.util.List;

public class RankGui {

    public static final String GUI_TITLE = ChatColor.translateAlternateColorCodes('&', "&0&l| &0Dash &0▶ &8Rangos y Ascensos");

    public static void open(Player player, ThunderRanks plugin) {
        PlayerData pd = plugin.getPlayerDataManager().getPlayerData(player);
        Rank currentRank = plugin.getRankManager().getRank(pd.getCurrentRankId());
        if (currentRank == null) currentRank = plugin.getRankManager().getFirstRank();

        RankTier currentTier = currentRank.getTier(pd.getCurrentTier());
        if (currentTier == null) currentTier = currentRank.getTier(1);

        Inventory inv = Bukkit.createInventory(null, 54, GUI_TITLE);

        // 1. Navbar inferior (Fila 6: slots 45 al 53)
        ItemStack navGlass = createItem(Material.BLACK_STAINED_GLASS_PANE, " ", null);
        for (int i = 45; i <= 53; i++) {
            inv.setItem(i, navGlass);
        }

        // Slot 45: Brújula a la esquina izquierda con info de progreso
        int currentXp = pd.getCurrentXp();
        int maxTierXp = (currentTier != null) ? currentTier.getMaxXp() : 1000;
        List<String> compassLore = List.of(
                "",
                "&7Rango actual: " + currentRank.getDisplayName() + " " + (currentTier != null ? currentTier.getRomanNumeral() : "I"),
                "&7Progreso acumulado: &e" + currentXp + " &7/ &f" + maxTierXp + " XP",
                getProgressBar(currentXp, maxTierXp),
                "",
                "&7Gana XP farmeando cultivos custom,",
                "&7minando o derrotando mobs para avanzar."
        );
        inv.setItem(45, createItem(Material.COMPASS, "&e&lProgreso de Etapa", compassLore));

        // Slot 49: Puerta de roble oscuro para cerrar
        List<String> doorLore = List.of(
                "",
                "&7Haz clic para cerrar este menú.",
                "",
                "&c&l▶ Cerrar"
        );
        inv.setItem(49, createItem(Material.DARK_OAK_DOOR, "&c&lCerrar Menú", doorLore));

        // Slot 53: Botón de ascensión (si está listo)
        boolean allMilestonesDone = (currentXp >= maxTierXp);
        if (allMilestonesDone) {
            if (pd.getCurrentTier() < 5) {
                String nextRoman = switch (pd.getCurrentTier() + 1) {
                    case 2 -> "II";
                    case 3 -> "III";
                    case 4 -> "IV";
                    case 5 -> "V";
                    default -> "";
                };
                double cost = (currentTier != null) ? currentTier.getRankupCost() : 0.0;
                List<String> btnLore = List.of(
                        "",
                        "&a¡Has completado los 5 hitos de esta etapa!",
                        "&7Siguiente sub-etapa: " + currentRank.getDisplayName() + " " + nextRoman,
                        "&7Coste: &e$" + String.format("%,.0f", cost),
                        "",
                        "&a&l▶ ¡Haz clic para ascender!"
                );
                ItemStack btn = createItem(Material.GOLD_BLOCK, "&6&l⚡ ¡ASCENDER A " + nextRoman + "! ⚡", btnLore);
                addGlow(btn);
                inv.setItem(53, btn);
            } else {
                Rank nextRank = plugin.getRankManager().getNextRank(currentRank.getId());
                if (nextRank != null) {
                    double majorCost = currentRank.getMajorRankupCost();
                    List<String> btnLore = List.of(
                            "",
                            "&6&l★ ¡ETAPA V CONQUISTADA! ★",
                            "&7Siguiente Rango Mayor: " + nextRank.getDisplayName() + " I",
                            "&7Coste: &e$" + String.format("%,.0f", majorCost),
                            "",
                            "&a&l▶ ¡Haz clic para la Gran Ascensión!"
                    );
                    ItemStack btn = createItem(Material.NETHER_STAR, "&d&l❖ ¡GRAN ASCENSIÓN! ❖", btnLore);
                    addGlow(btn);
                    inv.setItem(53, btn);
                }
            }
        }

        // Determinar si aplica animación de apertura (1 vez cada 6 horas)
        boolean animate = pd.shouldTriggerAnimation();

        if (!animate) {
            // Renderizado instantáneo
            renderRanksRow(inv, plugin, currentRank, currentTier);
            renderTiersRow(inv, currentRank, pd);
            renderMilestonesRow(inv, currentTier, pd);
            player.openInventory(inv);
        } else {
            // Renderizado con animación escalonada (sin lag, 3 ticks espaciados)
            player.openInventory(inv);
            player.playSound(player.getLocation(), Sound.BLOCK_NOTE_BLOCK_CHIME, 0.7f, 1.0f);

            Rank fRank = currentRank;
            RankTier fTier = currentTier;

            Bukkit.getScheduler().runTaskLater(plugin, () -> {
                if (player.getOpenInventory().getTitle().equals(GUI_TITLE)) {
                    renderRanksRow(inv, plugin, fRank, fTier);
                    player.playSound(player.getLocation(), Sound.BLOCK_NOTE_BLOCK_BELL, 0.7f, 1.2f);
                }
            }, 1L);

            Bukkit.getScheduler().runTaskLater(plugin, () -> {
                if (player.getOpenInventory().getTitle().equals(GUI_TITLE)) {
                    renderTiersRow(inv, fRank, pd);
                    player.playSound(player.getLocation(), Sound.BLOCK_NOTE_BLOCK_BELL, 0.7f, 1.4f);
                }
            }, 2L);

            Bukkit.getScheduler().runTaskLater(plugin, () -> {
                if (player.getOpenInventory().getTitle().equals(GUI_TITLE)) {
                    renderMilestonesRow(inv, fTier, pd);
                    player.playSound(player.getLocation(), Sound.ENTITY_EXPERIENCE_ORB_PICKUP, 0.7f, 1.5f);
                }
            }, 3L);
        }
    }

    private static void renderRanksRow(Inventory inv, ThunderRanks plugin, Rank currentRank, RankTier currentTier) {
        // Fila 1 (Top del menú): Slots 1 al 7
        List<Rank> allRanks = new ArrayList<>(plugin.getRankManager().getRanks());
        int[] topSlots = {1, 2, 3, 4, 5, 6, 7};
        int currentRankIndex = -1;

        for (int i = 0; i < allRanks.size(); i++) {
            if (allRanks.get(i).getId().equalsIgnoreCase(currentRank.getId())) {
                currentRankIndex = i;
                break;
            }
        }

        for (int i = 0; i < allRanks.size() && i < topSlots.length; i++) {
            Rank r = allRanks.get(i);
            int slot = topSlots[i];

            boolean isCurrent = (i == currentRankIndex);
            boolean isPassed = (i < currentRankIndex);

            List<String> lore = new ArrayList<>();
            lore.add("");
            if (isCurrent) {
                lore.add("&a&l▶ RANGO MAYOR ACTUAL ◀");
                lore.add("&7Sub-etapa activa: &e" + r.getDisplayName() + " " + (currentTier != null ? currentTier.getRomanNumeral() : "I"));
            } else if (isPassed) {
                lore.add("&2✔ RANGO SUPERADO");
                lore.add("&7Ya dominaste todas sus etapas.");
            } else {
                lore.add("&7🔒 RANGO BLOQUEADO");
                lore.add("&7Completa los rangos previos.");
            }
            lore.add("");
            if (!r.getNextRankId().isEmpty()) {
                lore.add("&7Coste Gran Ascensión: &a$" + String.format("%,.0f", r.getMajorRankupCost()));
            } else {
                lore.add("&d★ Cúspide Definitiva");
            }

            Color helmetColor = RankConfirmGui.getRankColor(r.getId());
            ItemStack helmetItem = createLeatherHelmet(helmetColor, r.getDisplayName(), lore);
            if (isCurrent) addGlow(helmetItem);
            inv.setItem(slot, helmetItem);
        }
    }

    private static void renderTiersRow(Inventory inv, Rank currentRank, PlayerData pd) {
        // Fila 3: Las 5 Sub-etapas (Slots 20 al 24)
        int[] tierSlots = {20, 21, 22, 23, 24};
        int playerTierNum = pd.getCurrentTier();

        for (int i = 1; i <= 5; i++) {
            int slot = tierSlots[i - 1];
            RankTier t = currentRank.getTier(i);
            if (t == null) continue;

            boolean isTierPassed = (i < playerTierNum);
            boolean isTierCurrent = (i == playerTierNum);

            Material mat;
            String title;
            List<String> lore = new ArrayList<>();
            lore.add("");

            if (isTierPassed) {
                mat = Material.LIME_DYE;
                title = "&a&l" + currentRank.getDisplayName() + " " + t.getRomanNumeral() + " &2✔";
                lore.add("&7Estado: &a&lSUB-ETAPA DOMINADA");
                lore.add("&7Los 5 hitos fueron reclamados.");
            } else if (isTierCurrent) {
                // LIGHT_GRAY_DYE brillante para la etapa actual
                mat = Material.LIGHT_GRAY_DYE;
                title = "&e&l" + currentRank.getDisplayName() + " " + t.getRomanNumeral() + " &6★ ACTUAL";
                lore.add("&7Estado: &e&lEN PROGRESO ACTIVO");
                lore.add("&7XP necesaria en esta etapa: &f" + t.getMaxXp() + " XP");
                lore.add("&7Coste de ascensión: &a$" + String.format("%,.0f", t.getRankupCost()));
            } else {
                mat = Material.GRAY_DYE;
                title = "&7&l" + currentRank.getDisplayName() + " " + t.getRomanNumeral() + " &8🔒";
                lore.add("&7Estado: &8Bloqueada");
                lore.add("&7Supera la sub-etapa anterior.");
            }

            ItemStack tierItem = createItem(mat, title, lore);
            if (isTierCurrent) addGlow(tierItem);
            inv.setItem(slot, tierItem);
        }
    }

    private static void renderMilestonesRow(Inventory inv, RankTier currentTier, PlayerData pd) {
        // Fila 4: Los 5 Hitos de recompensa (Slots 29 al 33)
        if (currentTier == null) return;

        int[] milestoneSlots = {29, 30, 31, 32, 33};
        int currentXp = pd.getCurrentXp();

        for (int i = 0; i < currentTier.getMilestones().size() && i < 5; i++) {
            RankMilestone m = currentTier.getMilestones().get(i);
            int slot = milestoneSlots[i];

            boolean completed = pd.isMilestoneCompleted(m.getNumber()) || currentXp >= m.getXpRequired();
            boolean inProgress = !completed && (i == 0 || pd.isMilestoneCompleted(i) || currentXp >= currentTier.getMilestones().get(i - 1).getXpRequired());

            Material mMat;
            String mTitle;
            List<String> mLore = new ArrayList<>();
            mLore.add("");

            if (completed) {
                mMat = Material.LIME_STAINED_GLASS_PANE;
                mTitle = "&a&lRecompensa " + m.getNumber() + "/5 &2✔";
                mLore.add("&7Requisito: &a" + m.getXpRequired() + " XP");
                mLore.add("&7Estado: &a&l¡RECLAMADA!");
                mLore.add("&7Premio: &e" + m.getDisplayReward());
            } else if (inProgress) {
                mMat = Material.YELLOW_STAINED_GLASS_PANE;
                mTitle = "&e&lRecompensa " + m.getNumber() + "/5 &6⚡";
                mLore.add("&7Progreso: &e" + currentXp + " &7/ &f" + m.getXpRequired() + " XP");
                mLore.add(getProgressBar(currentXp, m.getXpRequired()));
                mLore.add("&7Estado: &e&lEN PROGRESO");
                mLore.add("&7Premio: &e" + m.getDisplayReward());
            } else {
                mMat = Material.GRAY_STAINED_GLASS_PANE;
                mTitle = "&7&lRecompensa " + m.getNumber() + "/5 &8🔒";
                mLore.add("&7Requisito: &f" + m.getXpRequired() + " XP");
                mLore.add("&7Estado: &8Bloqueada");
                mLore.add("&7Premio: &7" + m.getDisplayReward());
            }

            ItemStack mItem = createItem(mMat, mTitle, mLore);
            if (completed || inProgress) addGlow(mItem);
            inv.setItem(slot, mItem);
        }
    }

    private static String getProgressBar(int current, int max) {
        int totalUnits = 20;
        float percent = max > 0 ? Math.min(1.0f, Math.max(0.0f, (float) current / (float) max)) : 0.0f;
        int filled = (int) (totalUnits * percent);
        int empty = totalUnits - filled;

        StringBuilder sb = new StringBuilder();
        if (filled > 0) {
            sb.append("&a&m").append(" ".repeat(filled));
        }
        if (empty > 0) {
            sb.append("&7&m").append(" ".repeat(empty));
        }
        sb.append("&r &e").append((int) (percent * 100)).append("%");

        return ChatColor.translateAlternateColorCodes('&', sb.toString());
    }

    public static ItemStack createLeatherHelmet(Color color, String name, List<String> lore) {
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

    public static ItemStack createItem(Material mat, String name, List<String> lore) {
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

    public static void addGlow(ItemStack item) {
        ItemMeta meta = item.getItemMeta();
        if (meta != null) {
            meta.addEnchant(Enchantment.UNBREAKING, 1, true);
            meta.addItemFlags(ItemFlag.HIDE_ENCHANTS);
            item.setItemMeta(meta);
        }
    }
}
