package com.thundermc.ranks;

import com.thundermc.ranks.command.AdminCommand;
import com.thundermc.ranks.command.RankCommand;
import com.thundermc.ranks.listener.GuiListener;
import com.thundermc.ranks.listener.XpListener;
import com.thundermc.ranks.manager.PlayerDataManager;
import com.thundermc.ranks.manager.RankManager;
import net.milkbowl.vault.economy.Economy;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.GameMode;
import org.bukkit.entity.Player;
import org.bukkit.plugin.RegisteredServiceProvider;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitTask;

public class ThunderRanks extends JavaPlugin {

    private Economy economy;
    private RankManager rankManager;
    private PlayerDataManager playerDataManager;
    private XpListener xpListener;
    private BukkitTask playtimeTask;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        if (!getConfig().contains("ranks.user") || !getConfig().contains("ranks.knight.tiers")) {
            saveResource("config.yml", true);
            reloadConfig();
            getLogger().info("Configuracion actualizada al nuevo sistema de 7 rangos y 5 sub-etapas.");
        }
        setupEconomy();

        rankManager = new RankManager(this);
        rankManager.loadRanks();

        playerDataManager = new PlayerDataManager(this);

        xpListener = new XpListener(this);
        getServer().getPluginManager().registerEvents(xpListener, this);
        getServer().getPluginManager().registerEvents(new GuiListener(this), this);

        if (getServer().getPluginManager().isPluginEnabled("ThunderCrops")) {
            getServer().getPluginManager().registerEvents(new com.thundermc.ranks.listener.ThunderCropsListener(this), this);
            getLogger().info("Integracion con ThunderCrops activada: los cultivos otorgaran XP de rango.");
        }

        RankCommand rankCmd = new RankCommand(this);
        if (getCommand("rangos") != null) getCommand("rangos").setExecutor(rankCmd);
        if (getCommand("rankup") != null) getCommand("rankup").setExecutor(rankCmd);

        AdminCommand adminCmd = new AdminCommand(this);
        if (getCommand("thunderranks") != null) {
            getCommand("thunderranks").setExecutor(adminCmd);
            getCommand("thunderranks").setTabCompleter(adminCmd);
        }

        startPlaytimeTask();

        getLogger().info("ThunderRanks v" + getDescription().getVersion() + " habilitado exitosamente.");
    }

    @Override
    public void onDisable() {
        if (playtimeTask != null) {
            playtimeTask.cancel();
            playtimeTask = null;
        }

        if (playerDataManager != null) {
            for (Player p : Bukkit.getOnlinePlayers()) {
                playerDataManager.unloadPlayer(p);
            }
            playerDataManager.saveData();
        }

        getLogger().info("ThunderRanks deshabilitado.");
    }

    private void setupEconomy() {
        if (getServer().getPluginManager().getPlugin("Vault") == null) {
            getLogger().warning("Vault no encontrado. El coste de rangos funcionara sin comprobacion de dinero.");
            return;
        }
        RegisteredServiceProvider<Economy> rsp = getServer().getServicesManager().getRegistration(Economy.class);
        if (rsp != null) {
            economy = rsp.getProvider();
            getLogger().info("Hook con Vault Economy establecido correctamente.");
        }
    }

    private void startPlaytimeTask() {
        if (playtimeTask != null) {
            playtimeTask.cancel();
            playtimeTask = null;
        }

        int interval = getConfig().getInt("settings.playtime-interval-seconds", 60);
        int xp = getConfig().getInt("settings.playtime-xp", 25);

        playtimeTask = Bukkit.getScheduler().runTaskTimer(this, () -> {
            for (Player p : Bukkit.getOnlinePlayers()) {
                if (p.getGameMode() != GameMode.CREATIVE) {
                    playerDataManager.addXp(p, xp);
                }
            }
        }, interval * 20L, interval * 20L);
    }

    public void reloadPlugin() {
        reloadConfig();
        rankManager.loadRanks();
        xpListener.loadXpValues();
        startPlaytimeTask();
    }

    public Economy getEconomy() { return economy; }
    public RankManager getRankManager() { return rankManager; }
    public PlayerDataManager getPlayerDataManager() { return playerDataManager; }

    public String getMessage(String key) {
        String prefix = getConfig().getString("messages.prefix", "&8[&e&lRangos&8] &r");
        String msg = getConfig().getString("messages." + key, "");
        return ChatColor.translateAlternateColorCodes('&', prefix + msg);
    }
}
