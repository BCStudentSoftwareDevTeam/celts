from collections import defaultdict
from datetime import date
from peewee import IntegrityError

import xlsxwriter

from app import app
from app.models.bonnerCohort import BonnerCohort
from app.models.eventRsvp import EventRsvp
from app.models.user import User

def makeBonnerXls():
    """
    Create and save a BonnerStudents.xlsx file with all of the current and former bonner students.
    Working with XLSX files: https://xlsxwriter.readthedocs.io/index.html

    Returns:
        The file path and name to the newly created file, relative to the web root.
    """
    filepath = app.config['files']['base_path'] + '/BonnerStudents.xlsx'
    workbook = xlsxwriter.Workbook(filepath, {'in_memory': True})
    worksheet = workbook.add_worksheet('students')
    bold = workbook.add_format({'bold': True})

    worksheet.write('A1', 'Cohort Year', bold)
    worksheet.set_column('A:A', 10)
    worksheet.write('B1', 'Student', bold)
    worksheet.set_column('B:B', 20)
    worksheet.write('C1', 'B-Number', bold)
    worksheet.set_column('C:C', 10)
    worksheet.write('D1', 'Student Email', bold)
    worksheet.set_column('D:D', 20)

    students = BonnerCohort.select(BonnerCohort, User).join(User).order_by(BonnerCohort.year.desc(), User.lastName)

    prev_year = 0
    row = 0
    for student in students:
        if prev_year != student.year:
            row += 1
            prev_year = student.year
            worksheet.write(row, 0, f"{student.year} - {student.year+1}", bold)

        worksheet.write(row, 1, student.user.fullName)
        worksheet.write(row, 2, student.user.bnumber)
        worksheet.write(row, 3, student.user.email)

        row += 1

    workbook.close()

    return filepath

def getBonnerCohorts(limit=None, currentYear=date.today().year):
    """
        Return a dictionary with years as keys and a list of bonner users as values. Returns empty lists for
        intermediate years, or the last 5 years if there are no older records.
    """
    years = list(BonnerCohort.select(BonnerCohort, User).join(User).order_by(BonnerCohort.year).execute())

    # Beans:
    # Latest visable start date 
    defaultStart = currentYear-4
    # Beans: the earliest a user has ever been in a bonner cohort or the default start, whichever is earlier
    cohorts = { year: [] for year in range(currentYear+1) }
    
    years = list(BonnerCohort.select(BonnerCohort, User)
                .join(User)
                .order_by(BonnerCohort.year)
                .execute())
    
    
    for cohort in years:
        # Beans: Calculate intended graduation year based on the assumption of four-year graduation
        graduation_year = cohort.year + 4

        # Beans:Ensure the graduation year is within the range of the default start year to the current year
        graduation_year = min(graduation_year, currentYear)

        # Beans: Add Bonner user to the respective graduation year cohort
        cohorts[graduation_year].append(cohort.user)


    # Beans: slice off the last n elements
    if limit:
        cohorts = dict(list(cohorts.items())[-limit:])

    return cohorts

def rsvpForBonnerCohort(year, event):
    """
    Adds an EventRsvp record to the given event for each user in the given Bonner year.
    """
    EventRsvp.insert_from(BonnerCohort.select(BonnerCohort.user, event).where(BonnerCohort.year == year),[EventRsvp.user, EventRsvp.event]).on_conflict(action='IGNORE').execute()
