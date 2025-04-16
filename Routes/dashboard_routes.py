from flask import Blueprint, render_template, session, redirect, url_for 
from DbOperation.empportOp import EmployeePortfolioOperations
from DbOperation.EmpReumeOp import EmployeeResumesOperations
from DbOperation.empprofileOp import EmployeeProfileOperations
import csv
import os
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
import pdfplumber as pdfplm
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
    
    reader = PdfReader(empresumedata['path'])
    number_of_pages = len(reader.pages)
    for i in range(0,number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        print(text)

    csv_file_path = r'SkillSet\tableConvert.com_24utfm.csv'  # raw string


    try:
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            
            output = []
            for row in reader:
                if len(row) >= 3:
                    output.append(row[2])
                    print(row[2])
        
        
    except FileNotFoundError:
        return f"File not found at path: {os.path.abspath(csv_file_path)}"

    # print('\n pdf miner')
    # text = extract_text(empresumedata['path'])
    # print(text)

    # print('\n PDF plumber')
    # with pdfplm.open('resum.pdf') as pdf:
    #     nopages = len(pdf.pages)
    #     for i in range(0,nopages):
    #         print(pdf.pages[i].extract_text())

    print(empresumedata)

    if user_data:
        return render_template('DashboardTemp/dashresume.html' , user_data=user_data , empportdata=empportdata , empresumedata=empresumedata , empprofilepath = empprofilepath)
    else:
        return render_template('homepagesTemp/login.html')


@dashboard_pages.route('/dashinter')
def dash_inter():
    user_data = session.get('empuser_data')
    return render_template('DashboardTemp/dashinterview.html', user_data=user_data)