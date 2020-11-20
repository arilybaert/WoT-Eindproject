import mysql.connector
import os

from dotenv import load_dotenv
from datetime import datetime, date


class DB(object):
    def __init__(self):

        self.now = datetime.now()
        self.today = date.today()

        # Load ENV variables
        load_dotenv()
        USER = os.getenv('USERNAME')
        PASSWORD = os.getenv('PASSWORD')
        HOST = os.getenv('HOST')
        DATABASE = os.getenv('DATABASE')
        RAISE_ON_WARNINGS = os.getenv('RAISE_ON_WARNINGS')

        # Set DB configuration
        config = {
        'user': USER,
        'password': PASSWORD,
        'host': HOST,
        'database': DATABASE,
        'raise_on_warnings': bool(RAISE_ON_WARNINGS)
        }

        # OPEN db connection
        self.db = mysql.connector.connect(**config)
        self.cursor = self.db.cursor()



    def get_data(self, query, value):
        try:
            self.cursor.execute(query, value)

            for (item) in self.cursor:
                    return item[0]
        except:
            return "Oh oh, something went wrong"

    def write_data(self, query, values):



        self.cursor.execute(query, values)
        self.db.commit()



    # # Get classroom
    # def find_class(self, classr):
    #     # query
    #     find_class_query = ("SELECT id FROM Classrooms WHERE title = %s")
    #     find_class_value =((str(classr.decode('unicode_escape').encode('ascii', 'utf-8')), ))

    #     self.cursor.execute(find_class_query, find_class_value)
    #     for (item) in self.cursor:
    #         # print(item[0]) # print proper classroom title
    #         return item[0]

    # Put student scan
    def put_student_scan(self, student_id, classroom_id):

        # set current date and time
        current_time = self.now.strftime("%H:%M:%S")
        current_date = self.today.strftime("%Y-%m-%d")

        # query
        put_students_query = ("INSERT INTO Classrooms_Students (scan_date, scan_time, Classroom_id, Student_id) VALUES (%s,%s,%s,%s)")
        put_students_value = (current_date, current_time, classroom_id, student_id)
        try:
            self.cursor.execute(put_students_query, put_students_value)
            self.db.commit()
        except:
            return "Oh oh, something went wrong"


    def close_connection(self):
        self.db.close()
