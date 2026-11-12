from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI # nos permite utilizar o crear el modelo
from langchain_core.prompts import PromptTemplate # importa la clase para crear la plantilla
from langchain_core.output_parsers import StrOutputParser # parsea y transformar la respuesta en un string
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
#respuesta = modelo.invoke("que es un token") #inveko sirve para generar la consulta 
#print(respuesta.content) # content sirve para obtener el contenido de la respuesta, la respuesta a nuestra prompt

#f-strings conciste en poner entre llaves el nombre de la variable ejemplo: {tema}
plantilla  = PromptTemplate.from_template(
    "Explica el concepto de {tema} en un parrafo, para alguien que recien comienza en {area}."
)

#prompt = plantilla.invoke({"tema": "tokenización", "area": "procesamiento de texto"})
#print(prompt.text) #prompt.text sirve para obtener el texto en este caso el que usamos como prompt = "Explica el concepto de {tema} en un parrafo, para alguien que recien comienza en {area}."

cadena_simple = plantilla | modelo | StrOutputParser() # | sirve para unir el prompt con el modelo y el output

respuesta = cadena_simple.invoke(
    {"tema": "embeddings", "area": "busqueda semantica"})

print(respuesta)# content es contenido de la respuesta completa y el text nuestro prompt

plantilla_conrol = ChatPromptTemplate.from_messages([
    ("system", "eres un experto en el area correspondiente, vas a responder siempre con texto simple para el usuario."),
    ("human", "Explica el concepto de {tema} en un parrafo, para alguien que recien comienza en {area}.") 
]) #system seria como el system instruction "el rol", human seria como el prompt