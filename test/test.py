import mysql.connector

# .ENV IMPORTS
import os
from dotenv import load_dotenv

load_dotenv()
USER = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
RAISE_ON_WARNINGS = os.getenv('RAISE_ON_WARNINGS')


# Database configuration

config = {
  'user': USER,
  'password': PASSWORD,
  'host': HOST,
  'database': DATABASE,
  'raise_on_warnings': bool(RAISE_ON_WARNINGS)
}

# OPEN db connection
db = mysql.connector.connect(**config)
cursor = db.cursor()

# SELECT queries
all_students = ("SELECT * FROM Students")
all_classrooms = ("SELECT * FROM Classrooms")
all_scans = ("SELECT c_s.scan, c_s.date,s.firstname, s.lastname,c.title FROM Classrooms_Students as c_s INNER JOIN Students as s on c_s.Student_id = s.id INNER JOIN Classrooms as c on c_s.Classroom_id = c.id")

# INSERT query
new_scan = ("INSERT INTO Classrooms_Students (date, scan, Classroom_id, Student_id) VALUES (%s,%s,%s,%s)")
val = ("2021-12-12", "23:23:23", "2", "3")



def get_data(query):
  cursor.execute(query)
  for (item) in cursor:
    print(item)

def write_data(query, values):
  cursor.execute(new_scan, val)
  db.commit()

# get_data(all_students)
write_data(new_scan, val)




db.close()