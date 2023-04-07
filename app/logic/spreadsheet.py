#query data and generate spreadsheet
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from peewee import fn, JOIN

# Total volunteer hours by program along with a sum of all programs
def volunteer():

    #What Anderson, Sreynit, Fleur worked on
    # query = (ProgramEvent
    #         .select(fn.SUM(EventParticipant.hoursEarned))
    #         .join(EventParticipant, on=(ProgramEvent.event == EventParticipant.event))
    #         .group_by(ProgramEvent.program_id))
    # result = query.scalar()
    # print(result)
   
    # Hours = {program.id: program.hours for program in query}
    # print(Hours)

    #Fleur and Sreynit after Anderson left (This is printing the correct total for each program)
    query = (ProgramEvent
            .select(ProgramEvent.program_id, fn.SUM(EventParticipant.hoursEarned).alias('sum'))
            .join(EventParticipant, on=(ProgramEvent.event == EventParticipant.event))
            .join(Program, on=(Program.id == ProgramEvent.program_id))
            .group_by(ProgramEvent.program_id))

    #Added by Anderson (nice job getting figured out!), I am not sure how yall will be accessing/passing around the data for the spreadsheet but I added the program name to it. The print below has the creats a dict with the program name as the key and the hours as the value. If you don't want to keep the program name here and will change is later then remove the second join I added. 
    print({pe.program.programName: pe.sum for pe in query})

    for row in query:
        print(row.program_id, getattr(row, 'sum'))

    totalHours = EventParticipant.select(fn.Sum(fn.Coalesce(EventParticipant.hoursEarned, 0))).scalar()

    print("Total Hours", totalHours)

    return query



# Volunteering numbers by class year
# Repeat volunteers (for individual events/programs and across all programs)
# Majors represented in volunteering
# Retention rates of volunteers (waiting for a bit of clarification from CELTS, check with me if you pick up this issue)
