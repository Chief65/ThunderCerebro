package com.thunderstudios.pets;

import com.thunderstudios.pets.command.PetCommand;
import com.thunderstudios.pets.egg.EggIncubationTask;
import com.thunderstudios.pets.egg.EggManager;
import com.thunderstudios.pets.listener.EggListener;
import com.thunderstudios.pets.listener.PetEventListener;
import com.thunderstudios.pets.pet.PetManager;
import org.bukkit.command.PluginCommand;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitTask;

public class ThunderPetsPlugin extends JavaPlugin {

    private PetManager petManager;
    private EggManager eggManager;
    private BukkitTask tickTask;
    private BukkitTask eggTask;

    @Override
    public void onEnable() {
        saveDefaultConfig();

        this.petManager = new PetManager(this);
        this.petManager.loadConfig();

        this.eggManager = new EggManager(this);

        getServer().getPluginManager().registerEvents(new PetEventListener(this), this);
        getServer().getPluginManager().registerEvents(new EggListener(this), this);

        PetCommand petCommand = new PetCommand(this);
        PluginCommand cmd = getCommand("pets");
        if (cmd != null) {
            cmd.setExecutor(petCommand);
            cmd.setTabCompleter(petCommand);
        }

        long interval = Math.max(1L, getConfig().getLong("settings.tick-interval", 1L));
        this.tickTask = getServer().getScheduler().runTaskTimer(this, () -> {
            petManager.tickAll();
        }, interval, interval);

        // Tarea de incubación de huevos: 1 vez por minuto (1200 ticks)
        this.eggTask = new EggIncubationTask(this).runTaskTimer(this, 1200L, 1200L);

        getLogger().info("ThunderPets v" + getDescription().getVersion() + " con Sistema de Huevos habilitado con exito.");
    }

    @Override
    public void onDisable() {
        if (tickTask != null) {
            tickTask.cancel();
            tickTask = null;
        }

        if (eggTask != null) {
            eggTask.cancel();
            eggTask = null;
        }

        if (petManager != null) {
            petManager.despawnAll();
        }

        getLogger().info("ThunderPets deshabilitado y todas las entidades de mascotas limpiadas.");
    }

    public PetManager getPetManager() {
        return petManager;
    }

    public EggManager getEggManager() {
        return eggManager;
    }
}
