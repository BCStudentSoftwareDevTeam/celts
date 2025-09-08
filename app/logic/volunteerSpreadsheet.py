from importlib.abc import ResourceReader
from os import major
import xlsxwriter
from peewee import fn, Case, JOIN
from collections import defaultdict

from app import app
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.program import Program
from app.models.event import Event
from app.models.term import Term

### READ ME FIRST! #################################################################
#
# It's very important that we understand the distinction between volunteers earning
# service hours and other things that we track in our system, like student labor, 
# bonner students, trainings, etc. The way we use 'volunteer' may not necessarily
# be the way CELTS uses it.
#
####################################################################################

def getFallTerm(academicYear):
    return Term.get(Term.description % "Fall%", Term.academicYear == academicYear)

def getSpringTerm(academicYear):
    return Term.get(Term.description % "Spring%", Term.academicYear == academicYear)


def getBaseQuery(academicYear):
    return (EventParticipant.select()
                            .join(User).switch(EventParticipant)
                            .join(Event)
                            .join(Program).switch(Event)
                            .join(Term)
                            .where(Term.academicYear == academicYear,
                                   Event.deletionDate == None, 
                                   Event.isCanceled == False)
                            .order_by(Event.startDate))


def getUniqueVolunteers(academicYear):
    base = getBaseQuery(academicYear)

    columns = ["Username", "Full Name", "B-Number"]
    query = (base.select(fn.DISTINCT(EventParticipant.user_id), fn.CONCAT(User.firstName, ' ', User.lastName), User.bnumber)
                 .where(Event.isService == True))

    return (columns,query.tuples())


def getVolunteerProgramEventByTerm(term):
    base = getBaseQuery(term.academicYear)

    columns = ["Full Name", "Username", "Program Name", "Event Name"]
    query = (base.select(fn.CONCAT(User.firstName, ' ', User.lastName), EventParticipant.user_id, Program.programName, Event.name)
                         .where(Event.term == term, Event.isService == True))

    return (columns,query.tuples())


def totalVolunteerHours(academicYear):
    base = getBaseQuery(academicYear)

    columns = ["Total Volunteer Hours"]
    query = base.select(fn.SUM(EventParticipant.hoursEarned)).where(Event.isService == True)

    return (columns, query.tuples())


def volunteerProgramHours(academicYear):
    base = getBaseQuery(academicYear)

    columns = ["Program Name", "Volunteer Username", "Volunteer Hours"]
    query = (base.select(Program.programName, EventParticipant.user_id, fn.SUM(EventParticipant.hoursEarned))
                 .where(Event.isService == True)
                 .group_by(Program.programName, EventParticipant.user_id))

    return (columns, query.tuples())


def onlyCompletedAllVolunteer(academicYear):
    base = getBaseQuery(academicYear)
    base2 = getBaseQuery(academicYear)

    columns = ["Username", "Full Name"]
    subQuery = base2.select(EventParticipant.user_id).where(~Event.isAllVolunteerTraining)

    query = (base.select(EventParticipant.user_id, fn.CONCAT(User.firstName, " ", User.lastName))
                 .where(Event.isAllVolunteerTraining, EventParticipant.user_id.not_in(subQuery)))

    return (columns, query.tuples())


def volunteerHoursByProgram(academicYear):
    base = getBaseQuery(academicYear)

    columns = ["Program", "Hours"]
    query = (base.select(Program.programName, fn.SUM(EventParticipant.hoursEarned).alias('sum'))
             .where(Event.isService == True)
             .group_by(Program.programName)
             .order_by(Program.programName))

    return (columns, query.tuples())


def volunteerMajorAndClass(academicYear, column, reorderClassLevel=False):
    base = getBaseQuery(academicYear)

    columns = ["Major", "Count"]
    query = (base.select(Case(None, ((column.is_null(), "Unknown"),), column), fn.COUNT(fn.DISTINCT(EventParticipant.user_id)).alias('count'))
                 .where(Event.isService == True)
                 .group_by(column))

    if reorderClassLevel:
        columns = ["Class Level", "Count"]
        query = query.order_by(Case(None, ((column == "Freshman", 1),
                                           (column == "Sophomore", 2),
                                           (column == "Junior", 3),
                                           (column == "Senior", 4),
                                           (column == "Graduating", 5),
                                           (column == "Non-Degree", 6),
                                           (column.is_null(), 7)),
                               8))
    else:
        query = query.order_by(column.asc(nulls='LAST'))

    return (columns, query.tuples())


def repeatVolunteersPerProgram(academicYear):
    base = getBaseQuery(academicYear)

    columns = ["Volunteer", "Program Name", "Event Count"]
    query = (base.select(fn.CONCAT(User.firstName, " ", User.lastName).alias('fullName'),
                                                     Program.programName.alias("programName"),
                                                     fn.COUNT(EventParticipant.event_id).alias('event_count'))
                 .where(Event.isService == True)
                 .group_by(User.firstName, User.lastName, Event.program)
                 .having(fn.COUNT(EventParticipant.event_id) > 1)
                 .order_by(Event.program, User.lastName))

    return (columns, query.tuples())


def repeatVolunteers(academicYear):
    base = getBaseQuery(academicYear)

    columns = ["Volunteer", "Number of Events"]
    query = (base.select(fn.CONCAT(User.firstName, " ", User.lastName), fn.COUNT(EventParticipant.user_id).alias('count'))
                 .where(Event.isService == True)
                 .group_by(User.firstName, User.lastName)
                 .having(fn.COUNT(EventParticipant.user_id) > 1))

    return (columns, query.tuples())


def getRetentionRate(academicYear):
    fallParticipationDict = termParticipation(getFallTerm(academicYear))
    springParticipationDict = termParticipation(getSpringTerm(academicYear))

    retentionList = []
    retentionRateDict = calculateRetentionRate(fallParticipationDict, springParticipationDict)
    for program, retentionRate in retentionRateDict.items():
        retentionList.append((program, str(round(retentionRate * 100, 2)) + "%"))

    columns = ["Program", "Retention Rate"]
    return (columns, retentionList)


def termParticipation(term):
    base = getBaseQuery(term.academicYear)

    participationQuery = (base.select(Event.program, EventParticipant.user_id.alias('participant'), Program.programName.alias("programName"))
                          .where(Event.term == term)
                          .order_by(EventParticipant.user))

    programParticipationDict = defaultdict(list)
    for result in participationQuery.dicts():
        programName = result['programName']
        participant = result['participant']
        programParticipationDict[programName].append(participant)

    return dict(programParticipationDict)


def removeNullParticipants(participantList):
    return list(filter(lambda participant: participant, participantList))


def calculateRetentionRate(fallDict, springDict):
    retentionDict = {}
    for program in fallDict:
        fallParticipants = set(removeNullParticipants(fallDict[program]))
        springParticipants = set(removeNullParticipants(springDict.get(program, [])))
        retentionRate = 0.0
        try:
            retentionRate = len(fallParticipants & springParticipants) / len(fallParticipants)
        except ZeroDivisionError:
            pass
        retentionDict[program] = retentionRate

    return retentionDict


def makeDataXls(sheetName, sheetData, workbook):
    (columnTitles, dataTuples) = sheetData
    worksheet = workbook.add_worksheet(sheetName)
    bold = workbook.add_format({'bold': True})

    worksheet.write_string(0, 0, sheetName)

    for column, title in enumerate(columnTitles):
        worksheet.write(1, column, title, bold)

    for column, rowData in enumerate(dataTuples):
        for data, value in enumerate(rowData):
            worksheet.write(column + 2, data, value)

    for column, title in enumerate(columnTitles):
        columnData = [title] + [rowData[column] for rowData in dataTuples]
        setColumnWidth = max(len(str(x)) for x in columnData)
        worksheet.set_column(column, column, setColumnWidth + 3)


def createSpreadsheet(academicYear):
    filepath = f"{app.config['files']['base_path']}/volunteer_data_{academicYear}.xlsx"
    workbook = xlsxwriter.Workbook(filepath, {'in_memory': True})

    makeDataXls("Total Service Hours", totalVolunteerHours(academicYear), workbook)
    makeDataXls("Total Service Hours By Program", volunteerHoursByProgram(academicYear), workbook)
    makeDataXls("Volunteers By Major", volunteerMajorAndClass(academicYear, User.major), workbook)
    makeDataXls("Volunteers By Class Level", volunteerMajorAndClass(academicYear, User.rawClassLevel, reorderClassLevel=True), workbook)
    makeDataXls("Repeat Participants", repeatVolunteers(academicYear), workbook)
    makeDataXls("Retention Rate By Semester", getRetentionRate(academicYear), workbook)
    makeDataXls("Unique Volunteers", getUniqueVolunteers(academicYear), workbook)
    makeDataXls("Volunteer Hours By Program", volunteerProgramHours(academicYear), workbook)
    makeDataXls("Only All Volunteer Training", onlyCompletedAllVolunteer(academicYear), workbook)

    fallTerm = getFallTerm(academicYear)
    springTerm = getSpringTerm(academicYear)
    makeDataXls(fallTerm.description, getVolunteerProgramEventByTerm(fallTerm), workbook)
    makeDataXls(springTerm.description, getVolunteerProgramEventByTerm(springTerm), workbook)

    workbook.close()

    return filepath
