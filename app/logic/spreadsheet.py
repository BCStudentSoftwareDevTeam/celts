import xlsxwriter
from peewee import fn, Case, JOIN
from collections import defaultdict

from app import app
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from app.models.event import Event
from app.models.term import Term


def volunteerHoursByProgram():
    query = ((Program.select(Program.programName, fn.SUM(EventParticipant.hoursEarned).alias('sum'))
                     .join(ProgramEvent)
                     .join(EventParticipant, on=(ProgramEvent.event == EventParticipant.event))
                     .group_by(Program.programName)
                     .order_by(Program.programName)))

    return query.tuples()

# def volunteerHoursAllPrograms():
#     totalHoursAllProgram = float(EventParticipant.select(fn.Sum(fn.Coalesce(EventParticipant.hoursEarned, 0))).scalar())

#     return totalHoursAllProgram

def volunteerMajorAndClass(column):

    majorAndClass = (User.select(Case(None, ((column.is_null(), "Unknown"),), column), fn.COUNT(fn.DISTINCT(EventParticipant.user_id)).alias('count'))
                         .join(EventParticipant, on=(User.username == EventParticipant.user_id))
                         .group_by(column)
                         .order_by(column.asc(nulls = 'LAST')))
    
    return majorAndClass.tuples()

def repeatVolunteersPerProgram():
    # Get people who participated in events more than once (individual program)
    repeatPerProgramQuery = (EventParticipant.select(fn.CONCAT(User.firstName, " ", User.lastName),Program.programName.alias("programName"),fn.Count(EventParticipant.event_id).alias('event_count'))
                                             .join(ProgramEvent, on=(EventParticipant.event_id == ProgramEvent.event_id))
                                             .join(Program, on=(ProgramEvent.program_id == Program.id))
                                             .join(User, on=(User.username == EventParticipant.user_id))
                                             .group_by(User.firstName, User.lastName, ProgramEvent.program_id)
                                             .having(fn.Count(EventParticipant.event_id) > 1)
                                             .order_by(ProgramEvent.program_id, User.lastName ))
        
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
            # retentionDict[program]= str(round(retention_rate * 100, 2)) + "%"
    return  retentionDict

def termParticipation(termDescription):
    participationQuery = (ProgramEvent.select(ProgramEvent.program_id, EventParticipant.user_id.alias('participant'), Program.programName.alias("progName"))
                                      .join(EventParticipant, JOIN.LEFT_OUTER, on=(ProgramEvent.event == EventParticipant.event))
                                      .join(Program, on=(Program.id == ProgramEvent.program_id))
                                      .join(Event, on=(ProgramEvent.event_id == Event.id))
                                      .join(Term, on=(Event.term_id == Term.id) )
                                      .where(Term.description == termDescription ))
    print(participationQuery)
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

    hoursByProgramColumn = ["Program", "Hours"]
    volunteerMajorColumn = ["Major", "Count"]
    volunteerClassColumn = ["Class Level", "Count"]
    repeatProgramEventVolunteerColumn = ["Volunteer", "Program Name", "Event Count"]
    repeatAllProgramVolunteerColumn = ["Volunteer", "Number of Events"]
    volunteerProgramRetentionRateAcrossTermColumn = ["Program", "Retention Rate"]

    makeDataXls(volunteerHoursByProgram(), hoursByProgramColumn, "Total Hours By Program", workbook)
    makeDataXls(volunteerMajorAndClass(User.major), volunteerMajorColumn, "Volunteers By Major", workbook)
    makeDataXls(volunteerMajorAndClass(User.classLevel), volunteerClassColumn, "Volunteers By Class Level", workbook)
    makeDataXls(repeatVolunteersPerProgram(), repeatProgramEventVolunteerColumn, "Repeat Volunteers Per Program", workbook)
    makeDataXls(repeatVolunteers(), repeatAllProgramVolunteerColumn, "Repeat Volunteers All Programs", workbook)
    makeDataXls(getRetentionRate(), volunteerProgramRetentionRateAcrossTermColumn, "Retention Rate By Semester", workbook)

    workbook.close()

    return filepath
