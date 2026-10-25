## Cómo instalar y ejecutar (Windows, PowerShell)

1. Clona el repositorio y entra a la carpeta:
   git clone https://github.com/OscarSebastianCT/ProyectoIA.git
   cd ProyectoIA

2. Crea y activa el entorno virtual:
   python -m venv venv
   venv\Scripts\activate

3. Instala las dependencias:
   pip install -r requirements.txt

4. Crea tu archivo .env a partir de la plantilla:
   copy .env.example .env
   Abre .env y escribe tu propia llave de Gemini en la línea GEMINI_API_KEY=
   (la llave se obtiene en https://aistudio.google.com/api-keys)

5. Ejecuta el proyecto:
   python src/consumir_gemini.py       # prueba de conexión con Gemini
   python src/consistencia.py          # prueba de consistencia del banco de prompts

## Estructura de carpetas

- `src/` : código fuente (módulo de consumo de la API, evaluación de modelos, prueba de consistencia).
- `src/prompts/` : banco de prompts y `registro_resultados.json` con los resultados de consistencia.
- `docs/` : diagrama de arquitectura y decisión de modelo.
- `tests/` : pruebas (se usarán más adelante en el programa).
- `requirements.txt` : dependencias del proyecto.
- `.env.example` : plantilla de variables de entorno, sin valores reales.
- `.gitignore` : excluye el entorno virtual y el archivo `.env`.

## Reglas del proyecto

- Ningún secreto (contraseña, llave de API, token) va escrito en el código ni en archivos que se suban al repositorio.
- Cada proyecto tiene su propio entorno virtual.
- Todo el trabajo vive en un repositorio de GitHub.

## Registro del ensayo de instalación limpia

- Fecha: 25/10/2026
- Encontrado: El .env.example usaba el nombre API_KEY, pero el código espera GEMINI_API_KEY; al instalar desde cero la petición fallaba con error 400.
- Corregido: Se cambió el nombre de la variable en .env.example a GEMINI_API_KEY.
- Resultado tras la corrección: Clonado, entorno virtual e instalación de dependencias funcionan desde cero; la ejecución requiere una llave válida de Gemini en el archivo .env.