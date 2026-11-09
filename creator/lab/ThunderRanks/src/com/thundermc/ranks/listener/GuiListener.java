package com.thundermc.ranks.listener;

import com.thundermc.ranks.ThunderRanks;
import com.thundermc.ranks.gui.RankConfirmGui;
import com.thundermc.ranks.gui.RankGui;
import org.bukkit.Sound;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryClickEvent;

public class GuiListener implements Listener {

    private final ThunderRanks plugin;

    public GuiListener(ThunderRanks plugin) {
        this.plugin = plugin;
    }

    @EventHandler
    public void onInventoryClick(InventoryClickEvent event) {
        String title = event.getView().getTitle();

        // Menú Principal de Rangos y Ascensos
        if (title.equals(RankGui.GUI_TITLE)) {
            event.setCancelled(true);
            if (!(event.getWhoClicked() instanceof Player player)) return;

            int slot = event.getRawSlot();

            // Slot 49: Puerta para cerrar menú
            if (slot == 49) {
                player.closeInventory();
                player.playSound(player.getLocation(), Sound.BLOCK_WOODEN_DOOR_CLOSE, 0.7f, 1.0f);
                return;
            }

            // Slot 53: Botón de ascensión (abre confirmación)
            if (slot == 53) {
                if (plugin.getPlayerDataManager().canRankup(player)) {
                    player.playSound(player.getLocation(), Sound.UI_BUTTON_CLICK, 0.7f, 1.0f);
                    RankConfirmGui.open(player, plugin);
                }
                return;
            }
        }

        // Menú de Confirmación de Ascenso (3 líneas)
        if (title.equals(RankConfirmGui.CONFIRM_TITLE)) {
            event.setCancelled(true);
            if (!(event.getWhoClicked() instanceof Player player)) return;

            int slot = event.getRawSlot();

            // Slot 11: LIME_WOOL (Confirmar Ascenso)
            if (slot == 11) {
                player.closeInventory();
                plugin.getPlayerDataManager().processRankup(player);
                return;
            }

            // Slot 15: RED_WOOL (Cancelar y volver a /rangos)
            if (slot == 15) {
                player.playSound(player.getLocation(), Sound.UI_BUTTON_CLICK, 0.7f, 1.0f);
                RankGui.open(player, plugin);
                return;
            }
        }
    }
}
