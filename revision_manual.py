import json

revision_manual = [

    # ---------- Casos con F1 bajo ----------

    {
        "numero": 2,
        "consulta": "¿cuando se creo python?",
        "f1": 0.43,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": (
            "respuesta correcta: 1991 (y la fecha 20-02-1991 también es real). agrega un dato extra "
            "(Guido van Rossum) y vino entre corchetes. aun siendo correcta, es el f1 más bajo de la corrida"
        ),
    },
    {
        "numero": 9,
        "consulta": "¿Qué trabajo se realizó? (OT 1003)",
        "f1": 0.45,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": (
            "dice el trabajo correcto (soldadura aluminotérmica en riel quebrado). baja la cobertura "
            "porque no repite 'en la OT 1003' ni los artículos 'una' y 'un' de la referencia"
        ),
    },
    {
        "numero": 1,
        "consulta": "¿que es python?",
        "f1": 0.48,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": (
            "correcta, pero agrega datos extra (alto nivel, propósito general, Guido van Rossum) que bajan "
            "la precisión. además la referencia dice 'programacion' sin tilde y la respuesta 'programación', "
            "por lo que esa palabra no coincide"
        ),
    },
    {
        "numero": 21,
        "consulta": "¿Cuál fue el primer por qué de la falla?",
        "f1": 0.53,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": (
            "responde lo del registro (el riel tenía una fisura), pero redactado como 'el primer por qué "
            "fue que...' mientras la referencia dice 'el riel se quebró porque...'. se castiga la redacción"
        ),
    },
    {
        "numero": 3,
        "consulta": "¿que es una lista en python?",
        "f1": 0.55,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": (
            "correcta. usa 'mutable' en vez de 'modificable' (sinónimo que no cuenta) y 'colección' con tilde "
            "vs 'coleccion' sin tilde en la referencia. también agrega datos extra y vino entre corchetes"
        ),
    },

    # ---------- Casos con F1 alto ----------

    {
        "numero": 10,
        "consulta": "¿Cuántos trabajos se realizaron en la semana?",
        "f1": 0.89,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "correcto (6 trabajos). solo agrega 'en total', que baja un poco la precisión",
    },
    {
        "numero": 7,
        "consulta": "¿Cuáles son los materiales involucrados en esta falla?",
        "f1": 0.90,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": (
            "correcto (riel, eclisa y pernos de eclisa). la cobertura no llega a 1 solo porque omite "
            "los artículos 'el', 'la' y 'los'"
        ),
    },
    {
        "numero": 16,
        "consulta": "¿Qué OT se realizaron en el sector Sierra Gorda?",
        "f1": 1.00,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": (
            "correcto (OT 1002 y 1006). el f1 1.00 refleja una respuesta perfecta; vino entre corchetes "
            "pero la limpieza los borró"
        ),
    },
    {
        "numero": 18,
        "consulta": "¿Dónde ocurrió la falla?",
        "f1": 1.00,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "correcto y textual (Km 152, sector Baquedano). aquí el f1 1.00 es confiable",
    },
    {
        "numero": 22,
        "consulta": "¿Cuál es la causa raíz según los 5 porqués?",
        "f1": 1.00,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": (
            "correcto, pero copia casi literal el 'por qué 5' del registro. el f1 1.00 confirma que "
            "coincide, no que el modelo entendió el análisis"
        ),
    },

]

with open("revision_manual.json", "w", encoding="utf-8") as archivo:
    json.dump(revision_manual, archivo, indent=2, ensure_ascii=False)

print(f"Guardados {len(revision_manual)} casos en revision_manual.json")