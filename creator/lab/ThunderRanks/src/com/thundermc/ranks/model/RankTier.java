package com.thundermc.ranks.model;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class RankTier {
    private final int tierNumber;
    private final double rankupCost;
    private final List<RankMilestone> milestones;

    public RankTier(int tierNumber, double rankupCost, List<RankMilestone> milestones) {
        this.tierNumber = tierNumber;
        this.rankupCost = rankupCost;
        this.milestones = milestones != null ? new ArrayList<>(milestones) : new ArrayList<>();
    }

    public int getTierNumber() {
        return tierNumber;
    }

    public double getRankupCost() {
        return rankupCost;
    }

    public List<RankMilestone> getMilestones() {
        return Collections.unmodifiableList(milestones);
    }

    public int getMaxXp() {
        if (milestones.isEmpty()) return 500;
        return milestones.get(milestones.size() - 1).getXpRequired();
    }

    public RankMilestone getMilestone(int number) {
        for (RankMilestone rm : milestones) {
            if (rm.getNumber() == number) return rm;
        }
        return null;
    }

    public int getCurrentMilestoneNumber(int currentXp) {
        int mNum = 1;
        for (RankMilestone m : milestones) {
            if (currentXp >= m.getXpRequired()) {
                mNum = Math.min(5, m.getNumber() + 1);
            } else {
                return m.getNumber();
            }
        }
        return 5;
    }

    public String getRomanNumeral() {
        return switch (tierNumber) {
            case 1 -> "I";
            case 2 -> "II";
            case 3 -> "III";
            case 4 -> "IV";
            case 5 -> "V";
            default -> String.valueOf(tierNumber);
        };
    }
}
