import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, request, make_response
from flask_cors import CORS

# Inicializar Flask
app = Flask(__name__)

# Habilitar CORS para Vercel frontend
CORS(app, origins=["https://feelist-5d2ltpug5-kerus-projects-11fb7bb5.vercel.app"])

# Cargar variables de entorno del archivo .env
load_dotenv()

# Ruta GET para verificar que la API esté viva
@app.route('/')
def home():
    return 'Feelist API corriendo. Mandá un POST a /api/monday.'

# Ruta principal que procesa la entrada del usuario
@app.route('/api/monday', methods=['POST'])
def monday():
    # Inicializar cliente de OpenAI
    cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Obtener datos JSON enviados por el usuario
    datos_recibidos = request.get_json()
    print("Mensaje recibido:", datos_recibidos)

    # Validación mínima
    if not datos_recibidos or "text" not in datos_recibidos:
        respuesta_error = make_response(json.dumps({"error": "Falta el texto del usuario"}), 400)
        respuesta_error.headers['Access-Control-Allow-Origin'] = 'https://feelist-5d2ltpug5-kerus-projects-11fb7bb5.vercel.app'
        return respuesta_error

    try:
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

        # Parsear respuesta de OpenAI
        contenido = respuesta.choices[0].message.content
        json_parseado = json.loads(contenido)
        print("Respuesta enviada:", json_parseado)

        # Preparar respuesta con headers CORS
        respuesta_ok = make_response(json.dumps(json_parseado, ensure_ascii=False))
        respuesta_ok.headers['Content-Type'] = 'application/json; charset=utf-8'
        respuesta_ok.headers['Access-Control-Allow-Origin'] = 'https://feelist-5d2ltpug5-kerus-projects-11fb7bb5.vercel.app'
        return respuesta_ok

    except Exception as error:
        print("Error interno:", error)
        respuesta_error = make_response(json.dumps({"error": "Error interno del servidor"}), 500)
        respuesta_error.headers['Access-Control-Allow-Origin'] = 'https://feelist-5d2ltpug5-kerus-projects-11fb7bb5.vercel.app'
        return respuesta_error

# Iniciar servidor si se ejecuta localmente
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
