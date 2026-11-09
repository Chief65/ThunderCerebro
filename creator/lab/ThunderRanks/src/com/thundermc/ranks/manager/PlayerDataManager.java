package com.thundermc.ranks.manager;

import com.thundermc.ranks.ThunderRanks;
import com.thundermc.ranks.model.PlayerData;
import com.thundermc.ranks.model.Rank;
import com.thundermc.ranks.model.RankMilestone;
import com.thundermc.ranks.model.RankTier;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Color;
import org.bukkit.FireworkEffect;
import org.bukkit.Location;
import org.bukkit.Sound;
import org.bukkit.boss.BarStyle;
import org.bukkit.boss.BossBar;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.entity.Firework;
import org.bukkit.entity.Player;
import org.bukkit.inventory.meta.FireworkMeta;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class PlayerDataManager {

    private final ThunderRanks plugin;
    private final Map<UUID, PlayerData> cache = new HashMap<>();
    private final File dataFile;
    private FileConfiguration dataConfig;

    public PlayerDataManager(ThunderRanks plugin) {
        this.plugin = plugin;
        this.dataFile = new File(plugin.getDataFolder(), "data.yml");
        loadData();
    }

    public void loadData() {
        if (!dataFile.exists()) {
            try {
                dataFile.getParentFile().mkdirs();
                dataFile.createNewFile();
            } catch (IOException ignored) {}
        }
        dataConfig = YamlConfiguration.loadConfiguration(dataFile);
    }

    public void saveData() {
        if (dataConfig == null) return;
        for (PlayerData pd : cache.values()) {
            String path = "players." + pd.getUuid().toString();
            dataConfig.set(path + ".rank", pd.getCurrentRankId());
            dataConfig.set(path + ".tier", pd.getCurrentTier());
            dataConfig.set(path + ".xp", pd.getCurrentXp());
            dataConfig.set(path + ".completed-milestones", pd.getCompletedMilestones().stream().toList());
        }
        try {
            dataConfig.save(dataFile);
        } catch (IOException e) {
            plugin.getLogger().warning("Error guardando data.yml: " + e.getMessage());
        }
    }

    public PlayerData getPlayerData(Player player) {
        return getPlayerData(player.getUniqueId());
    }

    public PlayerData getPlayerData(UUID uuid) {
        if (cache.containsKey(uuid)) {
            return cache.get(uuid);
        }

        String path = "players." + uuid.toString();
        String rankId = dataConfig.getString(path + ".rank", "user");
        int tier = dataConfig.getInt(path + ".tier", 1);
        int xp = dataConfig.getInt(path + ".xp", 0);

        PlayerData pd = new PlayerData(uuid, rankId, tier, xp);
        if (dataConfig.contains(path + ".completed-milestones")) {
            for (int m : dataConfig.getIntegerList(path + ".completed-milestones")) {
                pd.completeMilestone(m);
            }
        }

        cache.put(uuid, pd);
        return pd;
    }

    public void unloadPlayer(Player player) {
        PlayerData pd = cache.get(player.getUniqueId());
        if (pd != null) {
            pd.cleanup();
        }
    }

    public void addXp(Player player, int amount) {
        if (player == null || !player.isOnline() || amount <= 0) return;

        PlayerData pd = getPlayerData(player);
        Rank rank = plugin.getRankManager().getRank(pd.getCurrentRankId());
        if (rank == null) return;

        RankTier tier = rank.getTier(pd.getCurrentTier());
        if (tier == null) return;

        pd.addXp(amount);
        int currentXp = pd.getCurrentXp();
        int maxTierXp = tier.getMaxXp();

        // Actualizar y mostrar BossBar con 5 muescas/hitos
        updateAndShowBossBar(player, pd, rank, tier);

        // Revisar hitos desbloqueados dentro de la sub-etapa
        for (RankMilestone milestone : tier.getMilestones()) {
            if (currentXp >= milestone.getXpRequired() && !pd.isMilestoneCompleted(milestone.getNumber())) {
                pd.completeMilestone(milestone.getNumber());
                triggerMilestoneReward(player, rank, tier, milestone);
            }
        }
    }

    public void updateAndShowBossBar(Player player, PlayerData pd, Rank rank, RankTier tier) {
        int currentXp = pd.getCurrentXp();
        int maxTierXp = Math.max(1, tier.getMaxXp());
        int milestoneNum = tier.getCurrentMilestoneNumber(currentXp);

        double progress = Math.min(1.0, Math.max(0.0, (double) currentXp / (double) maxTierXp));

        String title = ChatColor.translateAlternateColorCodes('&',
                rank.getDisplayName() + " " + tier.getRomanNumeral() + " &8[&eEtapa " + milestoneNum + "/5&8] &f(" + currentXp + "/" + maxTierXp + " XP)");

        BossBar bar = pd.getBossBar();
        if (bar == null) {
            bar = Bukkit.createBossBar(title, rank.getBarColor(), BarStyle.SOLID);
            pd.setBossBar(bar);
        } else {
            bar.setTitle(title);
            bar.setColor(rank.getBarColor());
            bar.setStyle(BarStyle.SOLID);
        }

        bar.setProgress(progress);
        if (!bar.getPlayers().contains(player)) {
            bar.addPlayer(player);
        }
        bar.setVisible(true);

        int hideSeconds = plugin.getConfig().getInt("settings.bossbar-duration-seconds", 6);
        pd.setHideTask(Bukkit.getScheduler().runTaskLater(plugin, () -> {
            if (pd.getBossBar() != null) {
                pd.getBossBar().setVisible(false);
            }
        }, hideSeconds * 20L));
    }

    private void triggerMilestoneReward(Player player, Rank rank, RankTier tier, RankMilestone milestone) {
        player.playSound(player.getLocation(), Sound.ENTITY_PLAYER_LEVELUP, 1.0f, 1.25f);
        player.playSound(player.getLocation(), Sound.BLOCK_NOTE_BLOCK_CHIME, 1.0f, 1.5f);

        String msg = plugin.getMessage("milestone-complete")
                .replace("%milestone%", String.valueOf(milestone.getNumber()))
                .replace("%rank%", rank.getDisplayName())
                .replace("%tier%", tier.getRomanNumeral());
        player.sendMessage(msg);

        if (!milestone.getDisplayReward().isEmpty()) {
            player.sendMessage(ChatColor.GRAY + "Recompensa: " + ChatColor.YELLOW + milestone.getDisplayReward());
        }

        player.sendTitle(
                ChatColor.translateAlternateColorCodes('&', "&a&l¡HITO " + milestone.getNumber() + "/5 COMPLETADO!"),
                ChatColor.translateAlternateColorCodes('&', "&7Recompensa: &e" + milestone.getDisplayReward()),
                10, 40, 10
        );

        if (plugin.getEconomy() != null && milestone.getMoneyReward() > 0) {
            plugin.getEconomy().depositPlayer(player, milestone.getMoneyReward());
        }

        for (String cmd : milestone.getCommands()) {
            String parsed = cmd.replace("%player%", player.getName());
            Bukkit.dispatchCommand(Bukkit.getConsoleSender(), parsed);
        }

        // Si es el hito 5, alertar de la ascensión disponible
        if (milestone.getNumber() == 5) {
            if (tier.getTierNumber() < 5) {
                String nextRoman = switch (tier.getTierNumber() + 1) {
                    case 2 -> "II";
                    case 3 -> "III";
                    case 4 -> "IV";
                    case 5 -> "V";
                    default -> "";
                };
                player.sendMessage(plugin.getMessage("tierup-ready")
                        .replace("%rank%", rank.getDisplayName())
                        .replace("%tier%", tier.getRomanNumeral())
                        .replace("%next_tier%", rank.getDisplayName() + " " + nextRoman));
                player.playSound(player.getLocation(), Sound.UI_TOAST_CHALLENGE_COMPLETE, 1.0f, 1.2f);
            } else {
                // Tier 5 terminado -> Gran Ascensión de Rango
                Rank nextRank = plugin.getRankManager().getNextRank(rank.getId());
                if (nextRank != null) {
                    player.sendMessage(plugin.getMessage("rankup-ready")
                            .replace("%rank%", rank.getDisplayName())
                            .replace("%next_rank%", nextRank.getDisplayName()));
                    player.playSound(player.getLocation(), Sound.UI_TOAST_CHALLENGE_COMPLETE, 1.0f, 1.0f);
                }
            }
        }
    }

    public boolean canRankup(Player player) {
        PlayerData pd = getPlayerData(player);
        Rank currentRank = plugin.getRankManager().getRank(pd.getCurrentRankId());
        if (currentRank == null) return false;

        RankTier currentTier = currentRank.getTier(pd.getCurrentTier());
        if (currentTier == null) return false;

        return pd.getCurrentXp() >= currentTier.getMaxXp();
    }

    public void processRankup(Player player) {
        PlayerData pd = getPlayerData(player);
        Rank currentRank = plugin.getRankManager().getRank(pd.getCurrentRankId());
        if (currentRank == null) return;

        RankTier currentTier = currentRank.getTier(pd.getCurrentTier());
        if (currentTier == null) return;

        if (pd.getCurrentXp() < currentTier.getMaxXp()) {
            player.sendMessage(plugin.getMessage("not-ready-rankup")
                    .replace("%current%", String.valueOf(pd.getCurrentXp()))
                    .replace("%max%", String.valueOf(currentTier.getMaxXp())));
            return;
        }

        // Caso 1: Ascensión de Sub-etapa (ej. Knight I -> Knight II)
        if (currentTier.getTierNumber() < 5) {
            double cost = currentTier.getRankupCost();
            if (plugin.getEconomy() != null && cost > 0) {
                double balance = plugin.getEconomy().getBalance(player);
                if (balance < cost) {
                    player.sendMessage(plugin.getMessage("not-enough-money")
                            .replace("%cost%", String.format("%,.0f", cost))
                            .replace("%balance%", String.format("%,.0f", balance)));
                    player.playSound(player.getLocation(), Sound.ENTITY_VILLAGER_NO, 1.0f, 1.0f);
                    return;
                }
                plugin.getEconomy().withdrawPlayer(player, cost);
            }

            int nextTierNum = currentTier.getTierNumber() + 1;
            pd.setCurrentTier(nextTierNum);

            RankTier nextTier = currentRank.getTier(nextTierNum);
            player.sendMessage(plugin.getMessage("tierup-success")
                    .replace("%rank%", currentRank.getDisplayName())
                    .replace("%tier%", nextTier.getRomanNumeral()));

            player.playSound(player.getLocation(), Sound.UI_TOAST_CHALLENGE_COMPLETE, 1.0f, 1.2f);
            player.sendTitle(
                    ChatColor.translateAlternateColorCodes('&', "&a&l¡ASCENSIÓN LOGRADA!"),
                    ChatColor.translateAlternateColorCodes('&', "&7Has alcanzado " + currentRank.getDisplayName() + " " + nextTier.getRomanNumeral()),
                    10, 50, 15
            );

            updateAndShowBossBar(player, pd, currentRank, nextTier);
            saveData();
            return;
        }

        // Caso 2: Gran Ascensión de Rango Mayor (ej. Knight V -> Heroe I)
        Rank nextRank = plugin.getRankManager().getNextRank(currentRank.getId());
        if (nextRank == null) {
            player.sendMessage(plugin.getMessage("max-rank"));
            return;
        }

        double majorCost = currentRank.getMajorRankupCost();
        if (plugin.getEconomy() != null && majorCost > 0) {
            double balance = plugin.getEconomy().getBalance(player);
            if (balance < majorCost) {
                player.sendMessage(plugin.getMessage("not-enough-money")
                        .replace("%cost%", String.format("%,.0f", majorCost))
                        .replace("%balance%", String.format("%,.0f", balance)));
                player.playSound(player.getLocation(), Sound.ENTITY_VILLAGER_NO, 1.0f, 1.0f);
                return;
            }
            plugin.getEconomy().withdrawPlayer(player, majorCost);
        }

        // Asignar nuevo rango mayor y tier 1
        pd.setCurrentRankId(nextRank.getId());

        for (String cmd : currentRank.getRankupCommands()) {
            String parsed = cmd.replace("%player%", player.getName())
                    .replace("%next_rank%", nextRank.getId())
                    .replace("%rank%", currentRank.getId());
            Bukkit.dispatchCommand(Bukkit.getConsoleSender(), parsed);
        }

        spawnFirework(player.getLocation());
        player.playSound(player.getLocation(), Sound.UI_TOAST_CHALLENGE_COMPLETE, 1.0f, 1.0f);
        player.playSound(player.getLocation(), Sound.ENTITY_ENDER_DRAGON_GROWL, 0.6f, 1.3f);

        player.sendTitle(
                ChatColor.translateAlternateColorCodes('&', "&6&l¡GRAN ASCENSIÓN!"),
                ChatColor.translateAlternateColorCodes('&', "&7Has ascendido a " + nextRank.getDisplayName() + " I"),
                10, 60, 20
        );

        String broadcast = plugin.getMessage("rankup-success")
                .replace("%player%", player.getName())
                .replace("%rank%", nextRank.getDisplayName());
        Bukkit.broadcastMessage(broadcast);

        RankTier initialTier = nextRank.getTier(1);
        updateAndShowBossBar(player, pd, nextRank, initialTier != null ? initialTier : currentTier);
        saveData();
    }

    private void spawnFirework(Location loc) {
        try {
            Firework fw = loc.getWorld().spawn(loc.add(0, 1, 0), Firework.class);
            FireworkMeta meta = fw.getFireworkMeta();
            meta.addEffect(FireworkEffect.builder()
                    .withColor(Color.FUCHSIA, Color.ORANGE, Color.YELLOW, Color.WHITE)
                    .withFade(Color.PURPLE, Color.BLUE)
                    .with(FireworkEffect.Type.BALL_LARGE)
                    .withFlicker()
                    .withTrail()
                    .build());
            meta.setPower(1);
            fw.setFireworkMeta(meta);
        } catch (Throwable ignored) {}
    }
}
