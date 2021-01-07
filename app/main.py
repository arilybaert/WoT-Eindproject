# To extract the NFCID I used a class created by the GitHub users Doronhorowitz
# https://gist.github.com/doronhorwitz/fc5c4234a9db9ed87c53213d79e63b6c


from classes.db import DB
from classes.pn7150 import PN7150
from datetime import datetime, date
import json
import requests
import os


now = datetime.now()
today = date.today()
db = DB()

# set current date and time
current_time = now.strftime("%H:%M:%S")
current_date = today.strftime("%Y-%m-%d")


pn7150 = PN7150()

filename = "/home/pi/Desktop/config.txt"

exam = 0


#
# Read the config.txt file that is saved on the desktop to retreive all the variables
#

# Load txt file
if filename:
    with open(filename, 'r') as f:
        datastore = json.load(f)
    f.close()

# check if classroom is set
if datastore["classroom"] == "":
    print("no classroom has been set, what classroom is this?")

    data = {}

    # ask for classroom
    classroom = raw_input("")
    input = db.get_data(("SELECT title FROM classrooms WHERE title = %s"), ((str(classroom.decode('unicode_escape').encode('ascii', 'utf-8')), )))

    # validate classroom in db
    while(str(input) == "None"):
        print("Classroom: " + classroom + " is wrong or doesn't exist. Use this notation for example: B20")
        classroom = raw_input("")
        input = db.get_data(("SELECT title FROM classrooms WHERE title = %s"), ((str(classroom.decode('unicode_escape').encode('ascii', 'utf-8')), )))

    print("Classroom: " + classroom + " is set!")

    # update txt file with give classroom
    data["classroom"] = classroom
    with open(filename, 'r+') as f:
        data = json.load(f)
        data["classroom"] = classroom
        f.seek(0)
        json.dump(data, f)
        f.truncate()

else:
    classroom = datastore["classroom"]
    print("classroom has been set to " + datastore["classroom"])

if datastore["exam_mode"] == "0":
    print("exam mode is off")
    exam = 0
if datastore["exam_mode"] == "1":
    print("exam mode is on")
    exam = 1



def text_callback(text):
    db = DB()
    student_id = text.replace(" ", "")


    # QUERY to check if student exists
    find_student_query = ("SELECT COUNT(nfc_id) FROM students WHERE nfc_id = %s")
    find_student_value = ((str(student_id.decode('unicode_escape').encode('ascii', 'utf-8')), ))


    if db.get_data(find_student_query, find_student_value) == 0:
        print("this is a new student, creating new student row ...")
        # db.write_data(put_new_student_query, put_new_student_value)

        # RETRIEVE JWT token
        post_token = os.getenv('API_URL_TOKEN')
        body = {'grant_type': os.getenv('GRANT_TYPE'), 'client_id': os.getenv('CLIENT_ID'), 'resource': os.getenv('RESOURCE'), 'client_secret': os.getenv('CLIENT_SECRET')}
        token_res = requests.post(post_token, data = body) # save request results
        token_res_obj = json.loads(token_res.text) # convert results to python object

        # convert studentID to readable ID
        altered_student_id = "".join(reversed([student_id[i:i+2] for i in range(0, len(student_id), 2)]))
        decimal_id = int(altered_student_id, 16)

        # RETRIEVE student information
        post_student = os.getenv('API_URL_STUDENT_PREFIX') + str(decimal_id) + os.getenv('API_URL_STUDENT_SUFFIX')
        headers = {
            'Authorization': 'Bearer ' + token_res_obj['access_token']
        }
        student_info_res = requests.get(post_student, headers = headers) # save request results
        student_res_obj = json.loads(student_info_res.text) # convert results to python object


        #   QUERY to create new student
        put_new_student_query = ("INSERT INTO students (firstname, lastname, email, nfc_id) VALUES (%s,%s,%s,%s)")
        put_new_student_value = (student_res_obj['Voornaam'], student_res_obj['Naam'], student_res_obj['Email'], student_id)

        db.write_data(put_new_student_query, put_new_student_value) # write new student to db

    



    # query FIND CLASSROOM
    find_class_query = ("SELECT id FROM classrooms WHERE title = %s")
    find_class_value =((str(classroom.decode('unicode_escape').encode('ascii', 'utf-8')), ))

    # query WRITE NEW SCAN
    put_students_query = ("INSERT INTO classrooms__students (scan_date, scan_time, classroom_id, student_id, exam) VALUES (%s,%s,%s,%s,%s)")
    put_students_value = (current_date, current_time, db.get_data(find_class_query, find_class_value), student_id, exam)
    

    print(student_id)
    
    db.write_data(put_students_query, put_students_value)


pn7150.when_tag_read = text_callback
pn7150.start_reading()




db.close_connection()
