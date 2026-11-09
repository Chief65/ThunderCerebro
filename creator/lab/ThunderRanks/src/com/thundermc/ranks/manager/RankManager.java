package com.thundermc.ranks.manager;

import com.thundermc.ranks.ThunderRanks;
import com.thundermc.ranks.model.Rank;
import com.thundermc.ranks.model.RankMilestone;
import com.thundermc.ranks.model.RankTier;
import org.bukkit.Material;
import org.bukkit.boss.BarColor;
import org.bukkit.configuration.ConfigurationSection;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class RankManager {

    private final ThunderRanks plugin;
    private final Map<String, Rank> ranks = new LinkedHashMap<>();

    public RankManager(ThunderRanks plugin) {
        this.plugin = plugin;
    }

    public void loadRanks() {
        ranks.clear();
        ConfigurationSection section = plugin.getConfig().getConfigurationSection("ranks");
        if (section == null) return;

        for (String rankId : section.getKeys(false)) {
            ConfigurationSection rSec = section.getConfigurationSection(rankId);
            if (rSec == null) continue;

            String display = rSec.getString("display-name", rankId.toUpperCase());
            String colorStr = rSec.getString("bar-color", "BLUE");
            BarColor barColor;
            try {
                barColor = BarColor.valueOf(colorStr.toUpperCase());
            } catch (Exception e) {
                barColor = BarColor.BLUE;
            }

            String iconStr = rSec.getString("icon", "IRON_HELMET");
            Material icon = Material.getMaterial(iconStr.toUpperCase());
            if (icon == null) icon = Material.IRON_HELMET;

            String nextRank = rSec.getString("next-rank", "");
            double majorCost = rSec.getDouble("major-rankup-cost", 0.0);
            List<String> commands = rSec.getStringList("rankup-commands");

            List<RankTier> tiers = new ArrayList<>();
            ConfigurationSection tSec = rSec.getConfigurationSection("tiers");
            if (tSec != null) {
                for (String tKey : tSec.getKeys(false)) {
                    int tNum = Integer.parseInt(tKey);
                    ConfigurationSection tierSec = tSec.getConfigurationSection(tKey);
                    if (tierSec == null) continue;

                    double tierCost = tierSec.getDouble("cost", 0.0);
                    List<RankMilestone> milestones = new ArrayList<>();

                    ConfigurationSection mSec = tierSec.getConfigurationSection("milestones");
                    if (mSec != null) {
                        for (String mKey : mSec.getKeys(false)) {
                            int mNum = Integer.parseInt(mKey);
                            ConfigurationSection milestoneSec = mSec.getConfigurationSection(mKey);
                            if (milestoneSec == null) continue;

                            int xp = milestoneSec.getInt("xp", mNum * 100);
                            double money = milestoneSec.getDouble("money", 0.0);
                            String reward = milestoneSec.getString("reward", "");
                            List<String> mCmds = milestoneSec.getStringList("commands");

                            milestones.add(new RankMilestone(mNum, xp, money, reward, mCmds));
                        }
                    }

                    tiers.add(new RankTier(tNum, tierCost, milestones));
                }
            }

            Rank rank = new Rank(rankId.toLowerCase(), display, barColor, icon, nextRank.toLowerCase(), majorCost, commands, tiers);
            ranks.put(rankId.toLowerCase(), rank);
        }
    }

    public Rank getRank(String id) {
        if (id == null) return null;
        return ranks.get(id.toLowerCase());
    }

    public Rank getFirstRank() {
        if (ranks.isEmpty()) return null;
        return ranks.values().iterator().next();
    }

    public Rank getNextRank(String id) {
        Rank current = getRank(id);
        if (current == null || current.getNextRankId().isEmpty()) return null;
        return getRank(current.getNextRankId());
    }

    public Collection<Rank> getRanks() {
        return Collections.unmodifiableCollection(ranks.values());
    }
}
