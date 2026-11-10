from collections import defaultdict
from datetime import date
from peewee import IntegrityError, SQL, fn

import xlsxwriter

from app import app
from app.models.bonnerCohort import BonnerCohort
from app.models.certificationRequirement import CertificationRequirement
from app.models.event import Event
from app.models.eventParticipant import EventParticipant
from app.models.eventRsvp import EventRsvp
from app.models.requirementMatch import RequirementMatch
from app.models.user import User
from app.models.eventCohort import EventCohort
from app.models.term import Term
from app.logic.createLogs import createRsvpLog
from app.models.certification import Certification
def makeBonnerXls(selectedYear, noOfYears=1):
    """
    Create and save a BonnerStudents.xlsx file with all of the current and former bonner students.
    Working with XLSX files: https://xlsxwriter.readthedocs.io/index.html

    Params:
        selectedYear: The cohort year of interest.
        noOfYears: The number of years to be downloaded.

    Returns:
        The file path and name to the newly created file, relative to the web root.
    """
    selectedYear = int(selectedYear)
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

    # bonner event titles
    bonnerEvents = CertificationRequirement.select().where(CertificationRequirement.certification==Certification.BONNER).order_by(CertificationRequirement.order.asc())
    bonnerEventInfo = {bonnerEvent.id:(bonnerEvent.name, index + 4) for index, bonnerEvent in enumerate(bonnerEvents)}
    currentLetter = "E" # next column
    for bonnerEvent in bonnerEvents:
        worksheet.write(f"{currentLetter}1", bonnerEvent.name, bold)
        worksheet.set_column(f"{currentLetter}:{currentLetter}", 30)
        currentLetter = chr(ord(f"{currentLetter}") + 1)

    if noOfYears == "all":
        students = BonnerCohort.select(BonnerCohort, User).join(User).order_by(BonnerCohort.year.desc(), User.lastName)
    else:
        noOfYears = int(noOfYears)
        startingYear = selectedYear - noOfYears + 1
        students = BonnerCohort.select(BonnerCohort, User).where(BonnerCohort.year.between(startingYear, selectedYear)).join(User).order_by(BonnerCohort.year.desc(), User.lastName)
    
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

        # set event fields to the default "incomplete" status
        for eventName, eventSpreadsheetPosition in bonnerEventInfo.values():
            worksheet.write(row, eventSpreadsheetPosition, "Incomplete")
        
        bonnerEventsAttended = (
            RequirementMatch
            .select()
            .join(Event, on=(RequirementMatch.event == Event.id))
            .join(EventParticipant, on=(RequirementMatch.event == EventParticipant.event))
            .join(CertificationRequirement, on=(RequirementMatch.requirement == CertificationRequirement.id))
            .join(User, on=(EventParticipant.user == User.username))
            .where((CertificationRequirement.certification_id == Certification.BONNER) & (User.username == student.user.username))
        )

        certRequirementDates = {}
        for attendedEvent in bonnerEventsAttended:
            if bonnerEventInfo.get(attendedEvent.requirement.id):
                completedEvent = bonnerEventInfo[attendedEvent.requirement.id]
                if completedEvent[1] not in certRequirementDates:
                    certRequirementDates[completedEvent[1]] = []
                certRequirementDates[completedEvent[1]].append(attendedEvent.event.startDate.strftime('%m/%d/%Y'))

        for tableIndex, dates in certRequirementDates.items():
            worksheet.write(row, tableIndex, ", ".join(sorted(dates)))
        row += 1

    workbook.close()

    return filepath

def getBonnerCohorts(limit=None, currentYear=date.today().year):
    """
        Return a dictionary with years as keys and a list of bonner users as values. Returns empty lists for
        intermediate years, or the last 5 years if there are no older records.
    """
    bonnerCohorts = list(BonnerCohort.select(BonnerCohort, User).join(User).order_by(BonnerCohort.year).execute())

    firstYear = currentYear - 4 if not bonnerCohorts else min(currentYear - 4, bonnerCohorts[0].year)
    lastYear = currentYear if not bonnerCohorts else max(currentYear, bonnerCohorts[-1].year)


    cohorts = { year: [] for year in range(firstYear, lastYear + 1) }
    for cohort in bonnerCohorts:
        cohorts[cohort.year].append(cohort.user)

    # slice off cohorts that go over our limit starting with the earliest
    if limit:
        cohorts = dict(sorted(list(cohorts.items()), key=lambda e: e[0], reverse=True)[:limit])

    return cohorts



def rsvpForBonnerCohort(year, event):
    """
    Adds an EventRsvp record to the given event for each user in the given Bonner year.
    """
    EventRsvp.insert_from(BonnerCohort.select(BonnerCohort.user, event, SQL('NOW()'))
                                      .where(BonnerCohort.year == year),
                                      [EventRsvp.user, EventRsvp.event, EventRsvp.rsvpTime]).on_conflict(action='IGNORE').execute()
    
def addBonnerCohortToRsvpLog(year, event):
    """ This method adds the table information in the RSVP Log page"""
    bonnerCohort = list(BonnerCohort.select(fn.CONCAT(User.firstName, ' ', User.lastName).alias("fullName"))
                                    .join(User, on=(User.username == BonnerCohort.user))
                                    .where(BonnerCohort.year == year))
    for bonner in bonnerCohort:
        fullName = bonner.fullName
        createRsvpLog(eventId=event, content=f"Added {fullName} to RSVP list.") 