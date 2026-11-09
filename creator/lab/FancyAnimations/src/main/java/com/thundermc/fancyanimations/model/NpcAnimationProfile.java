package com.thundermc.fancyanimations.model;

import java.util.HashMap;
import java.util.Map;

/**
 * Representa el perfil de animaciones configurado para un NPC específico o como plantilla.
 */
public class NpcAnimationProfile {

    private boolean breathing = true;
    private boolean swaying = true;
    private boolean headTilt = true;
    private boolean nodding = true;
    private boolean microRotation = true;
    private boolean lookAtPlayer = true;
    private boolean cursorGlow = true;
    private boolean randomGestures = false;

    public NpcAnimationProfile() {
    }

    public NpcAnimationProfile(boolean breathing, boolean swaying, boolean headTilt,
                               boolean nodding, boolean microRotation, boolean lookAtPlayer,
                               boolean cursorGlow, boolean randomGestures) {
        this.breathing = breathing;
        this.swaying = swaying;
        this.headTilt = headTilt;
        this.nodding = nodding;
        this.microRotation = microRotation;
        this.lookAtPlayer = lookAtPlayer;
        this.cursorGlow = cursorGlow;
        this.randomGestures = randomGestures;
    }

    public static NpcAnimationProfile createEmpty() {
        return new NpcAnimationProfile(false, false, false, false, false, false, false, false);
    }

    public static NpcAnimationProfile createAmbientDefault() {
        return new NpcAnimationProfile(true, true, true, true, true, true, true, false);
    }

    public boolean isBreathing() {
        return breathing;
    }

    public void setBreathing(boolean breathing) {
        this.breathing = breathing;
    }

    public boolean isSwaying() {
        return swaying;
    }

    public void setSwaying(boolean swaying) {
        this.swaying = swaying;
    }

    public boolean isHeadTilt() {
        return headTilt;
    }

    public void setHeadTilt(boolean headTilt) {
        this.headTilt = headTilt;
    }

    public boolean isNodding() {
        return nodding;
    }

    public void setNodding(boolean nodding) {
        this.nodding = nodding;
    }

    public boolean isMicroRotation() {
        return microRotation;
    }

    public void setMicroRotation(boolean microRotation) {
        this.microRotation = microRotation;
    }

    public boolean isLookAtPlayer() {
        return lookAtPlayer;
    }

    public void setLookAtPlayer(boolean lookAtPlayer) {
        this.lookAtPlayer = lookAtPlayer;
    }

    public boolean isCursorGlow() {
        return cursorGlow;
    }

    public void setCursorGlow(boolean cursorGlow) {
        this.cursorGlow = cursorGlow;
    }

    public boolean isRandomGestures() {
        return randomGestures;
    }

    public void setRandomGestures(boolean randomGestures) {
        this.randomGestures = randomGestures;
    }

    /**
     * Aplica el estado del conjunto ambiental general.
     */
    public void setAmbient(boolean enable, NpcAnimationProfile ambientPreset) {
        if (enable) {
            this.breathing = ambientPreset.breathing;
            this.swaying = ambientPreset.swaying;
            this.headTilt = ambientPreset.headTilt;
            this.nodding = ambientPreset.nodding;
            this.microRotation = ambientPreset.microRotation;
            this.lookAtPlayer = ambientPreset.lookAtPlayer;
            this.cursorGlow = ambientPreset.cursorGlow;
            this.randomGestures = ambientPreset.randomGestures;
        } else {
            this.breathing = false;
            this.swaying = false;
            this.headTilt = false;
            this.nodding = false;
            this.microRotation = false;
            this.lookAtPlayer = false;
            this.cursorGlow = false;
            this.randomGestures = false;
        }
    }

    public boolean isAmbientActive() {
        return breathing || swaying || headTilt || nodding || microRotation || lookAtPlayer || cursorGlow;
    }

    public boolean getByName(String name) {
        return switch (name.toLowerCase()) {
            case "breathing", "respiracion" -> breathing;
            case "swaying", "balanceo" -> swaying;
            case "headtilt", "tilt", "ladeo" -> headTilt;
            case "nodding", "nod", "cabeceo" -> nodding;
            case "microrotation", "rotacion", "microrot" -> microRotation;
            case "lookatplayer", "lookat", "turntoplayer", "mirada" -> lookAtPlayer;
            case "cursorglow", "glow", "resplandor" -> cursorGlow;
            case "randomgestures", "gestos", "gestures" -> randomGestures;
            default -> false;
        };
    }

    public boolean setByName(String name, boolean value) {
        switch (name.toLowerCase()) {
            case "breathing", "respiracion" -> this.breathing = value;
            case "swaying", "balanceo" -> this.swaying = value;
            case "headtilt", "tilt", "ladeo" -> this.headTilt = value;
            case "nodding", "nod", "cabeceo" -> this.nodding = value;
            case "microrotation", "rotacion", "microrot" -> this.microRotation = value;
            case "lookatplayer", "lookat", "turntoplayer", "mirada" -> this.lookAtPlayer = value;
            case "cursorglow", "glow", "resplandor" -> this.cursorGlow = value;
            case "randomgestures", "gestos", "gestures" -> this.randomGestures = value;
            default -> {
                return false;
            }
        }
        return true;
    }

    public Map<String, Object> serialize() {
        Map<String, Object> map = new HashMap<>();
        map.put("breathing", breathing);
        map.put("swaying", swaying);
        map.put("head-tilt", headTilt);
        map.put("nodding", nodding);
        map.put("micro-rotation", microRotation);
        map.put("look-at-player", lookAtPlayer);
        map.put("cursor-glow", cursorGlow);
        map.put("random-gestures", randomGestures);
        return map;
    }

    public static NpcAnimationProfile deserialize(Map<String, Object> map) {
        NpcAnimationProfile profile = new NpcAnimationProfile();
        if (map.containsKey("breathing")) profile.setBreathing((Boolean) map.get("breathing"));
        if (map.containsKey("swaying")) profile.setSwaying((Boolean) map.get("swaying"));
        if (map.containsKey("head-tilt")) profile.setHeadTilt((Boolean) map.get("head-tilt"));
        if (map.containsKey("nodding")) profile.setNodding((Boolean) map.get("nodding"));
        if (map.containsKey("micro-rotation")) profile.setMicroRotation((Boolean) map.get("micro-rotation"));
        if (map.containsKey("look-at-player")) profile.setLookAtPlayer((Boolean) map.get("look-at-player"));
        if (map.containsKey("cursor-glow")) profile.setCursorGlow((Boolean) map.get("cursor-glow"));
        if (map.containsKey("random-gestures")) profile.setRandomGestures((Boolean) map.get("random-gestures"));
        return profile;
    }

    public NpcAnimationProfile clone() {
        return new NpcAnimationProfile(breathing, swaying, headTilt, nodding, microRotation, lookAtPlayer, cursorGlow, randomGestures);
    }
}
