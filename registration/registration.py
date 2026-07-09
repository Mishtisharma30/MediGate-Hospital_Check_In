"""
Register a new user by taking input from HTML form and add person to database of recognizable faces

For the input details and the image uploaded, a new person group person is created. The details obtained from the form as well as the 
face encoding is uploaded on a database.
"""

from flask import Flask, render_template, request, json, redirect, url_for
from flaskext.mysql import MySQL
import os
import numpy as np
import argparse
from create_person_group_person import create_pgp
import json

app = Flask(__name__)
mysql = MySQL()


if __name__ == '__main__':
    # configure arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--DB_USER", required=True, help="MySQL database user")
    ap.add_argument("-p", "--DB_PASSWORD", required=True, help="MySQL database password")
    args = vars(ap.parse_args())
    
    # MySQL configurations
    app.config['MYSQL_DATABASE_USER'] = args['DB_USER']
    app.config['MYSQL_DATABASE_PASSWORD'] = args['DB_PASSWORD']
    app.config['MYSQL_DATABASE_DB'] = 'master'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)

    @app.route("/")
    def main():
        return render_template("profile.html")

    @app.route("/upload", methods=['POST'])    
    def upload():

        # Get form inputs
        _firstName = request.form['firstName']
        _lastName = request.form['lastName']
        _contactnum = str(request.form['contactNum'])
        _aadharnum = str(request.form['aadharNum'])
        _gendertext = request.form['gender']
        _dob = request.form['dob']
        _aptnum = request.form['ApartmentNumber']
        _stadd = request.form['StreetAddress']
        _city = request.form['City']
        _state = request.form['State']
        _pincode = str(request.form['Pincode'])

        form = request.form 

        # Check if upload using POST or Ajax
        is_ajax = False
        if form.get("__ajax", None) == "true":
            is_ajax = True

        # Create upload directory using aadhar number as unique identifier
        my_cwd = os.path.dirname(__file__)
        target = os.path.join(my_cwd, 'static', 'uploads', f"{_aadharnum}")

        # Make directory at target path if it doesnt already exist
        try:
            if not os.path.exists(target):
                os.mkdir(target)
        except:
            if is_ajax:
                return ajax_response(False, "ajax Couldn't create upload directory: {}".format(target))
            else:
                return "Couldn't create upload directory: {}".format(target)

        print("=== Form Data ===")
        for key, value in form.items():
            print(key, ":", value)

    
        # Check if user already existing in database. Aadhar used as basis of check.
        queryString = "select User_ID from user where Aadhar_Num = '{}' ".format(_aadharnum)
        print(queryString)

        # Connecting to MySQL server
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(queryString)
        fetchLabel = cursor.fetchone()

        print(f"fetch label: {fetchLabel}")

        # If user not existing in db
        if fetchLabel is None:

            # Get picture uploaded in form and put at target path
            for upload in request.files.getlist("file"):
                filename = upload.filename.rsplit("/")[0]
                destination = "/".join([target, filename]) # destination = target + filename
                print("Accept incoming file:", filename)
                print("Save it to:", destination)
                upload.save(destination) # uploading to dest

            # Create face encoding from uploaded image
            faceEncoding = create_pgp(_aadharnum, destination)

            if isinstance(faceEncoding, str) and faceEncoding == 'Failed':
                return render_template('unsuccessful.html')

            faceEncodingStr = json.dumps(faceEncoding.tolist())

            # Convert gender input to single character inputs for db
            if _gendertext == 'male':
                _gender = 'M'
            elif _gendertext == 'female':
                _gender = 'F'
            else:
                _gender = 'O'
            
            # Insert data received into the db (User_ID will auto-increment)
            insertString = f"INSERT INTO user(First_Name, Last_Name, Contact_Num, Aadhar_Num, Gender, DOB, StreetAddress, ApartmentNumber, City, State, Pincode, FaceEncoding) VALUES('{_firstName}', '{_lastName}', '{_contactnum}', '{_aadharnum}', '{_gender}', '{_dob}', '{_stadd}', '{_aptnum}', '{_city}', '{_state}', '{_pincode}', '{faceEncodingStr}')"
            print(insertString)
            cursor2 = conn.cursor()
            cursor2.execute(insertString)
            conn.commit()

        else: # user exists in db
            return render_template('user_exists.html')


        if is_ajax:
            return ajax_response(True, _aadharnum)
        else:
            return render_template('successful.html')       

    
if __name__ == "__main__":
    app.run(debug=True)