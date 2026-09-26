# EsquemaEstiloItems.md
# Guia interna de referencia para crear items en el estilo exacto del servidor ThunderStudios Survival
# Generada por Antigravity IA | Actualizada: 2026-08-17

---

## 1. ESTRUCTURA BASE DEL YAML

Cada item sigue este esquema fijo:

```
<id_del_item>:
  item:
    ==: org.bukkit.inventory.ItemStack
    DataVersion: 4671
    id: minecraft:<material>
    count: 1
    components:
      minecraft:lore: '...'
      minecraft:custom_name: '...'
      minecraft:enchantments: '...'
      [minecraft:attribute_modifiers: '...' si tiene stats custom]
    schema_version: 1
```

- Los IDs son siempre en minusculas, sin espacios ni tildes (snake_case sin guiones bajos preferiblemente)
- DataVersion: 4671 (fijo para 1.21)
- schema_version: 1 (siempre al final, SIN indentacion extra bajo components)

---

## 2. ESTRUCTURA DEL NOMBRE (custom_name)

### Patron general:
- Cada caracter del nombre va en su propio objeto JSON
- Todos usan: bold:0b, obfuscated:0b, strikethrough:0b, underlined:0b, italic:0b
- El emoji de icono va al inicio y al final
- El espacio entre palabras es un caracter separado con su propio color
- El ultimo emoji y el espacio/string vacio final suelen mantener el color final del gradiente

### Template de un caracter:
{bold:0b,color:"#RRGGBB",italic:0b,obfuscated:0b,strikethrough:0b,text:"X",underlined:0b}

### Emojis por tipo de arma:
- Espada:  🗡  (U+1F5E1)
- Hacha:   🪓  (U+1FA93)
- Arco:    🏹  (U+1F3F9)
- Ballesta: 🏹 (mismo)
- Mazo:    🪧  (U+1FA67) o 🔨
- Lanza:   ⚜   (U+269C)
- Tridente: ♆  (U+2646)
- Escudo:  🛡   (U+1F6E1)
- Casco/Armadura: 🛡

### Saltos de linea en YAML:
Cuando el texto es largo, el servidor usa un salto real dentro del string YAML:
  text:"Texto largo\n  continuacion"
Esto se debe respetar igual que en el original.

---

## 3. GRADIENTES DE COLOR (COMO SE CALCULAN)

El degradado va letra por letra, interpolando linealmente entre color inicio y color fin.

### Formula:
  paso_R = (R_fin - R_ini) / (num_chars - 1)
  paso_G = (G_fin - G_ini) / (num_chars - 1)
  paso_B = (B_fin - B_ini) / (num_chars - 1)
  color_N = #(R_ini + N*paso_R)(G_ini + N*paso_G)(B_ini + N*paso_B)

### Regla observada: el ultimo caracter (emoji final) y el penultimo suelen tener el mismo color final.
### El espacio inicial (despues del primer emoji) tambien tiene un color entre inicio y primer char.

### Gradientes morados de referencia (EPICA):
| Variante       | Inicio    | Fin       | Descripcion                    |
|----------------|-----------|-----------|--------------------------------|
| Violeta puro   | #8B00FF   | #C060FF   | Purpura vivo, luminoso         |
| Indigo-violeta | #6600CC   | #AA44FF   | Mas oscuro, menos saturado     |
| Rosa-violeta   | #9C2F8D   | #001CFF   | Como espadaaracnofoba          |
| Cyan-violeta   | #7489FF   | #FF2FAD   | Como lanzaempaladora           |

---

## 4. ESTRUCTURA DEL LORE

### Patron estandar de la mayoria de items:
```
[
  "",                                            <- linea vacia inicial
  {extra:[{text:" "},{color:"dark_gray",text:"Efectos:"}],text:""},  <- cabecera
  {extra:[{text:" "},{color:"green",text:"✔ Efecto 1"}],text:""},    <- efecto(s)
  {extra:[{text:" "},{color:"green",text:"✔ Efecto 2"}],text:""},    <- (opcional)
  "",                                            <- linea vacia separadora
  {extra:[badge de calidad...],text:""}          <- badge SIEMPRE al final
]
```

### Cada linea de efectos usa este formato completo:
{extra:[
  {bold:0b,color:"white",italic:0b,obfuscated:0b,strikethrough:0b,text:" ",underlined:0b},
  {color:"green",italic:0b,text:"✔ Nombre del efecto"}
],text:""}

### Efectos en rojo (penalizaciones):
{color:"red",italic:0b,text:"-20% velocidad"}

### Linea de flavor/lore narrativo (OPCIONAL - algunos items no lo tienen):
{extra:[
  {bold:0b,...,text:" ",underlined:0b},
  {color:"gray",italic:0b,text:"«Texto de lore en cursiva gris»"}
],text:""}

---

## 5. BADGE DE CALIDAD (ultima linea del lore SIEMPRE)

El badge sigue este formato exacto:
{extra:[
  {bold:0b,color:"white",italic:0b,obfuscated:0b,strikethrough:0b,text:" ",underlined:0b},   <- ESPACIO DE SEPARACION (obligatorio)
  {bold:0b,color:"dark_gray",italic:0b,obfuscated:0b,strikethrough:0b,text:"⁂ ",underlined:0b},
  {bold:1b,color:"#COLOR1",italic:0b,obfuscated:0b,strikethrough:0b,text:"L1",underlined:0b},
  ...una entrada por cada letra de la calidad...
  {bold:0b,color:"yellow",italic:0b,text:"ESTRELLAS_LLENAS"},
  {color:"gray",italic:0b,text:"ESTRELLAS_VACIAS"}
],text:""}

### Colores y estrellas por calidad:
| Calidad | Letras | Colores del degradado (L→R)                          | Stars amarillas | Stars grises |
|---------|--------|-----------------------------------------------------|-----------------|--------------|
| SUPER   | S-U-P-E-R | #4BFD00→#47F504→#44EC08→#40E40C→#3CDB10          | ⭐              | ⭐⭐⭐⭐     |
| RARA    | R-A-R-A   | #008DFF→#0AA1FF→#13B4FF→#1DC8FF                   | ⭐⭐            | ⭐⭐⭐       |
| EPICA   | E-P-I-C-A | #A84EDE→#9B45DF→#8E3CE0→#8033E1→#732AE2           | ⭐⭐⭐          | ⭐⭐         |
| MITICA  | M-I-T-I-C-A | #B01111→#B61515→#BD1919→#C31E1E→#CA2222→#D02626 | ⭐⭐⭐⭐        | ⭐          |
| DIVINA  | D-I-V-I-N-A | #FD9A00→#FAAE00→#F7C200→#F5D700→#F2EB00→#EFFF00 | ⭐⭐⭐⭐⭐      | (ninguna)   |

NOTA: La ultima letra de la calidad siempre termina con " " (espacio) antes del cierre de comillas.
Ej: text:"A " no text:"A"

---

## 6. COSAS A EVITAR / ERRORES COMUNES

- NO usar unicode escapes (\u2714) si se puede escribir el char directo (✔ ⁂ ⭐)
  Aunque el servidor los acepta como JSON escapes, es mas limpio con el char directo.
- NO usar bold:1b en el nombre (siempre bold:0b en custom_name)
- NO dejar el badge de calidad sin espacio al final de la ultima letra
- NO olvidar la linea vacia "" al inicio del lore
- Los espacios entre palabras del nombre van como texto separado con su color interpolado
- El string vacio final "" en custom_name es opcional (algunos items lo tienen, otros no)
- schema_version: 1 va FUERA de components, como hermano de components

---

## 7. ITEMS CREADOS POR IA (LOG)

| Fecha      | ID              | Nombre          | Calidad | Material       | Notas                    |
|------------|-----------------|-----------------|---------|----------------|--------------------------|
| 2026-08-17 | pruebasdehoy    | Prueba de Hoy   | EPICA   | diamond_sword  | Primer item IA, gradiente morado->beige (corregir) |
| 2026-08-17 | espadavacio     | Espada del Vacio| EPICA   | diamond_sword  | Gradiente indigo puro    |
| 2026-08-17 | hachaumbratica  | Hacha Umbratica | EPICA   | diamond_axe    | Violeta luminoso         |
| 2026-08-17 | arcosombral     | Arco Sombral    | EPICA   | bow            | Purpura oscuro           |

