#query data and generate spreadsheet
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.programEvent import ProgramEvent
from peewee import fn

# Total volunteer hours by program along with a sum of all programs
def volunteer():
    query = (EventParticipant
            .select(ProgramEvent.program, fn.Sum(fn.Coalesce(EventParticipant.hoursEarned, 0)))
            .join(ProgramEvent, on=(EventParticipant.event == ProgramEvent.event))
            .group_by(ProgramEvent.program))
        
    print("SPREADSHEEEEEEEEEEEEEEEEt", list(query))

    return query



# Volunteering numbers by class year
# Repeat volunteers (for individual events/programs and across all programs)
# Majors represented in volunteering
# Retention rates of volunteers (waiting for a bit of clarification from CELTS, check with me if you pick up this issue)