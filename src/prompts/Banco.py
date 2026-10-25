BANCO_DE_PROMPT = [
    {
        # Clasificar una actividad registrada en una hoja de trabajo
        "nombre": "clasificar_actividad",
        "system_instruction": (
            "Clasifica la actividad de obra descrita. Responde únicamente con un JSON con las "
            "claves 'tipo' (una de: 'Mantenimiento', 'Reparación', 'Inspección', 'Instalación', "
            "'Otro') y 'es_urgente' (boolean)."
        ),
        "ejemplo_usuario": "Se cambiaron 12 durmientes dañados en el km 45, tramo con restricción de velocidad.",
        "claves_esperadas": ["tipo", "es_urgente"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "tipo": {
                    "type": "STRING",
                    "enum": ["Mantenimiento", "Reparación", "Inspección", "Instalación", "Otro"],
                },
                "es_urgente": {"type": "BOOLEAN"},
            },
            "required": ["tipo", "es_urgente"],
        },
    },
    {
        # Extraer datos clave de un registro de trabajo
        "nombre": "extraer_registro",
        "system_instruction": (
            "Extrae los datos del registro de trabajo. Responde únicamente con un JSON con las "
            "claves 'cuadrilla' (texto), 'ubicacion' (texto) y 'horas_trabajadas' (número)."
        ),
        "ejemplo_usuario": "Cuadrilla 3 trabajó en el km 120 desde las 8:00 hasta las 14:00 haciendo nivelación.",
        "claves_esperadas": ["cuadrilla", "ubicacion", "horas_trabajadas"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "cuadrilla": {"type": "STRING"},
                "ubicacion": {"type": "STRING"},
                "horas_trabajadas": {"type": "NUMBER"},
            },
            "required": ["cuadrilla", "ubicacion", "horas_trabajadas"],
        },
    },
    {
        # Decidir en qué fuente buscar la respuesta a una pregunta
        "nombre": "fuente_consulta",
        "system_instruction": (
            "Indica en qué fuente de información se debe buscar la respuesta a la pregunta. "
            "Responde únicamente con un JSON con la clave 'fuente' (una de: 'Hojas de trabajo', "
            "'Base de datos', 'Planilla de reportes', 'Otra')."
        ),
        "ejemplo_usuario": "¿Cuántas pautas entregó la cuadrilla 2 la semana pasada?",
        "claves_esperadas": ["fuente"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "fuente": {
                    "type": "STRING",
                    "enum": ["Hojas de trabajo", "Base de datos", "Planilla de reportes", "Otra"],
                },
            },
            "required": ["fuente"],
        },
    },
]