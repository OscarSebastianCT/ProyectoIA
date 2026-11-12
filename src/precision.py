from collections import Counter
from .pipeline_limpieza import procesar_texto
from .cliente import consultar_modelo
import json
import time

def contar_coincidencias(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> int:
    """Cuenta cuántos tokens comparten ambas listas, respetando repeticiones."""
    conteo_referencia = Counter(tokens_referencia)
    conteo_respuesta = Counter(tokens_respuesta)
    interseccion = conteo_referencia & conteo_respuesta
    return sum(interseccion.values())

def calcular_precision_cobertura_f1(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> dict[str, float]:
    """Calcula precisión, cobertura y F1 de dos listas de tokens."""
    coincidencias = contar_coincidencias(
        tokens_referencia, tokens_respuesta
    )

    if not tokens_respuesta or not tokens_referencia:
        return {"precision": 0.0, "cobertura": 0.0, "f1": 0.0}

    precision = coincidencias / len(tokens_respuesta)
    cobertura = coincidencias / len(tokens_referencia)

    if precision + cobertura == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * cobertura / (precision + cobertura)

    resultado = {
        "precision": precision,
        "cobertura": cobertura,
        "f1": f1,
    }

    return resultado

def calcular_metricas(texto_referencia, texto_respuesta):
    tokens_referencia = procesar_texto(texto_referencia)
    tokens_respuesta = procesar_texto(texto_respuesta)
    return calcular_precision_cobertura_f1(tokens_referencia, tokens_respuesta)

# Registros de ejemplo (datos ficticios): el modelo responde usando estos datos
REGISTROS = {
    "OT 1001": "OT 1001 | Fecha: 03-11-2026 | Tipo: correctivo | Lugar: Km 152, sector Baquedano | Jefe de grupo: Pedro Rojas | Cuadrilla: 4 personas | Trabajo: reemplazo de eclisa fracturada | Materiales: 1 par de eclisas, 6 pernos de eclisa, 6 golillas | Horas: 3",
    "OT 1002": "OT 1002 | Fecha: 04-11-2026 | Tipo: preventivo | Lugar: Km 210, sector Sierra Gorda | Jefe de grupo: Luis Araya | Cuadrilla: 5 personas | Trabajo: nivelación y apisonado de vía | Materiales: 12 m3 de balasto | Horas: 6",
    "OT 1003": "OT 1003 | Fecha: 05-11-2026 | Tipo: correctivo | Lugar: Km 152, sector Baquedano | Jefe de grupo: Pedro Rojas | Cuadrilla: 3 personas | Trabajo: soldadura aluminotérmica en riel quebrado | Materiales: 1 porción aluminotérmica, 1 molde, 1 crisol | Horas: 4",
    "Semana 45": "Resumen semana 45: OT 1001, Km 152 sector Baquedano, correctivo, reemplazo de eclisa. OT 1002, Km 210 sector Sierra Gorda, preventivo, nivelación de vía. OT 1003, Km 152 sector Baquedano, correctivo, soldadura aluminotérmica. OT 1004, Km 238 sector Carmen Alto, preventivo, inspección de cambio. OT 1005, Km 152 sector Baquedano, correctivo, cambio de durmientes. OT 1006, Km 210 sector Sierra Gorda, correctivo, reapriete de pernos.",
    "Falla Km 152": "Reporte de falla: riel quebrado en Km 152, sector Baquedano. Por qué 1: el riel tenía una fisura. Por qué 2: la junta con eclisa estaba suelta. Por qué 3: los pernos de la eclisa perdieron apriete. Por qué 4: no se hizo el reapriete programado. Por qué 5: la pauta de mantenimiento no incluía el reapriete de pernos. Materiales involucrados: riel, eclisa y pernos de eclisa.",
}

INSTRUCCION = "responde en español en una sola oracion de maximo 20 palabras, sin introduccion. si hay un registro, usa solo sus datos y escribe numeros, fechas y abreviaturas tal como aparecen en el."

def consultar(ot, pregunta):
    """Arma la consulta (con el registro si hay OT), llama al modelo y devuelve solo el texto."""
    consulta = f"{REGISTROS[ot]}\n\nPregunta: {pregunta}" if ot else pregunta
    texto = consultar_modelo(consulta, system_instruction=INSTRUCCION)
    try:
        return json.loads(texto)["respuesta"]  # si viene como {"respuesta": "..."}
    except (json.JSONDecodeError, KeyError, TypeError):
        return texto

# Cada caso: (ot, consulta, referencia)
casos = [
    # 1
    (None, "¿que es python?", "python es un lenguaje de programacion interpretado."),
    # 2
    (None, "¿cuando se creo python?", "python fue creado en 1991."),
    # 3
    (None, "¿que es una lista en python?", "una lista en python es una coleccion ordenada y modificable."),
    # 4
    ("OT 1001", "¿Qué materiales se utilizaron?", "En la OT 1001 se utilizaron 1 par de eclisas, 6 pernos de eclisa y 6 golillas."),
    # 5
    ("OT 1002", "¿Cuánto balasto se utilizó?", "En la OT 1002 se utilizaron 12 m3 de balasto."),
    # 6
    ("OT 1003", "¿Qué materiales se utilizaron?", "En la OT 1003 se utilizaron 1 porción aluminotérmica, 1 molde y 1 crisol."),
    # 7
    ("Falla Km 152", "¿Cuáles son los materiales involucrados en esta falla?", "Los materiales involucrados en la falla son el riel, la eclisa y los pernos de eclisa."),
    # 8
    ("OT 1001", "¿El trabajo es correctivo o preventivo?", "El trabajo de la OT 1001 es correctivo."),
    # 9
    ("OT 1003", "¿Qué trabajo se realizó?", "En la OT 1003 se realizó una soldadura aluminotérmica en un riel quebrado."),
    # 10
    ("Semana 45", "¿Cuántos trabajos se realizaron en la semana?", "En la semana 45 se realizaron 6 trabajos."),
    # 11
    ("Semana 45", "¿Cuántos trabajos fueron correctivos y cuántos preventivos?", "En la semana 45 hubo 4 trabajos correctivos y 2 preventivos."),
    # 12
    ("OT 1001", "¿Cuántas personas trabajaron y quién fue el jefe de grupo?", "En la OT 1001 trabajaron 4 personas y el jefe de grupo fue Pedro Rojas."),
    # 13
    ("OT 1002", "¿Quién fue el jefe de grupo?", "El jefe de grupo de la OT 1002 fue Luis Araya."),
    # 14
    ("OT 1002", "¿Dónde se realizó el trabajo?", "El trabajo de la OT 1002 se realizó en el Km 210, sector Sierra Gorda."),
    # 15
    ("Semana 45", "¿Dónde son los trabajos más frecuentes?", "Los trabajos más frecuentes fueron en el Km 152, sector Baquedano, con 3 trabajos."),
    # 16
    ("Semana 45", "¿Qué OT se realizaron en el sector Sierra Gorda?", "En el sector Sierra Gorda se realizaron las OT 1002 y 1006."),
    # 17
    ("Semana 45", "¿Qué trabajo se hizo en Carmen Alto y de qué tipo fue?", "En Carmen Alto se hizo una inspección de cambio de tipo preventivo."),
    # 18
    ("Falla Km 152", "¿Dónde ocurrió la falla?", "La falla ocurrió en el Km 152, sector Baquedano."),
    # 19
    ("OT 1002", "¿Cuántas horas duró el trabajo?", "El trabajo de la OT 1002 duró 6 horas."),
    # 20
    ("OT 1003", "¿En qué fecha se realizó el trabajo?", "La OT 1003 se realizó el 05-11-2026."),
    # 21
    ("Falla Km 152", "¿Cuál fue el primer por qué de la falla?", "El riel se quebró porque tenía una fisura."),
    # 22
    ("Falla Km 152", "¿Cuál es la causa raíz según los 5 porqués?", "La causa raíz es que la pauta de mantenimiento no incluía el reapriete de pernos."),
    # 23
    ("Falla Km 152", "¿Qué acción recomiendas para que la falla no se repita?", "Se debe incluir el reapriete de pernos de eclisa en la pauta de mantenimiento."),
]
resultados = []

for numero, (ot, consulta, referencia) in enumerate(casos, start=1):
    try:
        respuesta = consultar(ot, consulta)
    except RuntimeError:
        print(f"\n#{numero} falló, se salta: {consulta}")
        continue

    metricas = calcular_metricas(referencia, respuesta)
    print(f"\n#{numero} [{ot or 'Sin registro'}] Consulta:", consulta)
    print("Respuesta:", respuesta)
    print(f"Precision: {metricas['precision']:.2f} | Cobertura: {metricas['cobertura']:.2f} | F1: {metricas['f1']:.2f}")

    resultados.append({"numero": numero, "ot": ot, "consulta": consulta, "referencia": referencia, "respuesta": respuesta, **metricas, })
    time.sleep(3)

with open("resultados_metricas.json", "w", encoding="utf-8") as archivo:
    json.dump(resultados, archivo, indent=2, ensure_ascii=False)

def resumir_metricas(resultados):

    if not resultados:
        return {
            "precision_promedio": 0,
            "cobertura_promedio": 0,
            "f1_promedio": 0,
        }

    n = len(resultados)

    return {
        "precision_promedio": sum(
            r["precision"] for r in resultados
        ) / n,

        "cobertura_promedio": sum(
            r["cobertura"] for r in resultados
        ) / n,

        "f1_promedio": sum(r["f1"] for r in resultados) / n,
    }
print("\nPromedios")
print(resumir_metricas(resultados))

peores_casos = sorted( resultados, key=lambda r: r["f1"] )

for caso in peores_casos[:3]:
    print(caso["consulta"], caso[ "f1"])

# Muestra para la revisión manual: 5 con f1 más bajo + 5 con f1 más alto
muestra_para_revisar = peores_casos[:5] + peores_casos[-5:]
with open("muestra_para_revisar.json", "w", encoding="utf-8") as archivo:
    json.dump(muestra_para_revisar, archivo, indent=2, ensure_ascii=False)

print(f"\nGuardados {len(resultados)} de {len(casos)} resultados")

""""
referencia = procesar_texto(
    "python es un lenguaje de programacion interpretado."
)
texto_respuesta = consultar_modelo("¿qu es python?",
                                    system_instruction="responde en español con una definicion breve, en una sola oracion de maximo 15 palabras. sin listas, ejemplos ni introduccion")
    

respuesta = procesar_texto(texto_respuesta)
resultado = calcular_precision_cobertura_f1(referencia, respuesta)

print("Respuesta:", texto_respuesta)
print("Tokens de referencia:", len(referencia))
print("Tokens de respuesta:", len(respuesta))
print(resultado)
"""