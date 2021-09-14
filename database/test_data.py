'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''

from datetime import *
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.term import Term
from app.models.program import Program
from app.models.programEvent import ProgramEvent
from app.models.event import Event
from app.models.programBan import ProgramBan
from app.models.course import Course
from app.models.courseStatus import CourseStatus
from app.models.courseInstructor import CourseInstructor
from app.models.courseParticipant import CourseParticipant
from app.models.eventParticipant import EventParticipant
from app.models.interest import Interest
from app.models.facilitator import Facilitator

print("Inserting data for demo and testing purposes.")
users = [
    {
        "username": "ramsayb2",
        "bnumber": "B00173723",
        "email": "ramsayb2@berea.edu",
        "phoneNumber": "555-555-5555",
        "firstName": "Brian",
        "lastName": "Ramsay",
        "isStudent": False,
        "isFaculty": False,
        "isCeltsAdmin": True,
        "isCeltsStudentStaff": False
    },
    {
        "username" : "khatts",
        "bnumber" : "B00759107",
        "email": "khatts@berea.edu",
        "phoneNumber": "555-555-5555",
        "firstName" : "Sreynit",
        "lastName" : "Khatt",
        "isStudent": True,
        "isFaculty": False,
        "isCeltsAdmin": True,
        "isCeltsStudentStaff": False
    },
    {
        "username": "neillz",
        "bnumber": "B00751864",
        "email": "neillz@berea.edu",
        "phoneNumber": "555-555-5555",
        "firstName": "Zach",
        "lastName": "Neill",
        "isStudent": True,
        "isFaculty": False,
        "isCeltsAdmin": False,
        "isCeltsStudentStaff": False
    },

    {
        "username" : "lamichhanes2",
        "bnumber": "B00733993",
        "email": "lamichhanes2@berea.edu",
        "phoneNumber": "555-555-5555",
        "firstName": "Sandesh",
        "lastName":"Lamichhane",
        "isStudent": True,
        "isFaculty": True,
        "isCeltsAdmin": False,
        "isCeltsStudentStaff": False
    },
    {
        "username" : "ayisie",
        "bnumber": "B00739736",
        "email": "ayisie@berea.edu",
        "phoneNumber": "192202903939",
        "firstName": "Ebenezer",
        "lastName":"Ayisi",
        "isStudent": True,
        "isFaculty": False,
        "isCeltsAdmin": False,
        "isCeltsStudentStaff": False

    },
    {
        "username": "agliullovak",
        "bnumber": "B00759117",
        "email": "agliullovak@berea.edu",
        "phoneNumber": "555-555-5555",
        "firstName": "Karina",
        "lastName": "Agliullova",
        "isStudent": True,
        "isFaculty": False,
        "isCeltsAdmin": False,
        "isCeltsStudentStaff": False
    },
    {
        "username": "bryanta",
        "bnumber": "B00708826",
        "email": "bryanta@berea.edu",
        "phoneNumber": "85943311598",
        "firstName": "Alex",
        "lastName": "Bryant",
        "isStudent": True,
    },
    {
        "username": "partont",
        "bnumber": "B00751360",
        "email": "partont@berea.edu",
        "firstName": "Tyler",
        "lastName": "Parton",
        "isStudent": True,
        "phoneNumber": "9119119111"
    },
]

User.insert_many(users).on_conflict_replace().execute()

terms = [
    {
        "id": 1,
        "description": "Spring A 2021",
        "year": 2021,
        "academicYear": "2020-2021",
        "isBreak": False,
        "isSummer": False,
        "isCurrentTerm": False
    },
    {
        "id": 2,
        "description": "Spring B 2021",
        "year": 2021,
        "academicYear": "2020-2021",
        "isBreak": False,
        "isSummer": False,
        "isCurrentTerm": False
    },
    {
        "id": 3,
        "description": "Summer 2021",
        "year": 2021,
        "academicYear": "2020-2021",
        "isBreak": False,
        "isSummer": True,
        "isCurrentTerm": True
    },
    {
        "id": 4,
        "description": "Fall 2021",
        "year": 2021,
        "academicYear": "2021-2022",
        "isBreak": False,
        "isSummer": False,
        "isCurrentTerm": False
    },
    {
        "id": 5,
        "description": "Fall Break 2021",
        "year": 2021,
        "academicYear": "2021-2022",
        "isBreak": True,
        "isSummer": False,
        "isCurrentTerm": False
    },


]
Term.insert_many(terms).on_conflict_replace().execute()

programs = [
    {
        "id": 1,
        "programName": "Empty Bowls",
        "isStudentLed": True,
        "isBonnerScholars": False,
    },
    {
        "id": 2,
        "programName": "Berea Buddies",
        "isStudentLed": True,
        "isBonnerScholars": False,
    },
    {
        "id": 3,
        "programName": "Adopt A Grandparent",
        "isStudentLed": True,
        "isBonnerScholars": False,
    },
    {
        "id": 4,
        "programName": "No Required Events",
        "isStudentLed": False,
        "isBonnerScholars": False,
    },
    {
        "id": 5,
        "programName": "First Year Bonners",
        "isStudentLed": False,
        "isBonnerScholars": True,
    },
    {
        "id": 6,
        "programName": "Habitat For Humanity",
        "isStudentLed": False,
        "isBonnerScholars": False,
    }
]
Program.insert_many(programs).on_conflict_replace().execute()

events = [
    {
        "id": 1,
        "term": 1,
        "eventName": "Empty Bowls Spring",
        "description": "Empty Bowls Spring 2021",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "a big room",
        "startDate": datetime.strptime("2021 10 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 2,
        "term": 1,
        "eventName": "Berea Buddies",
        "description": "Berea Buddies Training",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "a big room",
        "startDate": datetime.strptime("2021 11 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 3,
        "term": 3,
        "eventName": "Adopt",
        "description": "Adopt A Grandparent",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "a big room",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 4,
        "term": 3,
        "eventName": "First Meetup",
        "description": "Berea Buddies First Meetup",
        "isTraining": False,
        "timeStart": datetime.strptime("6:00 am", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 am", "%I:%M %p"),
        "location": "a big room",
        "startDate": datetime.strptime("2021 6 25","%Y %m %d"),
        "endDate": datetime.strptime("2021 6 25","%Y %m %d")
    },
    {
        "id": 5,
        "term": 3,
        "eventName": "Tutoring",
        "description": "Tutoring Training",
        "isTraining": False,
        "timeStart": datetime.strptime("3:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "a bigish room",
        "startDate": datetime.strptime("2021 6 18","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 6,
        "term": 3,
        "eventName": "Making Bowls",
        "description": "Making Bowls Training",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "a big room",
        "startDate": datetime.strptime("2021 08 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 9 12","%Y %m %d")
    },
    {
        "id": 7,
        "term": 3,
        "eventName": "How To Make Buddies",
        "description": "How To Make Buddies Training",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Outisde",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 8,
        "term": 3,
        "eventName": "Adoption",
        "description": "Adoption 101 Training",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "a big room",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 9,
        "term": 3,
        "eventName": "Cleaning Bowls",
        "description": "Cleaning Bowls Training",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Dining Dishes Room",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")

    },
    {
        "id": 10,
        "term": 3,
        "eventName": "Whole Celts Training",
        "description": "Whole Celts Training",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Dining Dishes Room",
        "startDate": datetime.strptime("2021 1 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 6 12","%Y %m %d")
    },
    {
        "id": 11,
        "term": 3,
        "eventName": "Dummy Event",
        "description": "Not a required event",
        "isTraining": False,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Dining Dishes Room",
        "startDate": datetime.strptime("2021 6 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 7 12","%Y %m %d")
    },
    {
        "id": 12,
        "term": 3,
        "eventName": "Random Event",
        "description": "Not a required event",
        "isTraining": False,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Dining Dishes Room",
        "startDate": datetime.strptime("2021 6 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 7 12","%Y %m %d")
    },
    {
        "id": 13,
        "term": 2,
        "eventName": "unaffiliated event",
        "description": "Test event with no program",
        "isTraining": False,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Dining Dishes Room",
        "startDate": datetime.strptime("2021 6 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 7 12","%Y %m %d")
    },
    {
        "id": 14,
        "term": 2,
        "eventName": "All Volunteer Training",
        "description": "testing multiple programs",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "A Big Room",
        "startDate": datetime.strptime("2021 6 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 7 12","%Y %m %d")
    },
    {
        "id": 15,
        "term": 3,
        "eventName": "Event 1",
        "description": "Test for training",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Somewhere",
        "startDate": datetime.strptime("2021 6 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 7 12","%Y %m %d")
    },
]
Event.insert_many(events).on_conflict_replace().execute()

program_events = [
    {
        "event_id": 1,
        "program_id": 1
    },
    {
        "event_id": 2,
        "program_id": 1
    },
    {
        "event_id": 3,
        "program_id": 3
    },
    {
        "event_id": 4,
        "program_id": 2
    },
    {
        "event_id": 5,
        "program_id": 2
    },
    {
        "event_id": 6,
        "program_id": 3
    },
    {
        "event_id": 7,
        "program_id": 1
    },
    {
        "event_id": 8,
        "program_id": 2
    },
    {
        "event_id": 9,
        "program_id": 2
    },
    {
        "event_id": 10,
        "program_id": 3
    },
    {
        "event_id": 11,
        "program_id": 4
    },
    {
        "event_id": 12,
        "program_id": 3
    },

    {
        "event_id": 14,
        "program_id": 5
    },
    {
        "event_id": 14,
        "program_id": 6
    },
]
ProgramEvent.insert_many(program_events).on_conflict_replace().execute()

coursestatus = [
    {
        "status": "Completed"
    },
    {
        "status": "Approved"
    },
    {
        "status": "Pending"
    },
    {
        "status": "Requires Edit"
    }
]
CourseStatus.insert_many(coursestatus).on_conflict_replace().execute()

courses = [
    {
        "id": 1,
        "courseName": "Databases",
        "term": 2,
        "status": 1,
        "courseCredit": "",
        "createdBy": "",
        "isAllSectionsServiceLearning": True,
        "isPermanentlyDesignated": False,
        "sectionBQuestion1": "",
        "sectionBQuestion2": "",
        "sectionBQuestion3": "",
        "sectionBQuestion4": "",
        "sectionBQuestion5": "",
        "sectionBQuestion6": ""
    },
    {
        "id": 2,
        "courseName": "Spanish Help",
        "term": 1,
        "status": 2,
        "courseCredit": "",
        "createdBy": "",
        "isAllSectionsServiceLearning": True,
        "isPermanentlyDesignated": False,
        "sectionBQuestion1": "",
        "sectionBQuestion2": "",
        "sectionBQuestion3": "",
        "sectionBQuestion4": "",
        "sectionBQuestion5": "",
        "sectionBQuestion6": ""

    },
    {
        "id": 3,
        "courseName": "French Help",
        "term": 3,
        "status": 3,
        "courseCredit": "",
        "createdBy": "",
        "isAllSectionsServiceLearning": True,
        "isPermanentlyDesignated": False,
        "sectionBQuestion1": "",
        "sectionBQuestion2": "",
        "sectionBQuestion3": "",
        "sectionBQuestion4": "",
        "sectionBQuestion5": "",
        "sectionBQuestion6": ""

    },
]
Course.insert_many(courses).on_conflict_replace().execute()

courseInstructorRecords = [
    {
        "id": 1,
        "course": 1,
        "user": "ramsayb2"
    },
    {
        "id": 2,
        "course": 2,
        "user": "ramsayb2"
    },
    {
        "id": 3,
        "course": 2,
        "user": "neillz"
    },

]
CourseInstructor.insert_many(courseInstructorRecords).on_conflict_replace().execute()


courseHoursEarned = [
    {
        "course": 1,
        "user": "neillz",
        "hoursEarned": 2.0
    },
    {
        "course": 2,
        "user": "neillz",
        "hoursEarned": 3.0
    },
    {
        "course": 2,
        "user": "khatts",
        "hoursEarned": 4.0
    },
    {
        "course": 2,
        "user": "khatts",
        "hoursEarned": 4.0
    },
    {
        "course": 1,
        "user": "khatts",
        "hoursEarned": 1.0
    },
]
CourseParticipant.insert_many(courseHoursEarned).on_conflict_replace().execute()

eventParticipants = [
    {
        "user": "neillz",
        "event": 2,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 2
    },
    {
        "user": "bryanta",
        "event": 1,
        "rsvp": False,
        "attended": False,
        "hoursEarned": 0
    },
    {
        "user": "neillz",
        "event": 3,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 3
    },
    {
        "user": "neillz",
        "event": 4,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 1
    },
    {
        "user": "neillz",
        "event": 5,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 1
    },
    {
        "user": "neillz",
        "event": 1,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 8,
    },
    {
        "user": "khatts",
        "event": 1,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 3,
    },
    {
        "user": "khatts",
        "event": 3,
        "rsvp": True,
        "attended": False,
        "hoursEarned": 3,
    },
    {
        "user": "khatts",
        "event": 2,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 2,
    },
    {
        "user": "khatts",
        "event": 7,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 3,
    },
    {
        "user": "khatts",
        "event": 5,
        "rsvp": False,
        "attended": True,
        "hoursEarned": 8,
    },
    {
        "user" : "ayisie",
        "event" : "1",
        "rsvp" : True,
        "attended" : False,
        "hoursEarned" : None,
    },
    {
        "user" : "lamichhanes2",
        "event" : "1",
        "rsvp" : True,
        "attended" : True,
        "hoursEarned" : None,

    },
    {
        "user" : "lamichhanes2",
        "event" : "3",
        "rsvp" : True,
        "attended" : True,
        "hoursEarned" : None,
    },
    {
        "user" : "lamichhanes2",
        "event" : "4",
        "rsvp" : True,
        "attended" : True,
        "hoursEarned" : None,

    },
    {
        "user" : "lamichhanes2",
        "event" : "8",
        "rsvp" : False,
        "attended" : True,
        "hoursEarned" : None,
    },
    {
        "user" : "lamichhanes2",
        "event" : "9",
        "rsvp" : False,
        "attended" :True,
        "hoursEarned" : None,
    },
    {
        "user": "agliullovak",
        "event": 3,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 2
    },
    {
        "user": "agliullovak",
        "event": 6,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 1
    },
    {
        "user": "agliullovak",
        "event": 10,
        "rsvp": False,
        "attended": True,
        "hoursEarned": 12
    },
    {
        "user": "partont",
        "event": 1,
        "rsvp": False,
        "attended": True,
        "hoursEarned": 1
    },
    {
        "user": "partont",
        "event": 2,
        "rsvp": False,
        "attended": True,
        "hoursEarned": 5
    },
    {
        "user": "partont",
        "event": 7,
        "rsvp": False,
        "attended": True,
        "hoursEarned": 8
    },
]
EventParticipant.insert_many(eventParticipants).on_conflict_replace().execute()

interest = [

    {
        "program": 1,
        "user": "khatts"
    },
    {
        "program": 1,
        "user": "bryanta"
    },
    {
        "program": 2,
        "user" : "lamichhanes2"
    },
    {
        "program": 3,
        "user": "lamichhanes2"
    },
    {
        "program": 2,
        "user" : "ramsayb2"
    },
    {
        "program": 3,
        "user": "ramsayb2"
    }
]
Interest.insert_many(interest).on_conflict_replace().execute()

bannedUser = [
    {
        "user": "khatts",
        "program": 3,
    },

    {
        "user": "ayisie",
        "program": 1,
    }
]

ProgramBan.insert_many(bannedUser).on_conflict_replace().execute()

facilitators = [

    {
    'user': 'ramsayb2',
    'event': 1
    }
]
Facilitator.insert_many(facilitators).on_conflict_replace().execute()
