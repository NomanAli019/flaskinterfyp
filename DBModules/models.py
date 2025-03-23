from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/intervisio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)  # Store hashed passwords!
    phone_number = db.Column(db.String(50), nullable=False)
    house_address = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Employee {self.full_name}>"
    
class EmployeePortfolioData(db.Model):
    employee_portid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    job_acquired = db.Column(db.String(100), nullable=False)
    total_attempts = db.Column(db.Integer, nullable=False, default=0)
    pass_attempts = db.Column(db.Integer, nullable=False, default=0)
    losing_attempts = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<PortfolioData EmployeeID: {self.employee_id}, Job Acquired: {self.job_acquired}>"

class EmployeeResumes(db.Model):
    employee_res_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee_resume_path = db.Column(db.String(255), nullable=False)


    def __repr__(self):
        return f"<EmployeeResumes {self.employee_resume_path}>"

class EmployeeProfile(db.Model):
    profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    emp_pic_path = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<EmployeeProfile {self.emp_pic_path}>"


# Run this to create tables only once
if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        print("Tables created successfully in intervisio_db!")
