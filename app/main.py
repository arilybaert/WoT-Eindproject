# To extract the NFCID I used a class created by the GitHub users Doronhorowitz
# https://gist.github.com/doronhorwitz/fc5c4234a9db9ed87c53213d79e63b6c


from classes.db import DB
from classes.pn7150 import PN7150
from datetime import datetime, date
import json


now = datetime.now()
today = date.today()
db = DB()

# set current date and time
current_time = now.strftime("%H:%M:%S")
current_date = today.strftime("%Y-%m-%d")


pn7150 = PN7150()

filename = "/home/pi/Desktop/config.txt"




#
# Read the config.txt file that is dsave on the desktop to retreive all the variables
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
if datastore["exam_mode"] == "1":
    print("exam mode is on")



def text_callback(text):
    student_id = "eVunVfMWaa"
    print("classroom " + classroom)
    print("student ID " + student_id)

    # query FIND CLASSROOM
    find_class_query = ("SELECT id FROM classrooms WHERE title = %s")
    find_class_value =((str(classroom.decode('unicode_escape').encode('ascii', 'utf-8')), ))

    # query WRITE NEW SCAN
    put_students_query = ("INSERT INTO classrooms__students (scan_date, scan_time, Classroom_id, Student_id) VALUES (%s,%s,%s,%s)")

    put_students_value = (current_date, current_time, db.get_data(find_class_query, find_class_value), student_id)
    
    print(current_date)
    print(current_time)
    print(db.get_data(find_class_query, find_class_value))
    print(student_id)
    
    #db.write_data(put_students_query, put_students_value)
    
    # try:
    #     db.write_data(put_students_query, put_students_value)
    # except:
    #     print("oh oh wrong student ID")

pn7150.when_tag_read = text_callback
pn7150.start_reading()


# student_id = "eVunVfMWaa"
# print("classroom " + classroom)
# print("student ID " + student_id)
# # query FIND CLASSROOM
# find_class_query = ("SELECT id FROM classrooms WHERE title = %s")
# find_class_value =((str(classroom.decode('unicode_escape').encode('ascii', 'utf-8')), ))

# # query WRITE NEW SCAN
# put_students_query = ("INSERT INTO classrooms__students (scan_date, scan_time, Classroom_id, Student_id) VALUES (%s,%s,%s,%s)")

# put_students_value = (current_date, current_time, db.get_data(find_class_query, find_class_value), student_id)
# db.write_data(put_students_query, put_students_value)



db.close_connection()