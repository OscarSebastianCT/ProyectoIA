# Límites de la métrica de evaluación

## Qué mide

La métrica compara palabra por palabra la respuesta del modelo con una referencia escrita a mano, después de pasar ambas a minúsculas y quitar la puntuación. Calcula qué parte de la respuesta coincide con la referencia (precisión), qué parte de la referencia aparece en la respuesta (cobertura) y el equilibrio entre ambas (F1). No evalúa el significado ni si los datos son correctos.

## Modos de falla conocidos

- **Respuestas correctas con información extra puntúan bajo.** Ejemplo: caso #2, "¿cuándo se creó Python?". El modelo respondió "Python fue creado el 20-02-1991 por Guido van Rossum", que es correcto, y obtuvo F1 = 0.43, el más bajo de la corrida. En el caso #1 pasa lo mismo: agrega "alto nivel, propósito general, creado por Guido van Rossum" y queda con F1 = 0.48.
- **Decir lo mismo con otras palabras baja el F1.** Ejemplo: caso #21 (falla Km 152). La respuesta "el primer por qué fue que el riel tenía una fisura" es correcta, pero la referencia decía "el riel se quebró porque tenía una fisura": F1 = 0.53. En el caso #9 (OT 1003), "el trabajo realizado fue soldadura aluminotérmica en riel quebrado" es correcto y obtiene F1 = 0.45.
- **Los sinónimos no cuentan.** Ejemplo: caso #3. El modelo dijo que una lista es "mutable" y la referencia decía "modificable". Es la misma idea, pero no suma: F1 = 0.55.
- **Las tildes cuentan como palabras distintas.** Las referencias del Bloque 16 están sin tildes. En el caso #1, "programación" no coincide con "programacion", y en el caso #3, "colección" no coincide con "coleccion", aunque las respuestas están bien escritas.
- **Frases de relleno del modelo bajan la precisión.** Ejemplo: caso #5. "Se utilizó 12 m3 de balasto según el registro de la OT 1002" tiene el dato correcto, pero "según el registro" baja el F1 a 0.70. Lo mismo pasa en el caso #19, "duró 6 horas según el registro OT 1002", con F1 = 0.74.
- **No detecta si falta un dato pedido.** Ejemplo fuera de la muestra: caso #15. La pregunta era dónde son los trabajos más frecuentes; la referencia incluye "con 3 trabajos" y la respuesta no lo dice, pero igual obtiene F1 = 0.75. En el caso #23, la respuesta dice "pernos" sin especificar "de eclisa" y obtiene F1 = 0.76.
- **Un F1 perfecto puede venir de copiar el texto de entrada.** Ejemplo: caso #22 (causa raíz). La respuesta copia casi literal el "por qué 5" del registro: F1 = 1.00 confirma que coincide, no que el modelo entendió el análisis.
- **El formato de la respuesta contamina la métrica.** El modelo a veces responde dentro de una lista o un JSON. La limpieza borra los corchetes y comillas (el caso #16 obtuvo 1.00 igual), pero en los casos #13, #14, #17 y #20 se coló la palabra "respuesta" como un token más. En el caso #20 la cobertura es 1.00, pero la precisión baja a 0.54.

## Muestra revisada

De 23 resultados generados con `consultar_modelo` (modelo `gemini-3.5-flash-lite`), revisé 10 a mano, ordenando los resultados por F1: los 5 más bajos (casos #2, #9, #1, #21 y #3, con F1 entre 0.43 y 0.55) y los 5 más altos (casos #10, #7, #16, #18 y #22, con F1 entre 0.89 y 1.00). Cada caso fue calificado con la rúbrica de corrección factual, completitud y contradicción. El registro está en `revision_manual.py`.

Resultado: los 10 casos son correctos, completos y sin contradicciones. Es decir, en esta muestra **todos los F1 bajos correspondían a respuestas correctas**, castigadas por datos extra, redacción distinta, sinónimos o tildes. Los F1 altos sí correspondían a respuestas correctas, aunque en el caso #22 el puntaje viene de copiar el registro.

## Recomendación de uso

Para este pipeline, donde el modelo responde preguntas cortas sobre registros de OT, materiales, lugares y fallas de vía:

- **Usar el F1 para comparar en conjunto**, por ejemplo al probar un cambio de instrucción o de modelo sobre los 23 casos, y no para decidir si una respuesta individual está bien o mal.
- **Un F1 bajo (menor a 0.6) no significa que la respuesta esté mal.** En la muestra, los 5 casos más bajos eran correctos. Hay que revisarlos a mano antes de concluir algo.
- **Revisar a mano siempre las preguntas con números, cantidades o fechas**, porque la métrica no verifica que el dato sea el correcto ni detecta si falta (caso #15).
- **Revisar a mano siempre las preguntas abiertas**, como recomendaciones o acciones (caso #23).
- **Escribir las referencias con tildes y en una redacción parecida a la que se espera del modelo**, y pedirle que responda en texto plano, sin listas ni JSON, para no castigar respuestas correctas por escritura o formato.