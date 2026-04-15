from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS
import asyncio
import edge_tts
import os

# Serve frontend from same folder
app = Flask(__name__, static_folder=".")
CORS(app)

# ===== Serve frontend =====
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# ===== TTS function =====
async def generate_tts(text, voice, filename):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

# ===== API =====
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

# ===== Run (for Render) =====
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))