from flask import Flask
from DBModules.models import JobPost, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/intervisio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class JobPostOperations:
    @staticmethod
    def create_job_post(job_poster_name, job_poster_mail, job_poster_number,jobtitle , job_salary, job_poster_desc, whereyoufind):
        """Create a new job post entry."""
        with app.app_context():
            new_job = JobPost(
                job_poster_name=job_poster_name,
                job_poster_mail=job_poster_mail,
                job_poster_number=job_poster_number,
                job_title=jobtitle,
                job_salary=job_salary,
                job_poster_desc=job_poster_desc,
                whereyoufind=whereyoufind
            )
            db.session.add(new_job)
            db.session.commit()
            print(f"Job post created successfully by {job_poster_name}!")

    @staticmethod
    def get_job_post_by_id(job_id):
        """Retrieve a job post by ID."""
        with app.app_context():
            job = JobPost.query.filter_by(job_id=job_id).first()
            return {
                "job_id": job.job_id,
                "job_poster_name": job.job_poster_name,
                "job_poster_mail": job.job_poster_mail,
                "job_poster_number": job.job_poster_number,
                "job_title":job.job_title,
                "job_salary":job.job_salary,
                "job_poster_desc": job.job_poster_desc,
                "whereyoufind": job.whereyoufind
            } if job else None

    @staticmethod
    def get_all_job_posts():
        """Retrieve all job posts."""
        with app.app_context():
            jobs = JobPost.query.all()
            return [{
                "job_id": job.job_id,
                "job_poster_name": job.job_poster_name,
                "job_poster_mail": job.job_poster_mail,
                "job_poster_number": job.job_poster_number,
                "job_title":job.job_title,
                "job_salary":job.job_salary,
                "job_poster_desc": job.job_poster_desc,
                "whereyoufind": job.whereyoufind
            } for job in jobs] if jobs else []

    @staticmethod
    def update_job_post(job_id, job_poster_name=None, job_poster_mail=None, job_poster_number=None, job_poster_desc=None, whereyoufind=None):
        """Update a job post by ID."""
        with app.app_context():
            job = JobPost.query.filter_by(job_id=job_id).first()
            if job:
                if job_poster_name:
                    job.job_poster_name = job_poster_name
                if job_poster_mail:
                    job.job_poster_mail = job_poster_mail
                if job_poster_number:
                    job.job_poster_number = job_poster_number
                if job_poster_desc:
                    job.job_poster_desc = job_poster_desc
                if whereyoufind:
                    job.whereyoufind = whereyoufind
                
                db.session.commit()
                print(f"Job post ID {job_id} updated successfully!")
            else:
                print("Job post not found.")

    @staticmethod
    def delete_job_post(job_id):
        """Delete a job post by ID."""
        with app.app_context():
            job = JobPost.query.filter_by(job_id=job_id).first()
            if job:
                db.session.delete(job)
                db.session.commit()
                print(f"Job post ID {job_id} deleted successfully!")
            else:
                print("Job post not found.")
