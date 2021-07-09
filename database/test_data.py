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
from app.models.courseInstructor import CourseInstructor
from app.models.courseParticipant import CourseParticipant
from app.models.eventParticipant import EventParticipant
from app.models.interest import Interest

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
    {
        "username": "khatts",
        "bnumber": "B00759107",
        "email": "khatts@berea.edu",
        "phoneNumber": "555-555-5555",
        "firstName": "Sreynit",
        "lastName": "Khatt",
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
        "username": "lamichhanes2",
        "bnumber": "B00733993",
        "email": "lamichhanes2@berea.edu",
        "firstName": "Sandesh",
        "lastName": "Lamichhane",
        "isStudent": True,
        "phoneNumber": "8439743909"
    },
    {
        "username": "bryanta",
        "bnumber": "B00715348",
        "email": "bryanta@berea.edu",
        "firstName": "Alex",
        "lastName": "Bryant",
        "isStudent": True,
        "phoneNumber": "85943311598"
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
    },
    {
        "id": 2,
        "programName": "Berea Buddies",
    },
    {
        "id": 3,
        "programName": "Adopt A Grandparent",
    },

]
Program.insert_many(programs).on_conflict_replace().execute()


events = [
    {
        "id": 1,
        "program": 1,
        "term": 1,
        "eventName": "Empty Bowls Spring",
        "description": "Empty Bowls Spring 2021",
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "a big room",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 2,
        "program": 1,
        "term": 1,
        "eventName": "Berea Buddies",
        "description": "Berea Buddies Training",
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "a big room",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 3,
        "program": 3,
        "term": 3,
        "eventName": "Adopt",
        "description": "Adopt A Grandparent",
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "a big room",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 4,
        "program": 2,
        "term": 3,
        "eventName": "First Meetup",
        "description": "Berea Buddies First Meetup",
        "timeStart": datetime.strptime("6:00 am", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 am", "%I:%M %p"),
        "location": "a big room",
        "startDate": datetime.strptime("2021 6 25","%Y %m %d"),
        "endDate": datetime.strptime("2021 6 25","%Y %m %d")
    },
    {
        "id": 5,
        "program": 2,
        "term": 3,
        "eventName": "Tutoring",
        "description": "Tutoring Training",
        "timeStart": datetime.strptime("3:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "a bigish room",
        "startDate": datetime.strptime("2021 6 18","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 6,
        "program": 3,
        "term": 3,
        "eventName": "Making Bowls",
        "description": "Making Bowls Training",
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "a big room",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 7,
        "program": 1,
        "term": 3,
        "eventName": "How To Make Buddies",
        "description": "How To Make Buddies Training",
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Outisde",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 8,
        "program": 2,
        "term": 3,
        "eventName": "Adoption",
        "description": "Adoption 101 Training",
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "a big room",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 9,
        "program": 2,
        "term": 3,
        "eventName": "Cleaning Bowls",
        "description": "Cleaning Bowls Training",
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Dining Dishes Room",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")

    },
    {
        "id": 10,
        "program": 3,
        "term": 3,
        "eventName": "Whole Celts Training",
        "description": "Whole Celts Training",
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Dining Dishes Room",
        "startDate": datetime.strptime("2021 6 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 7 12","%Y %m %d")
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
CourseInstructor.insert_many(courseInstructorRecords).on_conflict_replace().execute()


courseHoursEarned = [
    {
        "course": Course.get_by_id(1),
        "user": User.get_by_id("neillz"),
        "hoursEarned": 2.0
    },
    {
        "course": Course.get_by_id(2),
        "user": User.get_by_id("neillz"),
        "hoursEarned": 3.0
    },
    {
        "course": Course.get_by_id(2),
        "user": User.get_by_id("khatts"),
        "hoursEarned": 4.0
    },
    {
        "course": Course.get_by_id(2),
        "user": User.get_by_id("khatts"),
        "hoursEarned": 4.0
    },
    {
        "course": Course.get_by_id(1),
        "user": User.get_by_id("khatts"),
        "hoursEarned": 1
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
    {
        "user": User.get_by_id("neillz"),
        "event": 1,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 8,
        },
    {
        "user": User.get_by_id("khatts"),
        "event": 1,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 3,
        },
    {
        "user": User.get_by_id("khatts"),
        "event": 2,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 2,
        },
    {
        "user": User.get_by_id("khatts"),
        "event": 5,
        "rsvp": True,
        "attended": True,
        "hoursEarned": 8,
        },

]
EventParticipant.insert_many(programHoursEarned).on_conflict_replace().execute()

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
