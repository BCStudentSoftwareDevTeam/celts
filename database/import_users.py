import pyodbc
from app import app
from app.models.user import User
from app.logic.utils import getUsernameFromEmail
import peewee

def main():
    """
    This function runs the updateRecords function once the script is run.
    """
    print("Don't forget to put the correct Tracy password in app/config/local-override.yml")

    addToDb(getStudentData())
    print("done.")
    addToDb(getFacultyStaffData())
    print("done.")

def getCursor():
    details = {
        "user": app.config["tracy"]["user"],
        "password": app.config["tracy"]["password"],
        "host": app.config["tracy"]["host"],
        "db": app.config["tracy"]["name"]
    }
    pyodbc_uri = 'DRIVER=FreeTDS;SERVER={};PORT=1433;DATABASE={};UID={};PWD={};TDS_Version=8.0;'.format(details['host'],details['db'],details['user'],details['password'])

    pyconn = pyodbc.connect(pyodbc_uri)  # connects a tcp based client socket to a tcp based server socket
    return pyconn.cursor()  # allows python to execute sql database commands

def addToDb(userList):
    for user in userList:
        try:
            User.insert(user).execute()

        except peewee.IntegrityError as e:
            if user['username']:
                (User.update(firstName = user['firstName'], lastName = user['lastName'], email = user['email'])
                     .where(user['bnumber'] == User.bnumber)).execute()
            else:
                print(f"No username for {user['bnumber']}!", user)

        except Exception as e:
            print(e)

def getFacultyStaffData():
    """
    This function pulls all the faculty and staff data from Tracy and formats for our table
    """
    print("Retrieving Faculty data from Tracy...",end="")
    c = getCursor()
    return [
          { "username": getUsernameFromEmail(row[4].strip()),
            "bnumber": row[1].strip(),
            "email": row[4].strip(),
            "phoneNumber": None, 
            "firstName": row[2].strip(),
            "lastName": row[3].strip(),
            "isStudent": False,
            "isFaculty": True,
            "isStaff": False,
          }
        for row in c.execute('select * from STUSTAFF')
    ]

def getStudentData():
    """
    This function pulls all the student data from Tracy and formats for our table
    """
    print("Retrieving Student data from Tracy...",end="")
    c = getCursor()
    return [
          { "username": getUsernameFromEmail(row[9].strip()),
            "bnumber": row[1].strip(),
            "email": row[9].strip(),
            "phoneNumber": None, 
            "firstName": row[2].strip(),
            "lastName": row[3].strip(),
            "isStudent": True,
          }
        for row in c.execute('select * from STUDATA')
    ]

if __name__ == '__main__':
    main()
