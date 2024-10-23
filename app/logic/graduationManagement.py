from collections import defaultdict
from typing import List, Dict
from playhouse.shortcuts import model_to_dict
from peewee import JOIN, fn, Case, DoesNotExist
import xlsxwriter

from app.models.user import User
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

def makeGraduatedXls():
    """
    Create and save a GraduatedStudent.xlsx file with all of the graduated students.
    Working with XLSX files: https://xlsxwriter.readthedocs.io/index.html

    Returns:
        The file path and name to the newly created file, relative to the web root.
    """
    filepath = app.config['files']['base_path'] + '/GraduatedStudents.xlsx'
    workbook = xlsxwriter.Workbook(filepath, {'in_memory': True})
    worksheet = workbook.add_worksheet('students')
    bold = workbook.add_format({'bold': True})

    worksheet.write('B1', 'Student', bold)
    worksheet.set_column('B:B', 20)
    worksheet.write('C1', 'B-Number', bold)
    worksheet.set_column('C:C', 10)
    worksheet.write('D1', 'Student Email', bold)
    worksheet.set_column('D:D', 20)

    # Modify query based on filter type
    if filterType == 'all':
        students = User.select().where(User.hasGraduated == True)
    elif filterType == 'cce':
        students = User.select().join(CCEModel).where(CCEModel.engagementCount > 0)  # Example for CCE students
    elif filterType == 'bonner':
        students = BonnerCohort.select(BonnerCohort, User).join(User).order_by(BonnerCohort.year.desc(), User.lastName)
    elif filterType == 'bonnercohorts':
        students = BonnerCohort.select(BonnerCohort, User).join(User).order_by(BonnerCohort.year.desc(), User.lastName)
    else:
        students = User.select()

    prev_year = 0
    row = 1
    for student in students:
        if filterType == 'bonner' and prev_year != student.year:
            row += 1
            prev_year = student.year
            worksheet.write(row, 0, f"{student.year} - {student.year+1}", bold)

        worksheet.write(row, 1, student.fullName)
        worksheet.write(row, 2, student.bnumber)
        worksheet.write(row, 3, student.email)

        row += 1

    workbook.close()

    return filepath