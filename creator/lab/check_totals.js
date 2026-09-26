const fs = require("fs");

const farmeoRaw = [
  { mat: "BAMBOO", name: "Bambú", sell: 1 },
  { mat: "BEETROOT", name: "Remolacha", sell: 20 },
  { mat: "BEETROOT_SEEDS", name: "Semillas de Remolacha", sell: 1 },
  { mat: "BROWN_MUSHROOM", name: "Champiñón Marrón", sell: 1 },
  { mat: "CACTUS", name: "Cactus", sell: 5 },
  { mat: "CARROT", name: "Zanahoria", sell: 15 },
  { mat: "CHORUS_FLOWER", name: "Flor del Chorus", sell: 1 },
  { mat: "CHORUS_FRUIT", name: "Fruta del Chorus", sell: 1 },
  { mat: "COCOA_BEANS", name: "Granos de Cacao", sell: 30 },
  { mat: "KELP", name: "Algas", sell: 2 },
  { mat: "MELON", name: "Sandía (Bloque)", sell: 7 },
  { mat: "MELON_SLICE", name: "Rodaja de Sandía", sell: 1 },
  { mat: "NETHER_WART", name: "Verruga del Nether", sell: 20 },
  { mat: "POTATO", name: "Patata", sell: 15 },
  { mat: "PUMPKIN", name: "Calabaza", sell: 7 },
  { mat: "PUMPKIN_SEEDS", name: "Semillas de Calabaza", sell: 1 },
  { mat: "RED_MUSHROOM", name: "Champiñón Rojo", sell: 1 },
  { mat: "SUGAR_CANE", name: "Caña de Azúcar", sell: 3 },
  { mat: "WHEAT", name: "Trigo", sell: 20 },
  { mat: "WHEAT_SEEDS", name: "Semillas de Trigo", sell: 1 },
  { mat: "SWEET_BERRIES", name: "Bayas Dulces", sell: 7 }
];

const mobsRaw = [
  { mat: "ARROW", name: "Flecha", sell: 1 },
  { mat: "BLAZE_POWDER", name: "Polvo de Blaze", sell: 1 },
  { mat: "BLAZE_ROD", name: "Vara de Blaze", sell: 2 },
  { mat: "BREEZE_ROD", name: "Vara de Breeze", sell: 2 },
  { mat: "BONE", name: "Hueso", sell: 4 },
  { mat: "ENDER_PEARL", name: "Perla de Ender", sell: 5 },
  { mat: "FEATHER", name: "Pluma", sell: 1 },
  { mat: "GUNPOWDER", name: "Pólvora", sell: 4 },
  { mat: "MAGMA_CREAM", name: "Crema de Magma", sell: 20 },
  { mat: "PHANTOM_MEMBRANE", name: "Membrana de Phantom", sell: 3 },
  { mat: "RABBIT_FOOT", name: "Pata de Conejo", sell: 1 },
  { mat: "RABBIT_HIDE", name: "Piel de Conejo", sell: 2 },
  { mat: "ROTTEN_FLESH", name: "Carne Podrida", sell: 2 },
  { mat: "SLIME_BALL", name: "Bola de Slime", sell: 7 },
  { mat: "SPIDER_EYE", name: "Ojo de Araña", sell: 1 },
  { mat: "STRING", name: "Hilo", sell: 15 },
  { mat: "PRISMARINE_SHARD", name: "Fragmento Prismarina", sell: 5 },
  { mat: "LEATHER", name: "Cuero", sell: 3 },
  { mat: "HONEYCOMB", name: "Panal", sell: 3 }
];

console.log("Farmeo:", farmeoRaw.length, "Mobs:", mobsRaw.length, "Total:", farmeoRaw.length + mobsRaw.length);
