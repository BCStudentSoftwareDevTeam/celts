from app.logic.emailHandler import EmailHandler
from app.models.event import Event
from datetime import date, datetime, timedelta

def checkForEvents():
    currentDate = date.today().strftime("%m/%d/%Y")
    today = datetime.strptime(currentDate,"%m/%d/%Y")
    tomorrowDate = today + timedelta(days=1)
    events = list(Event.select().where(Event.startDate==tomorrowDate))
    for i in range(len(events)):
        createData(events[i].id)

def createData(eventId):
    event = Event.get_by_id(eventId)
