from flask import Flask, request, send_file
from flask_cors import CORS
import asyncio
import edge_tts

app = Flask(__name__)
CORS(app)

async def generate_tts(text, voice, filename):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

@app.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get('text')
    voice = data.get('voice', 'en-US-AriaNeural')

    if not text:
        return {"error": "No text provided"}, 400

    filename = "output.mp3"

    asyncio.run(generate_tts(text, voice, filename))

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)