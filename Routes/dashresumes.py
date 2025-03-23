import os
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request 
from werkzeug.utils import secure_filename
from DbOperation.EmpReumeOp import EmployeeResumesOperations
from DbOperation.empportOp import EmployeePortfolioOperations
dash_resumes = Blueprint('dash_resumes', __name__)
empresumops = EmployeeResumesOperations()
empportops = EmployeePortfolioOperations()
# Get the main directory (one level up from Routes)
MAIN_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(MAIN_DIR, 'Resumes')  # Create 'Resumes' in the main directory
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
        filepath = os.path.join(UPLOAD_FOLDER, filename)  # Save in the main directory's Resumes folder
        
        file.save(filepath)
        filepath = f"/Resumes/{filename}"
        user_data = session.get('empuser_data')
        if user_data:  # Check if data exists
            employee_id = user_data.get("id")
            full_name = user_data.get("full_name")
            email = user_data.get("email")
            phone_number = user_data.get("phone_number")
            house_address = user_data.get("house_address")
            country = user_data.get("country")
            print(employee_id, full_name, email, phone_number, house_address, country)
            empresumops.upload_resume(employee_id,filepath)
            if empportops.check_portfolio_exists(employee_id):
                print("user zinda ha !")
            else:
                empportops.add_portfolio_data(employee_id,0,0,0,0)

        print(filepath)
        return jsonify({"message": "Resume uploaded successfully!", "filename": filename}), 200

    return jsonify({"error": "Invalid file format. Only PDF is allowed."}), 400
