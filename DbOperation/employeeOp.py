from flask import Flask
from DBModules.models import Employee, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/intervisio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class EmployeeOperations:
    @staticmethod
    def create_user(full_name, email, password, phone_number, house_address, country):
        with app.app_context():
            new_employee = Employee(
                full_name=full_name,
                email=email,
                password=password,  # Store a **hashed** password in production
                phone_number=phone_number,
                house_address=house_address,
                country=country
            )
            db.session.add(new_employee)
            db.session.commit()
            print(f"User {full_name} created successfully!")

    @staticmethod
    def check_user(email):
        with app.app_context():
            try:
                user = Employee.query.filter_by(email=email).first()
                if user:
                    return True
                else:
                    return False
            except Exception as e:
                return False
            
    @staticmethod
    def verify_user(email, password):
        with app.app_context():
            user = Employee.query.filter_by(email=email, password=password).first()
            if user:
                return user  # Return the full user object instead of just True
            return None  # Return None if no matching user is found



    @staticmethod
    def delete_user(email):
        with app.app_context():
            user = Employee.query.filter_by(email=email).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                print(f"User {user.full_name} deleted successfully!")
            else:
                print("User not found.")
