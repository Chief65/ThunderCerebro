package com.thunderstudios.pets.gui;

import com.thunderstudios.pets.ThunderPetsPlugin;
import com.thunderstudios.pets.pet.PetInstance;
import com.thunderstudios.pets.pet.PetModel;
import com.thunderstudios.pets.util.TextUtil;
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.Sound;
import org.bukkit.entity.Player;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemFlag;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;

import java.util.ArrayList;
import java.util.List;

public class PetMenu {

    private final ThunderPetsPlugin plugin;

    public PetMenu(ThunderPetsPlugin plugin) {
        this.plugin = plugin;
    }

    public void open(Player player) {
        String titleRaw = plugin.getConfig().getString("messages.menu-title", "&8&lCOSMÉTICOS &8▸ &eMascotas");
        String title = TextUtil.color(titleRaw);

        PetMenuHolder holder = new PetMenuHolder();
        Inventory inv = Bukkit.createInventory(holder, 27, title);
        holder.setInventory(inv);

        // Decoración de fondo
        ItemStack filler = createItem(Material.GRAY_STAINED_GLASS_PANE, " ", null, false);
        for (int i = 0; i < 27; i++) {
            inv.setItem(i, filler);
        }

        PetInstance activePet = plugin.getPetManager().getActivePet(player);
        String activePetId = (activePet != null) ? activePet.getModel().getId() : null;

        // Cargar mascotas
        for (PetModel model : plugin.getPetManager().getModels().values()) {
            boolean isEquipped = model.getId().equals(activePetId);

            ItemStack item = TextUtil.createCustomHead(model.getHeadTexture());
            ItemMeta meta = item.getItemMeta();
            if (meta != null) {
                meta.setDisplayName(TextUtil.color(model.getName()));

                List<String> lore = new ArrayList<>();
                lore.add(TextUtil.color(model.getQuality().getCanonTag()));
                lore.add(TextUtil.color("&7"));

                if (isEquipped) {
                    lore.add(TextUtil.color("&a✔ &lEQUIPADA ACTUALMENTE"));
                    lore.add(TextUtil.color("&7"));
                }

                for (String line : model.getGuiLore()) {
                    lore.add(TextUtil.color(line));
                }

                if (isEquipped) {
                    lore.add(TextUtil.color("&7"));
                    lore.add(TextUtil.color("&c✖ Clic para desequipar"));
                    meta.setEnchantmentGlintOverride(true);
                }

                meta.setLore(lore);
                meta.addItemFlags(ItemFlag.HIDE_ATTRIBUTES);
                item.setItemMeta(meta);
            }

            int slot = model.getGuiSlot();
            if (slot >= 0 && slot < 27) {
                inv.setItem(slot, item);
            }
        }

        // Botón de deselección / cerrar mascota
        List<String> closeLore = new ArrayList<>();
        closeLore.add(TextUtil.color("&7Guarda tu mascota activa"));
        closeLore.add(TextUtil.color("&8(Te quedarás sin cosmético visible)"));
        if (activePetId != null) {
            closeLore.add(TextUtil.color("&7"));
            closeLore.add(TextUtil.color("&eMascota actual: " + activePet.getModel().getName()));
            closeLore.add(TextUtil.color("&a▶ Clic para guardar"));
        } else {
            closeLore.add(TextUtil.color("&7"));
            closeLore.add(TextUtil.color("&8No tienes ninguna mascota activa."));
        }
        ItemStack deselectItem = createItem(Material.BARRIER, "&c&lDesactivar Mascota", closeLore, false);
        inv.setItem(22, deselectItem);

        player.openInventory(inv);
        player.playSound(player.getLocation(), Sound.BLOCK_CHEST_OPEN, 0.6f, 1.2f);
    }

    private ItemStack createItem(Material mat, String name, List<String> lore, boolean glint) {
        ItemStack item = new ItemStack(mat);
        ItemMeta meta = item.getItemMeta();
        if (meta != null) {
            meta.setDisplayName(TextUtil.color(name));
            if (lore != null) {
                meta.setLore(lore);
            }
            if (glint) {
                meta.setEnchantmentGlintOverride(true);
            }
            meta.addItemFlags(ItemFlag.HIDE_ATTRIBUTES);
            item.setItemMeta(meta);
        }
        return item;
    }
}
