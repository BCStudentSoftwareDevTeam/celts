from app.controllers.events import events_bp
from app.logic.getUpcomingEvents import getUpcomingEventsForUser

def showUpcomingEvents(username):
    upcomingEvents = getUpcomingEventsForUser(username)
    return upcomingEvents
