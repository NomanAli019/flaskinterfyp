from flask import Flask
from DBModules.models import EmployeeResumes, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/intervisio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class EmployeeResumesOperations:
    @staticmethod
    def upload_resume(employee_id, resume_path):
        with app.app_context():
            new_resume = EmployeeResumes(
                employee_id=employee_id,
                employee_resume_path=resume_path
            )
            db.session.add(new_resume)
            db.session.commit()
            print(f"Resume uploaded successfully for Employee ID {employee_id}!")

    @staticmethod
    def get_resumes_by_employee(employee_id):
        with app.app_context():
            resume = EmployeeResumes.query.filter_by(employee_id=employee_id)\
                              .order_by(EmployeeResumes.employee_res_id.desc())\
                              .first()
            if resume:
                return {
                    "id": resume.employee_res_id,
                    "employee_id": resume.employee_id,
                    "path": resume.employee_resume_path
                }
            return None
    @staticmethod
    def delete_resume(resume_id):
        with app.app_context():
            resume = EmployeeResumes.query.filter_by(employee_res_id=resume_id).first()
            if resume:
                db.session.delete(resume)
                db.session.commit()
                print(f"Resume ID {resume_id} deleted successfully!")
            else:
                print("Resume not found.")
