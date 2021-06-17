from app.models.program import Program
from app.models.interest import Interest
from app.models.event import Event
from app.models.user import User

def getUpcomingEventsForUser(username):
    user = User.get(User.username == username)
    interestedEvent = (Event.select(Event, Program, Interest)
                            .join(Program)
                            .switch(Event)
                            .join(Interest, on=(Event.program == Interest.program))
                            .where(Event.program_id == Program.id, Interest.user == user)
                            )
    upcomingEvents = []
    for event in interestedEvent.objects():
        #FIXME: Change event.description to event.eventName (or just add it to the dict). When the eventName column is filled
        upcomingEvents.append(
                            {"description": event.description,
                            "program":event.program,
                            "startDate": event.startDate,
                            "programName":event.programName,
                            "endDate": event.endDate})
    return upcomingEvents
