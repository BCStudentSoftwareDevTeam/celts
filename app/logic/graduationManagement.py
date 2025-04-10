import xlsxwriter
from app import app
from peewee import JOIN

from app.models.user import User
from app.models.bonnerCohort import BonnerCohort
from app.logic.minor import getMinorProgress

def getGraduationManagementUsers():
    """
    Function to fetch all senior students along with their CCE Minor Progress and Bonner Status 
    """

    elibibleUsers = (User.select(User.username, User.hasGraduated, User.classLevel, User.firstName, User.lastName, BonnerCohort.year)
                 .join(BonnerCohort, JOIN.LEFT_OUTER, on=(BonnerCohort.user == User.username))
                 .where(User.classLevel == 'Senior'))

    cceStudents = set([user["username"] for user in getMinorProgress()])

    graduationManagementUsers = []
    for user in elibibleUsers:
        userDict = user.__dict__
        graduationManagementUsers.append({
            "user": user,
            "cohort": userDict['bonnercohort'].year if 'bonnercohort' in userDict else None,
            "minorProgress": user.username in cceStudents})

    return graduationManagementUsers


def setGraduatedStatus(username, status):
    """
    Update a students graduation status based on the parameter status.
    """
    gradStudent = User.get(User.username == username)
    
    gradStudent.hasGraduated = int(status)
    gradStudent.save()
 

def makeGraduatedXls(filterType):
    """
    Create and save a GraduatedStudent.xlsx file with all of the graduated students.
    Working with XLSX files: https://xlsxwriter.readthedocs.io/index.html

    Returns:
        The file path and name to the newly created file, relative to the web root.
    """

    CCEusers = getMinorProgress()

    filepath = app.config['files']['base_path'] + '/GraduatedStudents.xlsx'
    workbook = xlsxwriter.Workbook(filepath, {'in_memory': True})
    worksheet = workbook.add_worksheet('students')
    bold = workbook.add_format({'bold': True})

    worksheet.write('A1', 'Graduated Students', bold)
    worksheet.set_column('A:A', 20)
    prev_year = 1
    row = 1

    if filterType == 'all':
        students = User.select().where(User.hasGraduated == True)
    elif filterType == 'cce':
        students = [student for student in CCEusers if student['hasGraduated']]
    # elif filterType == 'bonner':
    #     students = BonnerCohort.select(BonnerCohort, User).join(User).where(User.hasGraduated == True)

    #     print('##### Student list')

    #     for name in User.select(User.username):
            
    #         print(name)

    #     print('##### Student list')         
    #     print('bonner filter selected #####')
    # elif filterType == 'bonnercohorts':
    #     students = [student for student in bonnercohorts if student['hasGraduated']]
    else:
        students = User.select()

    for student in students:
        # if filterType == 'bonner' and prev_year != student.year:
        #     row += 1
        #     prev_year = student.year
        #     worksheet.write(row, 0, f"{student.year} - {student.year+1}", bold)

        if filterType == 'cce':
            worksheet.write(row, 0, f"{student['firstName']} {student['lastName']}")
            print('CCE student found #####')
        else:
            worksheet.write(row, 0, f"{student.firstName} {student.lastName}")
            print(' (all) student found #####')

        row += 1

    workbook.close()

    return filepath