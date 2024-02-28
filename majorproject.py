from flask import Flask, render_template, request, session, redirect
from mongoproject3 import MongoDBHelper
import datetime
import hashlib

web_app = Flask('Hospital')
web_app.secret_key = 'your_secret_key'  # Moved secret key initialization here


@web_app.route("/")
def login():
    return render_template("index.html")


@web_app.route("/register")
def register():
    return render_template("register.html")


@web_app.route("/register-patient", methods=['POST'])
def register_patient():
    email = request.form['email']

    db = MongoDBHelper(collection="Hospital")
    existing_station = db.fetch_one({'email': email})

    if existing_station:
        return render_template('error.html', message=f'{email} already registered')

    patient_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'contact': request.form['contact'],
        'email': request.form['email'],
        'gender': request.form['gender'],
        'password': hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest(),
        'createdOn': datetime.datetime.today()
    }
    print(patient_data)

    db.insert(patient_data)

    session['patient_id'] = str(patient_data['_id'])
    session['patient_first_name'] = patient_data['first_name']
    session['patient_email'] = patient_data['email']
    session['patient_contact'] = patient_data['contact']

    return render_template('patientDashboard.html')


@web_app.route("/login-patient", methods=['POST'])
def login_patient():
    login_data = {
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest(),
    }
    print(login_data)

    db = MongoDBHelper(collection="Hospital")
    documents = list(db.fetch(login_data))
    if len(documents) == 1:
        session['id'] = str(documents[0]['_id'])
        session['email'] = documents[0]['email']
        session['patient_id'] = str(documents[0]['_id'])
        session['first_name'] = documents[0]['first_name']
        print(vars(session))
        return render_template('patientDashboard.html')
    else:
        return render_template('error.html', message="Incorrect Email And Password ")


@web_app.route("/admin-login", methods=['POST'])
def admin_login():
    entered_email = request.form.get('email')
    entered_password = request.form.get('password')

    admin_email = "admin@example.com"
    admin_password = "admin123"

    if entered_email == admin_email and entered_password == admin_password:
        return render_template('admin-home.html')
    else:
        return render_template('error.html', message="Incorrect Email or Password ")



if __name__ == "__main__":
    web_app.run(port=5000)
