from flask import Blueprint, request, jsonify , session
from DbOperation.employeeOp import EmployeeOperations

check_credentials = Blueprint('check_credentials', __name__)

@check_credentials.route('/check-login', methods=['POST'])
def check_login():
    try:
        request_data = request.get_json()
        data = request_data.get("employeelg", {})
        email = data.get('email')
        password = data.get('password')

        user_data = EmployeeOperations.verify_user(email, password)

        if user_data:
            user_info = {
            "id":user_data.id,
            "full_name": user_data.full_name,
            "email": user_data.email,
            "phone_number": user_data.phone_number,
            "house_address": user_data.house_address,
            "country": user_data.country,
            }
            session['empuser_data'] = {
            "id": user_data.id,
            "full_name": user_data.full_name,
            "email": user_data.email,
            "phone_number": user_data.phone_number,
            "house_address": user_data.house_address,
            "country": user_data.country,
            }
            return jsonify({"success": True, "exists": True, "message": "Login successful", "user": user_info}), 200

        else:
            return jsonify({"success": False, "exists": False, "message": "Wrong credentials"}), 400

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500
