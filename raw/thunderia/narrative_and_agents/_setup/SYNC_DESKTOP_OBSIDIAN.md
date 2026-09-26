# Cómo tener los mismos .md en Desktop/ThunderStudios, Obsidian y GitHub

La forma correcta de que "los mismos archivos" existan en Desktop, en tu
vault de Obsidian y en GitHub NO es mantener tres copias sincronizadas a
mano (eso se desincroniza tarde o temprano). La forma correcta es que
existan **una sola vez en disco**, y que Obsidian simplemente "vea" esa
misma carpeta a través de un enlace.

## Arquitectura recomendada

1. `Escritorio/ThunderStudios/` es el **repositorio Git real**, clonado
   directamente desde
   `https://github.com/sermadita7777/ThunderStudios`.
2. Dentro de tu vault de Obsidian, en la ruta
   `Proyectos/ThunderStudios/UnderDog`, en vez de copiar archivos, creas un
   **enlace simbólico (symlink)** que apunta a
   `Escritorio/ThunderStudios/UnderDog`.
3. Resultado: Obsidian, el Finder/Explorador y GitHub muestran literalmente
   el mismo archivo. Editas en Obsidian → el cambio ya está en
   Desktop/ThunderStudios → hate `git add . && git commit && git push` y
   ya está en GitHub. No hay "réplica" que pueda desincronizarse porque
   nunca hay dos copias, solo dos puertas de entrada al mismo archivo.

## Paso 1 — clona el repo en el escritorio

```bash
cd ~/Desktop      # macOS/Linux
git clone https://github.com/sermadita7777/ThunderStudios.git
```

En Windows (PowerShell), sustituye `~/Desktop` por
`$env:USERPROFILE\Desktop`.

## Paso 2 — crea el symlink hacia tu vault

Sustituye `RUTA_DE_TU_VAULT` por la ruta real de tu vault de Obsidian.

**Windows (PowerShell, como administrador):**
```powershell
New-Item -ItemType Junction `
  -Path "RUTA_DE_TU_VAULT\Proyectos\ThunderStudios\UnderDog" `
  -Target "$env:USERPROFILE\Desktop\ThunderStudios\UnderDog"
```
(Se usa Junction en vez de symlink normal para evitar el requisito de modo
desarrollador de Windows.)

**macOS / Linux:**
```bash
mkdir -p "RUTA_DE_TU_VAULT/Proyectos/ThunderStudios"
ln -s ~/Desktop/ThunderStudios/UnderDog \
      "RUTA_DE_TU_VAULT/Proyectos/ThunderStudios/UnderDog"
```

## Paso 3 — activa el plugin de Obsidian si hace falta
En vaults con "Files & Links" estricto, activa la opción de seguir enlaces
simbólicos (en versiones recientes de Obsidian esto funciona sin
configuración extra en Mac/Linux; en Windows puede requerir que el vault
esté indexado tras crear la Junction — simplemente reabre el vault).

## Paso 4 — enlaza el grafo
Con el symlink ya puesto, los wikilinks `[[Noob]]`, `[[Pro]]`, etc. que
ya vienen escritos en los documentos de `03_Characters/` funcionarán solos
en la vista de grafo de Obsidian, porque Obsidian ve las notas como si
estuvieran dentro del vault (que es literalmente lo que son).

## Flujo de trabajo del día a día
1. Escribes/editas en Obsidian con total normalidad.
2. Cuando quieras guardar versión en GitHub:
   ```bash
   cd ~/Desktop/ThunderStudios
   git add .
   git commit -m "Actualiza ficha de Valyr"
   git push
   ```
3. Si usas Antigravity CLI para escribir contenido, ejecútalo con
   `Escritorio/ThunderStudios` como carpeta de trabajo (`agy` dentro de esa
   carpeta) — así lee automáticamente `AGENTS.md` y las skills, y lo que
   escriba aparece también en Obsidian al instante por el symlink.
