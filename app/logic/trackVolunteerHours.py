from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.event import Event
from peewee import fn

def trackVolunteerHours():
    """
    This function gets the data from the database so that we could use them in the UI.
    """
    trackHours = EventParticipant.select()

    return trackHours

def prereqParticipants(programID):
    prereqEvents = Event.select().where(Event.program == programID)
    prlist = []
    eventPreqDataList = []

    for prereq in prereqEvents:
        if prereq.isPrerequisiteForProgram:
            prlist.append(prereq.id)

    eventPreqData = (EventParticipant.select()
                                     .where(EventParticipant.event.in_(prlist)))

    for i in eventPreqData:
        eventPreqDataList.append(i.user.username)

    attendedPreq = list(filter(lambda user: eventPreqDataList.count(user) == len(prlist), eventPreqDataList))

    for user in attendedPreq:
        if user in attendedPreq:
            attendedPreq.remove(user)

    return attendedPreq


# Useful Junk

# <!-- <th></th> -->
    # <!-- <td>
    #   {% if attendedPreq[participant.user.username]=="Warning" %}
    #     <span class="bi bi-exclamation-triangle"></span>
    #   {% endif %}
    # </td> -->
