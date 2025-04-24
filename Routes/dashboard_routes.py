from flask import Blueprint, render_template, session, redirect, url_for , request , flash
from DbOperation.empportOp import EmployeePortfolioOperations
from DbOperation.EmpReumeOp import EmployeeResumesOperations
from DbOperation.empprofileOp import EmployeeProfileOperations
from DbOperation.JobPosterOp import JobPostOperations
from DbOperation.empsavedataOp import EmployerSavedDataOperations
import csv
import os
import re
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text

import pdfplumber as pdfplm
dashboard_pages = Blueprint('dashboard_pages', __name__)

empportops = EmployeePortfolioOperations()
empresumesops = EmployeeResumesOperations()
empprofilesops = EmployeeProfileOperations()
emplrjobsops  = JobPostOperations()
emplrsavdataops = EmployerSavedDataOperations()


@dashboard_pages.route('/dashhome')
def dashHome():
    user_data = session.get('empuser_data')
    userid = user_data['id']
    get_emplr_savedata = emplrsavdataops.get_entries_by_empid(userid)
    print(get_emplr_savedata)
    
    if user_data:
        return render_template('DashboardTemp/dashindex.html' , user_data=user_data , get_emplr_savedata=get_emplr_savedata)
    else:
        return render_template('homepagesTemp/login.html')
    

@dashboard_pages.route('/dashresume')
def dash_resum():
    user_data = session.get('empuser_data')
    empportdata = empportops.get_portfolio_by_employee(user_data['id'])
    empresumedata = empresumesops.get_resumes_by_employee(user_data['id'])
    empprofilepath = empprofilesops.get_profile_by_employee(user_data['id'])
    emplrjobdescs = emplrjobsops.get_all_job_posts()
    try:
        reader = PdfReader(empresumedata['path'])
        resumedatatext_list = []

        # Process pages: extract text and split into words
        for page in reader.pages:
            text = page.extract_text()
            if text:
                words = re.findall(r'\b\w+\b', text.lower())  # Split into words
                resumedatatext_list.append(words)

        csv_file_path = r'SkillSet\tableConvert.com_24utfm.csv'

        matched_skills = []

        try:
            with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header

                for row in reader:
                    if len(row) >= 3:
                        skill = row[2].strip().lower()
                        for word_list in resumedatatext_list:
                            if skill in word_list:
                                matched_skills.append(skill)
                                break

        except FileNotFoundError:
            print(f"File not found at path: {os.path.abspath(csv_file_path)}")

        print("Matched Skills:", matched_skills)
        jobids_matchted_list = [] 
        for job in emplrjobdescs:
            job_desc = job['job_poster_desc'].lower()
        
        # Extract words, ignoring punctuation (like commas, periods, etc.)
            job_words = re.findall(r'\b\w+\b', job_desc)

            matched_count = 0
            matched_in_desc = []

            for skill in matched_skills:
                if skill in job_words:
                    matched_count += 1
                    matched_in_desc.append(skill)

            print(f"Matched Skills in Job: {matched_in_desc}")

            if matched_count >= 3:
                jobids_matchted_list.append(job['job_id'])
        
        print(jobids_matchted_list)
    except Exception as e:
        print(f"An error occurred: {e}")


    try:
        all_suggested_jobsdata = []
        for jobid in jobids_matchted_list:
            jobdata = emplrjobsops.get_job_post_by_id(jobid)
            all_suggested_jobsdata.append(jobdata)
    except Exception as e:
        all_suggested_jobsdata = []

    # for jobid in jobids_matchted_list:

    

    # now those skills of user will be checked with the skills of the job description 



    

    

    if user_data:
        return render_template('DashboardTemp/dashresume.html' , user_data=user_data , empportdata=empportdata  , empprofilepath = empprofilepath , all_suggested_jobsdata=all_suggested_jobsdata)
    else:
        return render_template('homepagesTemp/login.html')


@dashboard_pages.route('/dashinter')
def dash_inter():
    user_data = session.get('empuser_data')
    if user_data:
        try:
            job_id = request.args.get('job_id')
        except Exception as e:
            flash('⚠️ You must select a job before going to the interview room.', 'warning')
            return redirect(url_for('dashboard_pages.dashHome'))

        user_data = session.get('empuser_data')
        print(job_id)
        if job_id:
            return render_template('DashboardTemp/dashinterview.html', user_data=user_data)
        else:
            flash('⚠️ You must select a job before going to the interview room.', 'warning')
            return redirect(url_for('dashboard_pages.dashHome'))
    else:
        return render_template('homepagesTemp/login.html')
    

@dashboard_pages.route('/dashsavedjobs')
def dash_saved_jobs():
    user_data = session.get('empuser_data')
    if user_data:
        return render_template("DashboardTemp/dashsavedjobs.html", user_data=user_data)
    else:
        return render_template('homepagesTemp/login.html')