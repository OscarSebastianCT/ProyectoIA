from collections import Counter
from .pipeline_limpieza import procesar_texto
from .cliente import consultar_modelo
import json

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

casos = [
    (
        "¿que es python?",
        "python es un lenguaje de programacion interpretado.",
    ),
    ("¿cuando se creo python?", "python fue creado en 1991."),
    (
        "¿que es una lista en python?",
        "una lista en python es una coleccion ordenada y modificable.",
    ),
]
resultados = []

for consulta, referencia in casos:
    respuesta = consultar_modelo(consulta,
                                system_instruction="responde en español con una definicion breve, en una sola oracion de maximo 15 palabras. sin listas, ejemplos ni introduccion")
    
    metricas = calcular_metricas(referencia, respuesta)
    print("Consulta:", consulta)
    print("Respuesta:", respuesta)
    print("Metricas:", metricas)


    resultados.append({"consulta": consulta, "respuesta": respuesta, **metricas, })

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
print("Promedios")
print(resumir_metricas(resultados))

peores_casos = sorted( resultados, key=lambda r: r["f1"] )

for caso in peores_casos[:3]:
    print(caso["consulta"], caso[ "f1"])

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