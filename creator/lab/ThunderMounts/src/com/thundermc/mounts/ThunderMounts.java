package com.thundermc.mounts;

import com.thundermc.mounts.command.MountCommand;
import com.thundermc.mounts.listener.MountListener;
import com.thundermc.mounts.manager.MountManager;
import org.bukkit.ChatColor;
import org.bukkit.plugin.java.JavaPlugin;

public class ThunderMounts extends JavaPlugin {

    private MountManager mountManager;

    @Override
    public void onEnable() {
        saveDefaultConfig();

        mountManager = new MountManager(this);

        getServer().getPluginManager().registerEvents(new MountListener(this), this);

        MountCommand cmd = new MountCommand(this);
        if (getCommand("mount") != null) {
            getCommand("mount").setExecutor(cmd);
            getCommand("mount").setTabCompleter(cmd);
        }

        getLogger().info("ThunderMounts v" + getDescription().getVersion() + " habilitado con éxito.");
    }

    @Override
    public void onDisable() {
        if (mountManager != null) {
            mountManager.cleanup();
        }
        getLogger().info("ThunderMounts deshabilitado.");
    }

    public MountManager getMountManager() {
        return mountManager;
    }

    public String getMessage(String key) {
        String prefix = getConfig().getString("messages.prefix", "&8[&6&lMonturas&8] &r");
        String msg = getConfig().getString("messages." + key, "");
        return ChatColor.translateAlternateColorCodes('&', prefix + msg);
    }
}
