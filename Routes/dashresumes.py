import os
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request 
from werkzeug.utils import secure_filename
from DbOperation.EmpReumeOp import EmployeeResumesOperations
from DbOperation.empportOp import EmployeePortfolioOperations
from DbOperation.empprofileOp import EmployeeProfileOperations

dash_resumes = Blueprint('dash_resumes', __name__)
empresumops = EmployeeResumesOperations()
empportops = EmployeePortfolioOperations()
empprofops = EmployeeProfileOperations()
# Get the main directory (one level up from Routes)
MAIN_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(MAIN_DIR, 'Resumes')  # Create 'Resumes' in the main directory
ALLOWED_EXTENSIONS = {'pdf'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
from datetime import datetime, timezone

# path for employee profile 
UPLOAD_FOLDER_EmpR = os.path.join(MAIN_DIR, "static/emprofiles")  # Fix the path
ALLOWED_EXTENSIONS_Empr = {"png", "jpg", "jpeg", "gif"}
os.makedirs(UPLOAD_FOLDER_EmpR, exist_ok=True)  # Ensure directory exists
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
        filepath = os.path.join(UPLOAD_FOLDER, filename)  # Save in the main directory's Resumes folder
        
        file.save(filepath)
        filepath = f"Resumes\{filename}"
        user_data = session.get('empuser_data')
        if user_data:  # Check if data exists
            employee_id = user_data.get("id")
            empresumops.upload_resume(employee_id,filepath)
            if empportops.check_portfolio_exists(employee_id):
                empportops.update_portfolio_attempts(employee_id, created_at=datetime.now(timezone.utc))
            else:
                empportops.add_portfolio_data(employee_id,0,0,0,0)

        
        return jsonify({"message": "Resume uploaded successfully!", "filename": filename}), 200

    return jsonify({"error": "Invalid file format. Only PDF is allowed."}), 400





def allowed_profilefile(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS_Empr

@dash_resumes.route("/upload_profile_picture", methods=["POST"])
def upload_profile_picture():
    if "profile_picture" not in request.files:
        return jsonify({"success": False, "message": "No file part"})

    file = request.files["profile_picture"]

    if file.filename == "":
        return jsonify({"success": False, "message": "No selected file"})

    if file and allowed_profilefile(file.filename):
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER_EmpR, filename)  # Use the variable directly
        file.save(file_path)
        file_path=f"/emprofiles/{filename}"

        user_data = session.get('empuser_data')
        if user_data:  # Check if data exists
            employee_id = user_data.get("id")
            if empprofops.check_empprof(1):
                empprofops.update_profile_picture(employee_id , file_path)
            else:
                empprofops.upload_profile_picture(employee_id , file_path)

        return jsonify({"success": True, "message": "Profile picture uploaded successfully!"})

    return jsonify({"success": False, "message": "Invalid file type. Only images are allowed."})
