package com.thunderstudios.headanimator;

import com.github.retrooper.packetevents.PacketEvents;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.List;

public class HeadAnimatorPlugin extends JavaPlugin {

    private AnimationManager animationManager;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        this.animationManager = new AnimationManager(this);

        loadConfiguration();

        // Register PacketEvents listener
        PacketEvents.getAPI().getEventManager().registerListener(animationManager);

        HeadCommand cmd = new HeadCommand(this);
        if (getCommand("headanimator") != null) {
            getCommand("headanimator").setExecutor(cmd);
            getCommand("headanimator").setTabCompleter(cmd);
        }

        getServer().getPluginManager().registerEvents(new HeadListener(this), this);

        animationManager.start();
        getLogger().info("HeadAnimator v" + getDescription().getVersion() + " habilitado correctamente con PacketEvents.");
    }

    @Override
    public void onDisable() {
        if (animationManager != null) {
            animationManager.stop();
            try {
                PacketEvents.getAPI().getEventManager().unregisterListener(animationManager);
            } catch (Exception ignored) {}
        }
        getLogger().info("HeadAnimator deshabilitado.");
    }

    public void reload() {
        reloadConfig();
        if (animationManager != null) {
            animationManager.stop();
        }
        loadConfiguration();
        if (animationManager != null) {
            animationManager.start();
        }
    }

    private void loadConfiguration() {
        animationManager.clearAnimations();

        ConfigurationSection animsSec = getConfig().getConfigurationSection("animations");
        if (animsSec != null) {
            for (String key : animsSec.getKeys(false)) {
                ConfigurationSection sec = animsSec.getConfigurationSection(key);
                if (sec == null) continue;

                String name = sec.getString("name", "&aCabeza Animada");
                int interval = sec.getInt("interval-ticks", 10);
                boolean pingPong = sec.getBoolean("ping-pong", true);
                List<String> lore = sec.getStringList("lore");
                List<String> frames = sec.getStringList("frames");

                HeadAnimation anim = new HeadAnimation(this, key, name, lore, interval, frames, pingPong);
                animationManager.registerAnimation(anim);
                getLogger().info("Cargada animacion '" + key + "' con " + anim.getFrameCount() + " fotogramas (Interval: " + anim.getIntervalTicks() + " ticks, PingPong: " + pingPong + ").");
            }
        }
    }

    public AnimationManager getAnimationManager() {
        return animationManager;
    }
}
