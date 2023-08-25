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


def getUniqueVolunteers():

    uniqueVolunteers = (EventParticipant.select(fn.DISTINCT(EventParticipant.user_id), fn.CONCAT(User.firstName, ' ', User.lastName), User.bnumber)
                                        .join(User).switch(EventParticipant)
                                        .join(Event)
                                        .join(Term)
                                        .where(Term.academicYear == "2022-2023")
                                        .order_by(EventParticipant.user_id))
    
    return uniqueVolunteers.tuples()

def getVolunteerProgramEventByTerm(term):
# Volunteers by term for each event the participated in for wich program. user: program, event, term

    bloo = (EventParticipant.select(fn.CONCAT(User.firstName, ' ', User.lastName), EventParticipant.user_id, Program.programName, Event.name)
                            .join(User).switch(EventParticipant)
                            .join(Event)
                            .join(Program)
                            .where(Event.term_id == term)
                            .order_by(EventParticipant.user_id))
    
    return bloo.tuples()

def totalVolunteerHours(): 
    
    query = (EventParticipant.select(fn.SUM(EventParticipant.hoursEarned)))

    return query.tuples()

def volunteerProgramHours():

    volunteerProgramHours = (EventParticipant.select(Program.programName, EventParticipant.user_id, fn.SUM(EventParticipant.hoursEarned))
                                             .join(Event, on=(EventParticipant.event_id == Event.id))
                                             .join(Program, on=(Event.program_id == Program.id))
                                             .group_by(Program.programName, EventParticipant.user_id))

    return volunteerProgramHours.tuples()

def onlyCompletedAllVolunteer():
    # Return volunteers that only attended the All Volunteer Training and then nothing else

    subQuery = (EventParticipant.select(EventParticipant.user_id)
                                .join(Event)
                                .join(Term)
                                .where(Event.name != "All Volunteer Training", Term.academicYear == "2022-2023"))

    onlyAllVolunteer = (EventParticipant.select(EventParticipant.user_id, fn.CONCAT(User.firstName, " ", User.lastName))
                                        .join(User).switch(EventParticipant)
                                        .join(Event)
                                        .join(Term)
                                        .where(Event.name == "All Volunteer Training", Term.academicYear == "2022-2023", EventParticipant.user_id.not_in(subQuery)))

    return onlyAllVolunteer.tuples()

def volunteerHoursByProgram():
    query = ((Program.select(Program.programName, fn.SUM(EventParticipant.hoursEarned).alias('sum')).join(Event)
                     .join(EventParticipant, on=(Event.id == EventParticipant.event_id))
                     .group_by(Program.programName)
                     .order_by(Program.programName)))

    return query.tuples()

def volunteerMajorAndClass(column, reorderClassLevel=False):

    majorAndClass = (User.select(Case(None, ((column.is_null(), "Unknown"),), column), fn.COUNT(fn.DISTINCT(EventParticipant.user_id)).alias('count'))
                         .join(EventParticipant, on=(User.username == EventParticipant.user_id))
                         .group_by(column))

    if reorderClassLevel:
        majorAndClass = majorAndClass.order_by(Case(None, ((column == "Freshman", 1),
                                                           (column == "Sophomore", 2),
                                                           (column == "Junior", 3),
                                                           (column == "Senior", 4),
                                                           (column == "Graduating", 5),
                                                           (column == "Non-Degree", 6),
                                                           (column.is_null(), 7)),
                                                            8))
    else: 
        majorAndClass = majorAndClass.order_by(column.asc(nulls = 'LAST'))
         
    return majorAndClass.tuples()

def repeatVolunteersPerProgram():
    # Get people who participated in events more than once (individual program)
    repeatPerProgramQuery = (EventParticipant.select(fn.CONCAT(User.firstName, " ", User.lastName),Program.programName.alias("programName"),fn.Count(EventParticipant.event_id).alias('event_count'))
                                             .join(Event, on=(EventParticipant.event_id ==Event.id))
                                             .join(Program, on=(Event.program == Program.id))
                                             .join(User, on=(User.username == EventParticipant.user_id))
                                             .group_by(User.firstName, User.lastName, Event.program)
                                             .having(fn.Count(EventParticipant.event_id) > 1)
                                             .order_by(Event.program, User.lastName ))
        
    return repeatPerProgramQuery.tuples()

def repeatVolunteers():
    # Get people who participated in events more than once (all programs)
    repeatAllProgramQuery = (EventParticipant.select(fn.CONCAT(User.firstName," ", User.lastName), fn.COUNT(EventParticipant.user_id).alias('count'))
                                             .join(User, on=(User.username == EventParticipant.user_id))
                                             .group_by(User.firstName, User.lastName)
                                             .having(fn.COUNT(EventParticipant.user_id) > 1))
    
    return repeatAllProgramQuery.tuples()

def getRetentionRate():
    retentionDict = []

    fallParticipationDict = termParticipation("Fall 2022")
    springParticipationDict = termParticipation("Spring 2023")  

    # calculate the retention rate using the defined function
    retention_rate_dict = calculateRetentionRate(fallParticipationDict, springParticipationDict)
    for program, retention_rate in retention_rate_dict.items():
         retentionDict.append((program, str(round(retention_rate * 100, 2)) + "%"))

    return  retentionDict

def termParticipation(termDescription):
    participationQuery = (Event.select(Event.program, EventParticipant.user_id.alias('participant'), Program.programName.alias("progName"))
                                      .join(EventParticipant, JOIN.LEFT_OUTER, on=(Event.id == EventParticipant.event))
                                      .join(Program, on=(Program.id == Event.program))
                                      .join(Term, on=(Event.term_id == Term.id) )
                                      .where(Term.description == termDescription ))

    programParticipationDict = defaultdict(list)
    for result in participationQuery.dicts():
        prog_name = result['progName']
        participant = result['participant']
        programParticipationDict[prog_name].append(participant)

    return programParticipationDict

def removeNullParticipants(bla):
    # loop through the list and remove all entries that do not have a participant
    return list(filter(lambda participant: bool(participant), bla))
    
# function to calculate the retention rate for each program
def calculateRetentionRate(fall_dict, spring_dict):
    retention_dict = {}
    for program in fall_dict.keys():
        fall_participants = set(removeNullParticipants(fall_dict[program]))
        spring_participants = set(removeNullParticipants(spring_dict.get(program, [])))
        retention_rate = 0.0
        try: 
            retention_rate = len(fall_participants & spring_participants) / len(fall_participants)
        except ZeroDivisionError:
            pass

        retention_dict[program] = retention_rate
  
    return retention_dict

# def halfRetentionRateRecurringEvents():

#     programs = ProgramEvent.select(ProgramEvent.program_id).distinct()

#     retention_rates = {}

#     # Loop over the programs and get the corresponding event IDs
#     for program in programs:
#         # Define the query for each program
#         query = (EventParticipant.select(EventParticipant.event_id.alias("event_id"), Event.name.alias("name"))
#                                  .join(Event, on=(EventParticipant.event_id == Event.id))
#                                  .join(ProgramEvent, on=(EventParticipant.event_id == ProgramEvent.event_id))
#                                  .join(Program, on=(Program.id == ProgramEvent.program_id))
#                                  .where((ProgramEvent.program_id == program.program_id) & (Event.recurringId != None))
#                                  .distinct()
#                                  .dicts())

#         event_count = 0
#         name_counts = defaultdict(int)

#         for result in query:
#             event_count += 1
#             participants = EventParticipant.select(EventParticipant.user_id).where(EventParticipant.event_id == result["event_id"])
#             for participant in participants:
#                 name = participant.user_id
#                 name_counts[name] += 1
                
#         half_count = event_count // 2
#         qualified_names = [name for name, count in name_counts.items() if count >= half_count]
        
#         if len(name_counts) > 0:
#             percentage = len(qualified_names) / len(name_counts) * 100
#         else:
#             percentage = 0

#         retention_rates[program.program.programName] = percentage

#     return retention_rates


# def fullRetentionRateRecurringEvents():
    
#     programs = ProgramEvent.select(ProgramEvent.program_id).distinct()

#     full_retention = {}

#     # Loop over the programs and get the corresponding event IDs
#     for program in programs:
#         # Define the query for each program
#         query = (EventParticipant.select(EventParticipant.event_id.alias("event_id"), Event.name.alias("name"))
#                                  .join(Event, on=(EventParticipant.event_id == Event.id))
#                                  .join(ProgramEvent, on=(EventParticipant.event_id == ProgramEvent.event_id))
#                                  .join(Program, on=(Program.id == ProgramEvent.program_id))
#                                  .where((ProgramEvent.program_id == program.program_id) & (Event.recurringId != None))
#                                  .distinct()
#                                  .dicts())

#         event_count = 0
#         name_counts = defaultdict(int)

#         for result in query:
#             event_count += 1
#             participants = EventParticipant.select(EventParticipant.user_id).where(EventParticipant.event_id == result["event_id"])
#             for participant in participants:
#                 name = participant.user_id
#                 name_counts[name] += 1
                
#         qualified_names = [name for name, count in name_counts.items() if count >= event_count]
        
#         if len(name_counts) > 0:
#             percentage = len(qualified_names) / len(name_counts) * 100
#         else:
#             percentage = 0

#         full_retention[program.program.programName] = percentage

#     return full_retention

# create a new Excel file

# define function to save data to a sheet in the Excel file
def makeDataXls(getData, columnTitles, sheetName, workbook):

    worksheet = workbook.add_worksheet(sheetName)
    bold = workbook.add_format({'bold': True})

    worksheet.write_string(0, 0, sheetName)

    for column, title in enumerate(columnTitles):
        worksheet.write(1, column, title, bold)

    for column, rowData in enumerate(getData):
        for data, value in enumerate(rowData):
            worksheet.write(column+2, data, value)
    
    for column, title in enumerate(columnTitles):
        columnData = [title] + [rowData[column] for rowData in getData]
        setColumnWidth = max(len(str(x)) for x in columnData)
        worksheet.set_column(column, column, setColumnWidth + 3)

def create_spreadsheet(): 
    filepath = app.config['files']['base_path'] + '/volunteer_data.xlsx'
    workbook = xlsxwriter.Workbook(filepath, {'in_memory': True})

    hoursByProgramColumns = ["Program", "Hours"]
    volunteerMajorColumns = ["Major", "Count"]
    volunteerClassColumns = ["Class Level", "Count"]
    repeatProgramEventVolunteerColumns = ["Volunteer", "Program Name", "Event Count"]
    repeatAllProgramVolunteerColumns = ["Volunteer", "Number of Events"]
    volunteerProgramRetentionRateAcrossTermColumns = ["Program", "Retention Rate"]
    uniqueVolunteersColumns = ["Username", "Full Name", "B-Number"]
    totalVolunteerHoursColumns = ["Total Volunteer Hours"]
    volunteerProgramHoursColumns = [ "Program Name", "Volunteer Username", "Volunteer Hours"]
    onlyCompletedAllVolunteerColumns = ["Username","Full Name "]
    volunteerProgramEventByTerm = ["Full Name", "Username", "Program Name", "Event Name"]


    makeDataXls(volunteerHoursByProgram(), hoursByProgramColumns, "Total Hours By Program", workbook)
    makeDataXls(volunteerMajorAndClass(User.major), volunteerMajorColumns, "Volunteers By Major", workbook)
    makeDataXls(volunteerMajorAndClass(User.classLevel, reorderClassLevel=True), volunteerClassColumns, "Volunteers By Class Level", workbook)
    makeDataXls(repeatVolunteersPerProgram(), repeatProgramEventVolunteerColumns, "Repeat Volunteers Per Program", workbook)
    makeDataXls(repeatVolunteers(), repeatAllProgramVolunteerColumns, "Repeat Volunteers All Programs", workbook)
    makeDataXls(getRetentionRate(), volunteerProgramRetentionRateAcrossTermColumns, "Retention Rate By Semester", workbook)
    makeDataXls(getUniqueVolunteers(), uniqueVolunteersColumns, "Unique Volunteers", workbook)
    makeDataXls(totalVolunteerHours(), totalVolunteerHoursColumns, "Total Hours", workbook)
    makeDataXls(volunteerProgramHours(), volunteerProgramHoursColumns, "Volunteer Hours By Program", workbook)
    makeDataXls(onlyCompletedAllVolunteer(), onlyCompletedAllVolunteerColumns , "Only All Volunteer Training", workbook)
    makeDataXls(getVolunteerProgramEventByTerm(Term.get_by_id(8)), volunteerProgramEventByTerm, "Fall 2022", workbook)
    
    workbook.close()

    return filepath
