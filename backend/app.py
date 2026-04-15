from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS
import edge_tts
import os
import asyncio

app = Flask(__name__, static_folder=".")
CORS(app)

# Serve frontend
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# FIXED TTS (safe async handling)
@app.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get('text')
    voice = data.get('voice', 'en-US-AriaNeural')

    if not text:
        return {"error": "No text provided"}, 400

    filename = "output.mp3"

    async def run_tts():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_tts())
    loop.close()

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))