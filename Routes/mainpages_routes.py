from flask import Blueprint, render_template, session, redirect, url_for 
main_pages = Blueprint('main_pages', __name__)

@main_pages.route('/')
def Home():
    return render_template('homepagesTemp/index.html')

@main_pages.route('/join-us')
def join_us():
    return render_template('homepagesTemp/joinus.html')

@main_pages.route('/login')
def login():
    user_data = session.get('empuser_data')
    
    if user_data:
        return redirect(url_for('dashboard_pages.dashHome'))
    else:
        return render_template('homepagesTemp/login.html')