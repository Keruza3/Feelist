import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, request, jsonify, Response

#carga el archivo.env que tiene la API KEY
load_dotenv()

# flask para abrir el 

app = Flask(__name__)

@app.route('/api/test', methods=['POST'])

# 1. obtener texto del usuario
# 2. armar mensajes
# 3. llamar a GPT
# 4. obtener respuesta
# 5. convertir string JSON a dict
# 6. devolverlo como respuesta
#conecta la la API KEY sin mostrarla
def test():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    data = request.get_json()
    print("Entro por chat:", data)
    
    # parametros para chat
    response = client.chat.completions.create(

    model=os.getenv("GPT_MODEL"),
    temperature=0.9,
    messages = [
        {"role": "system", "content": """
         Sos un asistente irónico, ansioso y útil llamado Monday. El usuario describe cómo se siente con frases raras o creativas.
         Tu tarea es transformar eso en un JSON que contenga:
         - "mood": una etiqueta emocional inventada que suene real
         - "quote": una frase pseudo-poética que refleje ese estado
         - "tracks": una lista de 3 canciones con título y artista
         Respondé solo en JSON válido, sin explicaciones, sin texto adicional, sin encabezados.
         """},
        {"role": "user", "content": data.get("text", "")}
    ],
    max_tokens=400 
    )
    # la respuesta se guarda en la variable "contenidoResp"
    content = response.choices[0].message.content
    # se guarda a texto el json
    parsed = json.loads(content)
    print("Salio por chat")

    return Response(
    json.dumps(parsed, ensure_ascii=False),
    content_type="application/json; charset=utf-8"
)

if __name__ == '__main__':
    app.run(debug=True)
