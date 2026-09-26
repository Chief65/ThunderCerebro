# ⛏️ Arquitectura y Composición de Minas — CataMines (ThunderMC)

Datos exactos de bloques, porcentajes de generación y loot drops extraídos directamente de las configuraciones de `CataMines` en el servidor.

---

### 📊 Mecánica del Sistema de Minas
Todas las minas están compuestas por una matriz de **Piedra (`stone`)** + **Bloque de Amatista (`amethyst_block`)**.
- Al picar la **Amatista**, el plugin suelta ítems RPG customizados con lore, precios para `/sellgui` (`Cristal Estelar`, etc.) y drops especiales de **ExecutableItems** (`Bolsa de Dinero`, llaves de cajas, etc.).
- La **Piedra** representa el material base a limpiar.

---

### 1. Mina Inicial (`minainicialnew.yml`)
- **Piedra (`stone`)**: `79.75%`
- **Amatista Especial (`amethyst_block`)**: `20.25%`
  - Drop base: **Cristal Estelar** (`$10` en `/sellgui`) — `100%`
  - Drop especial: **Bolsa de Dinero [I]** ($500 - $2k) — `0.8%`
  - Drop especial secundario: `1.5%`

---

### 2. Mina Knight (`minaknightnew.yml`)
- **Piedra (`stone`)**: `69.75%`
- **Amatista Especial (`amethyst_block`)**: `30.25%`
  - Drop base: **Cristal Estelar** — `100%`
  - Drop especial: **Bolsa de Dinero [I]** — `10.0%`
  - Drop especial secundario: `1.8%`

---

### 3. Mina Héroe (`minaheroenew.yml`)
- **Piedra (`stone`)**: `59.75%`
- **Amatista Especial (`amethyst_block`)**: `40.25%`
  - Drop base: **Cristal Estelar** — `100%`
  - Drop especial: **Bolsa de Dinero [II]** — `12.0%`
  - Drop especial: **Llaves / Fragmentos** — `2.2%`
  - Drop especial superior: `0.6%`

---

### 4. Mina Legend (`minalegendnew.yml`)
- **Piedra (`stone`)**: `49.75%`
- **Amatista Especial (`amethyst_block`)**: `50.25%`
  - Drop base: **Cristal Estelar** — `100%`
  - Drop especial: **Bolsa de Dinero [II] / [III]** — `15.0%`
  - Drop especial: **Llaves / Gemas** — `2.8%`
  - Drop especial: `0.8%`
  - Drop raro: `0.3%`

---

### 5. Mina Mythic (`minamythicnew.yml`)
- **Piedra (`stone`)**: `39.75%`
- **Amatista Especial (`amethyst_block`)**: `60.25%`
  - Drop base: **Cristal Estelar** — `100%`
  - Drop especial: **Bolsa de Dinero [III]** — `18.0%`
  - Drop especial: `3.5%`
  - Drop especial: `1.0%`
  - Drop raro: `0.4%`
  - Drop ultra raro: `0.1%`

---

### 6. Mina Titán (`minatitannew.yml`)
- **Piedra (`stone`)**: `29.75%`
- **Amatista Especial (`amethyst_block`)**: `70.25%`
  - Drop base: **Cristal Estelar** — `100%`
  - Drop especial: **Bolsa de Dinero Máxima** — `20.0%`
  - Drop especial: `4.0%`
  - Drop especial: `1.5%`
  - Drop raro: `0.5%`
  - Drop ultra raro: `0.1%`

---

### ☠️ 7. Mina PvP (`minapvp.yml`)
- **Piedra (`stone`)**: `20.00%`
- **Amatista Especial (`amethyst_block`)**: `80.00%`
  - Drop base: **Cristal Estelar** — `100%`
  - Drop especial: **Bolsa de Dinero Legendaria** — `30.0%`
  - Drop especial: `8.0%`
  - Drop especial: `4.0%`
  - Drop raro: `1.5%`
  - Drop muy raro: `0.4%`
  - Drop ultra raro: `0.1%`
