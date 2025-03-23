from flask import Blueprint, render_template, session, redirect, url_for 
from DbOperation.empportOp import EmployeePortfolioOperations
from DbOperation.EmpReumeOp import EmployeeResumesOperations
from DbOperation.empprofileOp import EmployeeProfileOperations
dashboard_pages = Blueprint('dashboard_pages', __name__)

empportops = EmployeePortfolioOperations()
empresumesops = EmployeeResumesOperations()
empprofilesops = EmployeeProfileOperations()


@dashboard_pages.route('/dashhome')
def dashHome():
    user_data = session.get('empuser_data')
    
    if user_data:
        return render_template('DashboardTemp/dashindex.html' , user_data=user_data)
    else:
        return render_template('homepagesTemp/login.html')
    

@dashboard_pages.route('/dashresume')
def dash_resum():
    user_data = session.get('empuser_data')
    empportdata = empportops.get_portfolio_by_employee(user_data['id'])
    empresumedata = empresumesops.get_resumes_by_employee(user_data['id'])
    empprofilepath = empprofilesops.get_profile_by_employee(user_data['id'])

    if user_data:
        return render_template('DashboardTemp/dashresume.html' , user_data=user_data , empportdata=empportdata , empresumedata=empresumedata , empprofilepath = empprofilepath)
    else:
        return render_template('homepagesTemp/login.html')


@dashboard_pages.route('/dashinter')
def dash_inter():
    return render_template('DashboardTemp/dashinterview.html')