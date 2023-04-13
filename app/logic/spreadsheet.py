#query data and generate spreadsheet
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from peewee import fn, JOIN


def volunteer():

    # Total volunteer hours by program along with a sum of all programs
    query = (ProgramEvent.select(ProgramEvent.program_id, fn.SUM(EventParticipant.hoursEarned).alias('sum'))
                         .join(EventParticipant, on=(ProgramEvent.event == EventParticipant.event))
                         .join(Program, on=(Program.id == ProgramEvent.program_id))
                         .group_by(ProgramEvent.program_id))

    totalHoursByProgram= {pe.program.programName: pe.sum for pe in query}

    totalHoursAllProgram = EventParticipant.select(fn.Sum(fn.Coalesce(EventParticipant.hoursEarned, 0))).scalar()

    print('Total Hours by Program', totalHoursByProgram)
    print('Total Hours', totalHoursAllProgram)


    # Majors represented in volunteering
    major_query = (User.select(User.major, fn.COUNT(fn.DISTINCT(EventParticipant.user_id)).alias('count'))
                         .join(EventParticipant, on=(User.username == EventParticipant.user_id))
                         .group_by(User.major))
 
    print("_____________majors represented___")
    for row in major_query:
        print(row.major, row.count)


    # Volunteering numbers by class year
    classLevel_query = (User.select(User.classLevel, fn.COUNT(fn.DISTINCT(EventParticipant.user_id)).alias('classCount'))
                         .join(EventParticipant, on=(User.username == EventParticipant.user_id))
                         .group_by(User.classLevel))

    print("_____________class year___")
    for row in classLevel_query:
        print(row.classLevel, row.classCount)


    print("_____________Repeat Volunteers___")
    # Repeat volunteers (for individual events/programs and across all programs)
    # Excluding all volunteer training for now
    # Get people who came more than once for a program
    p_query = (EventParticipant
                         .select(   EventParticipant.user_id,
                                    (ProgramEvent.program_id).alias('program_id'),
                                    Program.programName.alias("programName"),
                                    fn.Count(EventParticipant.event_id).alias('event_count'))
                         .join(ProgramEvent, on=(EventParticipant.event_id == ProgramEvent.event_id))
                         .join(Program, on=(ProgramEvent.program_id == Program.id))
                         .group_by(EventParticipant.user_id, ProgramEvent.program_id)
                         .having(fn.Count(EventParticipant.event_id) > 1))
    for result in p_query.dicts():
        print(f"Participant:", result["user"], "   Events:", result["event_count"], "    Program Id/Name:", result["program_id"], result["programName"])
    print("-----------------------")

    

    # People who came more than twice for a program
    # Get people/how many that participated in any to any event


    # Retention rates of volunteers (waiting for a bit of clarification from CELTS, check with me if you pick up this issue)




