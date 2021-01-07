import mysql.connector
import os
import requests
import json

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
        self.cursor.execute(query, value)

        for (item) in self.cursor:
            return item[0]

        try:
            self.cursor.execute(query, value)

            for (item) in self.cursor:
                return item[0]
        except:
            return "Oh oh, something went wrong"

    def write_data(self, query, values):



        self.cursor.execute(query, values)
        self.db.commit()


    def get_student_info(self, id):
        print("this is a new student, creating new student row ...")
        # db.write_data(put_new_student_query, put_new_student_value)

        # RETRIEVE JWT token
        post_token = os.getenv('API_URL_TOKEN')
        body = {'grant_type': os.getenv('GRANT_TYPE'), 'client_id': os.getenv('CLIENT_ID'), 'resource': os.getenv('RESOURCE'), 'client_secret': os.getenv('CLIENT_SECRET')}
        token_res = requests.post(post_token, data = body) # save request results
        token_res_obj = json.loads(token_res.text) # convert results to python object

        # convert studentID to readable ID
        altered_student_id = "".join(reversed([id[i:i+2] for i in range(0, len(id), 2)]))
        decimal_id = int(altered_student_id, 16)

        # RETRIEVE student information
        post_student = os.getenv('API_URL_STUDENT_PREFIX') + str(decimal_id) + os.getenv('API_URL_STUDENT_SUFFIX')
        headers = {
            'Authorization': 'Bearer ' + token_res_obj['access_token']
        }
        student_info_res = requests.get(post_student, headers = headers) # save request results
        student_res_obj = json.loads(student_info_res.text) # convert results to python object
        
        return student_res_obj

    def close_connection(self):
        self.db.close()
