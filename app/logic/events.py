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

def groupingEvents(term):

    studentLedEvents = (Event.select(Event,Program)
                             .join(ProgramEvent)
                             .join(Program)
                             .where(Program.isStudentLed,
                                    Event.term == term)
                             .distinct())

    print(list(studentLedEvents))
    programName = []
    eventDescription = []
    for e in studentLedEvents.objects():
        programName.append(e.programName)
        eventDescription.append(e.description)
    print(programName)
    print(eventDescription)
    # studentLedPrograms = []
    # [studentLedPrograms.append(event.programName) for event in studentLedEvents.objects()
    #                     if event.programName not in studentLedPrograms]
    # print(studentLedPrograms)
    studentLedEventsDict = { program:event for (program,event) in zip(programName, eventDescription)}
    #[studentLedEventsDict[event.programName].append(event.description) for event in studentLedEvents.objects()]
    print("studentLedEventsDict", studentLedEventsDict)


    # trainingEvents = (Event.select()
    #                        .where(Event.isTraining,
    #                               Event.term == term))

    # trainingPrograms = []
    # [trainingPrograms.append(event.program) for event in trainingEvents
    #                   if event.program not in trainingPrograms]
    #
    # bonnerScholarsEvents = (Event.select()
    #                              .join(Program)
    #                              .where(Program.isBonnerScholars,
    #                                     Event.term == term))

    # bonnerScholarsPrograms = []
    # [bonnerScholarsPrograms.append(event.program) for event in bonnerScholarsEvents
    #                         if event.program not in bonnerScholarsPrograms]
    #
    # oneTimeEvents = (Event.select()
    #                       .join(Program)
    #                       .where(Program.isStudentLed == False,
    #                              Event.isTraining == False,
    #                              Program.isBonnerScholars == False,
    #                              Event.term == term))
    # oneTimePrograms = []
    # [oneTimePrograms.append(event.program) for event in oneTimeEvents
    #                  if event.program not in oneTimePrograms]
    #
    # termName = Term.get_by_id(term).description
    #
    # return (studentLedEvents, studentLedPrograms, trainingEvents, trainingPrograms,
    # bonnerScholarsEvents, bonnerScholarsPrograms, oneTimeEvents, oneTimePrograms, termName)
    categorizedEvents = {"studentLed": studentLedEventsDict}
    print(categorizedEvents)
    return categorizedEvents
