import os  # sistema operativo
import requests  # posibilita generar peticiones
from dotenv import load_dotenv  # load_dotenv carga las variables de entorno
import time


load_dotenv()

# ---------- CONSTANTES ----------
API_KEY = os.getenv("GEMINI_API_KEY")
MODELO = "gemini-3.6-flash"  # se cambia aquí si queremos otro modelo
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


# 1) ARMAR PETICIÓN: recibe la pregunta y devuelve la url y el body
def armar_peticion(modelo, pregunta, system_instruction):
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacia")
    url = f"{URL_BASE}/{modelo}:generateContent?key={API_KEY}" 
    #se ve ejemplo: "https://generativelanguage.googleapis.com/v1beta/models/gemini-3:generateContent?key=API_KEY"

    body = {
        "systemInstruction":{
            "parts": [ {"text": system_instruction}] #parts es partes del contenido y text el formato es trozo texto plano
            
        },
        "contents": [
            {
                "parts": [
                    {"text": pregunta}
                ]
            }
        ]
    }

    return url, body


# 2) ENVIAR PETICIÓN: recibe url y body, hace el POST y devuelve el JSON
def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body, timeout=30) #request.post es la peticion, request es la libreria y post es el metodo
    except requests.exceptions.ConnectionError: #ConectionError es un error de conexion especial de la libreria python
        raise RuntimeError ("No se pudo conectar con el servidor. intenta de nuevo mas tarde")
    except requests.exceptions.Timeout: #Timeout es un error de tiempo especial de la libreria python
        raise RuntimeError ("No se pudo conectar con el servidor. se acabo el tiempo de espera") #RuntimeError significa error de ejecucion en tiempo de ejecucion
    
    if respuesta.status_code != 200:
        raise RuntimeError (f"Error en la peticion. status code: {respuesta.status_code}")
    try: 
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError ("la respuesta que llego no es un JSON")





# 3) EXTRAER TEXTO: recibe los datos (JSON) y saca solo el texto de la respuesta
def extraer_texto(datos):
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError ("la repuesta no trae el texto generado en el lugar definido") #raise es para levantar un error
    #runtimeerror significa error de ejecucion en tiempo de ejecucion



# CONEXIÓN: invoca las 3 funciones en orden
def obtener_datos_de_pruebas(pregunta):
    system_instruction = "Quiero que me lo digas como comentarista de futbol"
    url, body = armar_peticion(MODELO, pregunta, system_instruction)

    inicio = time.perf_counter() #empezamos a contar el tiempo


    datos = enviar_peticion(url, body)    # 2. envía la petición

    fin = time.perf_counter() #terminamos de contar
    latencia = fin - inicio #tiempo de ejecución
    print(f"Latencia de la peticion: {latencia:.2f} segundos") #imprime la latencia, el punto 2f es la cantidad de decimales que queremos

    costo = calcular_costos(datos, 0.00000075, 0.00000375)
    print(f"Costo de la peticion: ${costo:.6f} USD")
    return extraer_texto(datos)           # 3. extrae el texto


def calcular_costos(datos:dict, precio_entrada:float, precio_salida:float):
    #datos = {dic... "usageMetadata"}
    try:
        uso = datos["usageMetadata"] #se usa metada porque es un diccionario que contiene la informacion de uso

        """"
        uso = {
            "promptTokenCount": 10,
            "candidatesTokenCount": 471,
            "totalTokenCount": 1377,
            "promptTokensDetails": [
                {
                    "modality": "TEXT",
                    "tokenCount": 10
                }
            ],
            "thoughtsTokenCount": 896,
            "serviceTier": "standard"
        }
        """
        tokens_entrada = uso["promptTokenCount"] 
        tokens_salida = uso["candidatesTokenCount"] 
        tokens_razonamiento = uso["thoughtsTokenCount"] 
    except KeyError as error:
        raise RuntimeError(f"La respuesta no trae el dato de uso esperado: {error}")

    costo = (tokens_entrada * precio_entrada) + (tokens_salida * precio_salida) + (tokens_razonamiento * precio_salida)
    return costo

try:
    print(obtener_datos_de_pruebas("funciona mi conexcion?"))
except (ValueError, RuntimeError) as error: # esta linea dice 
    print("no se puede completar la operacion", error)


""""        
quiero ejecutar 4 veces la misms peticion con 1 modelo
y ante cada peticion se calcular e imprime: latencia, costo, respuesta

vuelve a hacer lo mismo con distintos modelos
3 modelos a comparar

OBJETIVO: Elijas el mejor modelo para tu proyecto

con un pront relacionado con tu proyecto

comparacion y costo por request (en la pagina)


"""