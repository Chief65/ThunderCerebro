# Módulo Creator — Laboratorio de Creación e I+D

Entorno dedicado a la ideación, prototipado, experimentación y generación de contenido avanzado (objetos ItemEdit, mecánicas de Minecraft 1.21.11, balances, lore y narrativas de ThunderStudios).

---

## 1. Principio de Aislamiento Estricto
* **Lectura libre**: Creator consume el conocimiento de `wiki/` y `raw/` como contexto y restricciones técnicas.
* **Escritura restringida**: Creator **NUNCA** modifica ni crea notas en `wiki/` ni en `raw/` de forma autónoma.
* **Promoción explícita**: Solo cuando el **Sr Ramos** lo ordene expresamente, un resultado final de `creator/output/` será documentado en la wiki oficial y registrado en `log.md`.

---

## 2. Estructura del Módulo

```text
creator/
├── README.md               # Este manifiesto
├── raw/                    # Ingesta en bruto para experimentos (inmutable)
│   ├── prompts/            # Ideas iniciales, notas rápidas, briefs
│   └── references/         # Ejemplos, fragmentos de configs externas
├── lab/                    # Espacio de trabajo iterativo / borradores
│   ├── items/              # Objetos ItemEdit en desarrollo, gradientes, tests
│   ├── mechanics/          # Mecánicas, sistemas de dungeons/minas
│   └── storylines/         # Narrativa, quests y lore THUNDERVERSE
└── output/                 # Resultados finales aprobados listos para producción
    ├── items/              # Archivos .yml listos para el servidor (/ie reload)
    ├── configs/            # Configs finales listas para desplegar
    └── blueprints/         # Diseños y planificaciones técnicas cerradas
```

---

## 3. Flujo de Trabajo en Creator

1. **Recepción / Ingesta (`creator/raw/`)**: Depósito de ideas base o referencias.
2. **Prototipado (`creator/lab/`)**: Iteración técnica, red teaming (exploits, balance, MSPT).
3. **Entrega (`creator/output/`)**: Archivo definitivo listo para uso o despliegue.
4. **Graduación a Memoria (Bajo petición)**: Migración ordenada a `wiki/`.
