from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, URL
import csv
import pandas as pd


from dynamic_programing_algorithms import weighted_interval_scheduling


import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv'}

app = Flask(__name__)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_schedule", methods=['GET', 'POST'])
def add_schedule():

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('view_schedule'))

    if request.method == 'GET':
        return render_template("wis_input.html")


@app.route("/view_schedule")
def view_schedule():

    jobs = []

    data = pd.read_csv("static/files/scheduled_surgeries.csv")

    for surgery in data.itertuples():
        start_time = ((int(surgery[3][:2])) * 24) + int(surgery[4][:2])
        end_time = start_time + int(surgery[5])
        new_surgery = weighted_interval_scheduling.Job(start_time, end_time, surgery[6], surgery[1], surgery[2])
        jobs.append(new_surgery)

    jobs_list = weighted_interval_scheduling.findMaxProfitJobs(jobs)
    jobs_list = weighted_interval_scheduling.findMaxProfitJobs(jobs)

    elements = []

    for i in jobs_list:
        print(jobs[i], end=' ')
        elements.append(jobs[i])
        print("\n")

    print( type(jobs_list))
    print(jobs_list)

    return render_template("wis_result.html", surgeries=elements)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == '__main__':
    app.run(debug=True)
