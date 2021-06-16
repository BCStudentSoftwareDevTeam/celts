from app.models.program import Program
from app.models.interest import Interest
from app.models.event import Event
from app.models.user import User


def showUpcomingEvents(userid):

    user = User.get(User.username == userid)


    joinedTable = (Interest.select()
                        .join(Event, on=(Interest.program == Event.program))
                        .where(Interest.user == user))

    for table in joinedTable.objects():
         print(table.event.description)
    # upcomingEvents = joinedTable.select(joinedTable.event.description)
    # print(list(upcomingEvents))
    print(list(joinedTable))



    # interestedPrograms = Interest.select(Interest.program).where(Interest.user == user)
    # print(len(interestedPrograms))
    # # upcomingEvents = Event.select(Event.description).where(Event.program == interestedPrograms)
    #
    # #if len(interestedPrograms) == 1:
    # upcomingEvents = Event.select(Event.description).where(Event.program == interestedPrograms)
    # return upcomingEvents
    # print(type(upcomingEvents))
    # print(list(upcomingEvents))
    # else:
    #     for program in list(interestedPrograms):
    #         #upcomingEvents = Event.select().join().where(Event.program == interestedPrograms[program])
    #         upcomingEvents = Event.select(Event.description).where(Event.program == program)
    #         print(list(upcomingEvents))
    #         print(program)
    # else:
    #     for program in range(len(interestedPrograms)):
    #         upcomingEvents = Event.select(Event.description).join(Event.program).where(Event.program == interestedPrograms[program])
    #
    return upcomingEvents
