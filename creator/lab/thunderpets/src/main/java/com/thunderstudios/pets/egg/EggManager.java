package com.thunderstudios.pets.egg;

import com.thunderstudios.pets.ThunderPetsPlugin;
import com.thunderstudios.pets.pet.PetModel;
import com.thunderstudios.pets.pet.PetQuality;
import com.thunderstudios.pets.util.TextUtil;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.Particle;
import org.bukkit.Sound;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemFlag;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.persistence.PersistentDataType;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public class EggManager {

    private final ThunderPetsPlugin plugin;
    private final Random random = new Random();

    public EggManager(ThunderPetsPlugin plugin) {
        this.plugin = plugin;
    }

    public NamespacedKey getKeyAccelerator() {
        return new NamespacedKey(plugin, "egg_accelerator");
    }

    public boolean isAccelerator(ItemStack item) {
        if (item == null || item.getType() == Material.AIR) return false;
        ItemMeta meta = item.getItemMeta();
        if (meta == null) return false;
        return meta.getPersistentDataContainer().has(getKeyAccelerator(), PersistentDataType.BYTE);
    }

    public ItemStack createAccelerator() {
        ItemStack potion = new ItemStack(Material.POTION);
        ItemMeta meta = potion.getItemMeta();
        if (meta == null) return potion;

        meta.setDisplayName(TextUtil.color("&#FD9A00&lPoción de Incubación Rápida"));
        List<String> lore = new ArrayList<>();
        lore.add(TextUtil.color("&8⁂ &#FD9A00&lD&#FAAE00&lI&#F7C200&lV&#F5D700&lI&#F2EB00&lN&#EFFF00&lA &e⭐⭐⭐⭐⭐"));
        lore.add(TextUtil.color("&7"));
        lore.add(TextUtil.color("&fUn elixir alquímico concentrado con calor mágico"));
        lore.add(TextUtil.color("&fque acelera al instante todas las tareas de"));
        lore.add(TextUtil.color("&fcuidado de un Huevo de Mascota."));
        lore.add(TextUtil.color("&7"));
        lore.add(TextUtil.color("&e▶ Haz Clic Derecho sosteniendo un huevo"));
        lore.add(TextUtil.color("&epara madurarlo al 100% de inmediato."));

        meta.addItemFlags(ItemFlag.HIDE_ATTRIBUTES);
        meta.addItemFlags(ItemFlag.HIDE_ADDITIONAL_TOOLTIP);
        meta.setEnchantmentGlintOverride(true);
        meta.getPersistentDataContainer().set(getKeyAccelerator(), PersistentDataType.BYTE, (byte) 1);
        meta.setLore(lore);
        potion.setItemMeta(meta);
        return potion;
    }

    public void hatch(Player player, ItemStack eggItem) {
        PetQuality quality = PetEgg.getQuality(eggItem, plugin);

        List<PetModel> candidates = new ArrayList<>();
        for (PetModel model : plugin.getPetManager().getModels().values()) {
            if (model.getQuality() == quality) {
                candidates.add(model);
            }
        }

        if (candidates.isEmpty()) {
            // Si no hay candidatos exactos de esa calidad, seleccionar cualquier modelo disponible
            candidates.addAll(plugin.getPetManager().getModels().values());
        }

        if (candidates.isEmpty()) {
            player.sendMessage(TextUtil.color("&cNo hay mascotas registradas para eclosionar."));
            return;
        }

        Collections.shuffle(candidates);
        PetModel selectedPet = candidates.get(0);

        // Consumir el huevo
        eggItem.setAmount(eggItem.getAmount() - 1);

        // Efectos audiovisuales de eclosión
        player.playSound(player.getLocation(), Sound.ENTITY_TURTLE_EGG_HATCH, 1.0f, 0.8f);
        player.playSound(player.getLocation(), Sound.UI_TOAST_CHALLENGE_COMPLETE, 0.8f, 1.2f);
        player.getWorld().spawnParticle(Particle.TOTEM_OF_UNDYING, player.getLocation().add(0, 1.2, 0), 35, 0.3, 0.3, 0.3, 0.1);
        player.getWorld().spawnParticle(Particle.FIREWORK, player.getLocation().add(0, 1.5, 0), 20, 0.2, 0.2, 0.2, 0.05);

        // Mensajes y título en pantalla
        player.sendTitle(
                TextUtil.color("&#FEEB00&l¡HUEVO ECLOSIONADO!"),
                TextUtil.color("&f¡Has obtenido a: " + selectedPet.getName() + "&f!"),
                10, 60, 20
        );

        String prefix = plugin.getConfig().getString("messages.prefix", "&6&lMASCOTAS &8▸ ");
        player.sendMessage(TextUtil.color(prefix + "&a¡Tu huevo ha eclosionado con éxito!"));
        player.sendMessage(TextUtil.color(prefix + "&fHas desbloqueado y recibido a: " + selectedPet.getName()));

        // Activar automáticamente la mascota obtenida
        plugin.getPetManager().togglePet(player, selectedPet.getId());
    }
}
