# To extract the NFCID I used a class created by the GitHub users Doronhorowitz
# https://gist.github.com/doronhorwitz/fc5c4234a9db9ed87c53213d79e63b6c


from classes.db import DB
from classes.pn7150 import PN7150
from datetime import datetime, date
import json


now = datetime.now()
today = date.today()
db = DB()
pn7150 = PN7150()

# set current date and time
current_time = now.strftime("%H:%M:%S")
current_date = today.strftime("%Y-%m-%d")


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

#
# Read nfc cards and write every scan to the db. IF student doesn't exists, it retrieves the info with the help of the Artevelde API
#

def text_callback(text):
    db = DB()
    student_id = text.replace(" ", "")

    # QUERY to check if student exists
    find_student_query = ("SELECT COUNT(nfc_id) FROM students WHERE nfc_id = %s")
    find_student_value = ((str(student_id.decode('unicode_escape').encode('ascii', 'utf-8')), ))


    if db.get_data(find_student_query, find_student_value) == 0:

        # RETRIEVE Student info via the Artevelde API
        student_res_obj = db.get_student_info(student_id)

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
