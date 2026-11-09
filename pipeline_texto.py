""" from pipeline_limpieza import *

referencia = "El cielo es azul."
respuesta = "el cielo es azul"

tokens_referencia = procesar_texto(referencia)
tokens_respuesta = procesar_texto(respuesta)

comunes = set(tokens_referencia) & set(tokens_respuesta)

if tokens_referencia:
    proporcion = len(comunes) / len(set(tokens_referencia))
else:
    proporcion = 0.0

print(f"Coincidencia: {proporcion:.0%}")"""

from cliente import consultar_modelo
from pipeline_limpieza import procesar_texto

consulta = "¿Qué es Python?"
referencia = "Python es un lenguaje de programación de alto nivel, interpretado y de propósito general."
respuesta = consultar_modelo(consulta)

crudo_ref = referencia.split()
crudo_resp = respuesta.split()

comunes_crudo = set(crudo_ref) & set(crudo_resp)
pct_crudo = len(comunes_crudo) / len(set(crudo_ref))

tokens_ref = procesar_texto(referencia)
tokens_resp = procesar_texto(respuesta)

comunes = set(tokens_ref) & set(tokens_resp)
pct_proc = len(comunes) / len(set(tokens_ref))


print(f"[Caso 1] Coincidencia texto crudo: {pct_crudo:.1%}")
print(f"[Caso 1] Coincidencia texto procesado: {pct_proc:.1%}")