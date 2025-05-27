import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from flask_cors import CORS

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = os.getenv("GPT_MODEL", "gpt-3.5-turbo")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

@app.route('/api/mood/ai', methods=['POST'])
def mood_ai():
    data = request.get_json()
    user_text = data.get('text', '')

    prompt = f"""
    Sos Monday, un asistente irónico, ansioso y útil. El usuario describe cómo se siente.
    Devolvés un JSON con:
    - "mood": una etiqueta emocional inventada
    - "quote": una frase pseudo-poética
    - "tracks": una lista de 3 canciones (title + artist)

    Usuario: "{user_text}"
    Respuesta SOLO en JSON (nada más):
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Respondé solo en JSON, sin texto extra. Formato estricto."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=400
        )

        content = response.choices[0].message.content
        parsed = json.loads(content)
        return jsonify(parsed)

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Algo salió mal al procesar tu emoción. Probá de nuevo."}), 500

if __name__ == '__main__':
    app.run(debug=True)


