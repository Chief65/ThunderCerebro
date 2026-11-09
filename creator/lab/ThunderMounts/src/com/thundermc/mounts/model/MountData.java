package com.thundermc.mounts.model;

public class MountData {

    private int remainingStaminaSeconds;
    private long cooldownEndTimestamp;
    private HorseStyle selectedStyle;
    private HorseArmor selectedArmor;

    public MountData(int remainingStaminaSeconds, long cooldownEndTimestamp, HorseStyle selectedStyle, HorseArmor selectedArmor) {
        this.remainingStaminaSeconds = remainingStaminaSeconds;
        this.cooldownEndTimestamp = cooldownEndTimestamp;
        this.selectedStyle = selectedStyle != null ? selectedStyle : HorseStyle.WHITE_PURE;
        this.selectedArmor = selectedArmor != null ? selectedArmor : HorseArmor.DIAMOND;
    }

    public int getRemainingStaminaSeconds() {
        checkCooldownExpired();
        return remainingStaminaSeconds;
    }

    public void setRemainingStaminaSeconds(int remainingStaminaSeconds) {
        this.remainingStaminaSeconds = Math.max(0, remainingStaminaSeconds);
    }

    public long getCooldownEndTimestamp() { return cooldownEndTimestamp; }

    public HorseStyle getSelectedStyle() { return selectedStyle; }
    public void setSelectedStyle(HorseStyle selectedStyle) { this.selectedStyle = selectedStyle; }

    public HorseArmor getSelectedArmor() { return selectedArmor; }
    public void setSelectedArmor(HorseArmor selectedArmor) { this.selectedArmor = selectedArmor; }

    public boolean isInCooldown() {
        checkCooldownExpired();
        return System.currentTimeMillis() < cooldownEndTimestamp;
    }

    public long getRemainingCooldownSeconds() {
        if (!isInCooldown()) return 0;
        return Math.max(0, (cooldownEndTimestamp - System.currentTimeMillis()) / 1000L);
    }

    public void startCooldown(int seconds) {
        this.remainingStaminaSeconds = 0;
        this.cooldownEndTimestamp = System.currentTimeMillis() + (seconds * 1000L);
    }

    public void checkCooldownExpired() {
        if (cooldownEndTimestamp > 0 && System.currentTimeMillis() >= cooldownEndTimestamp) {
            this.cooldownEndTimestamp = 0;
            this.remainingStaminaSeconds = 3600;
        }
    }

    public void consumeStamina(int seconds, int cooldownDuration) {
        this.remainingStaminaSeconds = Math.max(0, this.remainingStaminaSeconds - seconds);
        if (this.remainingStaminaSeconds <= 0) {
            startCooldown(cooldownDuration);
        }
    }

    public void reset() {
        this.remainingStaminaSeconds = 3600;
        this.cooldownEndTimestamp = 0;
    }
}
