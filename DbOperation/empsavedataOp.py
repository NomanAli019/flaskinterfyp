from flask import Flask
from DBModules.models import EmployerSavedData, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/intervisio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class EmployerSavedDataOperations:
    @staticmethod
    def create_entry(empid, job_aquired, total_attempts, no_of_passing_Attempts, no_of_losing_Attempts):
        with app.app_context():
            entry = EmployerSavedData(
                empid=empid,
                job_aquired=job_aquired,
                total_attempts=total_attempts,
                no_of_passing_Attempts=no_of_passing_Attempts,
                no_of_losing_Attempts=no_of_losing_Attempts
            )
            db.session.add(entry)
            db.session.commit()
            print(f"EmployerSavedData for EmpID {empid} created successfully!")

    @staticmethod
    def get_entries_by_empid(empid):
        with app.app_context():
            entry = EmployerSavedData.query.filter_by(empid=empid).first()
            if entry:
                return {
                    "id": entry.id,
                    "empid": entry.empid,
                    "job_aquired": entry.job_aquired,
                    "total_attempts": entry.total_attempts,
                    "no_of_passing_Attempts": entry.no_of_passing_Attempts,
                    "no_of_losing_Attempts": entry.no_of_losing_Attempts
                }
            else:
                return None

    @staticmethod
    def update_entry(empid, job_aquired=None, total_attempts=None, no_of_passing_Attempts=None, no_of_losing_Attempts=None):
        with app.app_context():
            entries = EmployerSavedData.query.filter_by(empid=empid).all()
            if not entries:
                print(f"No entries found for EmpID {empid}")
                return

            for entry in entries:
                if job_aquired is not None:
                    entry.job_aquired = job_aquired
                if total_attempts is not None:
                    entry.total_attempts = total_attempts
                if no_of_passing_Attempts is not None:
                    entry.no_of_passing_Attempts = no_of_passing_Attempts
                if no_of_losing_Attempts is not None:
                    entry.no_of_losing_Attempts = no_of_losing_Attempts

            db.session.commit()
            print(f"Entries for EmpID {empid} updated successfully!")

    @staticmethod
    def delete_entries_by_empid(empid):
        with app.app_context():
            entries = EmployerSavedData.query.filter_by(empid=empid).all()
            if entries:
                for entry in entries:
                    db.session.delete(entry)
                db.session.commit()
                print(f"Entries for EmpID {empid} deleted successfully!")
            else:
                print("No entries found to delete.")
