import os
from flask import Blueprint, render_template, session, redirect, url_for , jsonify , request
from werkzeug.utils import secure_filename

dash_resumes = Blueprint('dash_resumes', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'Resumes')
ALLOWED_EXTENSIONS = {'pdf'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@dash_resumes.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)  # Use local UPLOAD_FOLDER
        
        file.save(filepath)
        return jsonify({"message": "Resume uploaded successfully!", "filename": filename}), 200

    return jsonify({"error": "Invalid file format. Only PDF is allowed."}), 400
