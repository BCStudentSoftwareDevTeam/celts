'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''

from datetime import *

from app.models.user import User
from app.models.term import Term
from app.models.program import Program
from app.models.event import Event
from app.models.preqForProgram import PreqForProgram
from app.models.user import User
from app.models.interest import Interest

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
        "username": "khatts",
        "bnumber": "B00759107",
        "firstName": "Sreynit",
        "lastName": "Khatt",
        "phoneNumber": "12345678"
    },
    {
            "username": "lamichhanes2",
            "bnumber": "B00733993",
            "firstName": "Sandesh",
            "lastName": "Lamichhane",
            "phoneNumber": "8439743909"
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
        "programName": "Training"
    }
]
Program.insert_many(programs).on_conflict_replace().execute()


events = [
    {
        "id": 1,
        "program": 1,
        "term": 1,
        "description": "Empty Bowls Spring 2021",
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
    },
    {
        "id": 2,
        "program": 4,
        "term": 1,
        "description": "Berea Buddies Training",
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
    },
    {
        "id": 3,
        "program": 3,
        "term": 3,
        "description": "Adopt A Grandparent",
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
    },
    {
        "id": 4,
        "program": 2,
        "term": 3,
        "description": "Berea Buddies First Meetup",
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
    },
    {
        "id": 5,
        "program": 4,
        "term": 3,
        "description": "Tutoring Training",
        "timeStart": "1am",
        "timeEnd": "9pm",
        "location": "a bigish room",
    },
    {
        "id": 6,
        "program": 4,
        "term": 3,
        "description": "Making Bowls Training",
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
    },
    {
        "id": 7,
        "program": 4,
        "term": 3,
        "description": "How To Make Buddies Training",
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "Outisde",
    },
    {
        "id": 8,
        "program": 4,
        "term": 3,
        "description": "Adoption 101 Training",
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
    },
    {
        "id": 9,
        "program": 4,
        "term": 3,
        "description": "Cleaning Bowls Training",
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "Dining Dishes Room",
    },
    {
        "id": 10,
        "program": 4,
        "term": 3,
        "description": "Whole Celts Training",
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "Dining Dishes Room",
    }
]
Event.insert_many(events).on_conflict_replace().execute()

preqForProgram = [
    {
        "program": 1,
        "event": 1
    },
    {
        "program": 1,
        "event": 10
    },
    {
        "program": 2,
        "event": 10
    },
    {
        "program": 2,
        "event": 2
    },
    {
        "program": 3,
        "event": 3
    },
    {
        "program": 1,
        "event": 6
    },
    {
        "program": 1,
        "event": 7
    },
    {
        "program": 3,
        "event": 8
    },
    {
        "program": 1,
        "event": 9
    }

]
PreqForProgram.insert_many(preqForProgram).on_conflict_replace().execute()

interest = [

    {
        "program" : 1,
        "user": "khatts"
    },
    {
        "program": 2,
        "user" : "lamichhanes2"
    },
    {
        "program": 4,
        "user": "lamichhanes2"
    }
]
Interest.insert_many(interest).on_conflict_replace().execute()
