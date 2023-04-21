#query data and generate spreadsheet
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from app.models.event import Event
from app.models.term import Term
from peewee import *

def volunteer():

    # Total volunteer hours by program along with a sum of all programs
    query = (ProgramEvent.select(ProgramEvent.program_id, fn.SUM(EventParticipant.hoursEarned).alias('sum'))
                         .join(EventParticipant, on=(ProgramEvent.event == EventParticipant.event))
                         .join(Program, on=(Program.id == ProgramEvent.program_id))
                         .group_by(ProgramEvent.program_id))

    totalHoursByProgram= {pe.program.programName: pe.sum for pe in query}

    totalHoursAllProgram = EventParticipant.select(fn.Sum(fn.Coalesce(EventParticipant.hoursEarned, 0))).scalar()

    print('Total Hours by Program', totalHoursByProgram)
    print('Total Hours', totalHoursAllProgram)


    # Majors represented in volunteering
    majorQuery = (User.select(User.major, fn.COUNT(fn.DISTINCT(EventParticipant.user_id)).alias('count'))
                       .join(EventParticipant, on=(User.username == EventParticipant.user_id))
                       .group_by(User.major))
 
    print("_____________majors represented___")
    for row in majorQuery:
        print(row.major, row.count)


    # Volunteering numbers by class year
    classLevelQuery = (User.select(User.classLevel, fn.COUNT(fn.DISTINCT(EventParticipant.user_id)).alias('classCount'))
                            .join(EventParticipant, on=(User.username == EventParticipant.user_id))
                            .group_by(User.classLevel))

    print("_____________class year___")
    for row in classLevelQuery:
        print(row.classLevel, row.classCount)


    print("_____________Repeat Volunteers___")
    # Repeat volunteers (for individual events/programs and across all programs)
    # Excluding all volunteer training for now

    # Get people who came more than once (individual program)
    repeatPerProgramQuery = (EventParticipant.select(EventParticipant.user_id,(ProgramEvent.program_id).alias('program_id'),Program.programName.alias("programName"),fn.Count(EventParticipant.event_id).alias('event_count'))
                                             .join(ProgramEvent, on=(EventParticipant.event_id == ProgramEvent.event_id))
                                             .join(Program, on=(ProgramEvent.program_id == Program.id))
                                             .group_by(EventParticipant.user_id, ProgramEvent.program_id)
                                             .having(fn.Count(EventParticipant.event_id) > 1))


    for result in repeatPerProgramQuery.dicts():
        print(f"Participant:", result["user"], "   Events:", result["event_count"], "    Program Id/Name:", result["program_id"], result["programName"])
    print("-----------------------")
    

    # Get people who came more than once (all programs)
    repeatAllProgramQuery = (EventParticipant.select(EventParticipant.user_id, fn.COUNT(EventParticipant.user_id).alias('count'))
                                             .group_by(EventParticipant.user_id)
                                             .having(fn.COUNT(EventParticipant.user_id) > 1))

    for result in repeatAllProgramQuery:
        print(f"participant: {result.user_id}, count: {result.count}")
    print("-----------------------")

    




    # Retention rates of volunteers (waiting for a bit of clarification from CELTS, check with me if you pick up this issue)
    # We were thinking about overall retention from semester to semester generally, since we cannot do year to year yet. 
    # We would want this for recurring events as well as individual program participation.

    # Overall program retention from semester to semester

     #participation in a program in Fall

    fallParticipationQuery=(ProgramEvent.select(ProgramEvent.program_id, EventParticipant.user_id.alias('participants'), Program.programName.alias("progName"))
                                  .join(EventParticipant, on=(ProgramEvent.event == EventParticipant.event))
                                  .join(Program, on=(Program.id == ProgramEvent.program_id))
                                  .join(Event, on=(EventParticipant.event_id == Event.id))
                                  .join(Term, on=(Event.term_id == Term.id) )
                                  .where(Term.description == "Fall 2022"))
                                  
    # for result in fallParticipationQuery.dicts():
    #     print(f"Fall2022", result["participants"], result["progName"])
    fallParticipationDict = {}
    for result in fallParticipationQuery.dicts():
        prog_name = result['progName']
        participant = result['participants']
        if prog_name not in fallParticipationDict:
            fallParticipationDict[prog_name] = []
        fallParticipationDict[prog_name].append(participant)
    print(fallParticipationDict)
    print("------------------------")


    
      #participation in a program in Spring
    springParticipationQuery=(ProgramEvent.select(ProgramEvent.program_id, EventParticipant.user_id.alias('participants'), Program.programName.alias("progName"))
                                  .join(EventParticipant, on=(ProgramEvent.event == EventParticipant.event))
                                  .join(Program, on=(Program.id == ProgramEvent.program_id))
                                  .join(Event, on=(EventParticipant.event_id == Event.id))
                                  .join(Term, on=(Event.term_id == Term.id) )
                                #   .group_by(ProgramEvent.program_id)
                                  .where(Term.description == "Spring 2023"))
    # for result in springParticipationQuery.dicts():
    #     print(f"Spring2023", result["participants"], result["progName"])
    
    springParticipationDict = {}
    for result in springParticipationQuery.dicts():
        prog_name = result['progName']
        participant = result['participants']
        if prog_name not in springParticipationDict:
            springParticipationDict[prog_name] = []
        springParticipationDict[prog_name].append(participant)
    print(springParticipationDict)

    print("-----------------")


    #retention rate = (springParticipation/fallParticipation) * 100 ? (Do this by program)

    #retention rates by program
    # define a function to calculate the retention rate for each program
    def retention_rate(fall_dict, spring_dict):
        retention_dict = {}
        for program in fall_dict.keys():
            fall_participants = set(fall_dict[program])
            spring_participants = set(spring_dict.get(program, []))
            retention_rate = len(fall_participants & spring_participants) / len(fall_participants)
            retention_dict[program] = retention_rate
        return retention_dict

    # calculate the retention rate using the defined function
    retention_rate_dict = retention_rate(fallParticipationDict, springParticipationDict)

    for program, retention_rate in retention_rate_dict.items():
        print(f"{program}: {round(retention_rate * 100, 2)}%")
    print("-----------")
    


    #Half retention rate for recurring events (still working on this)
    #Fall 2022
    programs = ProgramEvent.select(ProgramEvent.program_id).distinct()
    

    # Loop over the programs and get the corresponding event IDs
    for program in programs:
        print(program)
        # Define the query for each program
        query = (EventParticipant
                .select(EventParticipant.event_id.alias("event_id"), Event.name.alias("name"))
                .join(Event, on=(EventParticipant.event_id == Event.id))
                .join(ProgramEvent, on=(EventParticipant.event_id == ProgramEvent.event_id))
                .where((ProgramEvent.program_id == program.program_id) & (Event.recurringId == True))
                .distinct()
                .dicts())

        results = query.execute()

        # Print the results for each program
        for result in results:
            print(result["event_id"], result["name"])

     