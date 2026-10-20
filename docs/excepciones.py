"""
try: intentar
except: si sucede ese error, haz x
raise: levanta un error. Lanza explicitamente una excepción
finally: ejecuta siempre sin importa si huno o no excepción
else: lo que se va a ejecutar si NO hubo ningun error

SINTAXIS:
TRY:
    #bloque de codigo que quiero tratar de realizar
EXCEPT error:
    #bloque de codigo que se va a ejecutar si hubo un error
"""
try:
    x = 10
    y = 0
    resultado = x / y
except ZeroDivisionError: #errore que aparece al intentar dividir entre 0
    print("No se puede dividir entre 0")
try:
    numero = int("hola ")
    print(numero)
except ValueError:
    print("No se puede convertir el string a entero")


try:
    texto = "hola clase !"
    num = 22
    frase = texto + num
except TypeError:
    print("tipos de datos distintos")


try:
    Frutas = ["manzana", "banana", "pera"]
    print(Frutas[6])
except IndexError:
    print("Fruta inexistente")


try:
    estudiante = {

        "nombre": "Juan",
        "apellido": "Perez",
        "edad": 20
    }
    print(estudiante["email"])

except KeyError:
    print("El estudiante no tiene email")

    