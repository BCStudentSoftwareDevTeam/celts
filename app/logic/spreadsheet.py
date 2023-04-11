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
    query_major = (User.select(User.username, User.major)
                       .join(EventParticipant)
                       .group_by(User.username, User.major))

    print("Majors represented in volunteering:")
    for row in query_major:
        print({row.username: row.major})


# # Volunteering numbers by class year
# Volunteering numbers by class year
# Repeat volunteers (for individual events/programs and across all programs)
# Retention rates of volunteers (waiting for a bit of clarification from CELTS, check with me if you pick up this issue)
