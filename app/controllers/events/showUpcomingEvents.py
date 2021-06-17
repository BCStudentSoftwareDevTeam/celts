from app.models.program import Program
from app.models.interest import Interest
from app.models.event import Event
from app.models.user import User
from flask import render_template
from app.controllers.events import events_bp


def getUpcomingEventsForUser(username):

    user = User.get(User.username == username)
    interestedEvent = (Event.select()
                            .join(Interest, on=(Event.program == Interest.program))
                            .where(Interest.user == user))

    #upcomingEvents = []
    # for event in interestedEvent.objects():
    #     #FIXME: Change event.description to event.eventName. When the eventName column is filled
    #     upcomingEvents.append({"description": event.description, "program":event.program, "startDate": event.startDate})

    return list(interestedEvent)


@events_bp.route('events/upcoming')
def showUpcomingEvents(username):

    user = User.get(User.username == "khatts") #FIXME: remove line once g.current_user gets implemented
    interestedEvent = getUpcomingEventsForUser(user)
    return render_template('showUpcomingEvents.html', upcomingEvents = list(interestedEvent))
