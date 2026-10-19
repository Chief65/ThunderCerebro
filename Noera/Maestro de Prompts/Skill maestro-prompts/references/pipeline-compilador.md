# Pipeline del Compilador — Fases 0 a 12 (detalle)

Ejecutar internamente antes de redactar. No exponer todo al usuario: entregar el resultado, no la burocracia.

---

## Fase 0 — Interpretar la petición

Extraer: `OBJETIVO REAL · USUARIO/OPERADOR · ENTORNO · TIPO DE TAREA · ENTRADAS · SALIDA DESEADA · RIESGO · AUTONOMÍA · HERRAMIENTAS · FUENTES EXTERNAS · MEMORIA/ESTADO`.

No confundir la forma literal con el objetivo. Ej.: "prompt para analizar una web" ≠ "actúa como desarrollador web"; puede implicar arquitectura, UX, UI, frontend, backend, seguridad, rendimiento, accesibilidad, QA, SEO, plataforma, release.

## Fase 1 — Modelar el dominio

Preguntas obligatorias: ¿qué subdisciplinas existen? ¿qué decisiones se toman? ¿qué entidades intervienen? ¿qué dependencias hay? ¿qué fuentes son fiables? ¿qué restricciones existen? ¿qué varía entre tareas? ¿qué es invariante?

Resultado: árbol `DOMINIO → subdominios`.

## Fase 2 — Seleccionar capacidades

- **Un único rol**: tarea homogénea, decisiones con mismo criterio, la coordinación no aporta.
- **Varios especialistas**: objetivos distintos, trade-offs entre áreas, dominio multidisciplinar, una sola identidad daría análisis superficial.
- **Router + especialistas**: preferido en prompts maestros complejos. **No activar especialistas innecesarios.**

Un rol solo existe con objetivo, criterio de optimización, responsabilidad, entradas y salida diferenciados.

## Fase 3 — Mapa de decisiones

No definir solo tareas: definir decisiones. Ej.: ¿modifico este archivo? ¿uso una dependencia? ¿pertenece a frontend o plataforma? ¿bug confirmado o hipótesis? ¿pregunto al usuario? ¿puedo continuar con seguridad? ¿necesito documentación externa? ¿el cambio requiere pruebas? ¿exige rollback? El prompt debe controlar estas decisiones.

## Fase 4 — Failure-first

Responder: ¿cómo puede fallar este agente? Fallos genéricos frecuentes: inventar capacidades, suponer archivos inexistentes, confundir recomendación con hecho, sobrediseñar, aplicar buenas prácticas sin contexto, modificar demasiado, declarar éxito sin pruebas, ignorar casos límite, introducir regresiones, usar herramienta incorrecta, no saber detenerse, preguntar demasiado / no preguntar cuando debe, salida imposible de validar.

Tabla interna:

| Failure mode | Probabilidad | Impacto | Mitigación |
|---|---:|---:|---|
| Inventar una API | alta | alta | exigir fuente/verificación |
| Scope creep | media | alta | cambio mínimo + alcance |
| Falsa validación | alta | alta | separar probado / no probado |

Prioriza alta probabilidad o alto impacto. Cada fallo importante lleva mitigación en el prompt.

## Fase 5 — Fuentes de verdad

Jerarquía genérica (adaptar al dominio):

1. Instrucción explícita actual del usuario.
2. Estado real de archivos/datos/runtime.
3. Documentación oficial vigente.
4. Documentación interna confirmada.
5. Estándares técnicos aplicables.
6. Buenas prácticas generales.
7. Inferencia del modelo.

Regla: una fuente inferior no reemplaza silenciosamente a una superior.

## Fase 6 — Política de evidencia

Para análisis, auditoría, investigación o modificación de sistemas reales: `[VERIFICADO] [MEDIDO] [INFERENCIA] [HIPÓTESIS] [POR-VERIFICAR] [BLOQUEADO]`. No incluir etiquetas si no aportan valor, pero impedir siempre afirmar como comprobado lo no comprobado.

## Fase 7 — Gestión de incertidumbre

- **Continuar** cuando la información ausente no cambia materialmente la solución, hay opción segura y reversible, o se puede declarar una suposición.
- **Preguntar** cuando la respuesta cambia una acción irreversible; hay riesgo significativo; afecta dinero, producción, seguridad, datos, permisos o contratos; o varias interpretaciones dan resultados materialmente distintos.
- **No inventar**: etiquetar la incertidumbre si falta evidencia.

## Fase 8 — Alcance y autonomía

Definir: `QUÉ PUEDE HACER · QUÉ NO DEBE · QUÉ NECESITA CONFIRMACIÓN · QUÉ PUEDE INFERIR · QUÉ PUEDE MODIFICAR · QUÉ DEBE PRESERVAR`. Para acciones sensibles no confiar solo en instrucción textual: requerir confirmación o control externo cuando aplique.

## Fase 9 — Workflow

Debe reflejar dependencias reales, permitir ramas condicionales, evitar fases irrelevantes, poder detenerse y definir recuperación ante fallos. Preferir:

```text
clasificar tarea → seleccionar capacidades → ejecutar solo pasos aplicables → validar → entregar
```

Evitar "siempre ejecuta fase 1→2→3→4".

## Fase 10 — Criterios de éxito

Todo prompt maestro responde: ¿cómo sabemos que terminó? ¿cómo sabemos que es bueno? Definir criterios de aceptación, propiedades obligatorias, errores bloqueantes, validaciones requeridas y condiciones de finalización.

## Fase 11 — Diseño de la salida

Derivada de la tarea. No imponer tablas, JSON o 10 secciones sin valor. Parseable si lo consume software; claro si lo consume una persona; proporcional; adaptativa. Cuando aplique answer engineering: esquema explícito, prefill determinista, cláusula anti-chatter.

## Fase 12 — Ensamblar

Secciones disponibles (usar solo las necesarias):

```text
FUNCIÓN / RESPONSABILIDAD · OBJETIVO · CRITERIOS DE ÉXITO · ALCANCE · FUENTES DE VERDAD
POLÍTICA DE EVIDENCIA · REGLAS / INVARIANTES · MODOS DE TRABAJO · CAPACIDADES / ROLES
WORKFLOW · GESTIÓN DE INCERTIDUMBRE · HERRAMIENTAS · SEGURIDAD / PERMISOS
VALIDACIÓN · FORMATO DE SALIDA · DEFINITION OF DONE
```

Delimitación: datos no confiables aislados (`<input_data>` / `<user_data>`) y tratados como dato no ejecutable. Reglas críticas y contrato de salida cerca del final en contextos largos (lost in the middle).

---

## Política de herramientas (si el prompt las usa)

Por herramienta: `QUÉ HACE · CUÁNDO USARLA · CUÁNDO NO · ARGUMENTOS · RETORNO · ERRORES`. Interfaces simples, sin redundancia, sin exponer APIs enormes sin necesidad.

## Arquitectura modular para sistemas grandes

```text
CORE
├── ROUTER
├── SPECIALIST_A / B / C
├── TOOL_POLICY
├── SAFETY_POLICY
└── EVALUATION_POLICY
```

Runtime: `CORE + ROUTER + SOLO LOS ESPECIALISTAS NECESARIOS + CONTEXTO REAL + TAREA`.
