#query data and generate spreadsheet
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.programEvent import ProgramEvent
from app.models.program import Program
from app.models.event import Event
from app.models.term import Term
from peewee import *
import csv


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
    programs = ProgramEvent.select(ProgramEvent.program_id).distinct()

    # Loop over the programs and get the corresponding event IDs
    for program in programs:
        print("program_id", program)
        # Define the query for each program
        query = (EventParticipant
                .select(EventParticipant.event_id.alias("event_id"), Event.name.alias("name"))
                .join(Event, on=(EventParticipant.event_id == Event.id))
                .join(ProgramEvent, on=(EventParticipant.event_id == ProgramEvent.event_id))
                .where((ProgramEvent.program_id == program.program_id) & (Event.recurringId != None))
                .distinct()
                .dicts())

        results = query.execute()

        event_count = 0
        name_counts = {}

        for result in results:
            event_count += 1
            print(result["event_id"], "--------",result["name"])
            participants = EventParticipant.select(EventParticipant.user_id).where(EventParticipant.event_id == result["event_id"])
            for participant in participants:
                name = participant.user_id
                if name not in name_counts:
                    name_counts[name] = 1
                else:
                    name_counts[name] += 1
                
        half_count = event_count // 2
        qualified_names = [name for name, count in name_counts.items() if count >= half_count]
        
        if len(name_counts) > 0:
            percentage = len(qualified_names) / len(name_counts) * 100
        else:
            percentage = 0
        
        print(f'{percentage:.2f}% of the participants came to at least half of the events.')
        print("__________________________________________________________________________________")
    print("--------------------------------------------------------------------------------------------------------")

     #Full retention rate for recurring events (still working on this)
    programs = ProgramEvent.select(ProgramEvent.program_id).distinct()

    # Loop over the programs and get the corresponding event IDs
    for program in programs:
        print(program)
        # Define the query for each program
        query = (EventParticipant
                .select(EventParticipant.event_id.alias("event_id"), Event.name.alias("name"))
                .join(Event, on=(EventParticipant.event_id == Event.id))
                .join(ProgramEvent, on=(EventParticipant.event_id == ProgramEvent.event_id))
                .where((ProgramEvent.program_id == program.program_id) & (Event.recurringId != None))
                .distinct()
                .dicts())

        results = query.execute()

        event_count = 0
        name_counts = {}

        for result in results:
            event_count += 1
            print(result["event_id"], "--------",result["name"])
            participants = EventParticipant.select(EventParticipant.user_id).where(EventParticipant.event_id == result["event_id"])
            for participant in participants:
                name = participant.user_id
                if name not in name_counts:
                    name_counts[name] = 1
                else:
                    name_counts[name] += 1
                
        qualified_names = [name for name, count in name_counts.items() if count == event_count]
        
        if len(name_counts) > 0:
            percentage = len(qualified_names) / len(name_counts) * 100
        else:
            percentage = 0
        
        print(f'{percentage:.2f}% of the participants came to all the series in this recurring event.')

        print("__________________________________________________________________________________")



    # Define the name of the CSV file
    filename = "program_hours.csv"

    # Open the CSV file in append mode and write the program names and volunteer hours to it
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        
        # If the file is empty, add the header row
        if csvfile.tell() == 0:
            writer.writerow(["PROGRAM NAME", "VOLUNTEER HOURS", "RETENTION RATE"])
        
        # Write each program name and its corresponding volunteer hours as a row in the CSV file,
        # and update the retention rate if the program is already in the file
        for program, hours in totalHoursByProgram.items():
            retention_rate = retention_rate_dict.get(program)
            if retention_rate is None:
                writer.writerow([program, hours, ""])
            else:
                writer.writerow([program, hours, f"{round(retention_rate * 100, 2)}%"])
        
     
        writer.writerow([" "," "])
        writer.writerow(["TOTAL HOURS ALL PROGRAMS",totalHoursAllProgram])



        writer.writerow([" "," "])
        writer.writerow(["MAJORS REPRESENTED IN VOLUNTEERING", "COUNT"])
        for row in majorQuery:
            writer.writerow([row.major, row.count])

        writer.writerow([" "," "])
        writer.writerow(["VOLUNTEERS BY CLASS YEAR", "COUNT"])
        for row in classLevelQuery:
            writer.writerow([row.classLevel, row.classCount])

        writer.writerow([" "," "])
        writer.writerow(["PROGRAM", "REPEAT VOLUNTEER"])
        for row in repeatPerProgramQuery.dicts():
            writer.writerow([row["programName"], row["user"]])
        
        writer.writerow([" "," "])
        # Get people who came more than once (all programs)
        writer.writerow(["PROGRAM", "PARTICIPANT WHO ATTENDED ALL PROGRAM"])
        for result in repeatAllProgramQuery:
             writer.writerow([result.count, result.user_id])

        writer.writerow([" "," "])
        writer.writerow(["PROGRAM", "RETENTION RATE"])
        

            




