import json
import time
from prompts.Banco import BANCO_DE_PROMPT
from consumir_gemini import armar_peticion, enviar_peticion, extraer_texto, parsear_respuesta_json

registro ={}

try:

    for prompt in BANCO_DE_PROMPT:
            exitos = 0
            intentos = 2
            for intento in range (intentos):
                url, body = armar_peticion("gemini-3.5-flash-lite",
                                            prompt["ejemplo_usuario"],
                                            prompt["system_instruction"],
                                            prompt["response_schema"]
                                            ) #armar_peticion(promt)
                respuesta = enviar_peticion(url, body) #enviar_peticion(url, body)
                texto = extraer_texto(respuesta) #extraer_texto(respuesta)
                try:
                    datos = parsear_respuesta_json(texto, prompt["claves_esperadas"]) #parsear_respuesta_json(texto, prompt["claves_requeridas"])
                    exitos += 1 #exitos ++         
                    print(f"Respuesta:{datos}")
                except ValueError as error:
                    print(f"Error en el intento {intento + 1} fallo: {error}")
                time.sleep(1)
            print(f"{prompt["nombre"]} exitos: {exitos}/{intentos} respuestas validas")
            registro[prompt["nombre"]] = {"exitos": exitos, "intentos": intentos}
        #cuanto termine de recorre los prompts quiero guarda esa infor en registro_resultados.json
    with open("src/prompts/registro_resultados.json", "w", encoding="utf-8") as archivo:
        json.dump(registro, archivo, indent=2, ensure_ascii=False)

except (ValueError, RuntimeError) as error:
    print("no se pudo completar la operacion", error)





