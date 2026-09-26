# ⛏️ Análisis de Minas — CataMines
> Última actualización: 2026-08-17 | Fuente: plugins/CataMines/mines/ (servidor Survival)

---

## 📌 Resumen del Sistema de Minas

Las minas funcionan en el mundo Dungeons. Cada mina tiene dos tipos de bloques:
- Piedra (stone) → bloque relleno, no da drops especiales
- Bloque de Amatista (amethyst_block) → bloque valioso, activa la loot table al romperlo

Al romper un bloque de amatista, SIEMPRE cae 1x Cristal Estelar (vendible a $10 c/u vía /sellgui),
MÁS tiradas de probabilidad adicionales para items especiales.

---

## 🏆 Progresión de Minas (de menor a mayor tier)

| # | Mina      | Archivo             | Bloque Amatista | Piedra  | Reset |
|---|-----------|---------------------|:-----------:|:-------:|:-----:|
| 1 | Inicial   | minainicialnew.yml  | 20.25%      | 79.75%  | 180s  |
| 2 | Knight    | minaknightnew.yml   | 30.25%      | 69.75%  | 180s  |
| 3 | Héroe     | minaheroenew.yml    | 40.25%      | 59.75%  | 220s  |
| 4 | Legend    | minalegendnew.yml   | 50.25%      | 49.75%  | 220s  |
| 5 | Mythic    | minamythicnew.yml   | 60.25%      | 39.75%  | 280s  |
| 6 | Titan     | minatitannew.yml    | 70.25%      | 29.75%  | 280s  |
| 7 | PvP       | minapvp.yml         | 80.00%      | 20.00%  | 480s  |

NOTA: Los archivos Inicial.yml y Knight.yml (sin "new") son versiones legacy. El análisis usa los *new.yml.

---

## 💰 Ingreso Base por Mina — Cristal Estelar ($10 c/u)

Cada bloque de amatista roto GARANTIZA 1 Cristal Estelar ($10).
Cálculo: Por cada 100 bloques minados → X bloques de amatista → X × $10

| Mina    | Cristales por 100 bloques | Ingresos por 100 bloques |
|---------|:------------------------:|:------------------------:|
| Inicial | ~20.25                   | ~$202                    |
| Knight  | ~30.25                   | ~$302                    |
| Héroe   | ~40.25                   | ~$402                    |
| Legend  | ~50.25                   | ~$502                    |
| Mythic  | ~60.25                   | ~$602                    |
| Titan   | ~70.25                   | ~$702                    |
| PvP     | ~80.00                   | ~$800                    |

---

## 🎰 Desglose de Drops Especiales por Mina

IMPORTANTE: Los drops especiales SOLO se tiran al romper un bloque de amatista.
Las probabilidades están expresadas como % sobre cada bloque de AMATISTA roto.

---

### 🟢 Mina Inicial (minainicialnew.yml)
Bloques: 20.25% amatista / 79.75% piedra | Reset: 3 minutos

| Item             | Nombre en juego          | % por amatista | % por bloque |
|------------------|--------------------------|:--------------:|:------------:|
| Cristal Estelar  | Vendible — $10 c/u       | 100%           | 20.25%       |
| Bolsa de Dinero  | $500–$2,000 al abrir     | 0.008%         | 0.0016%      |
| Pieza Super      | Llave SUPER (1 estrella) | 0.015%         | 0.0030%      |

Ratios:
- Bolsa de Dinero: 1 cada ~12,500 amatistas rotas
- Pieza Super:     1 cada ~6,667 amatistas rotas

---

### ⚔️ Mina Knight (minaknightnew.yml)
Bloques: 30.25% amatista / 69.75% piedra | Reset: 3 minutos

| Item             | Nombre en juego          | % por amatista | % por bloque |
|------------------|--------------------------|:--------------:|:------------:|
| Cristal Estelar  | Vendible — $10 c/u       | 100%           | 30.25%       |
| Bolsa de Dinero  | $500–$2,000 al abrir     | 0.100%         | 0.0303%      |
| Pieza Super      | Llave SUPER (1 estrella) | 0.018%         | 0.0054%      |

Ratios:
- Bolsa de Dinero: 1 cada ~1,000 amatistas rotas
- Pieza Super:     1 cada ~5,556 amatistas rotas

---

### 🦸 Mina Héroe (minaheroenew.yml)
Bloques: 40.25% amatista / 59.75% piedra | Reset: 3 min 40s

| Item             | Nombre en juego          | % por amatista | % por bloque |
|------------------|--------------------------|:--------------:|:------------:|
| Cristal Estelar  | Vendible — $10 c/u       | 100%           | 40.25%       |
| Bolsa de Dinero  | $500–$2,000 al abrir     | 0.120%         | 0.0483%      |
| Pieza Super      | Llave SUPER (1 estrella) | 0.022%         | 0.0089%      |
| Pieza Rara       | Llave RARA (2 estrellas) | 0.006%         | 0.0024%      |

Ratios:
- Bolsa de Dinero: 1 cada ~833 amatistas
- Pieza Rara:      1 cada ~16,667 amatistas

---

### 🌟 Mina Legend (minalegendnew.yml)
Bloques: 50.25% amatista / 49.75% piedra | Reset: 3 min 40s

| Item             | Nombre en juego            | % por amatista | % por bloque |
|------------------|----------------------------|:--------------:|:------------:|
| Cristal Estelar  | Vendible — $10 c/u         | 100%           | 50.25%       |
| Bolsa de Dinero  | $500–$2,000 al abrir       | 0.150%         | 0.0754%      |
| Pieza Super      | Llave SUPER (1 estrella)   | 0.028%         | 0.0141%      |
| Pieza Rara       | Llave RARA (2 estrellas)   | 0.008%         | 0.0040%      |
| Pieza Gadgets    | Llave EPICA (3 estrellas)  | 0.003%         | 0.0015%      |

Ratios:
- Bolsa de Dinero: 1 cada ~667 amatistas
- Pieza Gadgets:   1 cada ~33,333 amatistas

---

### 💜 Mina Mythic (minamythicnew.yml)
Bloques: 60.25% amatista / 39.75% piedra | Reset: 4 min 40s

| Item             | Nombre en juego            | % por amatista | % por bloque |
|------------------|----------------------------|:--------------:|:------------:|
| Cristal Estelar  | Vendible — $10 c/u         | 100%           | 60.25%       |
| Bolsa de Dinero  | $500–$2,000 al abrir       | 0.180%         | 0.1085%      |
| Pieza Super      | Llave SUPER (1 estrella)   | 0.035%         | 0.0211%      |
| Pieza Rara       | Llave RARA (2 estrellas)   | 0.010%         | 0.0060%      |
| Pieza Gadgets    | Llave EPICA (3 estrellas)  | 0.004%         | 0.0024%      |
| Pieza Mítica     | Llave MITICA (4 estrellas) | 0.001%         | 0.0006%      |

Ratios:
- Bolsa de Dinero: 1 cada ~556 amatistas
- Pieza Mítica:    1 cada ~100,000 amatistas

---

### 👑 Mina Titan (minatitannew.yml)
Bloques: 70.25% amatista / 29.75% piedra | Reset: 4 min 40s

| Item             | Nombre en juego            | % por amatista | % por bloque |
|------------------|----------------------------|:--------------:|:------------:|
| Cristal Estelar  | Vendible — $10 c/u         | 100%           | 70.25%       |
| Bolsa de Dinero  | $500–$2,000 al abrir       | 0.200%         | 0.1405%      |
| Pieza Super      | Llave SUPER (1 estrella)   | 0.040%         | 0.0281%      |
| Pieza Rara       | Llave RARA (2 estrellas)   | 0.015%         | 0.0105%      |
| Pieza Gadgets    | Llave EPICA (3 estrellas)  | 0.005%         | 0.0035%      |
| Pieza Mítica     | Llave MITICA (4 estrellas) | 0.001%         | 0.0007%      |

Ratios:
- Bolsa de Dinero: 1 cada ~500 amatistas
- Pieza Mítica:    1 cada ~100,000 amatistas

---

### ⚔️🔥 Mina PvP (minapvp.yml)
Bloques: 80% amatista / 20% piedra | Reset: 8 minutos (zona PvP activa)
AVISO: Mina de riesgo alto — zona PvP, coordenadas distintas a las demás

| Item             | Nombre en juego              | % por amatista | % por bloque |
|------------------|------------------------------|:--------------:|:------------:|
| Cristal Estelar  | Vendible — $10 c/u           | 100%           | 80.00%       |
| Bolsa de Dinero  | $500–$2,000 al abrir         | 0.300%         | 0.2400%      |
| Pieza Super      | Llave SUPER (1 estrella)     | 0.080%         | 0.0640%      |
| Pieza Rara       | Llave RARA (2 estrellas)     | 0.040%         | 0.0320%      |
| Pieza Gadgets    | Llave EPICA (3 estrellas)    | 0.015%         | 0.0120%      |
| Pieza Mítica     | Llave MITICA (4 estrellas)   | 0.004%         | 0.0032%      |
| Pieza Limited    | Llave DIVINA (5 estrellas)   | 0.001%         | 0.0008%      |

Ratios:
- Bolsa de Dinero: 1 cada ~333 amatistas
- Pieza Limited:   1 cada ~100,000 amatistas (EXCLUSIVA de esta mina)

---

## 📊 Tabla Comparativa Global

### % por bloque de AMATISTA roto

| Drop              | Inicial | Knight | Héroe  | Legend | Mythic | Titan  | PvP    |
|-------------------|:-------:|:------:|:------:|:------:|:------:|:------:|:------:|
| Cristal Estelar   | 100%    | 100%   | 100%   | 100%   | 100%   | 100%   | 100%   |
| Bolsa de Dinero   | 0.008%  | 0.1%   | 0.12%  | 0.15%  | 0.18%  | 0.2%   | 0.3%   |
| Pieza Super       | 0.015%  | 0.018% | 0.022% | 0.028% | 0.035% | 0.04%  | 0.08%  |
| Pieza Rara        | —       | —      | 0.006% | 0.008% | 0.01%  | 0.015% | 0.04%  |
| Pieza Gadgets     | —       | —      | —      | 0.003% | 0.004% | 0.005% | 0.015% |
| Pieza Mítica      | —       | —      | —      | —      | 0.001% | 0.001% | 0.004% |
| Pieza Limited     | —       | —      | —      | —      | —      | —      | 0.001% |

---

## 🔑 Sistema de Llaves Especiales

| Rareza | Material      | Pieza         | Estrellas   |
|--------|---------------|---------------|-------------|
| SUPER  | lime_dye      | Pieza Super   | ⭐☆☆☆☆      |
| RARA   | blue_dye      | Pieza Rara    | ⭐⭐☆☆☆     |
| EPICA  | yellow_dye    | Pieza Gadgets | ⭐⭐⭐☆☆    |
| MITICA | red_dye       | Pieza Mítica  | ⭐⭐⭐⭐☆   |
| DIVINA | white_dye     | Pieza Limited | ⭐⭐⭐⭐⭐  |

Las piezas se intercambian en /llaves para obtener llaves de cofre completas.

---

## 📝 Notas Técnicas

- Plugin: CataMines v2.5.11 (jar activo, sin .dis)
- Mundo: Dungeons para todas las minas de rango
- Mina PvP: misma dimension Dungeons pero coordenadas completamente distintas
- Modo reset: TIME (tiempo fijo), NO por porcentaje minado
- Fortune: false en todas las minas (las herramientas con Fortune NO multiplican drops)
- Los drops de la loot table son independientes entre sí (tiradas separadas por item)
- Bolsa de Dinero da entre $500 y $2,000 al abrirla (via ExecutableItems ei-id: bolsadedinero)
- Archivos legacy sin uso activo: Inicial.yml, Knight.yml (sin "new")
