from flask import Flask
from DBModules.models import EmployeePortfolioData, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/intervisio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class EmployeePortfolioOperations:
    @staticmethod
    def add_portfolio_data(employee_id, job_acquired, total_attempts=0, pass_attempts=0, losing_attempts=0):
        with app.app_context():
            new_portfolio = EmployeePortfolioData(
                employee_id=employee_id,
                job_acquired=job_acquired,
                total_attempts=total_attempts,
                pass_attempts=pass_attempts,
                losing_attempts=losing_attempts
            )
            db.session.add(new_portfolio)
            db.session.commit()
            print(f"Portfolio data added for Employee ID: {employee_id}")

    @staticmethod
    def get_portfolio_by_employee(employee_id):
        with app.app_context():
            portfolio = EmployeePortfolioData.query.filter_by(employee_id=employee_id).first()
            return {
                "employee_id": portfolio.employee_id,
                "job_acquired": portfolio.job_acquired,
                "total_attempts": portfolio.total_attempts,
                "pass_attempts": portfolio.pass_attempts,
                "losing_attempts": portfolio.losing_attempts,
                "created_at": portfolio.created_at
            } if portfolio else None

    @staticmethod
    def update_portfolio_attempts(employee_id, created_at=None):
        with app.app_context():
            portfolio = EmployeePortfolioData.query.filter_by(employee_id=employee_id).first()
            if portfolio:
                if created_at:
                    portfolio.created_at = created_at
                
                db.session.commit()
                print(f"Portfolio updated for Employee ID: {employee_id}")
            else:
                print("Portfolio not found.")

    @staticmethod
    def delete_portfolio(employee_id):
        with app.app_context():
            portfolio = EmployeePortfolioData.query.filter_by(employee_id=employee_id).first()
            if portfolio:
                db.session.delete(portfolio)
                db.session.commit()
                print(f"Portfolio data deleted for Employee ID: {employee_id}")
            else:
                print("Portfolio not found.")

    @staticmethod
    def check_portfolio_exists(employee_id):
        """Check if an employee's portfolio exists."""
        with app.app_context():
            exists = db.session.query(EmployeePortfolioData.query.filter_by(employee_id=employee_id).exists()).scalar()
            return exists
