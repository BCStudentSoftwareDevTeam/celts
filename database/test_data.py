'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''

from datetime import *
from app.models.eventParticipant import EventParticipant
from app.models.eventRsvp import EventRsvp
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
from app.models.courseQuestion import CourseQuestion
from app.models.questionNote import QuestionNote
from app.models.interest import Interest
from app.models.facilitator import Facilitator
from app.models.note import Note

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
    {
        "username": "mupotsal",
        "bnumber": "B00741640",
        "email": "mupotsal@berea.edu",
        "firstName": "Liberty",
        "lastName": "Mupotsa",
        "isStudent": True,
        "phoneNumber": "8599858594"
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
    {
        "id": 6,
        "description": "Spring 2024",
        "year": 2024,
        "academicYear": "2023-2024",
        "isBreak": False,
        "isSummer": False,
        "isCurrentTerm": False
    },


]
Term.insert_many(terms).on_conflict_replace().execute()

programs = [
    {
        "id": 1,
        "programName": "Empty Bowls",
        "isStudentLed": False,
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
        "id": 5,
        "programName": "Bonners Scholars",
        "isStudentLed": False,
        "isBonnerScholars": True,
    },
    {
        "id": 6,
        "programName": "Habitat For Humanity",
        "isStudentLed": False,
        "isBonnerScholars": False,
    },
    {
        "id": 7,
        "programName": "Berea Teen Mentoring",
        "isStudentLed": True,
        "isBonnerScholars": False,
    },
    {
        "id": 8,
        "programName": "Hispanic Outreach Program",
        "isStudentLed": True,
        "isBonnerScholars": False,
    },
    {
        "id": 9,
        "programName": "People Who Care",
        "isStudentLed": True,
        "isBonnerScholars": False,
    },
    {
        "id": 10,
        "programName": "Food Drive",
        "isStudentLed": False,
        "isBonnerScholars": False,
    },
    {
        "id": 12,
        "programName": "Berea Tutoring",
        "isStudentLed": False,
        "isBonnerScholars": False,
    }
]
Program.insert_many(programs).on_conflict_replace().execute()

events = [
    {
        "id": 1,
        "term": 1,
        "name": "Empty Bowls Spring Event 1",
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
        "name": "Hunger Hurts",
        "description": "Will donate Food to Community",
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
        "name": "Adoption 101",
        "description": "Lecture on adoption",
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
        "name": "First Meetup",
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
        "name": "Tutoring",
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
        "name": "Meet & Greet with Grandparent",
        "description": "Students meet with grandparent for the first time",
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
        "name": "Food Drive",
        "description": "Second event of food donation",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Outisde",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 8,
        "term": 1,
        "name": "Berea Buddies Second Meeting",
        "description": "Play game to bond with buddy",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "a big room",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 9,
        "term": 1,
        "name": "Field Trip with Buddies",
        "description": "A small trip to Berea Farm",
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
        "name": "All Celts Training",
        "description": "Training event for all CELTS programs",
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
        "name": "Dummy Event",
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
        "name": "Dinner with Grandparent",
        "description": "Second event with grandparent",
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
        "name": "unaffiliated event",
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
        "name": "All Volunteer Training",
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
        "name": "Event 1",
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

notes = [
    {
    "createdBy": "ramsayb2",
    "createdOn": datetime.strptime("2021 10 12","%Y %m %d"),
    "noteContent": "This is the content: test",
    "isPrivate":False
    },
    {
    "createdBy": "mupotsal",
    "createdOn": datetime.strptime("2021 10 12","%Y %m %d"),
    "noteContent": " I am not sure aboutr what you mean here: test",
    "isPrivate":False
    }
]

Note.insert_many(notes).on_conflict_replace().execute()
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

courseQuestions = [
    {
    "course":1,
    "questionContent":" Why are you interested in teaching this course?",
    "questionNumber":1,
    },
    {
    "course":1,
    "questionContent":"Is there anything confusing?",
    "questionNumber":2,
    },
    {
    "course":1,
    "questionContent":"How many students willl betaking this course?",
    "questionNumber":3,
    },
    {
    "course":1,
    "questionContent":" This is another random question",
    "questionNumber":4,
    },
    {
    "course":1,
    "questionContent":" Why are you interested in teaching this course?",
    "questionNumber":5,
    }
]

CourseQuestion.insert_many(courseQuestions).on_conflict_replace().execute()

questionNote = [
    {
    "question":1,
    "note":2
    }
]
QuestionNote.insert_many(questionNote).on_conflict_replace().execute()

eventParticipants = [
    {
        "user": "neillz",
        "event": 2,
        "attended": True,
        "hoursEarned": 2
    },
    {
        "user": "bryanta",
        "event": 1,
        "attended": False,
        "hoursEarned": 0
    },
    {
        "user": "neillz",
        "event": 3,
        "attended": True,
        "hoursEarned": 3
    },
    {
        "user": "neillz",
        "event": 4,
        "attended": True,
        "hoursEarned": 1
    },
    {
        "user": "neillz",
        "event": 5,
        "attended": True,
        "hoursEarned": 1
    },
    {
        "user": "neillz",
        "event": 1,
        "attended": True,
        "hoursEarned": 8,
    },
    {
        "user": "khatts",
        "event": 1,
        "attended": True,
        "hoursEarned": 3,
    },
    {
        "user": "khatts",
        "event": 3,
        "attended": False,
        "hoursEarned": 3,
    },
    {
        "user": "khatts",
        "event": 2,
        "attended": True,
        "hoursEarned": 2,
    },
    {
        "user": "khatts",
        "event": 7,
        "attended": True,
        "hoursEarned": 3,
    },
    {
        "user": "khatts",
        "event": 5,
        "attended": True,
        "hoursEarned": 8,
    },
    {
        "user" : "ayisie",
        "event" : "1",
        "attended" : False,
        "hoursEarned" : None,
    },
    {
        "user" : "lamichhanes2",
        "event" : "1",
        "attended" : True,
        "hoursEarned" : None,

    },
    {
        "user" : "lamichhanes2",
        "event" : "3",
        "attended" : True,
        "hoursEarned" : None,
    },
    {
        "user" : "lamichhanes2",
        "event" : "4",
        "attended" : True,
        "hoursEarned" : None,

    },
    {
        "user" : "lamichhanes2",
        "event" : "8",
        "attended" : True,
        "hoursEarned" : None,
    },
    {
        "user" : "lamichhanes2",
        "event" : "9",
        "attended" :True,
        "hoursEarned" : None,
    },
    {
        "user": "agliullovak",
        "event": 3,
        "attended": True,
        "hoursEarned": 2
    },
    {
        "user": "agliullovak",
        "event": 6,
        "attended": True,
        "hoursEarned": 1
    },
    {
        "user": "agliullovak",
        "event": 10,
        "attended": True,
        "hoursEarned": 12
    },
    {
        "user": "partont",
        "event": 1,
        "attended": True,
        "hoursEarned": 1
    },
    {
        "user": "partont",
        "event": 2,
        "attended": True,
        "hoursEarned": 5
    },
    {
        "user": "partont",
        "event": 7,
        "attended": True,
        "hoursEarned": 8
    },

    {
        "user": "mupotsal",
        "event": 7,
        "attended": True,
        "hoursEarned": 8
    },
]
EventParticipant.insert_many(eventParticipants).on_conflict_replace().execute()

eventRsvp =  [
    {
        "user":"mupotsal",
        "event": 7,
    },

]
EventRsvp.insert_many(eventRsvp).on_conflict_replace().execute()
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
