#query data and generate spreadsheet
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.programEvent import ProgramEvent
from peewee import fn, JOIN

# Total volunteer hours by program along with a sum of all programs
def volunteer():
    query = (EventParticipant
            .select(fn.SUM(EventParticipant.hoursEarned))
            .join(ProgramEvent, on=(EventParticipant.event_id == ProgramEvent.event_id))
            .group_by(ProgramEvent.program_id))
    result = query.scalar()
    print(result)


    totalHours = EventParticipant.select(fn.Sum(fn.Coalesce(EventParticipant.hoursEarned, 0))).scalar()

    print("Total Hours", totalHours)

    return query



# Volunteering numbers by class year
# Repeat volunteers (for individual events/programs and across all programs)
# Majors represented in volunteering
# Retention rates of volunteers (waiting for a bit of clarification from CELTS, check with me if you pick up this issue)