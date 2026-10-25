import consumir_gemini
import time
import pandas as pd   

def evaluar_modelo(nombre_modelo, pregunta, precio_entrada, precio_salida, repeticiones=4):
    """
    Ejecuta 'repeticiones' veces la misma petición para un modelo específico.
    Calcula e imprime Latencia, Costo y Respuesta de cada intento,
    además del promedio de latencia al final.
    """
    print("=" * 70)
    print(f" EVALUANDO MODELO: {nombre_modelo}")
    print("=" * 70)
    
    latencias = []
    costos = []

    for i in range(1, repeticiones + 1):
        print(f"\n--- Intento {i} de {repeticiones} ({nombre_modelo}) ---")
        
        # 1. Armar petición (puedes pasar el modelo si tu función lo requiere)
        url, body = consumir_gemini.armar_peticion( nombre_modelo, pregunta, system_instruction) 

        # 2. Medir latencia
        inicio = time.perf_counter()
        datos = consumir_gemini.enviar_peticion(url, body)
        fin = time.perf_counter()
        
        latencia = fin - inicio
        latencias.append(latencia)
        
        # 3. Calcular costo
        costo = consumir_gemini.calcular_costos(datos, precio_entrada, precio_salida)
        costos.append(costo)
        
        # 4. Extraer respuesta
        respuesta = consumir_gemini.extraer_texto(datos)
        
        # 5. Imprimir resultados de la petición actual
        print(f"Latencia:  {latencia:.2f} segundos")
        print(f"Costo:     ${costo:.6f} USD")
        print(f"Respuesta: {respuesta}")

    # Resumen acumulado del modelo
    latencia_promedio = sum(latencias) / len(latencias)
    costo_total = sum(costos)
    
    print("\n" + "-" * 40)
    print(f" RESUMEN {nombre_modelo}:")
    print(f" Latencia promedio: {latencia_promedio:.2f} segundos")
    print(f" Costo acumulado ({repeticiones} peticiones): ${costo_total:.6f} USD")
    print("-" * 40 + "\n")

# NUEVO: leer el Excel y convertirlo a texto
ruta_excel = "data/registros_prueba.xlsx"
tabla = pd.read_excel(ruta_excel)
datos_texto = tabla.to_csv(index=False)

# CAMBIADO: system instruction y pregunta relacionadas al proyecto
system_instruction = (
    "Eres un asistente que responde preguntas sobre registros de trabajos de obras. "
    "Usa SOLO los datos entregados. Responde con un JSON con las claves: "
    '"respuesta" (número o texto), "filas_usadas" (cuántas filas consideraste) y "explicacion" (máximo 1 frase). '
    "Si los datos no permiten responder, pon null en respuesta y dilo en la explicación."
)

pregunta_prueba = (
    f"Datos:\n{datos_texto}\n\n"
    "Pregunta: ¿Cuántos registros tienen a “Julio Varela” en la columna “Personal que Ejecuta la Pauta/ Colaborador EPS” y además el valor “RPAMPA( Pampa-Prat )” en la columna “Ramal”?"
)
modelos = [
    {
        "nombre": "gemini-3.6-flash",
        "precio_entrada": 0.00000075,
        "precio_salida": 0.00000375
    },
    {
        "nombre": "gemini-3.5-flash-lite",
        "precio_entrada": 0.00000030,
        "precio_salida": 0.00000250
    },
    {
        "nombre": "gemini-3.1-flash-lite",
        "precio_entrada": 0.00000025,
        "precio_salida": 0.00000150
    }
]

# Procesar los 3 modelos consecutivamente
for config in modelos:
    try:
        evaluar_modelo(
            nombre_modelo=config["nombre"],
            pregunta=pregunta_prueba,
            precio_entrada=config["precio_entrada"],
            precio_salida=config["precio_salida"],
            repeticiones=4
        )
    except RuntimeError as error:
        print(f"No se pudo evaluar {config['nombre']}: {error}\n")