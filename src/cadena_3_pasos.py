from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI # nos permite utilizar o crear el modelo
from langchain_core.prompts import PromptTemplate # importa la clase para crear la plantilla
from langchain_core.output_parsers import StrOutputParser # parsea y transformar la respuesta en un string
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

plantilla_extraccion = PromptTemplate.from_template("Lee el siguiente texto y devuleve solo sus 3 puntos clave, uno por linea, sin desarrollarlos: \n\n{texto}")

paso_extraccion = plantilla_extraccion | modelo | StrOutputParser()

texto_prueba = (
    "Los modelos de lenguaje grandes generan texto "
    "prediciendo un token a la vez, basándose en el "
    "texto que ya generaron antes. Cada token puede "
    "ser una palabra completa, parte de una palabra, "
    "o un signo de puntuación. Antes de que el modelo "
    "genere una respuesta, el texto de entrada se "
    "divide en tokens, un proceso llamado tokenización."
)

puntos = paso_extraccion.invoke(
    {"texto": texto_prueba}
)
print(puntos)

plantilla_simplificacion = PromptTemplate.from_template("Reescribre estos punto en lenguaje simple, sin jerga tecnica para alguien sin conocimiento previso: \n\n{puntos}")

paso_simplificacion = plantilla_simplificacion | modelo | StrOutputParser()

simple = paso_simplificacion.invoke(
    {"puntos": puntos}

)

print(simple)


plantilla_formato = PromptTemplate.from_template("escribe este texto en una lista de viñetas mardown de maximo 3 lineas, sin introduccion: \n\n{texto_simple}")

paso_formato = plantilla_formato | modelo | StrOutputParser()

formato = paso_formato.invoke(
    {"texto_simple": simple}
)

print(formato)