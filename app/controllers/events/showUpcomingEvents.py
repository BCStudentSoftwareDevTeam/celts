from app.models.program import Program
from app.models.interest import Interest
from app.models.event import Event
from app.models.user import User


def showUpcomingEvents(userid):

    user = User.get(User.username == userid)

    interestedEvent = (Event.select(Event, Interest)
                        .join(Interest, on=(Event.program == Interest.program))
                        .where(Interest.user == user))

    upcomingEvents = []
    for event in interestedEvent.objects():
        print(event.description)
        upcomingEvents.append(event.description)
    print(upcomingEvents)

    print()

    return upcomingEvents
