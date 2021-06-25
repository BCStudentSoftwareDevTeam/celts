from app.models.program import Program
from app.models.interest import Interest
from app.models.event import Event
from app.models.user import User
from datetime import date, datetime, time

def getUpcomingEventsForUser(user):

    interestedEvents = (Event.select()
                            .join(Interest, on=(Event.program == Interest.program))
                            .where(Interest.user == user)
                            )
    upcomingEvents = []

    for event in interestedEvents:

        if event.startDate >= date.today() and event.timeStart > datetime.now().time():
            upcomingEvents.append(event)

    return upcomingEvents
