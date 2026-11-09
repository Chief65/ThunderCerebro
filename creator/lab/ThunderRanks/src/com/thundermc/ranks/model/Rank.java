package com.thundermc.ranks.model;

import org.bukkit.Material;
import org.bukkit.boss.BarColor;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class Rank {
    private final String id;
    private final String displayName;
    private final BarColor barColor;
    private final Material icon;
    private final String nextRankId;
    private final double majorRankupCost;
    private final List<String> rankupCommands;
    private final Map<Integer, RankTier> tiers = new LinkedHashMap<>();

    public Rank(String id, String displayName, BarColor barColor, Material icon,
                String nextRankId, double majorRankupCost, List<String> rankupCommands, List<RankTier> tierList) {
        this.id = id;
        this.displayName = displayName;
        this.barColor = barColor != null ? barColor : BarColor.BLUE;
        this.icon = icon != null ? icon : Material.IRON_HELMET;
        this.nextRankId = nextRankId != null ? nextRankId : "";
        this.majorRankupCost = majorRankupCost;
        this.rankupCommands = rankupCommands != null ? rankupCommands : List.of();

        if (tierList != null) {
            for (RankTier t : tierList) {
                this.tiers.put(t.getTierNumber(), t);
            }
        }
    }

    public String getId() { return id; }
    public String getDisplayName() { return displayName; }
    public BarColor getBarColor() { return barColor; }
    public Material getIcon() { return icon; }
    public String getNextRankId() { return nextRankId; }
    public double getMajorRankupCost() { return majorRankupCost; }
    public List<String> getRankupCommands() { return rankupCommands; }

    public RankTier getTier(int number) {
        RankTier t = tiers.get(number);
        if (t != null) return t;
        if (!tiers.isEmpty()) return tiers.values().iterator().next();
        return new RankTier(1, 0.0, List.of(new RankMilestone(1, 100, 0.0, "", List.of())));
    }

    public Collection<RankTier> getTiers() {
        return Collections.unmodifiableCollection(tiers.values());
    }
}
