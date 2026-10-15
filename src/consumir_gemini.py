import os #sistema operativo
import requests #posibilita generar peticiones
from dotenv import load_dotenv #load_dotenv carga las variables de entorno

load_dotenv()

def obtener_datos_de_pruebas(pregunta):
    api_key = os.getenv("GEMINI_API_KEY")

    modelo = "gemini-flash-latest" #el modelo que vamos a usar (lo podemos segun el modelo que queramos y se ve en la url de abajo)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}" #la url de la api   

    #apy_key en ves de mandarlo en encabezado lo mandamos direcatmante por la url

    body = {
        "contents": [
        {
            "parts":[
            {
                "text": pregunta
            }
            ]
        }
        ]
    }

    response = requests.post(url, json=body) #genera la peticion post, que va hacer guardado en la variable response
    datos = response.json()
    return datos["candidates"][0]["content"]["parts"][0]["text"] #imprime solo la respuesta
    
print(obtener_datos_de_pruebas("confirma si mi conexion esta funcionando."))