from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from resume_parser import extract_text
from analyzer import analyze_resume

# Initialize app
app = Flask(__name__)
CORS(app)  # Enable frontend-backend communication

# Upload folder setup
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ✅ Home route (for testing deployment)
@app.route('/')
def home():
    return "AI Resume Analyzer Running!"


# ✅ Main analyze route
@app.route('/analyze', methods=['POST'])
def analyze():

    # Check file
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


# ✅ Run server (for local + deployment)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)