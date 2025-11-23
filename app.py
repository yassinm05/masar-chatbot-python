from flask import Flask, request, jsonify
from flask_cors import CORS
from pydub import AudioSegment
import speech_recognition as sr
import io
import os

# Import from our modular files
from config import Config
# FIXED: Imported from 'chatbot_logic' without .py extension
from chatbot_logic import main_chatbot_flow, generate_study_response

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Masar Chatbot API is running!"

# --- ENDPOINT 1: General Chatbot (Text) ---
@app.route("/api/chat", methods=['POST'])
def chat():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization header with Bearer token is required"}), 401

    token = auth_header.split(' ')[1]
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    user_query = data['query']
    student_id = data.get('studentId') 

    bot_response = main_chatbot_flow(
        user_query=user_query,
        token=token,
        student_id=student_id
    )
    return jsonify({"response": bot_response})

# --- ENDPOINT 2: General Chatbot (Voice) ---
@app.route("/api/transcribe", methods=['POST'])
def transcribe_audio():
    # 1. Auth
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization header with Bearer token is required"}), 401
    token = auth_header.split(' ')[1]
    student_id = request.form.get('studentId')

    # 2. Process Audio
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file found"}), 400

    audio_file = request.files['audio']
    try:
        # Requires FFmpeg installed on the system for local testing
        webm_audio = AudioSegment.from_file(audio_file, format="webm")
        wav_io = io.BytesIO()
        webm_audio.export(wav_io, format="wav")
        wav_io.seek(0)
    except Exception as e:
        return jsonify({"error": f"Audio conversion failed: {e}"}), 500

    # 3. Speech to Text
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_io) as source:
        audio_data = recognizer.record(source)

    text = None
    try:
        text = recognizer.recognize_google(audio_data, language='en-US')
    except sr.UnknownValueError:
        try:
            text = recognizer.recognize_google(audio_data, language='ar-EG')
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand the audio"}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Speech service error: {e}"}), 503
    
    # 4. Chatbot Flow
    if text:
        bot_response = main_chatbot_flow(
            user_query=text,
            token=token,
            student_id=student_id
        )
        return jsonify({"response": bot_response, "transcription": text})
    else:
        return jsonify({"error": "Transcription failed"}), 500

# --- ENDPOINT 3: Study with AI (Called by .NET) ---
@app.route("/generate", methods=['POST'])
def generate():
    data = request.get_json()
    if not data or 'context' not in data or 'prompt' not in data:
        return jsonify({"error": "Request body must contain 'context' and 'prompt'."}), 400

    result = generate_study_response(data['context'], data['prompt'])
    
    if result["success"]:
        return jsonify({"answer": result["answer"]})
    else:
        return jsonify({"error": result["error"]}), 500

if __name__ == "__main__":
    # This block runs when you type 'python app.py'
    port = 5000
    
    print(f"\n--- Masar Chatbot is Live! ---")
    print(f"Local URL: http://127.0.0.1:{port}")
    print(f"------------------------------\n")
    
    app.run(host="127.0.0.1", port=port, debug=True)