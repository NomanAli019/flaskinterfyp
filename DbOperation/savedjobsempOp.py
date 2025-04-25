from flask import Flask
from DBModules.models import SavedJobsData, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/intervisio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class SavedJobsDataOperations:
    @staticmethod
    def create_saved_job(empid, jobid):
        """Create a new saved job entry."""
        with app.app_context():
            new_saved_job = SavedJobsData(empid=empid, jobid=jobid)
            db.session.add(new_saved_job)
            db.session.commit()
            print(f"Saved job created successfully for EmpID {empid} and JobID {jobid}!")

    @staticmethod
    def get_saved_job_by_id(saved_id):
        """Retrieve a saved job by ID."""
        with app.app_context():
            saved_job = SavedJobsData.query.filter_by(id=saved_id).first()
            return {
                "id": saved_job.id,
                "empid": saved_job.empid,
                "jobid": saved_job.jobid
            } if saved_job else None

    @staticmethod
    def get_all_saved_jobs():
        """Retrieve all saved jobs."""
        with app.app_context():
            saved_jobs = SavedJobsData.query.all()
            return [{
                "id": job.id,
                "empid": job.empid,
                "jobid": job.jobid
            } for job in saved_jobs] if saved_jobs else []

    @staticmethod
    def update_saved_job(saved_id, empid=None, jobid=None):
        """Update a saved job entry by ID."""
        with app.app_context():
            saved_job = SavedJobsData.query.filter_by(id=saved_id).first()
            if saved_job:
                if empid:
                    saved_job.empid = empid
                if jobid:
                    saved_job.jobid = jobid
                db.session.commit()
                print(f"Saved job ID {saved_id} updated successfully!")
            else:
                print("Saved job not found.")

    @staticmethod
    def delete_saved_job(saved_id):
        """Delete a saved job entry by ID."""
        with app.app_context():
            saved_job = SavedJobsData.query.filter_by(id=saved_id).first()
            if saved_job:
                db.session.delete(saved_job)
                db.session.commit()
                print(f"Saved job ID {saved_id} deleted successfully!")
            else:
                print("Saved job not found.")

    @staticmethod
    def is_job_saved_by_emp(empid, jobid):
        """Check if a job is already saved by the given employee."""
        with app.app_context():
            exists = SavedJobsData.query.filter_by(empid=empid, jobid=jobid).first()
            return True if exists else False

    @staticmethod
    def get_saved_jobs_by_empid(empid):
        """Retrieve all saved jobs for a specific employee."""
        with app.app_context():
            saved_jobs = SavedJobsData.query.filter_by(empid=empid).all()
            return [{
                "id": job.id,
                "empid": job.empid,
                "jobid": job.jobid
            } for job in saved_jobs] if saved_jobs else []
