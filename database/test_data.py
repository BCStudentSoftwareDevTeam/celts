'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''

from datetime import *
from app.models.eventParticipant import EventParticipant
from app.models.user import User
from app.models.term import Term
from app.models.program import Program
from app.models.event import Event
from app.models.programBan import ProgramBan


print("Inserting data for demo and testing purposes.")
users = [
    {
        "username": "ramsayb2",
        "bnumber": "B000173723",
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
        "isFaculty": False,
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

    }

]
User.insert_many(users).on_conflict_replace().execute()

terms = [
    {
        "id": 1,
        "description": "Spring A 2021",
        "year": 2021,
        "academicYear": "2020-2021",
        "isBreak": False,
        "isSummer": False
    },
    {
        "id": 2,
        "description": "Spring B 2021",
        "year": 2021,
        "academicYear": "2020-2021",
        "isBreak": False,
        "isSummer": False
    },
    {
        "id": 3,
        "description": "Summer 2021",
        "year": 2021,
        "academicYear": "2020-2021",
        "isBreak": False,
        "isSummer": True
    },
    {
        "id": 4,
        "description": "Fall 2021",
        "year": 2021,
        "academicYear": "2021-2022",
        "isBreak": False,
        "isSummer": False
    },
    {
        "id": 5,
        "description": "Fall Break 2021",
        "year": 2021,
        "academicYear": "2021-2022",
        "isBreak": True,
        "isSummer": False
    },

]
Term.insert_many(terms).on_conflict_replace().execute()

programs = [
    {
        "id": 1,
        "programName": "Empty Bowls"
    },
    {
        "id": 2,
        "programName": "Berea Buddies"
    },
    {
        "id": 3,
        "programName": "Adopt A Grandparent"
    },
    {
        "id": 4,
        "programName": "No Required Events"
    },
]
Program.insert_many(programs).on_conflict_replace().execute()


events = [
    {
        "id": 1,
        "program": 1,
        "term": 1,
        "description": "Empty Bowls Spring 2021",
        "isTraining": True,
        "isPrerequisiteForProgram": True,
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
    },
    {
        "id": 2,
        "program": None,
        "term": 1,
        "description": "Berea Buddies Training",
        "isTraining": True,
        "isPrerequisiteForProgram": True,
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
    },
    {
        "id": 3,
        "program": 3,
        "term": 3,
        "description": "Adopt A Grandparent",
        "isTraining": True,
        "isPrerequisiteForProgram": True,
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
    },
    {
        "id": 4,
        "program": 2,
        "term": 3,
        "description": "Berea Buddies First Meetup",
        "isTraining": True,
        "isPrerequisiteForProgram": True,
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
    },
    {
        "id": 5,
        "program": None,
        "term": 3,
        "description": "Tutoring Training",
        "isTraining": True,
        "isPrerequisiteForProgram": True,
        "timeStart": "1am",
        "timeEnd": "9pm",
        "location": "a bigish room",
    },
    {
        "id": 6,
        "program": None,
        "term": 3,
        "description": "Making Bowls Training",
        "isTraining": True,
        "isPrerequisiteForProgram": True,
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
    },
    {
        "id": 7,
        "program": None,
        "term": 3,
        "description": "How To Make Buddies Training",
        "isTraining": True,
        "isPrerequisiteForProgram": True,
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "Outisde",
    },
    {

        "id": 8,
        "program": None,
        "term": 3,
        "description": "Adoption 101 Training",
        "isTraining": True,
        "isPrerequisiteForProgram": True,
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
    },
    {
        "id": 9,
        "program": None,
        "term": 3,
        "description": "Cleaning Bowls Training",
        "isTraining": True,
        "isPrerequisiteForProgram": True,
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "Dining Dishes Room",
    },
    {
        "id": 10,
        "program": 3,
        "term": 3,
        "description": "Whole Celts Training",
        "isTraining": True,
        "isPrerequisiteForProgram": False,
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "Dining Dishes Room",
    },
    {
        "id": 11,
        "program": 4,
        "term": 3,
        "description": "Not a required event",
        "isTraining": False,
        "isPrerequisiteForProgram": False,
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "Dining Dishes Room",
    }
]
Event.insert_many(events).on_conflict_replace().execute()


EventParticipants = [
    {
        "user" : "lamichhanes2",
        "event" : "1",
        "rsvp" : True,
        "attended" : True,
        "hoursEarned" : None,

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
        "event" : "4",
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
]
EventParticipant.insert_many(EventParticipants).on_conflict_replace().execute()

bannedUser = [
    {
        "user": "khatts",
        "program": 1,

    }
]
ProgramBan.insert_many(bannedUser).on_conflict_replace().execute()
