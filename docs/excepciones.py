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


def dividir ():
    try:
        num1 = int(input("ingresa el primer numero: ")) #ingresa el primer numero
        num2 = int(input("ingresa el segundo numero: "))
        resultado = num1 / num2
        print(f"El resultado es: {resultado}")
    except ValueError:
        print("la calculadora solo acepta numeros entero")
    except ZeroDivisionError:
        print("la calculadora no puede dividir entre 0") #error que aparece al intentar dividir entre 0 ")
    except Exception as error:#atrapa errores de forma general, error tendra detalles de su excepcion
        print(f"Ocurrio un error inesperado: {error}") 
    finally:
        print("Gracias por usar la calculadora")

#dividir()

try:
    bebidas =["Coca-Cola", "Agua saborizada", "chocolate caliente", "Cerveza"]
    bebidas_deseada = input("Que bebida prefieres? ")
    if bebidas_deseada not in bebidas:
        raise ValueError(f"La bebida no esta disponible") #raise levanta un error
    else:
        print(f"Tu bebida favorita es {bebidas_deseada} esta lista")
except ValueError as error: #error tendra detalles de su excepcion 
    print(f"Error: {error}")

