BANCO_DE_PROMPT = [
    {
        # Clasificar un gasto de la casa
        "nombre": "clasificar_gasto",
        "system_instruction": (
            "Clasifica el gasto. Responde únicamente con un JSON con las claves "
            "'categoria' (una de: 'Comida', 'Cuentas', 'Transporte', 'Hogar', 'Otro') "
            "y 'es_necesario' (boolean)."
        ),
        "ejemplo_usuario": "Pagué la cuenta de la luz, 35.000 pesos.",
        "claves_esperadas": ["categoria", "es_necesario"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "categoria": {
                    "type": "STRING",
                    "enum": ["Comida", "Cuentas", "Transporte", "Hogar", "Otro"],
                },
                "es_necesario": {"type": "BOOLEAN"},
            },
            "required": ["categoria", "es_necesario"],
        },
    },
    {
        # Sugerir qué cocinar con lo que hay en el refri
        "nombre": "sugerir_comida",
        "system_instruction": (
            "Sugiere un plato con los ingredientes indicados. Responde únicamente con un "
            "JSON con las claves 'plato' (texto) y 'minutos' (número)."
        ),
        "ejemplo_usuario": "Tengo arroz, huevos, una cebolla y un tomate.",
        "claves_esperadas": ["plato", "minutos"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "plato": {"type": "STRING"},
                "minutos": {"type": "NUMBER"},
            },
            "required": ["plato", "minutos"],
        },
    },
    {
        # Decidir cada cuánto hacer una tarea del hogar
        "nombre": "frecuencia_tarea",
        "system_instruction": (
            "Indica cada cuánto se recomienda hacer la tarea del hogar. Responde únicamente "
            "con un JSON con la clave 'frecuencia' (una de: 'Diaria', 'Semanal', 'Mensual', "
            "'Anual')."
        ),
        "ejemplo_usuario": "Limpiar el filtro de la lavadora.",
        "claves_esperadas": ["frecuencia"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "frecuencia": {
                    "type": "STRING",
                    "enum": ["Diaria", "Semanal", "Mensual", "Anual"],
                },
            },
            "required": ["frecuencia"],
        },
    },
]