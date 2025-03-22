from flask import Blueprint, render_template, session, redirect, url_for 
dashboard_pages = Blueprint('dashboard_pages', __name__)

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

    if user_data:
        return render_template('DashboardTemp/dashresume.html' , user_data=user_data)
    else:
        return render_template('homepagesTemp/login.html')


@dashboard_pages.route('/dashinter')
def dash_inter():
    return render_template('DashboardTemp/dashinterview.html')