package com.thundermc.ranks.model;

import org.bukkit.boss.BossBar;
import org.bukkit.scheduler.BukkitTask;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

public class PlayerData {
    private final UUID uuid;
    private String currentRankId;
    private int currentTier;
    private int currentXp;
    private final Set<Integer> completedMilestones = new HashSet<>();
    private long lastAnimationTimestamp = 0;

    private transient BossBar bossBar;
    private transient BukkitTask hideTask;

    public PlayerData(UUID uuid, String currentRankId, int currentTier, int currentXp) {
        this.uuid = uuid;
        this.currentRankId = currentRankId != null ? currentRankId.toLowerCase() : "user";
        this.currentTier = Math.max(1, Math.min(5, currentTier));
        this.currentXp = currentXp;
    }

    public UUID getUuid() { return uuid; }

    public String getCurrentRankId() { return currentRankId; }
    public void setCurrentRankId(String currentRankId) {
        this.currentRankId = currentRankId.toLowerCase();
        this.currentTier = 1;
        this.currentXp = 0;
        this.completedMilestones.clear();
    }

    public int getCurrentTier() { return currentTier; }
    public void setCurrentTier(int currentTier) {
        this.currentTier = Math.max(1, Math.min(5, currentTier));
        this.currentXp = 0;
        this.completedMilestones.clear();
    }

    public int getCurrentXp() { return currentXp; }
    public void setCurrentXp(int currentXp) { this.currentXp = currentXp; }
    public void addXp(int amount) { this.currentXp += amount; }

    public Set<Integer> getCompletedMilestones() { return completedMilestones; }
    public boolean isMilestoneCompleted(int milestone) { return completedMilestones.contains(milestone); }
    public void completeMilestone(int milestone) { completedMilestones.add(milestone); }

    public long getLastAnimationTimestamp() { return lastAnimationTimestamp; }
    public void setLastAnimationTimestamp(long lastAnimationTimestamp) { this.lastAnimationTimestamp = lastAnimationTimestamp; }

    public boolean shouldTriggerAnimation() {
        long now = System.currentTimeMillis();
        if (now - lastAnimationTimestamp >= 21600000L) {
            lastAnimationTimestamp = now;
            return true;
        }
        return false;
    }

    public BossBar getBossBar() { return bossBar; }
    public void setBossBar(BossBar bossBar) { this.bossBar = bossBar; }

    public BukkitTask getHideTask() { return hideTask; }
    public void setHideTask(BukkitTask hideTask) {
        if (this.hideTask != null) {
            this.hideTask.cancel();
        }
        this.hideTask = hideTask;
    }

    public void cleanup() {
        if (hideTask != null) {
            hideTask.cancel();
            hideTask = null;
        }
        if (bossBar != null) {
            bossBar.removeAll();
            bossBar = null;
        }
    }
}
