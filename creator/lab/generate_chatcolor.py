import os

colors = [
    {
        'id': 'chatcolor_negro',
        'code': '0',
        'name': 'Negro',
        'prefix': '&8',
        'hex': '&#333333',
        'display': '&#333333Negro',
        'material': 'BLACK_WOOL'
    },
    {
        'id': 'chatcolor_azul_oscuro',
        'code': '1',
        'name': 'Azul Oscuro',
        'prefix': '&1',
        'hex': '&#0000AA',
        'display': '&#0000AAAzul Oscuro',
        'material': 'BLUE_WOOL'
    },
    {
        'id': 'chatcolor_verde_oscuro',
        'code': '2',
        'name': 'Verde Oscuro',
        'prefix': '&2',
        'hex': '&#00AA00',
        'display': '&#00AA00Verde Oscuro',
        'material': 'GREEN_WOOL'
    },
    {
        'id': 'chatcolor_cian',
        'code': '3',
        'name': 'Cian',
        'prefix': '&3',
        'hex': '&#00AAAA',
        'display': '&#00AAAACian',
        'material': 'CYAN_WOOL'
    },
    {
        'id': 'chatcolor_rojo_oscuro',
        'code': '4',
        'name': 'Rojo Oscuro',
        'prefix': '&4',
        'hex': '&#AA0000',
        'display': '&#AA0000Rojo Oscuro',
        'material': 'RED_WOOL'
    },
    {
        'id': 'chatcolor_morado',
        'code': '5',
        'name': 'Morado',
        'prefix': '&5',
        'hex': '&#AA00AA',
        'display': '&#AA00AAMorado',
        'material': 'PURPLE_WOOL'
    },
    {
        'id': 'chatcolor_dorado',
        'code': '6',
        'name': 'Dorado',
        'prefix': '&6',
        'hex': '&#FFAA00',
        'display': '&#FFAA00Dorado',
        'material': 'ORANGE_WOOL'
    },
    {
        'id': 'chatcolor_gris',
        'code': '7',
        'name': 'Gris',
        'prefix': '&7',
        'hex': '&#AAAAAA',
        'display': '&#AAAAAAGris',
        'material': 'LIGHT_GRAY_WOOL'
    },
    {
        'id': 'chatcolor_gris_oscuro',
        'code': '8',
        'name': 'Gris Oscuro',
        'prefix': '&8',
        'hex': '&#555555',
        'display': '&#555555Gris Oscuro',
        'material': 'GRAY_WOOL'
    },
    {
        'id': 'chatcolor_azul',
        'code': '9',
        'name': 'Azul',
        'prefix': '&9',
        'hex': '&#5555FF',
        'display': '&#5555FFAzul',
        'material': 'BLUE_WOOL'
    },
    {
        'id': 'chatcolor_verde',
        'code': 'a',
        'name': 'Verde Lima',
        'prefix': '&a',
        'hex': '&#55FF55',
        'display': '&#55FF55Verde Lima',
        'material': 'LIME_WOOL'
    },
    {
        'id': 'chatcolor_celeste',
        'code': 'b',
        'name': 'Celeste',
        'prefix': '&b',
        'hex': '&#55FFFF',
        'display': '&#55FFFFCeleste',
        'material': 'LIGHT_BLUE_WOOL'
    },
    {
        'id': 'chatcolor_rojo',
        'code': 'c',
        'name': 'Rojo',
        'prefix': '&c',
        'hex': '&#FF5555',
        'display': '&#FF5555Rojo',
        'material': 'RED_WOOL'
    },
    {
        'id': 'chatcolor_rosa',
        'code': 'd',
        'name': 'Rosa',
        'prefix': '&d',
        'hex': '&#FF55FF',
        'display': '&#FF55FFRosa',
        'material': 'PINK_WOOL'
    },
    {
        'id': 'chatcolor_magenta',
        'code': 'd',
        'name': 'Magenta',
        'prefix': '&d',
        'hex': '&#FF55FF',
        'display': '&#FF55FFMagenta',
        'material': 'MAGENTA_WOOL'
    },
    {
        'id': 'chatcolor_amarillo',
        'code': 'e',
        'name': 'Amarillo',
        'prefix': '&e',
        'hex': '&#FFFF55',
        'display': '&#FFFF55Amarillo',
        'material': 'YELLOW_WOOL'
    },
    {
        'id': 'chatcolor_blanco',
        'code': 'f',
        'name': 'Blanco',
        'prefix': '&f',
        'hex': '&#FFFFFF',
        'display': '&#FFFFFFBlanco',
        'material': 'WHITE_WOOL'
    }
]

out_dir = 'creator/lab/chatcolor'
os.makedirs(out_dir, exist_ok=True)

for c in colors:
    color_hex = c['hex']
    color_display = c['display']
    color_prefix = c['prefix']
    color_name = c['name']
    code = c['code']
    mat = c['material']
    file_id = c['id']

    content = f"""name: '{color_prefix}✔ &fColor &8▶ {color_display} &7(3d)'
lore:
- '&8ᴄᴏꜱᴍᴇᴛɪᴄᴏ'
- ''
- ' &7Cosmetico listo'
- ' &7para reclamar.'
- ''
- ' &8● &fChat: {color_display}'
- ' &7(ᴛᴇᴍᴘᴏʀᴀʟ: 3 ᴅíᴀꜱ)'
- ''
- ' &8⁂ &#008DFF&lR&#0AA1FF&lA&#13B4FF&lR&#1DC8FF&lA &e⭐⭐&7⭐⭐⭐'
- ''
- '&7▶ ᴄʟɪᴄᴋ ᴅᴇʀ - ʀᴇᴄʟᴀᴍᴀʀ'
material: {mat}
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
variables: {{}}
activators:
  activator1:
    name: '&eReclamar Color de Chat'
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
      pausePlaceholdersConditions: {{}}
    globalCooldownFeatures:
      cooldown: 0
      displayCooldownMessage: false
    otherEICooldowns: {{}}
    requiredItems: {{}}
    requiredExecutableItems: {{}}
    requiredMagics: {{}}
    detailedSlots:
    - -1
    - 40
    playerCommands:
    - 'effect give %player% minecraft:darkness 4 0 true'
    - 'title %player% times 0 20 5'
    - 'title %player% title \"{color_display}\"'
    - 'title %player% subtitle \"&8▪ &fᴀᴄᴛɪᴠᴀɴᴅᴏ &8[{color_hex}&m &8&m &8&m &8&m &8&m &r&8] &75s\"'
    - 'execute at %player% run playsound minecraft:item.bundle.drop_contents master %player% ~ ~ ~ 0.8 1.0'
    - 'execute at %player% run playsound minecraft:block.note_block.hat master %player% ~ ~ ~ 0.8 1.0'
    - 'DELAY_TICK 10'
    - 'title %player% title \"{color_display}\"'
    - 'title %player% subtitle \"&8▪ &fᴀᴄᴛɪᴠᴀɴᴅᴏ &8[{color_hex}&m {color_hex}&m &8&m &8&m &8&m &r&8] &74s\"'
    - 'execute at %player% run playsound minecraft:item.bundle.drop_contents master %player% ~ ~ ~ 0.8 1.1'
    - 'execute at %player% run playsound minecraft:block.note_block.hat master %player% ~ ~ ~ 0.8 1.1'
    - 'DELAY_TICK 10'
    - 'title %player% title \"{color_display}\"'
    - 'title %player% subtitle \"&8▪ &fᴀᴄᴛɪᴠᴀɴᴅᴏ &8[{color_hex}&m {color_hex}&m {color_hex}&m &8&m &8&m &r&8] &73s\"'
    - 'execute at %player% run playsound minecraft:item.bundle.drop_contents master %player% ~ ~ ~ 0.8 1.2'
    - 'execute at %player% run playsound minecraft:block.note_block.hat master %player% ~ ~ ~ 0.8 1.2'
    - 'DELAY_TICK 10'
    - 'title %player% title \"{color_display}\"'
    - 'title %player% subtitle \"&8▪ &fᴀᴄᴛɪᴠᴀɴᴅᴏ &8[{color_hex}&m {color_hex}&m {color_hex}&m {color_hex}&m &8&m &r&8] &72s\"'
    - 'execute at %player% run playsound minecraft:item.bundle.drop_contents master %player% ~ ~ ~ 0.8 1.3'
    - 'execute at %player% run playsound minecraft:block.note_block.hat master %player% ~ ~ ~ 0.8 1.3'
    - 'DELAY_TICK 10'
    - 'title %player% title \"{color_display}\"'
    - 'title %player% subtitle \"&8▪ &fᴀᴄᴛɪᴠᴀɴᴅᴏ &8[{color_hex}&m {color_hex}&m {color_hex}&m {color_hex}&m {color_hex}&m &r&8] &71s\"'
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
    - 'title %player% title \"{color_display}\"'
    - 'title %player% subtitle \"&f¡ᴄᴏʟᴏʀ ᴅᴇ ᴄʜᴀᴛ ᴀᴄᴛɪᴠᴀᴅᴏ! &7(3 días)\"'
    - 'lp user %player% permission settemp chatcolor.color.{code} true 3d'
    - 'chatcolor %player% {code}'
    - 'title %player% actionbar \"&a✔ &fᴄᴏʟᴏʀ ᴅᴇ ᴄʜᴀᴛ ᴀᴄᴛɪᴠᴀᴅᴏ: {color_display} &7(3d)\"'
    - 'SEND_MESSAGE &r'
    - 'SEND_MESSAGE &8[&#FEEB00ThunderMc&8] &#008DFF⭐ &lCOSMÉTICO CHATCOLOR ACTIVADO &8| &fColor {color_display}&f.'
    - 'SEND_MESSAGE &r  &8• &fDuración: &e3 Días &7(expira automáticamente)'
    - 'SEND_MESSAGE &r  &8• &fMenú: &7Usa &#008DFF/chatcolor &7para gestionarlo.'
    - 'SEND_MESSAGE &r'
    playerConditions: {{}}
    worldConditions: {{}}
    itemConditions: {{}}
    customConditions: {{}}
    placeholdersConditions: {{}}
    variablesModification: {{}}
displayConditions:
  playerConditions: {{}}
  worldConditions: {{}}
  itemConditions: {{}}
  placeholdersConditions: {{}}
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
    with open(f'{out_dir}/{file_id}.yml', 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Generated {len(colors)} chatcolor items successfully.")
