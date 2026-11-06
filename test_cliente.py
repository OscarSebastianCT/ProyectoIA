# Se usan mocks para no llamar a la API real ni esperar tiempo de verdad.
# Para correrlas:  pytest test_cliente.py -v

from unittest.mock import patch, Mock

import pytest

import cliente
from src.consumir_gemini import enviar_peticion


# Este fixture se ejecuta solo antes de cada prueba (autouse=True)
# y deja el costo acumulado en 0, para que una prueba no afecte a otra.
@pytest.fixture(autouse=True)
def reiniciar_costo_total():
    cliente.costo_total_sesion = 0
    yield


# ================= TESTS ENVIAR PETICION =================

def test_enviar_peticion_credencial_invalida():
    # Simulamos que el servidor responde 401 (API key incorrecta)
    respuesta_falsa = Mock(status_code=401)

    # Reemplazamos requests.post para que devuelva nuestra respuesta falsa
    with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):#with es 
        # Con 401 se espera un ValueError
        with pytest.raises(ValueError):
            enviar_peticion("https://ejemplo.invalid", {"pregunta": "test"})


def test_enviar_peticion_limite_de_uso():
    # Simulamos que el servidor responde 429 (límite de uso alcanzado)
    respuesta_falsa = Mock(status_code=429)

    with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):
        # Con 429 se espera un TimeoutError (para que luego se pueda reintentar)
        with pytest.raises(TimeoutError):
            enviar_peticion("https://ejemplo.invalid", {"pregunta": "test"})


def test_enviar_peticion_exito():
    # Simulamos una respuesta exitosa (200) con un JSON de ejemplo
    respuesta_falsa = Mock(status_code=200)
    respuesta_falsa.json.return_value = {"texto": "respuesta simulada"}

    with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):
        resultado = enviar_peticion("https://ejemplo.invalid", {"pregunta": "test"})

    # La función debe devolver el mismo JSON que entregó el servidor
    assert resultado == {"texto": "respuesta simulada"}


# ================= TESTS REINTENTOS =================

def test_con_reintento_agota_intentos():
    # Función falsa que siempre falla con timeout
    def siempre_falla():
        raise TimeoutError("simulado")

    # Reemplazamos time.sleep para que la prueba no espere de verdad
    with patch("cliente.time.sleep"):
        # Después de 3 intentos fallidos, con_reintento debe lanzar el error
        with pytest.raises(TimeoutError):
            cliente.con_reintento(siempre_falla, intentos=3)


def test_con_reintento_no_reintenta_value_error():
    # Operación falsa que lanza ValueError (error que NO se debe reintentar)
    operacion = Mock(side_effect=ValueError("simulado"))

    with patch("cliente.time.sleep") as dormir:
        with pytest.raises(ValueError):
            cliente.con_reintento(operacion)

    # Se llamó una sola vez y nunca esperó: no hubo reintentos
    operacion.assert_called_once()
    dormir.assert_not_called()


# ================= TESTS COSTO =================

def test_registrar_costo_acumula():
    # Respuesta falsa con la misma forma que la de Gemini: 1000 tokens usados
    respuesta_falsa = {
        "usageMetadata": {
            "totalTokenCount": 1000
        }
    }

    # No necesita mocks: registrar_costo no usa la red
    costo = cliente.registrar_costo(respuesta_falsa)

    # 1000 tokens deben costar exactamente COSTO_POR_1000_TOKENS
    assert costo == cliente.COSTO_POR_1000_TOKENS
    # Como partimos en 0 (por el fixture), el acumulado debe ser el mismo valor
    assert cliente.costo_total_sesion == cliente.COSTO_POR_1000_TOKENS


# ================= TESTS CONSULTAR MODELO =================

def test_consultar_modelo_convierte_error():
    # Simulamos que con_reintento agotó todos sus intentos
    error_simulado = TimeoutError("simulado")

    with patch(
        "cliente.con_reintento",
        side_effect=error_simulado,
    ):
        # consultar_modelo debe convertir el TimeoutError en RuntimeError
        # y el mensaje debe avisar que el servicio no responde
        with pytest.raises(RuntimeError, match="no responde"):
            cliente.consultar_modelo("Pregunta de prueba")