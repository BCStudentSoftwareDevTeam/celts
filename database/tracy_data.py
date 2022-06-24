import pyodbc
from app.models.user import User
import schedule
import time

def main():
    """
    This function runs the updateRecords function once every 24 hours.
    """
    schedule.every(24).hours.do(updateRecords)

    while 1:
        schedule.run_pending()
        time.sleep(1)

def updateRecords():
    """
    Sets up a connection with an external database and creates new entries for both
    students and faculty in the Users table of the Celts database.
    Currently pulling from Tracy, might need to be update in the future.
    """
    details = {
        "user": "ute_limited",
        "password": "VB6PlU$WcbDBqZ3m0IDX",
        "server": "timemachine1sql.berea.edu",
        "db": "UTE"
    }
    getFacultyUserData(details) # TODO: make it so function updates entries based on bnumber
    getStudentUserData(details) # TODO: make it so function updates entries based on bnumber

def getFacultyUserData(details):
    """
    This function pulls all the faculty data from another database and creates new users
    in the Celts user table.
    Currently pulling data from the Tracy database.
    """
    pyodbc_uri = 'DRIVER=FreeTDS;SERVER={};PORT=1433;DATABASE={};UID={};PWD={};TDS_Version=8.0;'.format(details['server'],details['db'],details['user'],details['password'])

    pyconn = pyodbc.connect(pyodbc_uri)  # connects a tcp based client socket to a tcp based server socket
    c = pyconn.cursor()  # allows python to execute sql database commands

    for row in c.execute('select * from STUSTAFF'):
        try:
            user = {"username": getUsernameFromEmail(row[4]), #Tracy does not have this information
                    "bnumber": row[1],
                    "email": row[4],
                    "phoneNumber": None, # None currently as Tracy does not have phone #'s in database
                    "firstName": row[2],
                    "lastName": row[3],
                    "isStudent": False,
                    "isFaculty": True,
                    "isCeltsAdmin":False,
                    "isCeltsStudentStaff": False
            }
            User.insert(user).execute()
        except Exception as e:
            # Duplicate entry exceptions are expected due to user data already being
            # in the User table of the Celts database
            print(e, " Duplicate entry exceptions are expected.")

def getStudentUserData(details):
    """
    This function pulls all the student data from another database and creates new users
    in the Celts user table.
    Currently pulling data from the Tracy database.
    """
    pyodbc_uri = 'DRIVER=FreeTDS;SERVER={};PORT=1433;DATABASE={};UID={};PWD={};TDS_Version=8.0;'.format(details['server'],details['db'],details['user'],details['password'])
    pyconn = pyodbc.connect(pyodbc_uri)
    c = pyconn.cursor()

    for row in c.execute('select * from STUDATA'):
        try:
            user = {"username": getUsernameFromEmail(row[9]),
                    "bnumber": row[1],
                    "email": row[9],
                    "phoneNumber": None,
                    "firstName": row[2],
                    "lastName": row[3],
                    "isStudent": True,
                    "isFaculty": False,
                    "isCeltsAdmin":False,
                    "isCeltsStudentStaff": False
            }
            User.insert(user).execute()
        except Exception as e:
            # Duplicate entry exceptions are expected due to user data already being
            # in the User table of the Celts database
            print(e, " Duplicate entry exceptions are expected.")

def getUsernameFromEmail(emailStr):
    """
    This function loops through a users email until the index is an "@" and creates the
    username.
    This function will most likely not be needed once we access data from another DB.
    """
    username = ''
    for i in emailStr:
        if i != '@':
            username += i
        else:
            return username

if __name__ == '__main__':
    main()
