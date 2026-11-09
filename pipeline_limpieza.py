import re
from collections import Counter

def limpiar_texto(texto: str) -> str:
    """Limpia el texto: minúsculas, sin puntuación y sin espacios extra."""
    if not isinstance(texto, str):
        tipo = type(texto).__name__
        raise TypeError(f"El argumento debe ser de tipo str, no {tipo}.")
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip() #strip sirve para quitar los espacios en blanco
    return texto

def tokenizar(texto_limpio: str) -> list[str]:
    """Convierte texto limpio en una lista de tokens."""
    return texto_limpio.split() #split sirve para separar los tokens

def vectorizar(tokens: list[str]) -> Counter: # counter es para contar
    """Cuenta cuántas veces aparece cada token."""
    return Counter(tokens)

def procesar_texto(texto):
    texto_limpio = limpiar_texto(texto)
    return tokenizar(texto_limpio)

if __name__ == "__main__":
    texto = "El gato, el perro y el gato corren."
    texto_limpio = limpiar_texto(texto)
    tokens = tokenizar(texto_limpio)
    conteo = vectorizar(tokens)
    print("Texto limpio:", texto_limpio)
    print("Tokens:", tokens)
    print("Conteo:", conteo)