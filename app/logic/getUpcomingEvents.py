from app.models.program import Program
from app.models.interest import Interest
from app.models.event import Event
from app.models.user import User
from datetime import date, datetime, time

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
        today = date.today()
        times = datetime.now().time()
        event_time = event.timeStart
        #FIXME: Change event.description to event.eventName (or just add it to the dict). When the eventName column is filled
        if event.startDate >= today and event.timeStart > times:
            print(event.timeStart)
            upcomingEvents.append(
                                    {"description": event.description,
                                    "program":event.program,
                                    "startDate": event.startDate,
                                    "programName":event.programName,
                                    "endDate": event.endDate})
    return upcomingEvents
