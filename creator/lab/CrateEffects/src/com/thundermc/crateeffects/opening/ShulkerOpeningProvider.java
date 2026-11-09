package com.thundermc.crateeffects.opening;

import com.thundermc.crateeffects.CrateEffects;
import org.bukkit.entity.Player;
import su.nightexpress.excellentcrates.CratesPlugin;
import su.nightexpress.excellentcrates.api.opening.Opening;
import su.nightexpress.excellentcrates.crate.cost.Cost;
import su.nightexpress.excellentcrates.crate.impl.CrateSource;
import su.nightexpress.excellentcrates.opening.AbstractProvider;
import su.nightexpress.nightcore.config.FileConfig;

public class ShulkerOpeningProvider extends AbstractProvider {

    private final CrateEffects effectsPlugin;

    public ShulkerOpeningProvider(CrateEffects effectsPlugin, CratesPlugin ecPlugin, String id) {
        super(ecPlugin, id);
        this.effectsPlugin = effectsPlugin;
    }

    @Override
    public void load(FileConfig config) {
        // Puede leer configuraciones personalizadas de archivo si se requiere
    }

    @Override
    public Opening createOpening(Player player, CrateSource source, Cost cost) {
        return new ShulkerOpening(effectsPlugin, this.plugin, player, source, cost);
    }
}
