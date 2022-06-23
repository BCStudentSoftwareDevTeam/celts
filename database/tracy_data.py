import pyodbc # module that accesses ODBC (MySQL) databases
from app.models.user import User


details = {                     # information to access server
    "user": "ute_limited",
    "password": "VB6PlU$WcbDBqZ3m0IDX",
    "server": "timemachine1sql.berea.edu",
    "db": "UTE"
}
def main():
    # uniform resource identifier contains name which refers to an object in the web
    pyodbc_uri = 'DRIVER=FreeTDS;SERVER={};PORT=1433;DATABASE={};UID={};PWD={};TDS_Version=8.0;'.format(details['server'],details['db'],details['user'],details['password'])

    pyconn = pyodbc.connect(pyodbc_uri)  # connects a tcp based client socket to a tcp based server socket
    c = pyconn.cursor()  # allows python to execute sql database command??

    for row in c.execute('select * from STUSTAFF'):
        try:
            user = {"username": getUsernameFromEmail(row[4]),
                    "bnumber": row[1],
                    "email": row[4],
                    "phoneNumber": "000000",
                    "firstName": row[2],
                    "lastName": row[3],
                    "isStudent": False,
                    "isFaculty": True,
                    "isCeltsAdmin":False,
                    "isCeltsStudentStaff": False
            }

            User.insert(user).execute()
        except:
            pass


def getUsernameFromEmail(emailStr):
    newEmailStr = ''

    for i in emailStr:
        if i != '@':
            newEmailStr += i
        else:
            return newEmailStr

main()
