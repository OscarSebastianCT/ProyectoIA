import os  # sistema operativo
import requests  # posibilita generar peticiones
from dotenv import load_dotenv  # load_dotenv carga las variables de entorno

load_dotenv()

# ---------- CONSTANTES ----------
API_KEY = os.getenv("GEMINI_API_KEY")
MODELO = "gemini-flash-latest"  # se cambia aquí si queremos otro modelo
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


# 1) ARMAR PETICIÓN: recibe la pregunta y devuelve la url y el body
def armar_peticion(pregunta):
    url = f"{URL_BASE}/{MODELO}:generateContent?key={API_KEY}" 
    #se ve ejemplo: "https://generativelanguage.googleapis.com/v1beta/models/gemini-3:generateContent?key=API_KEY"

    body = {
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
    respuesta = requests.post(url, json=body)
    return respuesta.json()


# 3) EXTRAER TEXTO: recibe los datos (JSON) y saca solo el texto de la respuesta
def extraer_texto(datos):
    return datos["candidates"][0]["content"]["parts"][0]["text"]

# CONEXIÓN: invoca las 3 funciones en orden
def obtener_datos_de_pruebas(pregunta):
    url, body = armar_peticion(pregunta)  # 1. crea url y body
    datos = enviar_peticion(url, body)    # 2. envía la petición
    return extraer_texto(datos)           # 3. extrae el texto


print(obtener_datos_de_pruebas("confirma si mi conexion esta funcionando."))