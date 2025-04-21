from flask import Blueprint, request, jsonify , session , make_response , redirect , url_for
from DbOperation.employeeOp import EmployeeOperations
from DbOperation.empsavedataOp import EmployerSavedDataOperations

emplrsavdataops = EmployerSavedDataOperations()

register_user = Blueprint('register_user', __name__)

@register_user.route('/register-employee', methods=['POST'])
def register_emp():
    try:
        request_data = request.get_json()

        data = request_data.get("employeeData", {})
        print("Employee Data:", data)  # Debugging log

        full_name = data.get('full_name')
        email = data.get('email')
        password = data.get('password')
        phone_number = data.get('phone_number')
        house_address = data.get('house_address')
        country = data.get('country')

        if not all([full_name, email, password, phone_number, house_address, country]):
            return jsonify({"success": False, "message": "All fields are required"}), 400

        if EmployeeOperations.check_user(email):
            print("User exists!")  # Debugging
            return jsonify({"success": False, "exists": True, "message": "User already exists"}), 400

        print("Creating user...")  # Debugging
        newempid = EmployeeOperations.create_user(full_name, email, password, phone_number, house_address, country)
        
        emplrsavdataops.create_entry(newempid,0,0,0,0)
        return jsonify({"success": True, "exists": False, "message": "Employee registered successfully!"}), 200


    except Exception as e:
        print("Error:", str(e))  # Debugging log
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

@register_user.route('/logout')
def logout_user():
    session.clear()
    
    # Create a response object
    response = make_response(redirect(url_for('main_pages.login')))
    
    # Set headers to prevent the page from being cached
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'  # Older HTTP/1.0 caches
    response.headers['Expires'] = '0'  # Make sure the page expires immediately
    
    return response