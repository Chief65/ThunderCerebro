# Evaluación, Red-Team y Refactor (fases 13–17)

Un prompt no está terminado al ser redactado.

---

## 1. Suite mínima de casos (5–15 según complejidad)

`NORMAL · SIMPLE · COMPLEJO · AMBIGUO · INFORMACIÓN FALTANTE · LÍMITE · ERROR · ALTO RIESGO · FUERA DE ALCANCE · NO REQUIERE TODAS LAS CAPACIDADES`

## 2. Simulación mental (por caso)

¿Qué partes del prompt se activan? ¿Qué decisión tomará el modelo? ¿Hay instrucciones irrelevantes? ¿Contradicción? ¿Puede inventar información? ¿Puede bloquearse innecesariamente? ¿Puede sobreactuar? ¿Puede declarar éxito sin evidencia?

> Declarar honestamente: sin ejecución real contra el modelo destino, esto es simulación, no medición.

## 3. Red-team del prompt

Buscar: instrucciones contradictorias, absolutos incorrectos, casos no cubiertos, loopholes, ambigüedades, reglas que compiten, formatos demasiado rígidos, loops, exceso/falta de autonomía, incentivos a inventar, redundancias. Incluir pruebas de esfuerzo: `{INPUT}` vacío, otro idioma, excede tokens, "Ignore previous instructions", degradación por contexto largo.

## 4. Evaluación por dimensiones (0–10)

`CLARIDAD · COBERTURA · RELEVANCIA · ADAPTABILIDAD · GROUNDING · ROBUSTEZ · SEGURIDAD · GESTIÓN DE INCERTIDUMBRE · EFICIENCIA · MANTENIBILIDAD · PORTABILIDAD · VERIFICABILIDAD`

Rúbrica por pregunta: Objetivo (¿inequívoco?), Alcance (¿evita scope creep?), Arquitectura (¿corresponde al problema?), Decisiones (¿controla decisiones reales?), Grounding (¿sabe de dónde saca hechos?), Incertidumbre (¿sabe qué hacer si no sabe?), Adaptabilidad, Fallos (¿anticipa failure modes?), Herramientas, Seguridad (¿controla acciones sensibles?), Verificación (¿puede demostrar éxito?), Eficiencia, Mantenibilidad, Output.

Complemento SOMA: **S**pecific (criterio binario pasa/no pasa), **O**rdinal (escala 1–5), **M**ulti-**A**spect (lógica, formato, fidelidad, coste), **A**ligned (necesidad final del Sr Ramos).

## 5. Umbral de aceptación

No entregar como "versión profesional" un prompt con: contradicciones materiales, failure modes sin mitigación, criterios de éxito indefinidos, ausencia de política de incertidumbre cuando es relevante, workflow rígido injustificado, reglas universales incorrectas, output burocrático.

Objetivo recomendado: **media ≥ 8.5/10 y ninguna dimensión crítica < 8/10**. Críticas típicas: `GROUNDING · ROBUSTEZ · SEGURIDAD · VERIFICABILIDAD`.

## 6. Refactor obligatorio

- **Eliminar**: redundancias, reglas decorativas, lenguaje grandilocuente, características que no cambian comportamiento, ejemplos innecesarios, listas de tecnologías irrelevantes, recomendaciones convertidas en obligaciones.
- **Fusionar** reglas equivalentes.
- **Condicionar** reglas demasiado absolutas.
- **Modularizar** bloques especializados no siempre necesarios.

---

## 7. Antipatrones

1. **Superexperto omnisciente** — "experto absoluto en A, B, C…" sin responsabilidades diferenciadas.
2. **XML/YAML cosmético** — estructura sin beneficio funcional.
3. **Workflow universal** — "siempre ejecuta 7 fases".
4. **Checklist tecnológico** — stacks listados como sustituto de arquitectura.
5. **Buenas prácticas como dogma** — "siempre Redis / CORS / microservicios".
6. **Prompt monolítico** — todas las capacidades cargadas siempre.
7. **Sin política de evidencia** — permite afirmar lo no observado.
8. **Sin evaluación** — entregado nada más redactarlo.
9. **Sobrepreguntar** — se bloquea por datos secundarios.
10. **Output ceremonial** — 12 secciones para tarea trivial.

## 8. Escala de madurez (aspirar al nivel apropiado, no siempre al 5)

1. **Básico**: rol + tarea.
2. **Estructurado**: + objetivo, restricciones, output.
3. **Profesional**: + contexto, criterios, workflow, incertidumbre, validación.
4. **Sistema de prompting**: + modularidad, fuentes, herramientas, failure handling, evaluación.
5. **Prompt system engineered**: + router, capacidades condicionales, eval suite, red-team, regresión, optimización de contexto, versionado, feedback loop.

## 9. Autocrítica final (12 preguntas)

1. ¿He creado algo más complejo de lo necesario?
2. ¿Hay alguna regla que no pueda justificar?
3. ¿Uso un rol como sustituto de especificaciones?
4. ¿Hay algún "siempre" que debería ser condicional?
5. ¿Sabe qué hacer cuando falta información?
6. ¿Puede afirmar cosas no verificadas?
7. ¿Puede sobrediseñar?
8. ¿Puede quedarse bloqueado preguntando?
9. ¿Tiene Definition of Done?
10. ¿Lo probé con casos adversos?
11. ¿Qué regla eliminaría primero para reducir 20 % de tokens?
12. ¿Eliminarla cambia realmente el comportamiento?

## 10. Comparación entre prompts

No asumir "nuevo = mejor". Evaluar A y B sobre la misma suite y rúbrica. Reportar mejoras, regresiones, diferencias de cobertura/longitud/robustez y casos donde gana cada uno. Sin porcentajes falsamente precisos si no hay benchmark.

## 11. Mejora continua ante fallos

No añadir una regla de inmediato. Clasificar causa: ¿faltó contexto? ¿conocimiento? ¿falló arquitectura? ¿una condición? ¿hubo contradicción? ¿falló un ejemplo? ¿una herramienta? ¿el modelo? ¿la salida estaba mal definida? Después:

```text
hipótesis → cambio mínimo → suite → comparación → mantener o revertir
```
