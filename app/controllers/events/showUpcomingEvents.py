from app.controllers.events import events_bp
from app.logic.getUpcomingEvents import getUpcomingEventsForUser

@events_bp.route('/events/upcoming')
def showUpcomingEvents(username):
    upcomingEvents = getUpcomingEventsForUser(username)
    return upcomingEvents
