from flask import Blueprint, render_template, session, redirect, url_for , request , flash , jsonify
import requests
from DbOperation.empportOp import EmployeePortfolioOperations
from DbOperation.EmpReumeOp import EmployeeResumesOperations
from DbOperation.empprofileOp import EmployeeProfileOperations
from DbOperation.JobPosterOp import JobPostOperations
from DbOperation.empsavedataOp import EmployerSavedDataOperations
from DbOperation.savedjobsempOp import SavedJobsDataOperations
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
savedjobsops = SavedJobsDataOperations()


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

    if user_data:
        return render_template('DashboardTemp/dashresume.html' , user_data=user_data , empportdata=empportdata  , empprofilepath = empprofilepath , all_suggested_jobsdata=all_suggested_jobsdata)
    else:
        return render_template('homepagesTemp/login.html')


@dashboard_pages.route('/dashinter', methods=['GET', 'POST'])
def dash_inter():
    user_data = session["empuser_data"]
    job_id = request.args.get("job_id")
    
    

    if request.method == 'GET':
        # Setup session on first load
        if "chat_history" not in session:
            user_data = session["empuser_data"]
            name = user_data['full_name']
            resume_info = "2+ years of experience in Python coding"
            job_description = emplrjobsops.get_job_post_by_id(job_id)['job_poster_desc']

            system_prompt = (
                f"You are a strict HR assistant conducting a job interview with a candidate named {name}. "
                f"The candidate's resume mentions: {resume_info}. "
                f"The job description mentions: {job_description}. "
                "Ask only 10 questions in total. "
                "The first 4 questions must be about the candidate's past experience. "
                "The next 6 questions must be technical and scenario-based. "
                "Only ask one question at a time. "
                "Ask counter-questions based on the candidate’s answers. "
                "Evaluate at the end with a score and strengths/weaknesses."
            )

            session["chat_history"] = [{"role": "system", "content": system_prompt}]
            session["question_count"] = 0

            # Ask first question
            payload = {
                "model": "mistral-large-latest",
                "messages": session["chat_history"]
            }

            response = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer Cn66z1g23eruHwrjmO1wdO1ezcMQVPOO",
                    "Content-Type": "application/json"
                },
                json=payload
            )

            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"]
                session["chat_history"].append({"role": "assistant", "content": reply})
                session["question_count"] += 1
            else:
                reply = "Sorry, the bot couldn't start the interview right now."

        else:
            # If already started
            reply = session["chat_history"][-1]["content"]

        return render_template("DashboardTemp/dashinterview.html",user_data=user_data ,bot_reply=reply, job_id=job_id)
    
    elif request.method == 'POST':
        data = request.get_json()
        user_input = data.get("user_input", "").strip()
        job_id = data.get("job_id")

        if not user_input:
            return jsonify({"error": "Please type your answer to proceed."})

        session["chat_history"].append({"role": "user", "content": user_input})

        if session.get("question_count", 0) >= 10:
            return jsonify({
                "bot_reply": "✅ Thank you. The interview is complete. Please wait while we evaluate your performance.",
                "finished": True
            })

        # Call API
        payload = {
            "model": "mistral-large-latest",
            "messages": session["chat_history"]
        }

        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": "Bearer Cn66z1g23eruHwrjmO1wdO1ezcMQVPOO",
                "Content-Type": "application/json"
            },
            json=payload
        )

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            session["chat_history"].append({"role": "assistant", "content": reply})
            session["question_count"] += 1
            return jsonify({"bot_reply": reply})
        else:
            return jsonify({"error": "Sorry, the bot is currently unavailable."})


    # user_data = session.get('empuser_data')
    # if user_data:
    #     try:
    #         job_id = request.args.get('job_id')
    #     except Exception as e:
            
    #         flash('⚠️ You must select a job before going to the interview room.', 'warning')
    #         return redirect(url_for('dashboard_pages.dashHome'))

    #     user_data = session.get('empuser_data')
    #     print(job_id)
    #     if job_id:
    #         empid = user_data['id']
    #         jobdesc = emplrjobsops.get_job_post_by_id(job_id)
    #         jobdesc = jobdesc['job_poster_desc']
    #         print(jobdesc)
    #         return render_template('DashboardTemp/dashinterview.html', user_data=user_data)
    #     else:
    #         flash('⚠️ You must select a job before going to the interview room.', 'warning')
    #         return redirect(url_for('dashboard_pages.dashHome'))
    # else:
    #     return render_template('homepagesTemp/login.html')
    

@dashboard_pages.route('/dashsavedjobs')
def dash_saved_jobs():
    user_data = session.get('empuser_data')
    if user_data:
        empid = user_data['id']
        savedjobsdata = savedjobsops.get_saved_jobs_by_empid(empid)
        alljobsavedata = []

        for job in savedjobsdata:
            aselectedjob = emplrjobsops.get_job_post_by_id(job['jobid'])
            alljobsavedata.append(aselectedjob)
        print(alljobsavedata)
        
        return render_template("DashboardTemp/dashsavedjobs.html", user_data=user_data , alljobsavedata=alljobsavedata)
    else:
        return render_template('homepagesTemp/login.html')