from importlib.abc import ResourceReader
from os import major
from peewee import fn, Case, JOIN
from collections import defaultdict


from app import app
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.program import Program
from app.models.event import Event
from app.models.term import Term


def getUniqueVolunteers(academicYear):
    uniqueVolunteers = (EventParticipant.select(fn.DISTINCT(EventParticipant.user_id), fn.CONCAT(User.firstName, ' ', User.lastName), User.bnumber)
                        .join(User).switch(EventParticipant)
                        .join(Event)
                        .join(Term)
                        .where(Term.academicYear == academicYear)
                        .order_by(EventParticipant.user_id))

    return uniqueVolunteers.tuples()


def getVolunteerProgramEventByTerm(term):
    volunteersByTerm = (EventParticipant.select(fn.CONCAT(User.firstName, ' ', User.lastName), EventParticipant.user_id, Program.programName, Event.name)
                        .join(User).switch(EventParticipant)
                        .join(Event)
                        .join(Program)
                        .where(Event.term_id == term)
                        .order_by(EventParticipant.user_id))

    return volunteersByTerm.tuples()


def totalVolunteerHours(academicYear):
    query = (EventParticipant.select(fn.SUM(EventParticipant.hoursEarned))
                             .join(Event, on=(EventParticipant.event == Event.id))
                             .join(Term, on=(Event.term == Term.id))
                             .where(Term.academicYear == academicYear)
             )

    return query.tuples()


def volunteerProgramHours(academicYear):
    volunteerProgramHours = (EventParticipant.select(Program.programName, EventParticipant.user_id, fn.SUM(EventParticipant.hoursEarned))
                             .join(Event, on=(EventParticipant.event_id == Event.id))
                             .join(Program, on=(Event.program_id == Program.id))
                             .join(Term, on=(Event.term == Term.id))
                             .where(Term.academicYear == academicYear)
                             .group_by(Program.programName, EventParticipant.user_id))

    return volunteerProgramHours.tuples()


def onlyCompletedAllVolunteer(academicYear):
    subQuery = (EventParticipant.select(EventParticipant.user_id)
                .join(Event)
                .join(Term)
                .where(Event.name != "All Volunteer Training", Term.academicYear == academicYear))

    onlyAllVolunteer = (EventParticipant.select(EventParticipant.user_id, fn.CONCAT(User.firstName, " ", User.lastName))
                        .join(User).switch(EventParticipant)
                        .join(Event)
                        .join(Term)
                        .where(Event.name == "All Volunteer Training", Term.academicYear == academicYear, EventParticipant.user_id.not_in(subQuery)))

    return onlyAllVolunteer.tuples()


def volunteerHoursByProgram(academicYear):
    query = (Program.select(Program.programName, fn.SUM(EventParticipant.hoursEarned).alias('sum'))
             .join(Event)
             .join(EventParticipant, on=(Event.id == EventParticipant.event_id))
             .join(Term, on=(Term.id == Event.term))
             .where(Term.academicYear == academicYear)
             .group_by(Program.programName)
             .order_by(Program.programName))

    return query.tuples()


def volunteerMajorAndClass(academicYear, column, reorderClassLevel=False):
    majorAndClass = (User.select(Case(None, ((column.is_null(), "Unknown"),), column), fn.COUNT(fn.DISTINCT(EventParticipant.user_id)).alias('count'))
                     .join(EventParticipant, on=(User.username == EventParticipant.user_id))
                     .join(Event, on=(EventParticipant.event_id == Event.id))
                     .join(Term, on=(Event.term == Term.id))
                     .where(Term.academicYear == academicYear)
                     .group_by(column))

    if reorderClassLevel:
        majorAndClass = majorAndClass.order_by(Case(None, ((column == "Freshman", 1),
                                                           (column == "Sophomore", 2),
                                                           (column == "Junior", 3),
                                                           (column == "Senior", 4),
                                                           (column == "Graduating", 5),
                                                           (column == "Non-Degree", 6),
                                                           (column.is_null(), 7)),
                                               8))
    else:
        majorAndClass = majorAndClass.order_by(column.asc(nulls='LAST'))

    return majorAndClass.tuples()


def repeatVolunteersPerProgram(academicYear):
    repeatPerProgramQuery = (EventParticipant.select(fn.CONCAT(User.firstName, " ", User.lastName).alias('fullName'),
                                                     Program.programName.alias("programName"),
                                                     fn.COUNT(EventParticipant.event_id).alias('event_count'))
                             .join(Event, on=(EventParticipant.event_id == Event.id))
                             .join(Program, on=(Event.program == Program.id))
                             .join(User, on=(User.username == EventParticipant.user_id))
                             .join(Term, on=(Event.term == Term.id))
                             .where(Term.academicYear == academicYear)  
                             .group_by(User.firstName, User.lastName, Event.program)
                             .having(fn.COUNT(EventParticipant.event_id) > 1)
                             .order_by(Event.program, User.lastName))

    return repeatPerProgramQuery.tuples()


def repeatVolunteers(academicYear):
    repeatAllProgramQuery = (EventParticipant.select(fn.CONCAT(User.firstName, " ", User.lastName), fn.COUNT(EventParticipant.user_id).alias('count'))
                             .join(User, on=(User.username == EventParticipant.user_id))
                             .join(Event, on=(EventParticipant.event == Event.id))
                             .join(Term, on=(Event.term == Term.id))
                             .where(Term.academicYear == academicYear)
                             .group_by(User.firstName, User.lastName)
                             .having(fn.COUNT(EventParticipant.user_id) > 1))

    return repeatAllProgramQuery.tuples()


def getRetentionRate(academicYear):
    retentionList = []
    fall, spring = academicYear.split("-")
    fallParticipationDict = termParticipation(f"Fall {fall}")
    springParticipationDict = termParticipation(f"Spring {spring}")

    retentionRateDict = calculateRetentionRate(fallParticipationDict, springParticipationDict)
    for program, retentionRate in retentionRateDict.items():
        retentionList.append((program, str(round(retentionRate * 100, 2)) + "%"))

    return retentionList


def termParticipation(termDescription):
    participationQuery = (Event.select(Event.program, EventParticipant.user_id.alias('participant'), Program.programName.alias("programName"))
                          .join(EventParticipant, JOIN.LEFT_OUTER, on=(Event.id == EventParticipant.event))
                          .join(Program, on=(Event.program == Program.id))
                          .join(Term, on=(Event.term_id == Term.id))
                          .where(Term.description == termDescription)
                          .order_by(EventParticipant.user))

    programParticipationDict = defaultdict(list)
    for result in participationQuery.dicts():
        programName = result['programName']
        participant = result['participant']
        programParticipationDict[programName].append(participant)

    return dict(programParticipationDict)


def removeNullParticipants(participantList):
    return list(filter(lambda participant: participant, participantList))


def calculateRetentionRate(fallDict, springDict):
    retentionDict = {}
    for program in fallDict:
        fallParticipants = set(removeNullParticipants(fallDict[program]))
        springParticipants = set(removeNullParticipants(springDict.get(program, [])))
        retentionRate = 0.0
        try:
            retentionRate = len(fallParticipants & springParticipants) / len(fallParticipants)
        except ZeroDivisionError:
            pass
        retentionDict[program] = retentionRate

    return retentionDict

def repeatVolunteersPerProgram(academicYear):
    repeatPerProgramQuery = (EventParticipant.select(fn.CONCAT(User.firstName, " ", User.lastName).alias('fullName'),
                                                     Program.programName.alias("programName"),
                                                     fn.COUNT(EventParticipant.event_id).alias('event_count'))
                             .join(Event, on=(EventParticipant.event_id == Event.id))
                             .join(Program, on=(Event.program == Program.id))
                             .join(User, on=(User.username == EventParticipant.user_id))
                             .join(Term, on=(Event.term == Term.id))
                             .where(Term.academicYear == academicYear)  
                             .group_by(User.firstName, User.lastName, Event.program)
                             .having(fn.COUNT(EventParticipant.event_id) > 1)
                             .order_by(Event.program, User.lastName))

    return repeatPerProgramQuery.tuples()


def generateReportsChartsDataJson(academicYear):
  reportsChartsDataJson = {}

  hoursByProgram = volunteerHoursByProgram(academicYear)
  volunteerByMajor = volunteerMajorAndClass(academicYear, User.major)
  volunteersByClassLevel = volunteerMajorAndClass(academicYear, User.classLevel, True)
  repeatVolunteersPerProgramm = repeatVolunteersPerProgram(academicYear)
  repeatVolunteersAllPrograms = repeatVolunteers(academicYear)


  reportsChartsDataJson["hoursByProgram"] = list(hoursByProgram)
  reportsChartsDataJson["volunteerByMajor"] = list(volunteerByMajor)
  reportsChartsDataJson["volunteersByClassLevel"] = list(volunteersByClassLevel)
  reportsChartsDataJson["repeatVolunteersPerProgram"] = list(repeatVolunteersPerProgramm) 
  reportsChartsDataJson["repeatVolunteersAllPrograms"] = list(repeatVolunteersAllPrograms)

  

  return reportsChartsDataJson

