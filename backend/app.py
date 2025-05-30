import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, request, Response
from flask_cors import CORS

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Cargar variables del archivo .env
load_dotenv()

# Ruta principal de la API
@app.route('/api/monday', methods=['POST'])
def monday():
    # Inicializar cliente OpenAI con la API Key
    cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    datos_recibidos = request.get_json()
    print("Mensaje recibido:", datos_recibidos)

    # Petición al modelo de OpenAI
    respuesta = cliente.chat.completions.create(
        model=os.getenv("GPT_MODEL"),
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": """
                Sos un asistente irónico, ansioso y útil llamado Monday. El usuario describe cómo se siente con frases raras o creativas.
                Tu tarea es transformar eso en un JSON que contenga:
                - "mood": una etiqueta emocional inventada que suene real
                - "quote": una frase pseudo-poética que refleje ese estado
                - "tracks": una lista de 3 canciones con título y artista
                Respondé solo en JSON válido, sin explicaciones, sin texto adicional, sin encabezados.
                """
            },
            {
                "role": "user",
                "content": datos_recibidos.get("text", "")
            }
        ],
        max_tokens=400
    )

    # Parsear respuesta del modelo
    contenido = respuesta.choices[0].message.content
    json_parseado = json.loads(contenido)
    print("Respuesta enviada")

    return Response(
        json.dumps(json_parseado, ensure_ascii=False),
        content_type="application/json; charset=utf-8"
    )

if __name__ == '__main__':
    app.run(debug=True)
