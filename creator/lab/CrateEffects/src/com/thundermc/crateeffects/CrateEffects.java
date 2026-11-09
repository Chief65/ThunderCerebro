package com.thundermc.crateeffects;

import com.thundermc.crateeffects.opening.ShulkerOpeningProvider;
import org.bukkit.Bukkit;
import org.bukkit.plugin.java.JavaPlugin;
import su.nightexpress.excellentcrates.CratesAPI;
import su.nightexpress.excellentcrates.CratesPlugin;

public class CrateEffects extends JavaPlugin {

    private EffectConfig effectConfig;
    private ShulkerOpeningProvider shulkerProvider;

    @Override
    public void onEnable() {
        saveDefaultConfig();

        this.effectConfig = new EffectConfig(this);
        this.effectConfig.load();

        // Registro de Listeners desacoplados
        Bukkit.getPluginManager().registerEvents(new FireworkDamageListener(this), this);
        Bukkit.getPluginManager().registerEvents(new RewardEffectListener(this), this);

        // Registro de Comandos
        CrateEffectsCommand cmd = new CrateEffectsCommand(this);
        if (getCommand("crateeffects") != null) {
            getCommand("crateeffects").setExecutor(cmd);
            getCommand("crateeffects").setTabCompleter(cmd);
        }

        // Registro del Opening Provider Shulker en ExcellentCrates
        registerShulkerProvider();

        getLogger().info("CrateEffects v" + getDescription().getVersion() + " iniciado exitosamente (Modo Addon Seguro).");
    }

    private void registerShulkerProvider() {
        if (Bukkit.getPluginManager().isPluginEnabled("ExcellentCrates")) {
            try {
                CratesPlugin ec = CratesAPI.getPlugin();
                this.shulkerProvider = new ShulkerOpeningProvider(this, ec, "shulker_box");
                ec.getOpeningManager().loadProvider(this.shulkerProvider);
                getLogger().info("Provider de animacion 'shulker_box' registrado con exito en ExcellentCrates.");
            } catch (Throwable t) {
                getLogger().warning("No se pudo registrar 'shulker_box' en ExcellentCrates: " + t.getMessage());
            }
        }
    }

    @Override
    public void onDisable() {
        Bukkit.getScheduler().cancelTasks(this);
        getLogger().info("CrateEffects detenido y tareas canceladas.");
    }

    public EffectConfig getEffectConfig() {
        return effectConfig;
    }

    public ShulkerOpeningProvider getShulkerProvider() {
        return shulkerProvider;
    }
}
