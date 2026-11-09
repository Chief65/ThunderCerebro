package com.thundermc.fancyanimations;

import com.thundermc.fancyanimations.command.FancyAnimCommand;
import com.thundermc.fancyanimations.config.ConfigManager;
import com.thundermc.fancyanimations.engine.AnimationEngine;
import com.thundermc.fancyanimations.listener.FancyNpcEventListener;
import com.thundermc.fancyanimations.network.PacketUtil;
import org.bukkit.Bukkit;
import org.bukkit.command.PluginCommand;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitTask;

/**
 * FancyAnimations — Addon oficial de cinemática y animaciones ambientales para FancyNpcs.
 * Desarrollado para ThunderMC Network (Paper 1.21.11 / Geyser).
 */
public class FancyAnimationsPlugin extends JavaPlugin {

    private static FancyAnimationsPlugin instance;
    private ConfigManager configManager;
    private AnimationEngine animationEngine;
    private BukkitTask tickTask;

    @Override
    public void onEnable() {
        instance = this;

        // 1. Verificación de dependencia estricta con FancyNpcs
        if (getServer().getPluginManager().getPlugin("FancyNpcs") == null) {
            getLogger().severe("=================================================");
            getLogger().severe("[FancyAnimations] ERROR FATAL: FancyNpcs no encontrado!");
            getLogger().severe("Este addon requiere FancyNpcs para operar.");
            getLogger().severe("=================================================");
            getServer().getPluginManager().disablePlugin(this);
            return;
        }

        // 2. Inicializar Configuración
        this.configManager = new ConfigManager(this);
        this.configManager.load();

        // 3. Inicializar Pipeline de Paquetes
        PacketUtil.init();

        // 4. Inicializar Motor Cinemático
        this.animationEngine = new AnimationEngine(this, configManager);

        // 5. Inicializar Comandos
        FancyAnimCommand cmdHandler = new FancyAnimCommand(configManager, animationEngine);
        PluginCommand fanimCmd = getCommand("fanim");
        if (fanimCmd != null) {
            fanimCmd.setExecutor(cmdHandler);
            fanimCmd.setTabCompleter(cmdHandler);
        }
        PluginCommand npcsCmd = getCommand("npcs");
        if (npcsCmd != null) {
            npcsCmd.setExecutor(cmdHandler);
            npcsCmd.setTabCompleter(cmdHandler);
        }

        // 6. Registrar Eventos
        getServer().getPluginManager().registerEvents(new FancyNpcEventListener(configManager, animationEngine, cmdHandler), this);

        // 7. Iniciar Tarea Cinemática del Motor (Scheduler)
        int interval = configManager.getUpdateInterval();
        this.tickTask = Bukkit.getScheduler().runTaskTimer(this, () -> {
            try {
                animationEngine.tick();
            } catch (Exception e) {
                getLogger().warning("[FancyAnimations] Error en ciclo cinemático: " + e.getMessage());
            }
        }, 10L, interval);

        getLogger().info("=================================================");
        getLogger().info("[FancyAnimations] v1.0.0 habilitado con éxito!");
        getLogger().info("[FancyAnimations] Perfil ambiental por defecto: " + configManager.getDefaultProfile().toUpperCase());
        getLogger().info("[FancyAnimations] Compatible con Paper 1.21.11 & Bedrock/Geyser.");
        getLogger().info("=================================================");
    }

    @Override
    public void onDisable() {
        if (tickTask != null && !tickTask.isCancelled()) {
            tickTask.cancel();
        }
        if (animationEngine != null) {
            animationEngine.clearAll();
        }
        if (configManager != null) {
            configManager.save();
        }
        getLogger().info("[FancyAnimations] Plugin deshabilitado.");
    }

    public static FancyAnimationsPlugin getInstance() {
        return instance;
    }

    public ConfigManager getConfigManager() {
        return configManager;
    }

    public AnimationEngine getAnimationEngine() {
        return animationEngine;
    }
}
