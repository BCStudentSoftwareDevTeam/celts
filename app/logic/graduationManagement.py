from collections import defaultdict
from typing import List, Dict
from playhouse.shortcuts import model_to_dict
from peewee import JOIN, fn, Case, DoesNotExist
import xlsxwriter
from app import app

from app.models.user import User
from app.logic.minor import getMinorProgress
from app.logic.bonner import getBonnerCohorts
from app.models.bonnerCohort import BonnerCohort
from app.models.term import Term


def getGraduatedStudent(username):
    """
    This function marks students as graduated
    Parameters:
    username: username of the user graduating
    """
    gradStudent = User.get(User.username == username)
    if gradStudent:
        gradStudent.hasGraduated = True
        gradStudent.save()
        return True
    return False

def removeGraduatedStudent(username):
    """
    This function unmarks students as graduated
    Parameters:
    username: username of the user graduating

    """
    notGradStudent = User.get(User.username == username)
    if notGradStudent:
        notGradStudent.hasGraduated = False
        notGradStudent.save()
        return True
    return False

def makeGraduatedXls(filterType='all'):
    """
    Create and save a GraduatedStudent.xlsx file with all of the graduated students.
    Working with XLSX files: https://xlsxwriter.readthedocs.io/index.html

    Returns:
        The file path and name to the newly created file, relative to the web root.
    """
    CCEusers = getMinorProgress()
    bonnercohorts = getBonnerCohorts()

    filepath = app.config['files']['base_path'] + '/GraduatedStudents.xlsx'
    workbook = xlsxwriter.Workbook(filepath, {'in_memory': True})
    worksheet = workbook.add_worksheet('students')
    bold = workbook.add_format({'bold': True})

    worksheet.write('A1', 'Graduated Students', bold)
    worksheet.set_column('A:A', 20)

    row = 1

    if filterType == 'all':
        students = User.select().where(User.hasGraduated == True)
    elif filterType == 'cce':
        students = [student for student in CCEusers if student['hasGraduated']]
    elif filterType == 'bonner':
        students = BonnerCohort.select(BonnerCohort, User).join(User).where(User.hasGraduated == True)
    elif filterType == 'bonnercohorts':
        students = [student for student in bonnercohorts if student['hasGraduated']]
    else:
        students = User.select()

    for student in students:
        if filterType == 'bonner' and prev_year != student.year:
            row += 1
            prev_year = student.year
            worksheet.write(row, 0, f"{student.year} - {student.year+1}", bold)

        if filterType == 'cce':
            worksheet.write(row, 0, student['firstName'])
            worksheet.write(row, 1, student['lastName'])
        else:
            worksheet.write(row, 0, student.firstName)
            worksheet.write(row, 1, student.lastName)

        row += 1

    workbook.close()

    return filepath