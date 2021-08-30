from app.models.event import Event
from app.models.program import Program
from app.models.term import Term
from app.models.interest import Interest
from app.models.programEvent import ProgramEvent
from peewee import DoesNotExist
from datetime import *
def getEvents(program_id=None):

    if program_id:
        Program.get_by_id(program_id) # raises an exception if program doesn't exist
        return (Event.select(Event).join(ProgramEvent)
                     .where(ProgramEvent.program == program_id).distinct())
    else:
        return Event.select()

def groupEventsByProgram(eventQuery):
    programs = {}

    for event in eventQuery.objects():
        programs.setdefault(Program.get_by_id(event.program_id), []).append(event)

    return programs

def groupEventsByCategory(term):

    term = Term.get_by_id(term)

    studentLedEvents = (Event.select(Event, Program.id.alias("program_id"))
                             .join(ProgramEvent)
                             .join(Program)
                             .where(Program.isStudentLed,
                                    Event.term == term))

    trainingEvents = (Event.select(Event, Program.id.alias("program_id"))
                           .join(ProgramEvent)
                           .join(Program)
                           .where(Event.isTraining,
                                  Event.term == term))


    bonnerScholarsEvents = (Event.select(Event, Program.id.alias("program_id"))
                                 .join(ProgramEvent)
                                 .join(Program)
                                 .where(Program.isBonnerScholars,
                                        Event.term == term))

    oneTimeEvents = (Event.select(Event, Program.id.alias("program_id"))
                          .join(ProgramEvent)
                          .join(Program)
                          .where(Program.isStudentLed == False,
                                 Event.isTraining == False,
                                 Program.isBonnerScholars == False,
                                 Event.term == term))

    categorizedEvents = {"Student Led Events" : groupEventsByProgram(studentLedEvents),
                         "Trainings" : groupEventsByProgram(trainingEvents),
                         "Bonner Scholars" : groupEventsByProgram(bonnerScholarsEvents),
                         "One Time Events" : groupEventsByProgram(oneTimeEvents)}
    return categorizedEvents



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
