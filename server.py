from flask import Flask, redirect, request, url_for, render_template
import database_manager

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mentors')
def mentors():
    data = database_manager.select_query("SELECT mentors.first_name, mentors.last_name, schools.country FROM mentors \
                                       INNER JOIN schools ON mentors.city = schools.city")
    table_header = list(data[0].keys())
    return render_template('table.html', data=data, table_header=table_header)


@app.route('/all-school')
def all_school():
    data = database_manager.select_query("SELECT COALESCE(mentors.first_name, 'No data') AS mentor_first_name, COALESCE(mentors.last_name, 'No data') AS mentor_last_name, schools.name, schools.country \
                                       FROM mentors \
                                       RIGHT JOIN schools ON mentors.city = schools.city \
                                       ORDER BY mentors.id")
    table_header = list(data[0].keys())
    return render_template('table.html', data=data, table_header=table_header)                                   


@app.route('/mentors-by-country')
def mentors_by_country():
    data = database_manager.select_query("SELECT COUNT(mentors.id), schools.country FROM mentors \
                                       INNER JOIN schools ON mentors.city = schools.city \
                                       GROUP BY schools.country")
    table_header = list(data[0].keys())
    return render_template('table.html', data=data, table_header=table_header)    

@app.route('/contacts')
def contacts():
    data = database_manager.select_query("SELECT schools.name, mentors.first_name, mentors.last_name FROM mentors \
                                       INNER JOIN schools ON mentors.id = schools.contact_person \
                                       ORDER BY schools.name")
    table_header = list(data[0].keys())
    return render_template('table.html', data=data, table_header=table_header)

@app.route('/applicants')
def applicants():
    data = database_manager.select_query("SELECT applicants.first_name, applicants.application_code, applicants_mentors.creation_date \
                                       FROM applicants \
                                       INNER JOIN applicants_mentors ON applicants.id = applicants_mentors.applicant_id AND applicants_mentors.creation_date > '2016-01-01' \
                                       ORDER BY applicants_mentors.creation_date")
    table_header = list(data[0].keys())
    return render_template('table.html', data=data, table_header=table_header)

@app.route('/applicants-and-mentros')
def applicants_and_mentors():
    data = database_manager.select_query("SELECT applicants.first_name, applicants.application_code, COALESCE(mentors.first_name, 'No data') AS mentor_first_name, COALESCE(mentors.last_name, 'No data') AS mentor_last_name \
                                       FROM applicants_mentors \
                                       INNER JOIN mentors ON applicants_mentors.mentor_id = mentors.id \
                                       RIGHT JOIN applicants ON applicants_mentors.applicant_id = applicants.id \
                                       ORDER BY applicants.id")
    table_header = list(data[0].keys())
    return render_template('table.html', data=data, table_header=table_header)

if __name__ == "__main__":
    app.run(debug=True)
