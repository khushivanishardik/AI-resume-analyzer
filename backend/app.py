from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from resume_parser import extract_text
from analyzer import analyze_resume

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "AI Resume Analyzer Running!"

@app.route('/analyze', methods=['POST'])
def analyze():

    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files['resume']
    job_pref = request.form['job']

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    resume_text = extract_text(file_path)

    result = analyze_resume(resume_text, job_pref)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)