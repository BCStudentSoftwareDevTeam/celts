#query data and generate spreadsheet
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.programEvent import ProgramEvent
from peewee import fn, JOIN

# Total volunteer hours by program along with a sum of all programs
def volunteer():
    query = (ProgramEvent
            .select(fn.SUM(EventParticipant.hoursEarned).alias('hours'))
            .join(EventParticipant, on=(ProgramEvent.event == EventParticipant.event))
            .group_by(ProgramEvent.program_id)).execute()
    # result = query.scalar()
    # print(result)
    Hours = {program.id: program.hours for program in query}
    print(Hours)


    totalHours = EventParticipant.select(fn.Sum(fn.Coalesce(EventParticipant.hoursEarned, 0))).scalar()

    print("Total Hours", totalHours)

    return query



# Volunteering numbers by class year
# Repeat volunteers (for individual events/programs and across all programs)
# Majors represented in volunteering
# Retention rates of volunteers (waiting for a bit of clarification from CELTS, check with me if you pick up this issue)