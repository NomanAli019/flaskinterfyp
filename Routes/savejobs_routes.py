from flask import Blueprint, render_template, session, redirect, url_for , request , flash
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
dashboard_savedjobs = Blueprint('dashboard_savedjobs', __name__)

empportops = EmployeePortfolioOperations()
empresumesops = EmployeeResumesOperations()
empprofilesops = EmployeeProfileOperations()
emplrjobsops  = JobPostOperations()
emplrsavdataops = EmployerSavedDataOperations()
savedjobsops = SavedJobsDataOperations()


@dashboard_savedjobs.route('/dash_savingjob')
def dash_savingjob():
    user_data = session.get('empuser_data')
    if user_data:
        job_id = request.args.get('job_id')
        empid = user_data['id']
        if job_id:
            if savedjobsops.is_job_saved_by_emp(empid , job_id):
                flash('⚠️ The following job is already saved for you try with new one', 'warning')
                return redirect(url_for('dashboard_pages.dashHome'))
            else:
                flash('✅ Job added to saved successfully!', 'success')
                savedjobsops.create_saved_job(empid , job_id)
                return redirect(url_for('dashboard_pages.dash_resum'))

       
    else:
        return render_template('homepagesTemp/login.html')