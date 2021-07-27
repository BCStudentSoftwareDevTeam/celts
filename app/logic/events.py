from app.models.event import Event
from app.models.program import Program
from app.models.term import Term
from app.models.programEvent import ProgramEvent
from peewee import DoesNotExist

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
        programs.setdefault(event.programName, []).append(event.description)

    return programs

def groupingEvents(term):
    studentLedEvents = (Event.select(Event, Program)
                             .join(ProgramEvent)
                             .join(Program)
                             .where(Program.isStudentLed,
                                    Event.term == term))

    trainingEvents = (Event.select(Event, Program)
                           .join(ProgramEvent)
                           .join(Program)
                           .where(Event.isTraining,
                                  Event.term == term))


    bonnerScholarsEvents = (Event.select(Event, Program)
                                 .join(ProgramEvent)
                                 .join(Program)
                                 .where(Program.isBonnerScholars,
                                        Event.term == term))

    oneTimeEvents = (Event.select(Event, Program)
                          .join(ProgramEvent)
                          .join(Program)
                          .where(Program.isStudentLed == False,
                                 Event.isTraining == False,
                                 Program.isBonnerScholars == False,
                                 Event.term == term))

    # termName = Term.get_by_id(term).description

    categorizedEvents = {"Student Led Events" : groupEventsByProgram(studentLedEvents),
                         "Trainings" : groupEventsByProgram(trainingEvents),
                         "Bonner Scholars" : groupEventsByProgram(bonnerScholarsEvents),
                         "One Time Events" : groupEventsByProgram(oneTimeEvents)}

    print(categorizedEvents)
    return categorizedEvents
