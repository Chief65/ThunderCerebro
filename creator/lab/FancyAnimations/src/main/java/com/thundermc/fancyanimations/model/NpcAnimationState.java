package com.thundermc.fancyanimations.model;

import org.bukkit.Location;

import java.util.Random;

/**
 * Mantiene el estado cinemático y los acumuladores de tiempo para un NPC en ejecución.
 */
public class NpcAnimationState {

    private final Location baseLocation;
    private long tick = 0;

    // Seguimiento suave custom de cabeza y rotación
    private float currentLookYaw;
    private float currentLookPitch;
    private boolean lookInitialized = false;

    // Micro-rotación suave (mirar a su alrededor de forma natural cuando no hay jugadores cerca)
    private float currentYawOffset = 0.0f;
    private float targetYawOffset = 0.0f;
    private long nextMicroRotationTick = 40;

    // Asentimiento / Cabeceo orgánico
    private boolean isNodding = false;
    private int nodProgress = 0;
    private long nextNodTick = 100;

    // Ladeo de cabeza (fase senoidal independiente)
    private float tiltPhase = 0.0f;

    // Gestos aleatorios
    private long nextGestureTick = 200;

    // Sonidos ambientales
    private long nextAmbientSoundTick = 100;

    private static final Random RANDOM = new Random();

    public NpcAnimationState(Location baseLocation) {
        this.baseLocation = baseLocation.clone();
        this.currentLookYaw = baseLocation.getYaw();
        this.currentLookPitch = baseLocation.getPitch();
        this.lookInitialized = true;

        // Inicializar con fases aleatorias para desincronizar NPCs cercanos
        this.tick = RANDOM.nextInt(200);
        this.tiltPhase = RANDOM.nextFloat() * 6.28f;
        this.nextMicroRotationTick = 60 + RANDOM.nextInt(100);
        this.nextNodTick = 80 + RANDOM.nextInt(160);
        this.nextGestureTick = 150 + RANDOM.nextInt(250);
        this.nextAmbientSoundTick = 80 + RANDOM.nextInt(200);
    }

    public Location getBaseLocation() {
        return baseLocation;
    }

    public long getTick() {
        return tick;
    }

    public void incrementTick() {
        this.tick++;
    }

    public float getCurrentLookYaw() {
        return currentLookYaw;
    }

    public void setCurrentLookYaw(float currentLookYaw) {
        this.currentLookYaw = currentLookYaw;
    }

    public float getCurrentLookPitch() {
        return currentLookPitch;
    }

    public void setCurrentLookPitch(float currentLookPitch) {
        this.currentLookPitch = currentLookPitch;
    }

    public boolean isLookInitialized() {
        return lookInitialized;
    }

    public void setLookInitialized(boolean lookInitialized) {
        this.lookInitialized = lookInitialized;
    }

    public float getCurrentYawOffset() {
        return currentYawOffset;
    }

    public void setCurrentYawOffset(float currentYawOffset) {
        this.currentYawOffset = currentYawOffset;
    }

    public float getTargetYawOffset() {
        return targetYawOffset;
    }

    public void setTargetYawOffset(float targetYawOffset) {
        this.targetYawOffset = targetYawOffset;
    }

    public long getNextMicroRotationTick() {
        return nextMicroRotationTick;
    }

    public void setNextMicroRotationTick(long nextMicroRotationTick) {
        this.nextMicroRotationTick = nextMicroRotationTick;
    }

    public boolean isNodding() {
        return isNodding;
    }

    public void setNodding(boolean nodding) {
        isNodding = nodding;
    }

    public int getNodProgress() {
        return nodProgress;
    }

    public void setNodProgress(int nodProgress) {
        this.nodProgress = nodProgress;
    }

    public void incrementNodProgress() {
        this.nodProgress++;
    }

    public long getNextNodTick() {
        return nextNodTick;
    }

    public void setNextNodTick(long nextNodTick) {
        this.nextNodTick = nextNodTick;
    }

    public float getTiltPhase() {
        return tiltPhase;
    }

    public void setTiltPhase(float tiltPhase) {
        this.tiltPhase = tiltPhase;
    }

    public long getNextGestureTick() {
        return nextGestureTick;
    }

    public void setNextGestureTick(long nextGestureTick) {
        this.nextGestureTick = nextGestureTick;
    }

    public void triggerNodNow() {
        this.isNodding = true;
        this.nodProgress = 0;
    }

    public long getNextAmbientSoundTick() {
        return nextAmbientSoundTick;
    }

    public void setNextAmbientSoundTick(long nextAmbientSoundTick) {
        this.nextAmbientSoundTick = nextAmbientSoundTick;
    }
}
