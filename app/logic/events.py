from app.models.event import Event
from app.models.program import Program
from peewee import DoesNotExist

def getEvents(program_id=None):

    if program_id:
        Program.get_by_id(program_id) # raises an exception if program doesn't exist
        return Event.select(Event).where(Event.program == program_id)
    else:
        return Event.select()

def groupingEvents(termID):
    # groupEvents = sorted(groupEvents, key = itemgetter('Event.program'))
    #
    # for key, value in groupby(groupEvents,key = itemgetter('Event.program')):
    #     print(key)
    #     for k in value:
    #         print(k)
    # return (key,k)

    groupEvents = (Event.select(Event.description,Event.program).where(Event.term == termID).order_by(Event.program))
    for item in list(groupEvents.objects()):
        print(item.program)







# events = [item for item in groupEvents.objects()]

    #check if the program are the same
    return groupEvents
    # return [group for group in groupingEvents|compare(Event.program)]
