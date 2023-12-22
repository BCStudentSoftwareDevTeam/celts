import logging
import sys
import pyodbc
from ldap3 import Server, Connection, ALL
import peewee

from app import app
from app.models.user import User
from app.logic.utils import getUsernameFromEmail

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("import_users_log.txt")
    ]
)

def main():
    """
    This function runs the updateRecords function once the script is run.
    """
    logging.info("Don't forget to put the correct Tracy and LDAP passwords in app/config/local-override.yml")

    logging.info("\nGetting Updated Names, Majors, and Class Levels\n--------------------------------------------------\n")

    addToDb(getStudentData())
    logging.info("done.")
    addToDb(getFacultyStaffData())
    logging.info("done.")

    logging.info("\n\nGetting Preferred Names\n--------------------------\n")

    ldap = getLdapConn()
    logging.info("LDAP Connected.")

    people = fetchLdapList(ldap, alphaRange('a','d'))
    people += fetchLdapList(ldap, alphaRange('e','j'))
    people += fetchLdapList(ldap, alphaRange('k','p'))
    people += fetchLdapList(ldap, alphaRange('q','z'))

    updateFromLdap(people)
    logging.info("Update Complete.")

def alphaRange(start,end):
    return [chr(i) for i in range(ord(start), ord(end)+1)]

def getLdapConn():
    server = Server ('berea.edu', port=389, use_ssl=False, get_info='ALL')
    conn   = Connection (server, user=app.config['ldap']['user'], password=app.config['ldap']['password'])
    if not conn.bind():
        logging.error(conn.result)
        raise Exception("BindError")

    return conn

def fetchLdapList(conn, startletters):
    # Get the givennames from LDAP - we have to segment them to make sure each request is under 1500
    conn.search('dc=berea,dc=edu',
      f"(|" + "".join(map(lambda s: f"(givenname={s}*)", startletters)) + ")",
      attributes = ['samaccountname', 'givenname', 'sn', 'employeeid']
      )
    logging.info(f"Found {len(conn.entries)} {startletters[0]}-{startletters[-1]} in AD");
    return conn.entries

def updateFromLdap(people):
    for person in people:
        bnumber = str(get_key(person, 'employeeid')).strip()
        preferred = str(get_key(person, 'givenname')).strip()

        if preferred:
            count = User.update(firstName=preferred).where(User.bnumber == bnumber).execute()
            if count:
                logging.info(f"Updating {bnumber} name to {preferred}")

# Return the value for a key or None
# Can't use .get() because it's a ldap3.abstract.entry.Entry instead of a Dict
def get_key(entry, key):
    if key in entry:
        return entry[key]
    else:
        return None

def getMssqlCursor():
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
                (User.update(firstName = user['firstName'], lastName = user['lastName'], email = user['email'], major = user['major'], classLevel = user['classLevel'])
                     .where(user['bnumber'] == User.bnumber)).execute()
            else:
                logging.warning(f"No username for {user['bnumber']}!", user)

        except Exception as e:
            logging.error(e)

def getFacultyStaffData():
    """
    This function pulls all the faculty and staff data from Tracy and formats for our table
    """
    logging.info("Retrieving Faculty data from Tracy...",end="")
    c = getMssqlCursor()
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
            "major": None,
            "classLevel": None,
          }
        for row in c.execute('select * from STUSTAFF')
    ]

def getStudentData():
    """
    This function pulls all the student data from Tracy and formats for our table
    """
    logging.info("Retrieving Student data from Tracy...",end="")
    c = getMssqlCursor()
    return [
          { "username": getUsernameFromEmail(row[9].strip()),
            "bnumber": row[1].strip(),
            "email": row[9].strip(),
            "phoneNumber": None, 
            "firstName": row[2].strip(),
            "lastName": row[3].strip(),
            "isStudent": True,
            "major": row[6].strip(),
            "classLevel": row[4].strip()
          }
        for row in c.execute('select * from STUDATA')
    ]

if __name__ == '__main__':
    main()