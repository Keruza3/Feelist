import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS

# Inicializar Flask
app = Flask(__name__)

# Habilitar CORS solo para tu frontend de Vercel
CORS(app, resources={r"/api/*": {"origins": "https://feelist-5d2ltpug5-kerus-projects-11fb7bb5.vercel.app"}})

# Cargar variables de entorno
load_dotenv()

@app.route('/')
def home():
    return 'Feelist API corriendo. Mandá un POST a /api/monday.'

@app.route('/api/monday', methods=['POST'])
def monday():
    try:
        cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        datos = request.get_json()

        if not datos or "text" not in datos:
            return jsonify({"error": "Falta el texto del usuario"}), 400

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
                    NO respondas nada fuera de un JSON válido. Si no entendés el input, igual devolvé un JSON de prueba.
                    """
                },{
                    "role": "user",
                    "content": datos.get("text")
                }
            ],
            max_tokens=400
        )

        contenido = respuesta.choices[0].message.content
        return jsonify(json.loads(contenido))

    except Exception as e:
        print("Error interno:", str(e))
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)

