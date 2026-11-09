package com.thundermc.ranks.model;

import java.util.List;

public class RankMilestone {
    private final int number;
    private final int xpRequired;
    private final double moneyReward;
    private final String displayReward;
    private final List<String> commands;

    public RankMilestone(int number, int xpRequired, double moneyReward, String displayReward, List<String> commands) {
        this.number = number;
        this.xpRequired = xpRequired;
        this.moneyReward = moneyReward;
        this.displayReward = displayReward != null ? displayReward : "";
        this.commands = commands != null ? commands : List.of();
    }

    public int getNumber() { return number; }
    public int getXpRequired() { return xpRequired; }
    public double getMoneyReward() { return moneyReward; }
    public String getDisplayReward() { return displayReward; }
    public List<String> getCommands() { return commands; }
}
