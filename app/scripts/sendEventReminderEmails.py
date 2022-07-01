from app.logic.emailHandler import EmailHandler
from app.models.event import Event
from app.models.term import Term
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from datetime import date, datetime, timedelta

def checkForEvents():
    currentDate = date.today().strftime("%m/%d/%Y")
    today = datetime.strptime(currentDate,"%m/%d/%Y")
    tomorrowDate = today + timedelta(days=1)
    currentTerm = Term.get(Term.id).where(Term.isCurrentTerm==1)
    events = list(Event.select().where(Event.startDate==tomorrowDate))
    for i in range(len(events)):
        programId = ProgramEvent.get(ProgramEvent.program).where(Program.event==events[i].id)
        senderName = Program.get(Program.senderName)
        createData(events[i].id, programId, currentTerm, "Reminder", "Interested", )


def createData(eventId, programId, selectedTerm, templateIdentifier, recipientsCategory, emailSender, subject, body):
    event = Event.get_by_id(eventId)
