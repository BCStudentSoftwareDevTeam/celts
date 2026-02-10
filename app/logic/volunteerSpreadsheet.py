from os import major
import xlsxwriter
from peewee import fn, Case, JOIN, SQL, Select
from collections import defaultdict
from datetime import date, datetime,time
from app import app
from app.models import mainDB
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

    # As we add joins to this query, watch out for duplicate participant rows being added

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

    columns = ["Full Name", "Email", "B-Number"]
    subquery = (base.select(fn.DISTINCT(EventParticipant.user_id).alias('user_id'), fn.CONCAT(User.firstName, ' ', User.lastName).alias("fullname"), User.bnumber)
                 .where(Event.isService == True)).alias('subq')
    query = Select().from_(subquery).select(subquery.c.fullname, fn.CONCAT(subquery.c.user_id,'@berea.edu'), subquery.c.bnumber)

    return (columns,query.tuples().execute(mainDB))


def volunteerProgramHours(academicYear):
    base = getBaseQuery(academicYear)

    columns = ["Program Name", "Volunteer Hours", "Volunteer Name", "Volunteer Email", "Volunteer B-Number"]
    query = (base.select(Program.programName, 
                         fn.SUM(EventParticipant.hoursEarned),
                         fn.CONCAT(User.firstName, ' ', User.lastName), 
                         fn.CONCAT(EventParticipant.user_id,'@berea.edu'), 
                         User.bnumber) 
                 .where(Event.isService == True)
                 .group_by(Program.programName, EventParticipant.user_id))

    return (columns, query.tuples())

def onlyCompletedAllVolunteer(academicYear):
    base = getBaseQuery(academicYear)
    base2 = getBaseQuery(academicYear)

    columns = ["Full Name", "Email", "B-Number"]
    subQuery = base2.select(EventParticipant.user_id).where(~Event.isAllVolunteerTraining)

    query = (base.select(fn.CONCAT(User.firstName, ' ', User.lastName), 
                         fn.CONCAT(EventParticipant.user_id,'@berea.edu'), 
                         User.bnumber) 
                 .where(Event.isAllVolunteerTraining, EventParticipant.user_id.not_in(subQuery)))

    return (columns, query.tuples())

def totalHours(academicYear):
    base = getBaseQuery(academicYear)

    columns = ["Total Service Hours", "Total Training Hours", "Other Participation Hours"]
    query = base.select(fn.SUM(Case(None,((Event.isService, EventParticipant.hoursEarned),),0)),
                        fn.SUM(Case(None,((Event.isTraining, EventParticipant.hoursEarned),),0)),
                        fn.SUM(Case(None,((~Event.isService & ~Event.isTraining, EventParticipant.hoursEarned),),0)))

    return (columns, query.tuples())

def totalHoursByProgram(academicYear):
    base = getBaseQuery(academicYear)

    columns = ["Program", "Service Hours", "Training Hours", "Other Hours"]
    query = (base.select(Program.programName,
                         fn.SUM(Case(None,((Event.isService, EventParticipant.hoursEarned),),0)),
                         fn.SUM(Case(None,((Event.isTraining, EventParticipant.hoursEarned),),0)),
                         fn.SUM(Case(None,((~Event.isService & ~Event.isTraining, EventParticipant.hoursEarned),),0)))
                 .group_by(Program.programName)
                 .order_by(Program.programName))

    return (columns, query.tuples())

def makeCase(fieldname):
    return Case(fieldname,((1, "Yes"),(0, "No"),),"None")

def getAllTermData(term):
    base = getBaseQuery(term.academicYear)

    columns = ["Program Name", "Event Name", "Event Description", "Event Date", "Event Start Time", "Event End Time", "Event Location",
               "Food Provided", "Labor Only", "Training Event", "RSVP Required", "Service Event", "Engagement Event", "All Volunteer Training",
               "RSVP Limit", "Series #", "Is Repeating Event", "Contact Name", "Contact Email",
               "Student First Name", "Student Last Name", "Student Email", "Student B-Number", "Student Phone", "Student CPO", "Student Major", "Student Has Graduated", "Student Class Level", "Student Dietary Restrictions",
               "Hours Earned"]
    query = (base.select(Program.programName,Event.name, Event.description, Event.startDate, Event.timeStart, Event.timeEnd, Event.location, 
                         makeCase(Event.isFoodProvided), makeCase(Event.isLaborOnly), makeCase(Event.isTraining), makeCase(Event.isRsvpRequired), makeCase(Event.isService), makeCase(Event.isEngagement), makeCase(Event.isAllVolunteerTraining), 
                         Event.rsvpLimit, Event.seriesId, makeCase(Event.isRepeating), Event.contactName, Event.contactEmail,
                         User.firstName, User.lastName, fn.CONCAT(User.username,'@berea.edu'), User.bnumber, User.phoneNumber,User.cpoNumber,User.major, makeCase(User.hasGraduated), User.rawClassLevel, User.dietRestriction, 
                         EventParticipant.hoursEarned)
                         .where(Event.term == term))

    return (columns,query.tuples())

def volunteerMajorAndClass(academicYear, column, classLevel=False):
    base = getBaseQuery(academicYear)

    columns = ["Major", "Count"]
    query = (base.select(Case(None, ((column.is_null(), "Unknown"),), column), fn.COUNT(fn.DISTINCT(EventParticipant.user_id)).alias('count'))
                 .where(Event.isService == True)
                 .group_by(column))

    if classLevel:
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
        query = query.order_by(SQL("count").desc())

    return (columns, query.tuples())


def repeatParticipantsPerProgram(academicYear):
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


def repeatParticipants(academicYear):
    base = getBaseQuery(academicYear)

    columns = ["Number of Events", "Full Name", "Email", "B-Number"]
    query = (base.select(fn.COUNT(EventParticipant.user_id).alias('count'),
                         fn.CONCAT(User.firstName, ' ', User.lastName), 
                         fn.CONCAT(EventParticipant.user_id,'@berea.edu'), 
                         User.bnumber) 
                 .group_by(User.firstName, User.lastName)
                 .having(fn.COUNT(EventParticipant.user_id) > 1)
                 .order_by(SQL("count").desc()))

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


def makeDataXls(sheetName, sheetData, workbook, sheetDesc=None):
    # assumes the length of the column titles matches the length of the data
    (columnTitles, dataTuples) = sheetData
    worksheet = workbook.add_worksheet(sheetName)
    bold = workbook.add_format({'bold': True})

    worksheet.write_string(0, 0, sheetName, bold)
    if sheetDesc:
        worksheet.write_string(1, 0, sheetDesc)

    for column, title in enumerate(columnTitles):
        worksheet.write(3, column, title, bold)

    for row, rowData in enumerate(dataTuples):
        for column, value in enumerate(rowData):
            # dates and times should use their text representation
            if isinstance(value, (datetime, date, time)):
                value = str(value)

            worksheet.write(row + 4, column, value)

    # set the width to the size of the text, with a maximum of 50 characters
    for column, title in enumerate(columnTitles):
        # put all of the data in each column into a list
        columnData = [title] + [rowData[column] for rowData in dataTuples]

        # find the largest item in the list (and cut it off at 50)
        setColumnWidth = min(max(len(str(x)) for x in columnData),50)

        worksheet.set_column(column, column, setColumnWidth + 3)


def createSpreadsheet(academicYear):
    filepath = f"{app.config['files']['base_path']}/volunteer_data_{academicYear}.xlsx"
    workbook = xlsxwriter.Workbook(filepath, {'in_memory': True})

    makeDataXls("Total Hours", totalHours(academicYear), workbook, sheetDesc=f"All participation hours for {academicYear}.")
    makeDataXls("Total Hours By Program", totalHoursByProgram(academicYear), workbook, sheetDesc=f"All participation hours by program for {academicYear}.")
    makeDataXls("Program Volunteers", volunteerProgramHours(academicYear), workbook, sheetDesc="Total program service hours for each volunteer.")
    makeDataXls("Volunteers By Major", volunteerMajorAndClass(academicYear, User.major), workbook, sheetDesc="All volunteers who participated in service events, by major.")
    makeDataXls("Volunteers By Class Level", volunteerMajorAndClass(academicYear, User.rawClassLevel, classLevel=True), workbook, sheetDesc="All volunteers who participated in service events, by class level. Our source for this data does not seem to be particularly accurate.")
    makeDataXls("Repeat Participants", repeatParticipants(academicYear), workbook, sheetDesc="Students who participated in multiple events, whether earning service hours or not.")
    makeDataXls("Unique Volunteers", getUniqueVolunteers(academicYear), workbook, sheetDesc=f"All students who participated in at least one service event during {academicYear}.")
    makeDataXls("Only All Volunteer Training", onlyCompletedAllVolunteer(academicYear), workbook, sheetDesc="Students who participated in an All Volunteer Training, but did not participate in any service events.")
    makeDataXls("Retention Rate By Semester", getRetentionRate(academicYear), workbook, sheetDesc="The percentage of students who participated in service events in the fall semester who also participated in a service event in the spring semester. Does not currently account for fall graduations.")

    fallTerm = getFallTerm(academicYear)
    springTerm = getSpringTerm(academicYear)
    makeDataXls(fallTerm.description, getAllTermData(fallTerm), workbook, sheetDesc= "All event participation for the term, excluding deleted or canceled events.")
    makeDataXls(springTerm.description, getAllTermData(springTerm), workbook, sheetDesc="All event participation for the term, excluding deleted or canceled events.")

    workbook.close()

    return filepath
