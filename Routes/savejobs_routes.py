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
dashboard_savedjobs = Blueprint('dashboard_savedjobs', __name__)

empportops = EmployeePortfolioOperations()
empresumesops = EmployeeResumesOperations()
empprofilesops = EmployeeProfileOperations()
emplrjobsops  = JobPostOperations()
emplrsavdataops = EmployerSavedDataOperations()


@dashboard_savedjobs.route('/dash_savingjob')
def dash_savingjob():
    user_data = session.get('empuser_data')
    if user_data:
        return render_template("DashboardTemp/dashsavedjobs.html", user_data=user_data)
    else:
        return render_template('homepagesTemp/login.html')