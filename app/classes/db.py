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


    def close_connection(self):
        self.db.close()
