import logging
import pyodbc
import sys
import argparse
from ldap3 import Server, Connection, ALL
import peewee

from app import app
from app.models.user import User
from app.logic.utils import getUsernameFromEmail

# Argument parser for log levels
def parseArgs():
    parser = argparse.ArgumentParser(description="Import users script with logging.")
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Set the logging level'
    )
    return parser.parse_args()

arguments = parseArgs()
logLevels = getattr(logging, arguments.log_level.upper(), logging.INFO)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logLevels)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logLevels)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
consoleHandler.setFormatter(formatter)

logger.addHandler(consoleHandler)

def main():
    """
    This function runs the updateRecords function once the script is run.
    """
    logger.info("Script started.")
    logger.info("Don't forget to put the correct Tracy and LDAP passwords in app/config/local-override.yml")
    
    logger.info("Getting Updated Names, Majors, and Class Levels")
    
    studentData = addToDb(getStudentData())
    studentAdded = studentData[0]
    studentUpdated = studentData[1]
    logger.info(f"{studentAdded} students were added.")
    logger.info(f"{studentUpdated} students were updated.")
    logger.info("Finished updating student data.")
    
    facultyStaffData = addToDb(getFacultyStaffData())
    facultyStaffAdded = facultyStaffData[0]
    facultyStaffUpdated = facultyStaffData[1]
    logger.info(f"{facultyStaffAdded} faculties/staffs were added.")
    logger.info(f"{facultyStaffUpdated} faculties/staffs were updated.")
    logger.info("Finished updating faculty and staff data.")

    logger.info("Getting Preferred Names from LDAP")
    ldap = getLdapConn()
    logger.info("LDAP Connected.")

    people = fetchLdapList(ldap, alphaRange('a','d'))
    people += fetchLdapList(ldap, alphaRange('e','j'))
    people += fetchLdapList(ldap, alphaRange('k','p'))
    people += fetchLdapList(ldap, alphaRange('q','z'))

    updateFromLdap(people)
    logger.info("Update from LDAP Complete.")

def alphaRange(start, end):
    return [chr(i) for i in range(ord(start), ord(end)+1)]

def getLdapConn():
    try:
        server = Server('berea.edu', port=389, use_ssl=False, get_info=ALL)
        conn = Connection(server, user=app.config['ldap']['user'], password=app.config['ldap']['password'])
        if not conn.bind():
            logger.error(f"LDAP bind failed: {conn.result}")
            raise Exception("BindError")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to LDAP: {e}")
        raise

def fetchLdapList(conn, startletters):
    try:
        conn.search(
            'dc=berea,dc=edu',
            f"(|" + "".join(map(lambda s: f"(givenname={s}*)", startletters)) + ")",
            attributes=['samaccountname', 'givenname', 'sn', 'employeeid']
        )
        logger.info(f"Found {len(conn.entries)} entries for {startletters[0]}-{startletters[-1]} in AD")
        return conn.entries
    except Exception as e:
        logger.error(f"Failed to fetch LDAP list for {startletters[0]}-{startletters[-1]}: {e}")
        raise

def updateFromLdap(people):
    for person in people:
        bnumber = str(get_key(person, 'employeeid')).strip()
        preferred = str(get_key(person, 'givenname')).strip()

        if preferred:
            try:
                count = User.update(firstName=preferred).where(User.bnumber == bnumber).execute()
                if count:
                    logger.debug(f"Updated {bnumber} name to {preferred}")
            except Exception as e:
                logger.error(f"Failed to update user {bnumber} with preferred name {preferred}: {e}")

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
    pyodbc_uri = 'DRIVER=FreeTDS;SERVER={};PORT=1433;DATABASE={};UID={};PWD={};TDS_Version=8.0;'.format(
        details['host'], details['db'], details['user'], details['password']
    )
    try:
        pyconn = pyodbc.connect(pyodbc_uri)
        logger.info("Connected to Tracy database.")
        return pyconn.cursor()
    except Exception as e:
        logger.error(f"Failed to connect to Tracy database: {e}")
        raise

def addToDb(userList):
    usersAdded = 0
    usersUpdated = 0
    for user in userList:
        try:
            User.insert(user).execute()
            logger.debug(f"Inserted user {user['bnumber']}")
            userAdded += 1
        except peewee.IntegrityError as e:
            try:
                if user['username']:
                    (User.update(
                        firstName=user['firstName'],
                        lastName=user['lastName'],
                        email=user['email'],
                        major=user['major'],
                        classLevel=user['classLevel'],
                        cpoNumber=user['cpoNumber']
                    ).where(User.bnumber == user['bnumber'])).execute()
                    logger.debug(f"Updated user {user['bnumber']}")
                    userUpdated += 1
                else:
                    logger.warning(f"No username for {user['bnumber']}!", user)
            except Exception as e:
                logger.error(f"Failed to update user {user['bnumber']}: {e}")
        except Exception as e:
            logger.error(f"Failed to insert or update user {user['bnumber']}: {e}")
            
        return [usersAdded, usersUpdated]

def getFacultyStaffData():
    logger.info("Retrieving Faculty and Staff data from Tracy...")
    try:
        c = getMssqlCursor()
        return [ 
            {
                "username": getUsernameFromEmail(row[4].strip()),
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
                "cpoNumber": row[5].strip(),
            }
            for row in c.execute('select * from STUSTAFF')
        ]
    except Exception as e:
        logger.error(f"Failed to retrieve Faculty and Staff data: {e}")
        raise

def getStudentData():
    logger.info("Retrieving Student data from Tracy...")
    try:
        c = getMssqlCursor()
        return [
            {
                "username": getUsernameFromEmail(row[9].strip()),
                "bnumber": row[1].strip(),
                "email": row[9].strip(),
                "phoneNumber": None, 
                "firstName": row[2].strip(),
                "lastName": row[3].strip(),
                "isStudent": True,
                "major": row[6].strip(),
                "classLevel": row[4].strip(),
                "cpoNumber": row[10].strip(),
            }
            for row in c.execute('select * from STUDATA')
        ]
    except Exception as e:
        logger.error(f"Failed to retrieve Student data: {e}")
        raise

if __name__ == '__main__':
    main()
