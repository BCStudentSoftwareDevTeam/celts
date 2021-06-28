'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''

from datetime import *

from app.models.user import User
from app.models.term import Term
from app.models.program import Program
from app.models.event import Event
from app.models.course import Course
from app.models.courseStatus import CourseStatus
from app.models.courseInstructors import CourseInstructors
from app.models.courseParticipant import CourseParticipant
from app.models.eventParticipant import EventParticipant

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
        "programName": "Empty Bowls",
        "term": 1
    },
    {
        "id": 2,
        "programName": "Berea Buddies",
        "term": 2
    },
    {
        "id": 3,
        "programName": "Adopt A Grandparent",
        "term": 3
    },
    {
        "id": 4,
        "programName": "Training",
        "term": 4
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

coursestatus = [
    {
        "status": "Approve"
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
]
Course.insert_many(courses).on_conflict_replace().execute()

courseInstructorRecords = [
    {
        "id": 1,
        "course": Course.get_by_id(1),
        "user": User.get_by_id("ramsayb2")
    },
    {
        "id": 2,
        "course": Course.get_by_id(2),
        "user": User.get_by_id("ramsayb2")
    },
]
CourseInstructors.insert_many(courseInstructorRecords).on_conflict_replace().execute()

courseHoursEarned = [
    {
        "course": Course.get_by_id(1),
        "user": User.get_by_id("neillz"),
        "hoursEarned": 2
    },
    {
        "course": Course.get_by_id(2),
        "user": User.get_by_id("neillz"),
        "hoursEarned": 3
    },
]
CourseParticipant.insert_many(courseHoursEarned).on_conflict_replace().execute()

programHoursEarned = [
    {
        "user": User.get_by_id("neillz"),
        "event": 2,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 2
    },
    {
        "user": User.get_by_id("neillz"),
        "event": 3,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 3
    },
    {
        "user": User.get_by_id("neillz"),
        "event": 4,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 1
    },
    {
        "user": User.get_by_id("neillz"),
        "event": 5,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 1
        },
]
EventParticipant.insert_many(programHoursEarned).on_conflict_replace().execute()
