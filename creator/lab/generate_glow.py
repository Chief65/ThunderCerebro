import os

colors = [
    ('glow_morado', 'PURPLE_DYE', 'dark_purple', 'Morado', '&#AA00AA', '&5'),
    ('glow_rosa', 'PINK_DYE', 'light_purple', 'Rosa', '&#FF55FF', '&d'),
    ('glow_rojo', 'RED_DYE', 'red', 'Rojo', '&#FF5555', '&c'),
    ('glow_rojo_oscuro', 'NETHER_WART', 'dark_red', 'Rojo Oscuro', '&#AA0000', '&4'),
    ('glow_dorado', 'ORANGE_DYE', 'gold', 'Dorado', '&#FFAA00', '&6'),
    ('glow_amarillo', 'YELLOW_DYE', 'yellow', 'Amarillo', '&#FFFF55', '&e'),
    ('glow_verde', 'LIME_DYE', 'green', 'Verde Lima', '&#55FF55', '&a'),
    ('glow_verde_oscuro', 'GREEN_DYE', 'dark_green', 'Verde Oscuro', '&#00AA00', '&2'),
    ('glow_celeste', 'LIGHT_BLUE_DYE', 'aqua', 'Celeste', '&#55FFFF', '&b'),
    ('glow_cian', 'CYAN_DYE', 'dark_aqua', 'Cian', '&#00AAAA', '&3'),
    ('glow_azul', 'BLUE_DYE', 'blue', 'Azul', '&#5555FF', '&9'),
    ('glow_azul_oscuro', 'LAPIS_LAZULI', 'dark_blue', 'Azul Oscuro', '&#0000AA', '&1'),
    ('glow_blanco', 'WHITE_DYE', 'white', 'Blanco', '&#FFFFFF', '&f'),
    ('glow_gris', 'LIGHT_GRAY_DYE', 'gray', 'Gris', '&#AAAAAA', '&7'),
    ('glow_gris_oscuro', 'GRAY_DYE', 'dark_gray', 'Gris Oscuro', '&#555555', '&8'),
    ('glow_negro', 'BLACK_DYE', 'black', 'Negro', '&#333333', '&0'),
    ('glow_arcoiris', 'GLOWSTONE_DUST', 'rainbow', 'Arcoiris', '&#FFAA00', '&e')
]

TEMPLATE = """name: '{{PREFIX}}✔ &fGlow &8▶ {{TITLE}} &7(3d)'
lore:
- '&8ᴄᴏꜱᴍᴇᴛɪᴄᴏ'
- ''
- ' &7Cosmetico listo'
- ' &7para reclamar.'
- ''
- ' &8● &fBrillo: {{TITLE}}'
- ' &7(ᴛᴇᴍᴘᴏʀᴀʟ: 3 ᴅíᴀꜱ)'
- ''
- ' &8⁂ &#008DFF&lR&#0AA1FF&lA&#13B4FF&lR&#1DC8FF&lA &e⭐⭐&7⭐⭐⭐'
- ''
- '&7▶ ᴄʟɪᴄᴋ ᴅᴇʀ - ʀᴇᴄʟᴀᴍᴀʀ'
material: {{MATERIAL}}
glow: true
disableStack: false
keepItemOnDeath: false
canBeUsedOnlyByTheOwner: false
storeItemInfo: false
unbreakable: false
usage: 0
usageLimit: -1
cancelEventIfNoPerm: false
cancelEventIfNotOwner: false
disabledWorlds: []
config_5: true
disableEnchantGlide: false
onlyOwnerBlackListedActivators: []
isDurabilityBasedOnUsage: false
cancelEventIfNoPermission: false
whitelistedWorlds: []
glider: false
keepDefaultAttributes: false
hiders:
  hideEnchantments: true
  hideUnbreakable: true
  hideAttributes: true
  hidePotionEffects: true
  hideAdditionalTooltip: true
  hideTooltip: false
  hideToolTip: false
  hideUsage: true
  hideDestroys: false
  hidePlacedOn: false
  hideDye: false
  hideArmorTrim: false
giveFirstJoinFeatures:
  giveFirstJoin: false
  giveFirstJoinAmount: 1
  giveFirstJoinSlot: 0
restrictions:
  cancel-item-place: true
  cancel-item-craft: true
  cancel-anvil: true
  locked-in-inventory: false
variables: {}
activators:
  activator1:
    name: '&eReclamar Glow'
    option: PLAYER_RIGHT_CLICK
    typeTarget: NO_TYPE_TARGET
    usageModification: -1
    cancelEvent: true
    noActivatorRunIfTheEventIsCancelled: false
    autoUpdateItem: false
    cooldownFeatures:
      cooldown: 6
      cooldownMsg: '&cEspera &f%time_S%s &cpara activar otro cosmético.'
      cancelEventIfInCooldown: true
      pausePlaceholdersConditions: {}
    globalCooldownFeatures:
      cooldown: 0
      displayCooldownMessage: false
    otherEICooldowns: {}
    requiredItems: {}
    requiredExecutableItems: {}
    requiredMagics: {}
    detailedSlots:
    - -1
    - 40
    playerCommands:
    - 'effect give %player% minecraft:darkness 4 0 true'
    - 'title %player% times 0 20 5'
    - 'title %player% title "{{TITLE}}"'
    - 'title %player% subtitle "&8▪ &fᴀᴄᴛɪᴠᴀɴᴅᴏ &8[{{HEX}}&m &8&m &8&m &8&m &8&m &r&8] &75s"'
    - 'execute at %player% run playsound minecraft:item.bundle.drop_contents master %player% ~ ~ ~ 0.8 1.0'
    - 'execute at %player% run playsound minecraft:block.note_block.hat master %player% ~ ~ ~ 0.8 1.0'
    - 'DELAY_TICK 10'
    - 'title %player% title "{{TITLE}}"'
    - 'title %player% subtitle "&8▪ &fᴀᴄᴛɪᴠᴀɴᴅᴏ &8[{{HEX}}&m {{HEX}}&m &8&m &8&m &8&m &r&8] &74s"'
    - 'execute at %player% run playsound minecraft:item.bundle.drop_contents master %player% ~ ~ ~ 0.8 1.1'
    - 'execute at %player% run playsound minecraft:block.note_block.hat master %player% ~ ~ ~ 0.8 1.1'
    - 'DELAY_TICK 10'
    - 'title %player% title "{{TITLE}}"'
    - 'title %player% subtitle "&8▪ &fᴀᴄᴛɪᴠᴀɴᴅᴏ &8[{{HEX}}&m {{HEX}}&m {{HEX}}&m &8&m &8&m &r&8] &73s"'
    - 'execute at %player% run playsound minecraft:item.bundle.drop_contents master %player% ~ ~ ~ 0.8 1.2'
    - 'execute at %player% run playsound minecraft:block.note_block.hat master %player% ~ ~ ~ 0.8 1.2'
    - 'DELAY_TICK 10'
    - 'title %player% title "{{TITLE}}"'
    - 'title %player% subtitle "&8▪ &fᴀᴄᴛɪᴠᴀɴᴅᴏ &8[{{HEX}}&m {{HEX}}&m {{HEX}}&m {{HEX}}&m &8&m &r&8] &72s"'
    - 'execute at %player% run playsound minecraft:item.bundle.drop_contents master %player% ~ ~ ~ 0.8 1.3'
    - 'execute at %player% run playsound minecraft:block.note_block.hat master %player% ~ ~ ~ 0.8 1.3'
    - 'DELAY_TICK 10'
    - 'title %player% title "{{TITLE}}"'
    - 'title %player% subtitle "&8▪ &fᴀᴄᴛɪᴠᴀɴᴅᴏ &8[{{HEX}}&m {{HEX}}&m {{HEX}}&m {{HEX}}&m {{HEX}}&m &r&8] &71s"'
    - 'execute at %player% run playsound minecraft:item.bundle.drop_contents master %player% ~ ~ ~ 0.8 1.4'
    - 'execute at %player% run playsound minecraft:block.note_block.hat master %player% ~ ~ ~ 0.8 1.4'
    - 'DELAY_TICK 10'
    - 'execute at %player% run playsound minecraft:ui.toast.challenge_complete master %player% ~ ~ ~ 1 1.0'
    - 'execute at %player% run playsound minecraft:entity.player.levelup master %player% ~ ~ ~ 1 1.4'
    - 'execute at %player% run playsound minecraft:entity.firework_rocket.blast master %player% ~ ~ ~ 1 1.1'
    - 'execute at %player% run playsound minecraft:entity.firework_rocket.twinkle master %player% ~ ~ ~ 1 1.0'
    - 'PARTICLE FIREWORK 40 0.5 0.5'
    - 'PARTICLE TOTEM 35 0.4 0.4'
    - 'PARTICLE END_ROD 30 0.4 0.4'
    - 'PARTICLE VILLAGER_HAPPY 25 0.3 0.3'
    - 'title %player% times 0 35 10'
    - 'title %player% title "{{TITLE}}"'
    - 'title %player% subtitle "&f¡ɢʟᴏᴡ ᴀᴄᴛɪᴠᴀᴅᴏ! &7(3 días)"'
    - 'lp user %player% permission settemp fancyglow.{{FG_COLOR}} true 3d'
    - 'glow set %player% {{FG_COLOR}}'
    - 'title %player% actionbar "&a✔ &fɢʟᴏᴡ ᴀᴄᴛɪᴠᴀᴅᴏ: {{TITLE}} &7(3d)"'
    - 'SEND_MESSAGE &r'
    - 'SEND_MESSAGE &8[&#FEEB00ThunderMc&8] &#008DFF⭐ &lCOSMÉTICO GLOW ACTIVADO &8| &fBrillo {{TITLE}}&f.'
    - 'SEND_MESSAGE &r  &8• &fDuración: &e3 Días &7(expira automáticamente)'
    - 'SEND_MESSAGE &r  &8• &fMenú: &7Usa &#008DFF/glow &7para cambiarlo o desactivarlo.'
    - 'SEND_MESSAGE &r'
    playerConditions: {}
    worldConditions: {}
    itemConditions: {}
    customConditions: {}
    placeholdersConditions: {}
    variablesModification: {}
displayConditions:
  playerConditions: {}
  worldConditions: {}
  itemConditions: {}
  placeholdersConditions: {}
  enableFeature: false
foodFeatures:
  isMeat: false
  nutrition: 1
  saturation: 0.5
  canAlwaysEat: false
consumableFeatures:
  isConsumable: false
  animation: EAT
  hasConsumableParticles: true
  consumeSeconds: 3
weaponFeatures:
  cancelDefaultDamage: false
  damagePerHit: 1
  canUseOnlyDuringBlocking: false
  cancelSwordBlockingDamage: false
  swordBlockingDamageMultiplier: 1.0
  customSwordBlockingTime: 0
whitelistedWorlds: []
recognitions: []
"""

os.makedirs('creator/lab/glow', exist_ok=True)

for file_id, material, fg_color, color_name, hex_color, prefix_color in colors:
    title_display = f"{hex_color}{color_name}" if fg_color != 'rainbow' else '&#FF5555A&#FFAA00r&#FFFF55c&#55FF55o&#55FFFFi&#5555FFr&#FF55FFi&#AA00AAs'
    content = (TEMPLATE
               .replace('{{PREFIX}}', prefix_color)
               .replace('{{TITLE}}', title_display)
               .replace('{{MATERIAL}}', material)
               .replace('{{HEX}}', hex_color)
               .replace('{{FG_COLOR}}', fg_color))
    with open(f'creator/lab/glow/{file_id}.yml', 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Generated {len(colors)} glow items successfully.")
