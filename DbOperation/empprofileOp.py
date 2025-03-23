from flask import Flask
from DBModules.models import EmployeeProfile, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/intervisio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class EmployeeProfileOperations:
    @staticmethod
    def upload_profile_picture(employee_id, pic_path):
        with app.app_context():
            new_profile = EmployeeProfile(
                employee_id=employee_id,
                emp_pic_path=pic_path
            )
            db.session.add(new_profile)
            db.session.commit()

    @staticmethod
    def get_profile_by_employee(employee_id):
        with app.app_context():
            profile = EmployeeProfile.query.filter_by(employee_id=employee_id).first()
            return {"id": profile.profile_id, "employee_id": profile.employee_id, "path": profile.emp_pic_path} if profile else None

    @staticmethod
    def update_profile_picture(employee_id, new_pic_path):
        with app.app_context():
            profile = EmployeeProfile.query.filter_by(employee_id=employee_id).first()
            if profile:
                profile.emp_pic_path = new_pic_path
                db.session.commit()
                print(f"Profile picture updated successfully for Employee ID {employee_id}!")
            else:
                print("Profile not found.")

    @staticmethod
    def delete_profile_picture(profile_id):
        with app.app_context():
            profile = EmployeeProfile.query.filter_by(profile_id=profile_id).first()
            if profile:
                db.session.delete(profile)
                db.session.commit()
                print(f"Profile picture with ID {profile_id} deleted successfully!")
            else:
                print("Profile picture not found.")

    @staticmethod
    def check_empprof(employee_id):
        with app.app_context():
            profile_exists = EmployeeProfile.query.filter_by(employee_id=employee_id).first() 
            if profile_exists:
                return True
            else:
                return False
