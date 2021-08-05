from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.interest import Interest
from app.models.event import Event
from app.models.user import User
from datetime import date, datetime, time

def getUpcomingEventsForUser(user,asOf=datetime.now()):
    """
        Get the list of upcoming events that the user is interested in.

        :param user: a username or User object
        :param asOf: The date to use when determining future and past events. 
                      Used in testing, defaults to the current timestamp.
        :return: A list of Event objects
    """

    events = (Event.select(Event)
                            .join(ProgramEvent)
                            .join(Interest, on=(ProgramEvent.program == Interest.program))
                            .where(Interest.user == user)
                            .where(Event.startDate >= asOf)
                            .where(Event.timeStart > asOf.time())
                            .distinct() # necessary because of multiple programs
                            .order_by(Event.startDate)
                            )
    return list(events)
