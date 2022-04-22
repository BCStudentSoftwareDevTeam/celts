'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''

from datetime import datetime, timedelta
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
from app.models.studentManager import StudentManager
from app.models.emailTemplate import EmailTemplate
from app.models.backgroundCheck import BackgroundCheck
from app.models.matchParticipants import MatchParticipants
from app.models.outsideParticipant import OutsideParticipant
from app.models.adminLogs import AdminLogs


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
        "phoneNumber": "555-985-1234",
        "firstName": "Zach",
        "lastName": "Neill",
        "isStudent": True,
        "isFaculty": False,
        "isCeltsAdmin": False,
        "isCeltsStudentStaff": True
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
        "phoneNumber": "8599858594",
        "isCeltsStudentStaff": True
    },

]

User.insert_many(users).on_conflict_replace().execute()


terms = [
    {
        "id": 1,
        "description": "Fall 2020",
        "year": 2020,
        "academicYear": "2020-2021",
        "isSummer": False,
        "isCurrentTerm": False
    },
    {
        "id": 2,
        "description": "Spring A 2021",
        "year": 2021,
        "academicYear": "2020-2021",
        "isSummer": False,
        "isCurrentTerm": False
    },
    {
        "id": 3,
        "description": "Spring B 2021",
        "year": 2021,
        "academicYear": "2020-2021",
        "isSummer": False,
        "isCurrentTerm": False
    },
    {
        "id": 4,
        "description": "Summer 2021",
        "year": 2021,
        "academicYear": "2020-2021",
        "isSummer": True,
        "isCurrentTerm": True
    },
    {
        "id": 5,
        "description": "Fall 2021",
        "year": 2021,
        "academicYear": "2021-2022",
        "isSummer": False,
        "isCurrentTerm": False
    },
    {
        "id": 6,
        "description": "Spring 2022",
        "year": 2022,
        "academicYear": "2021-2022",
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
        "term": 2,
        "name": "Empty Bowls Spring Event 1",
        "description": "Empty Bowls Spring 2021",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Seabury Center",
        "startDate": datetime.strptime("2021 10 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 2,
        "term": 2,
        "name": "Hunger Hurts",
        "description": "Will donate Food to Community",
        "isTraining": False,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Berea Community School",
        "startDate": datetime.strptime("2021 11 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 3,
        "term": 4,
        "name": "Adoption 101",
        "description": "Lecture on adoption",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Alumni Patio",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 4,
        "term": 4,
        "name": "First Meetup",
        "description": "Berea Buddies First Meetup",
        "isTraining": False,
        "timeStart": datetime.strptime("6:00 am", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 am", "%I:%M %p"),
        "location": "Stephenson Building",
        "startDate": datetime.strptime("2021 6 25","%Y %m %d"),
        "endDate": datetime.strptime("2021 6 25","%Y %m %d")
    },
    {
        "id": 5,
        "term": 4,
        "name": "Tutoring",
        "description": "Tutoring Training",
        "isTraining": False,
        "timeStart": datetime.strptime("3:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Woodspen",
        "startDate": datetime.strptime("2021 6 18","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 6,
        "term": 4,
        "name": "Meet & Greet with Grandparent",
        "description": "Students meet with grandparent for the first time",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Woods-Penniman",
        "startDate": datetime.strptime("2021 08 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 9 12","%Y %m %d")
    },
    {
        "id": 7,
        "term": 4,
        "name": "Empty Bowl with Community",
        "description": "Open to Berea community",
        "isTraining": False,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Berea Community Park",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 8,
        "term": 3,
        "name": "Berea Buddies Second Meeting",
        "description": "Play game to bond with buddy",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Stephenson Building",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")
    },
    {
        "id": 9,
        "term": 3,
        "name": "Field Trip with Buddies",
        "description": "A small trip to Berea Farm",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Berea Farm",
        "startDate": datetime.strptime("2021 12 12","%Y %m %d"),
        "endDate": datetime.strptime("2022 6 12","%Y %m %d")

    },
    {
        "id": 10,
        "term": 1,
        "name": "All Celts Training",
        "description": "Training event for all CELTS programs",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Stephenson Building",
        "startDate": datetime.strptime("2021 1 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 6 12","%Y %m %d")
    },
    {
        "id": 11,
        "term": 4,
        "name": "Celts Admin Meeting",
        "description": "Not a required event",
        "isTraining": False,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Stephenson Building",
        "startDate": datetime.strptime("2021 6 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 7 12","%Y %m %d")
    },
    {
        "id": 12,
        "term": 4,
        "name": "Dinner with Grandparent",
        "description": "Second event with grandparent",
        "isTraining": False,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Boone Tavern",
        "startDate": datetime.strptime("2021 6 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 7 12","%Y %m %d")
    },
    {
        "id": 13,
        "term": 3,
        "name": "Community Clean Up",
        "description": "This event doesn't belong to any program",
        "isTraining": False,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Berea Community Park",
        "startDate": datetime.strptime("2021 6 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 7 12","%Y %m %d")
    },
    {
        "id": 14,
        "term": 1,
        "name": "All Volunteer Training",
        "description": "testing multiple programs",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Woods-Penniman",
        "startDate": datetime.strptime("2021 6 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 7 12","%Y %m %d")
    },
    {
        "id": 15,
        "term": 4,
        "name": "Training Event",
        "description": "Test for training",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Alumni Building",
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
    "noteContent": "I think the training is put in wrong",
    "isPrivate":False
    },
    {
    "createdBy": "mupotsal",
    "createdOn": datetime.strptime("2021 10 12","%Y %m %d"),
    "noteContent": "I agree with your comment on training",
    "isPrivate":False
    }
]

Note.insert_many(notes).on_conflict_replace().execute()
courses = [
    {
        "id": 1,
        "courseName": "Databases",
        "term": 3,
        "status": 1,
        "courseCredit": "",
        "createdBy": "",
        "isAllSectionsServiceLearning": True,
        "isPermanentlyDesignated": False,

    },
    {
        "id": 2,
        "courseName": "Spanish Help",
        "term": 2,
        "status": 2,
        "courseCredit": "",
        "createdBy": "",
        "isAllSectionsServiceLearning": True,
        "isPermanentlyDesignated": False,

    },
    {
        "id": 3,
        "courseName": "French Help",
        "term": 4,
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
    "course":3,
    "questionContent":" This is another random question",
    "questionNumber":4,
    },
    {
    "course":2,
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
        "event": 1,
        "hoursEarned": 2
    },
    {
        "user": "khatts",
        "event": 1,
        "hoursEarned": 2
    },
    {
        "user": "neillz",
        "event": 2,
        "hoursEarned": 2
    },
    {
        "user": "bryanta",
        "event": 5,
        "hoursEarned": 0
    },
    {
        "user": "khatts",
        "event": 3,
        "hoursEarned": 3,
    },
    {
        "user" : "ayisie",
        "event" : 1,
        "hoursEarned" : None,
    },
    {
        "user": "partont",
        "event": 2,
        "hoursEarned": 5
    },
    {
        "user": "khatts",
        "event": 6,
        "hoursEarned": 3,
    },
    {
        "user": "khatts",
        "event": 10,
        "hoursEarned": 3,
    }
]
EventParticipant.insert_many(eventParticipants).on_conflict_replace().execute()

eventRsvp =  [
    {
        "user":"mupotsal",
        "event": 7,
    },
    {
        "user":"khatts",
        "event": 3,
    },
    {
        "user":"agliullovak",
        "event": 6,
    },
    {
        "user":"ayisie",
        "event": 1,
    },
    {
        "user":"bryanta",
        "event": 5,
    },
    {
        "user":"neillz",
        "event": 2,
    },
    {
        "user":"partont",
        "event": 2,
    },
    {
        "user":"lamichhanes2",
        "event": 9,
    }
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
        "endDate": datetime.now() + timedelta(days=360),
        "banNote": 1,
    },

    {
        "user": "ayisie",
        "program": 1,
        "endDate": datetime.now() + timedelta(days=150),
        "banNote": 2,
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

studentManagerPrograms = [
    {
    'user':'khatts',
    'program':1
    },
    {
    'user':'mupotsal',
    'program':2
    },
    {
    'user':'ayisie',
    'program':12
    },
    {
    'user':'neillz',
    'program':'1'
    },
    {
    'user':'neillz',
    'program':12
    }
]

StudentManager.insert_many(studentManagerPrograms).on_conflict_replace().execute()

emailTemplates = [
    {
    'subject': 'Test Email',
    'body': 'Hello {name}, This is a test event named {event_name} located in {location}. Other info: {start_date}-{end_date} and this {start_time}-{end_time}.',
    'action': 'sent',
    'purpose': 'Test',
    'replyToAddress': 'j5u6j9w6v1h0p3g1@bereacs.slack.com'
    },
    {
    'subject': 'Test Email 2',
    'body': 'Hello {name}, This is another test event named {event_name} located in {location}. Other info: {start_date}-{end_date} and this {start_time}-{end_time}. The link is {event_link}',
    'action': 'sent',
    'purpose': 'Test2',
    'replyToAddress': 'j5u6j9w6v1h0p3g1@bereacs.slack.com'
    }
]

EmailTemplate.insert_many(emailTemplates).on_conflict_replace().execute()

background = [
    {
    "user": "khatts",
    "type": "CAN",
    "passBackgroundCheck": False,
    "datePassed": datetime.strptime("2021 10 12","%Y %m %d")
    },
    {
    "user":"mupotsal",
    "type": "SHS",
    "passBackgroundCheck":True,
    "datePassed": datetime.strptime("2021 10 12","%Y %m %d")
    },
]
BackgroundCheck.insert_many(background).on_conflict_replace().execute()


outsideParticipants = [
        {
            "email": "maryjones@example.gmail.com",
            "firstName": "Mary",
            "lastName": "Jones",
            "phoneNumber": "859965452"
        },
        {
            "email": "moorek@example.gmail.com",
            "firstName": "Moore",
            "lastName": "Katelyn",
            "phoneNumber": "859945452"
        },
        {
            "email": "jonesm@example.gmail.com",
            "firstName": "Kacy",
            "lastName": "Madison",
            "phoneNumber": "859978452"
        },
        {
            "email": "gracen@example.gmail.com",
            "firstName": "Grace",
            "lastName": "Nicholas",
            "phoneNumber": "859978452"
        },
        {
            "email": "isaacp@example.gmail.com",
            "firstName": "Isaac",
            "lastName": "White",
            "phoneNumber": "859988452"
        },
        {
            "email": "jefft@example.gmail.com",
            "firstName": "Jefferson",
            "lastName": "Thomas",
            "phoneNumber": "859978452"
        },
]

OutsideParticipant.insert_many(outsideParticipants).on_conflict_replace().execute()

matches = [
    {
    "volunteer": "mupotsal",
    "outsideParticipant": "maryjones@example.gmail.com",
    "event":7
    },
    {
    "volunteer": "ayisie",
    "outsideParticipant": "moorek@example.gmail.com",
    "event":7
    },
    {
    "volunteer":None,
    "outsideParticipant": "jonesm@example.gmail.com",
    "event":7
    },
]
MatchParticipants.insert_many(matches).on_conflict_replace().execute()

logs = [
   {
   "createdBy":"ramsayb2",
   "createdOn": datetime.strptime("2021 12 15","%Y %m %d"),
   "logContent": "Made Liberty Admin."
   },
   {
   "createdBy":"neillz",
   "createdOn": datetime.strptime("2021 12 15","%Y %m %d"),
   "logContent": "Created Adoption Event."
   }
]
AdminLogs.insert_many(logs).on_conflict_replace().execute()
