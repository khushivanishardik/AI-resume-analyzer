from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import threading

from resume_parser import extract_text
from analyzer import analyze_resume, get_model

# Initialize app
app = Flask(__name__)
CORS(app)

# Upload folder setup
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ✅ Background model loading (non-blocking)
def preload_model():
    try:
        print("Loading model in background...")
        get_model()
        print("Model loaded successfully")
    except Exception as e:
        print("Error loading model:", e)

threading.Thread(target=preload_model).start()


# ✅ Home route
@app.route('/')
def home():
    return "AI Resume Analyzer Running!"


# ✅ Analyze route
@app.route('/analyze', methods=['POST'])
def analyze():

    if 'resume' not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400

    file = request.files['resume']
    job_pref = request.form.get('job', '')

    if file.filename == '':
        return jsonify({"error": "Empty file"}), 400

    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Extract text
    resume_text = extract_text(file_path)

    if not resume_text:
        return jsonify({"error": "Could not extract text"}), 500

    # Analyze
    result = analyze_resume(resume_text, job_pref)

    return jsonify(result)


# ✅ Run server (Render compatible)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)