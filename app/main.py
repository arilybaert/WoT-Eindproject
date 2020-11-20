from classes.db import DB
from datetime import datetime, date


now = datetime.now()
today = date.today()
db = DB()


# set current date and time
current_time = now.strftime("%H:%M:%S")
current_date = today.strftime("%Y-%m-%d")


print("What classroom is this?")

# handle client input and db query
classroom = raw_input("")
input = db.get_data(("SELECT title FROM Classrooms WHERE title = %s"), ((str(classroom.decode('unicode_escape').encode('ascii', 'utf-8')), )))

# check input and validate it
if str(input) == "None":
    print("Classroom: " + classroom + " is wrong or doesn't exist. Use this notation for example: B20")
else:
    print("Classroom: " + classroom + " is set!")




while (False):

    # query FIND CLASSROOM
    find_class_query = ("SELECT id FROM Classrooms WHERE title = %s")
    find_class_value =((str(classroom.decode('unicode_escape').encode('ascii', 'utf-8')), ))


    # INPUT STUDENT ID
    student_id = raw_input("")

    # query WRITE NEW SCAN
    put_students_query = ("INSERT INTO Classrooms_Students (scan_date, scan_time, Classroom_id, Student_id) VALUES (%s,%s,%s,%s)")
    put_students_value = (current_date, current_time, db.get_data(find_class_query, find_class_value), student_id)

    db.write_data(put_students_query, put_students_value)

db.close_connection()