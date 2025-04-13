from flask import Blueprint, render_template, session, redirect, url_for  , request , jsonify
from DbOperation.JobPosterOp import JobPostOperations
jobpostops = JobPostOperations()
main_pages = Blueprint('main_pages', __name__)

@main_pages.route('/')
def Home():
    return render_template('homepagesTemp/index.html')

@main_pages.route('/submit-job', methods=['POST'])
def submit_job():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    job_description = data.get('job_description')
    source = data.get('source')

    if not all([name, email, phone, job_description, source]):
        return jsonify({"message": "All fields are required!"}), 400

    jobpostops.create_job_post(name , email , phone,job_description , source)
    print(f"New Job Posted by {name} ({email}) from {source}: {job_description}")

    return jsonify({"message": "Job posted successfully!"})

    # return render_template('homepagesTemp/index.html')

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