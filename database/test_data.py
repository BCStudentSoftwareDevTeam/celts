'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''

from datetime import *

from app.models.term import Term
from app.models.program import Program
from app.models.event import Event

print("Inserting data for demo and testing purposes.")
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
]
Program.insert_many(programs).on_conflict_replace().execute()


events = [
    {
        "id": 1,
        "term": 1,
        "description": "Empty Bowls Spring 2021",
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
        "program": 1
    },
    {
        "id": 2,
        "term": 1,
        "description": "Berea Buddies Training",
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
        "program": 2
    },
    {
        "id": 3,
        "term": 3,
        "description": "Adopt A Grandparent",
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
        "program": 3
    },
    {
        "id": 4,
        "term": 3,
        "description": "Berea Buddies First Meetup",
        "timeStart": "6pm",
        "timeEnd": "9pm",
        "location": "a big room",
        "program": 2
    },
]
Event.insert_many(events).on_conflict_replace().execute()
