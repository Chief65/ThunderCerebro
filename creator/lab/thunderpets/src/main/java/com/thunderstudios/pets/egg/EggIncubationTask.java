package com.thunderstudios.pets.egg;

import com.thunderstudios.pets.ThunderPetsPlugin;
import com.thunderstudios.pets.util.TextUtil;
import org.bukkit.Bukkit;
import org.bukkit.Sound;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;
import org.bukkit.scheduler.BukkitRunnable;

public class EggIncubationTask extends BukkitRunnable {

    private final ThunderPetsPlugin plugin;

    public EggIncubationTask(ThunderPetsPlugin plugin) {
        this.plugin = plugin;
    }

    @Override
    public void run() {
        for (Player player : Bukkit.getOnlinePlayers()) {
            if (!player.isOnline()) continue;

            for (ItemStack item : player.getInventory().getContents()) {
                if (PetEgg.isEgg(item, plugin)) {
                    boolean completed = PetEgg.addMinute(item, plugin);
                    if (completed && PetEgg.isReadyToHatch(item, plugin)) {
                        player.playSound(player.getLocation(), Sound.BLOCK_NOTE_BLOCK_CHIME, 1.0f, 1.8f);
                        player.sendMessage(TextUtil.color("&a&l¡Tu Huevo de Mascota está listo para eclosionar! &eHaz clic derecho para abrirlo."));
                    }
                }
            }
        }
    }
}
