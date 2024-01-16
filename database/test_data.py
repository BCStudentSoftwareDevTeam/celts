'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''

from datetime import datetime, timedelta
from app.models.eventRsvp import EventRsvp
from app.models.user import User
from app.models.bonnerCohort import BonnerCohort
from app.models.term import Term
from app.models.program import Program
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
from app.models.note import Note
from app.models.profileNote import ProfileNote
from app.models.programManager import ProgramManager
from app.models.emailTemplate import EmailTemplate
from app.models.backgroundCheck import BackgroundCheck
# from app.models.backgroundCheckType import BackgroundCheckType
from app.models.adminLog import AdminLog
from app.models.emailLog import EmailLog
from app.models.attachmentUpload import AttachmentUpload
from app.models.certification import Certification
from app.models.certificationRequirement import CertificationRequirement
from app.models.celtsLabor import CeltsLabor

print("Inserting data for demo and testing purposes.")
users = [
    {
        "username": "ramsayb2",
        "bnumber": "B00763721",
        "email": "ramsayb2@berea.edu",
        "phoneNumber": "(555)555-5555",
        "firstName": "Brian",
        "lastName": "Ramsay",
        "isStudent": False,
        "isFaculty": False,
        "isStaff": True,
        "isCeltsAdmin": True,
        "isCeltsStudentStaff": False,
        "dietRestriction": "Diary",
        "major": None,
        "classLevel": None,

    },
    {
        "username" : "khatts",
        "bnumber" : "B00759107",
        "email": "khatts@berea.edu",
        "phoneNumber": "(555)555-5555",
        "firstName" : "Sreynit",
        "lastName" : "Khatt",
        "isStudent": True,
        "isFaculty": False,
        "isCeltsAdmin": True,
        "isCeltsStudentStaff": False,
        "major": "Computer Science",
        "classLevel": "Senior",
    },
    {
        "username": "neillz",
        "bnumber": "B00751864",
        "email": "neillz@berea.edu",
        "phoneNumber": "(555)985-1234",
        "firstName": "Zach",
        "lastName": "Neill",
        "isStudent": True,
        "isFaculty": False,
        "isCeltsAdmin": False,
        "isCeltsStudentStaff": True,
        "major": "Psychology",
        "classLevel": "Sophomore",
    },

    {
        "username" : "lamichhanes2",
        "bnumber": "B00733993",
        "email": "lamichhanes2@berea.edu",
        "phoneNumber": "(555)555-5555",
        "firstName": "Sandesh",
        "lastName":"Lamichhane",
        "isStudent": True,
        "isFaculty": True,
        "isCeltsAdmin": False,
        "isCeltsStudentStaff": False,
        "major": None,
        "classLevel": None,
    },
    {
        "username" : "ayisie",
        "bnumber": "B00739736",
        "email": "ayisie@berea.edu",
        "phoneNumber": "(220)290-3939",
        "firstName": "Ebenezer",
        "lastName":"Ayisi",
        "isStudent": True,
        "isFaculty": False,
        "isCeltsAdmin": False,
        "isCeltsStudentStaff": False,
        "major": "Chemistry",
        "classLevel": "Junior",

    },
    {
        "username": "agliullovak",
        "bnumber": "B00759117",
        "email": "agliullovak@berea.edu",
        "phoneNumber": "(555)555-5555",
        "firstName": "Karina",
        "lastName": "Agliullova",
        "isStudent": True,
        "isFaculty": False,
        "isCeltsAdmin": False,
        "isCeltsStudentStaff": False,
        "major": None,
        "classLevel": None,
    },
    {
        "username": "bryanta",
        "bnumber": "B00708826",
        "email": "bryanta@berea.edu",
        "phoneNumber": "(859)433-1159",
        "firstName": "Alex",
        "lastName": "Bryant",
        "isStudent": True,
        "major": "Biology",
        "classLevel": "Senior",
    },
    {
        "username": "partont",
        "bnumber": "B00751360",
        "email": "partont@berea.edu",
        "firstName": "Tyler",
        "lastName": "Parton",
        "isStudent": True,
        "phoneNumber": "(859)433-1559",
        "major": "Computer Science",
        "classLevel": "Senior",
    },
    {
        "username": "mupotsal",
        "bnumber": "B00741640",
        "email": "mupotsal@berea.edu",
        "firstName": "Liberty",
        "lastName": "Mupotsa",
        "isStudent": True,
        "phoneNumber": "(859)463-1159",
        "isCeltsStudentStaff": True,
        "major": None,
        "classLevel": None,
    },
    {
        "username": "heggens",
        "bnumber": "B00765098",
        "email": "heggens@berea.edu",
        "firstName": "Scott",
        "lastName": "Heggen",
        "phoneNumber": "(859)985-5555",
        "isCeltsAdmin": False,
        "isFaculty": True,
        "isCeltsStudentStaff": False,
        "isStaff": True,
        "major": None,
        "classLevel": None,
    },
     {
        "username": "qasema",
        "bnumber": "B00000000",
        "email": "qasema@berea.edu",
        "firstName": "Ala",
        "lastName": "Qasem",
        "phoneNumber": "8599723821",
        "isCeltsAdmin": True,
        "isFaculty": True,
        "isCeltsStudentStaff": False,
        "isStaff": True,
        "major": None,
        "classLevel": None,
    },
    {
        "username": "stettnera2",
        "bnumber": "B00719955",
        "email": "stettnera2@berea.edu",
        "phoneNumber": "(555)555-5555",
        "firstName": "Anderson",
        "lastName": "Stettner",
        "isStudent": False,
        "isFaculty": False,
        "isStaff": True,
        "isCeltsAdmin": True,
        "isCeltsStudentStaff": False,
        "major": None,
        "classLevel": None,
    },
    {
        "username": "bledsoef",
        "bnumber": "B00776544",
        "email": "bledsoef@berea.edu",
        "firstName": "Finn",
        "lastName": "Bledsoe",
        "phoneNumber": "(123)456-7890",
        "isCeltsAdmin": False,
        "isFaculty": True,
        "isCeltsStudentStaff": False,
        "isStaff": True,
    },
]

User.insert_many(users).on_conflict_replace().execute()

bonners = [
    { "year": 2020, "user": "neillz" },
    { "year": 2020, "user": "ramsayb2" },
    { "year": 2021, "user": "qasema" },
    { "year": 2021, "user": "neillz" },
    { "year": 2021, "user": "mupotsal" },
    { "year": 2021, "user": "neillz" },
    { "year": 2021, "user": "ramsayb2" },
    { "year": 2022, "user": "khatts" },
    { "year": 2022, "user": "ayisie" },
    { "year": 2022, "user": "neillz" },
    { "year": 2022, "user": "ramsayb2" },
    ]
BonnerCohort.insert_many(bonners).on_conflict_replace().execute()

certs = [
        { "id": 1, "name": "Bonner" },
        { "id": 2, "name": "CESC Minor" },
        { "id": 3, "name": "CPR" },
        { "id": 4, "name": "Confidentiality" },
        { "id": 5, "name": "I9" },
]
Certification.insert_many(certs).on_conflict_replace().execute()

reqs = [
        { "id": 1,
          "certification": 1,
          "name": "Bonner Orientation",
          "frequency": "once",
          "isRequired": True,
          "order": 1,
        },
        { "id": 2,
          "certification": 1,
          "name": "All Bonner Meeting",
          "frequency": "term",
          "isRequired": True,
          "order": 2,
        },
        { "id": 3,
          "certification": 1,
          "name": "First Year Service Trip",
          "frequency": "once",
          "isRequired": True,
          "order": 3,
        },
        { "id": 4,
          "certification": 1,
          "name": "Sophomore Exchange",
          "frequency": "once",
          "isRequired": True,
          "order": 4,
        },
        { "id": 5,
          "certification": 1,
          "name": "Junior Recommitment",
          "frequency": "once",
          "isRequired": True,
          "order": 5,
        },
        { "id": 6,
          "certification": 1,
          "name": "Senior Legacy Training",
          "frequency": "once",
          "isRequired": True,
          "order": 6,
        },
        { "id": 7,
          "certification": 1,
          "name": "Senior Presentation of Learning",
          "frequency": "once",
          "isRequired": True,
          "order": 7,
        },
        { "id": 8,
          "certification": 1,
          "name": "Bonner Congress",
          "frequency": "once",
          "isRequired": False,
        },
        { "id": 9,
          "certification": 1,
          "name": "Bonner Student Leadership Institute",
          "frequency": "once",
          "isRequired": False,
        },
        { "id": 10,
          "certification": 3,
          "name": "CPR Training",
          "frequency": "once",
          "isRequired": True,
          "order": 2,
        },
        { "id": 11,
          "certification": 3,
          "name": "Volunteer Training",
          "frequency": "once",
          "isRequired": True,
          "order": 1,
        },
]
CertificationRequirement.insert_many(reqs).on_conflict_replace().execute()

terms = [
    {
        "id": 1,
        "description": "Fall 2020",
        "year": 2020,
        "academicYear": "2020-2021",
        "isSummer": False,
        "isCurrentTerm": False,
        "termOrder": "2020-3"
    },
    {
        "id": 2,
        "description": "Spring 2021",
        "year": 2021,
        "academicYear": "2020-2021",
        "isSummer": False,
        "isCurrentTerm": False,
        "termOrder": "2021-1"
    },
    
    {
        "id": 3,
        "description": "Summer 2021",
        "year": 2021,
        "academicYear": "2020-2021",
        "isSummer": True,
        "isCurrentTerm": True,
        "termOrder": "2021-2"
    },
    {
        "id": 4,
        "description": "Fall 2021",
        "year": 2021,
        "academicYear": "2021-2022",
        "isSummer": False,
        "isCurrentTerm": False,
        "termOrder": "2021-3"
    },
    {
        "id": 5,
        "description": "Spring 2022",
        "year": 2022,
        "academicYear": "2021-2022",
        "isSummer": False,
        "isCurrentTerm": False,
        "termOrder": "2022-1"
    },

]
Term.insert_many(terms).on_conflict_replace().execute()

programs = [
    {
        "id": 1,
        "programName": "Hunger Initiatives",
        "programUrl": "https://www.berea.edu/celts/community-service-programs/hunger-initiatives/",
        "programDescription": "Each year 200 people stand in line to get into Woods-Penniman for the Annual Empty Bowls Event sponsored by the Berea College ceramics students and CELTS. Students, faculty, staff and community members each pay $10 for a beautiful bowl, soup and the privilege of helping those in need in our community.",
        "isStudentLed": False,
        "isBonnerScholars": False,
        "isOtherCeltsSponsored": False,
        "contactEmail": "",
        "contactName": ""
    },
    {
        "id": 2,
        "programName": "Berea Buddies",
        "programUrl": "https://www.berea.edu/celts/community-service-programs/volunteer-opportunities/berea-buddies-program/",
        "programDescription": "The Berea Buddies program is dedicated to establishing long-term mentorships between Berea youth (Little Buddies) and Berea College students (Big Buddies). Volunteers serve children by offering them friendship and quality time. Big and Little Buddies meet each other every Monday or Tuesday during the academic year, except on school and national holidays, to enjoy structured activities around campus.",
        "isStudentLed": True,
        "isBonnerScholars": False,
        "isOtherCeltsSponsored": False,
        "contactEmail": "bereabuddies@berea.edu",
        "contactName": ""

    },
    {
        "id": 3,
        "programName": "Adopt-a-Grandparent",
        "programUrl": "https://www.berea.edu/celts/community-service-programs/volunteer-opportunities/adopt-a-grandparent-program/",
        "programDescription": "Adopt-a-Grandparent (AGP) is an outreach program for Berea elders. The program matches college student volunteers with residents of local long-term care centers. Volunteers visit with residents for at least an hour per week, and participate in special monthly programs.",
        "isStudentLed": True,
        "isBonnerScholars": False,
        "isOtherCeltsSponsored": False,
        "contactEmail": "",
        "contactName": ""
    },
    {
        "id": 4,
        "programName": "People Who Care",
        "programUrl": "https://www.berea.edu/celts/community-service-programs/volunteer-opportunities/people-who-care-program/",
        "programDescription":"People Who Care (PWC) helps to connect Berea College students with organizations and opportunities that promote change through advocacy, education, action, and direct community service. Volunteers may serve at local shelters, work with the Fair Trade University Campaign, or help to raise awareness about local issues like domestic violence, homelessness, fair trade, and AIDS awareness education. Students are welcome to participate as volunteers in PWC’s projects.",
        "isStudentLed": True,
        "isBonnerScholars": False,
        "isOtherCeltsSponsored": False,
        "contactEmail": "",
        "contactName": ""
    },
    {
        "id": 5,
        "programName": "Bonner Scholars",
        "programUrl": "https://www.berea.edu/celts/bonner-scholars-program/",
        "programDescription": "The Bonner Scholars Program is a unique opportunity for students who want to combine a strong commitment to service with personal growth, teamwork, leadership development, and scholarship. Students who have completed an application for the Berea College class of 2026 may apply to be a Bonner Scholar.",
        "isStudentLed": False,
        "isBonnerScholars": True,
        "isOtherCeltsSponsored": False,
        "contactEmail": "",
        "contactName": ""
    },
    {
        "id": 6,
        "programName": "Habitat for Humanity",
        "programUrl": "https://www.berea.edu/celts/community-service-programs/volunteer-opportunities/habitat-for-humanity-program/",
        "programDescription": "Through the work of Habitat for Humanity International, thousands of low-income families have found hope through affordable housing. Hard work and volunteering have resulted in the organization sheltering more than two million people worldwide.",
        "isStudentLed": False,
        "isBonnerScholars": False,
        "isOtherCeltsSponsored": False,
        "contactEmail": "",
        "contactName": ""
    },
    {
        "id": 7,
        "programName": "Berea Teen Mentoring",
        "programUrl": "https://www.berea.edu/celts/community-service-programs/volunteer-opportunities/teen-mentoring-program/",
        "programDescription": "Berea Teen Mentoring (BTM) brings Berea community youth, from ages 13-18, into a group setting for mentorship and enrichment programs. Staff members are assisted during the weekly program by Berea College student volunteers, who act as mentors for these program participants. The mission of the program is to stimulate and cultivate personal growth for young adults in the Berea community.",
        "isStudentLed": True,
        "isBonnerScholars": False,
        "isOtherCeltsSponsored": False,
        "contactEmail": "",
        "contactName": ""
    },
    {
        "id": 8,
        "programName": "Hispanic Outreach Program",
        "programUrl": "https://www.berea.edu/celts/community-service-programs/volunteer-opportunities/hispanic-outreach-project/",
        "programDescription": "The Hispanic Outreach Program (HOP) is a service-learning effort which brings together CELTS, several community organizations, and the Department of Foreign Languages at Berea College. HOP aims to build bridges among the Spanish-speaking and English-speaking residents of Madison County.",
        "isStudentLed": True,
        "isBonnerScholars": False,
        "isOtherCeltsSponsored": False,
        "contactEmail": "",
        "contactName": ""
    },
    {
        "id": 9,
        "programName": "CELTS-Sponsored Event",
        "programUrl": "https://www.berea.edu/centers/center-for-excellence-in-learning-through-service",
        "programDescription": "This program hosts a myriad of different celts sponsored events that are not owned by any other program.",
        "isStudentLed": False,
        "isBonnerScholars": False,
        "isOtherCeltsSponsored": True,
        "contactEmail": "",
        "contactName": ""
    },
    {
        "id": 10,
        "programName": "Berea Tutoring",
        "programUrl": "https://www.berea.edu/celts/community-service-programs/volunteer-opportunities/berea-tutoring-program/",
        "programDescription": "Berea Tutoring provides an encouraging atmosphere for local students who need help in achieving academic success, and for college volunteers who want to learn more about teaching or volunteering. Our mission is to increase conceptual understanding in academic subject areas, enrich educational experiences, and build self-confidence by providing college-aged tutors to local school children.",
        "isStudentLed": False,
        "isBonnerScholars": False,
        "isOtherCeltsSponsored": False,
        "contactEmail": "",
        "contactName": ""
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
        "endDate": datetime.strptime("2022 6 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 1
        
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
        "endDate": datetime.strptime("2022 6 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 1
        
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
        "endDate": datetime.strptime("2022 6 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 3
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
        "endDate": datetime.strptime("2021 6 25","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 2
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
        "endDate": datetime.strptime("2022 6 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 2
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
        "endDate": datetime.strptime("2021 9 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 3
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
        "endDate": datetime.strptime("2022 6 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 1
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
        "endDate": datetime.strptime("2022 6 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 2
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
        "endDate": datetime.strptime("2022 6 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 2

    },
    {
        "id": 10,
        "term": 1,
        "name": "Adopt-a-Grandparent Training",
        "description": "Training event for the Adopt-a-Grandparent program.",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Stephenson Building",
        "startDate": datetime.strptime("2021 1 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 6 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 3
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
        "endDate": datetime.strptime("2021 7 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 9
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
        "endDate": datetime.strptime("2021 7 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 3
    },
    {
        "id": 13,
        "term": 3,
        "name": "Community Clean Up",
        "description": "This event doesn't belong to any major program",
        "isTraining": False,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Berea Community Park",
        "startDate": datetime.strptime("2021 6 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 7 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 9
    },
    {
        "id": 14,
        "term": 1,
        "name": "All Volunteer Training",
        "description": "testing multiple programs",
        "isTraining": True,
        "isAllVolunteerTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Woods-Penniman",
        "startDate": datetime.strptime("2021 6 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 7 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 9
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
        "endDate": datetime.strptime("2021 7 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 9
    },
    {
        #Event being created for recurrance events
        "id": 16,
        "term": 4,
        "name": "Training Event",
        "description": "Test for training",
        "isTraining": True,
        "timeStart": datetime.strptime("6:00 pm", "%I:%M %p"),
        "timeEnd": datetime.strptime("9:00 pm", "%I:%M %p"),
        "location": "Alumni Building",
        "startDate": datetime.strptime("2021 6 12","%Y %m %d"),
        "endDate": datetime.strptime("2021 7 12","%Y %m %d"),
        "contactEmail": "testEmail",
        "contactName": "testName",
        "program": 9
    },
]
Event.insert_many(events).on_conflict_replace().execute()

notes = [
    {
        "id": 1,
        "createdBy": "ramsayb2",
        "createdOn": datetime.strptime("2021 10 12","%Y %m %d"),
        "noteContent": "I think the training is put in wrong",
        "isPrivate":False,
        "noteType": "ban"
    },
    {
        "id": 2,
        "createdBy": "mupotsal",
        "createdOn": datetime.strptime("2021 10 12","%Y %m %d"),
        "noteContent": "I agree with your comment on training",
        "isPrivate":False,
        "noteType": "question"
    },
    {
        "id": 3,
        "createdBy": "mupotsal",
        "createdOn": datetime.strptime("2021 10 12","%Y %m %d"),
        "noteContent": "tells bad jokes",
        "isPrivate": True,
        "noteType": "ban"
    },
    {
        "id": 4,
        "createdBy": "neillz",
        "createdOn": datetime.strptime("2021 11 26","%Y %m %d"),
        "noteContent": "Allergic to water",
        "isPrivate": False,
        "noteType": "profile"
    },
    {
        "id": 5,
        "createdBy": "neillz",
        "createdOn": datetime.strptime("2021 11 30","%Y %m %d"),
        "noteContent": "Allergic to food",
        "isPrivate": False,
        "noteType": "profile"
    },
    {
        "id": 6,
        "createdBy": "ramsayb2",
        "createdOn": datetime.strptime("2021 11 30","%Y %m %d"),
        "noteContent": "Run when in sight",
        "isPrivate": False,
        "noteType": "profile"
    }
]
Note.insert_many(notes).on_conflict_replace().execute()

courses = [
    {
        "id": 1,
        "courseName": "Databases",
        "courseAbbreviation": "",
        "term": 3,
        "status": 1,
        "courseCredit": "",
        "createdBy": "ramsayb2",
        "isAllSectionsServiceLearning": True,
        "isPermanentlyDesignated": False,

    },
    {
        "id": 2,
        "courseName": "Spanish Help",
        "courseAbbreviation": "SPN 104",
        "term": 2,
        "status": 2,
        "courseCredit": "",
        "createdBy": "heggens",
        "isAllSectionsServiceLearning": True,
        "isPermanentlyDesignated": False,

    },
    {
        "id": 3,
        "courseName": "Frenchy Help",
        "courseAbbreviation": "FRN 103",
        "term": 3,
        "status": 3,
        "courseCredit": "",
        "createdBy": "ramsayb2",
        "isAllSectionsServiceLearning": True,
        "isPermanentlyDesignated": False,

    },
    {
        "id": 4,
        "courseName": "Testing",
        "courseAbbreviation": "",
        "term": 2,
        "status": 1,
        "courseCredit": "",
        "createdBy": "heggens",
        "isAllSectionsServiceLearning": True,
        "isPermanentlyDesignated": False,

    }
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
    {
        "id": 4,
        "course": 3,
        "user": "heggens"
    },
    {
        "id": 5,
        "course": 4,
        "user": "ramsayb2"
    },
    {
        "id": 6,
        "course": 4,
        "user": "qasema"
    },
    {
        "id": 7,
        "course": 1,
        "user": "bledsoef"
    }

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
    "questionContent":"This is testing for the first question.",
    "questionNumber":1,
    },
    {
    "course":1,
    "questionContent":"This is testing for the second question.",
    "questionNumber":2,
    },
        {
    "course":1,
    "questionContent":"This is testing for the third question.",
    "questionNumber":3,
    },
    {
    "course":1,
    "questionContent":"This is testing for the fourth question.",
    "questionNumber":4,
    },
    {
    "course":1,
    "questionContent":"This is testing for the fifth question.",
    "questionNumber":5,
    },
    {
    "course":1,
    "questionContent":"This is testing for the sixth question.",
    "questionNumber":6,
    },
    {
    "course":2,
    "questionContent":"This is testing for the first question.",
    "questionNumber":1,
    },
    {
    "course":2,
    "questionContent":"This is testing for the second question.",
    "questionNumber":2,
    },
        {
    "course":2,
    "questionContent":"This is testing for the third question.",
    "questionNumber":3,
    },
    {
    "course":2,
    "questionContent":"This is testing for the fourth question.",
    "questionNumber":4,
    },
    {
    "course":2,
    "questionContent":"This is testing for the fifth question.",
    "questionNumber":5,
    },
    {
    "course":2,
    "questionContent":"This is testing for the sixth question.",
    "questionNumber":6,
    },
    {
    "course":3,
    "questionContent":"This is testing for the first question.",
    "questionNumber":1,
    },
    {
    "course":3,
    "questionContent":"This is testing for the second question.",
    "questionNumber":2,
    },
        {
    "course":3,
    "questionContent":"This is testing for the third question.",
    "questionNumber":3,
    },
    {
    "course":3,
    "questionContent":"This is testing for the fourth question.",
    "questionNumber":4,
    },
    {
    "course":3,
    "questionContent":"This is testing for the fifth question.",
    "questionNumber":5,
    },
    {
    "course":3,
    "questionContent":"This is testing for the sixth question.",
    "questionNumber":6,
    },
    {
    "course":4,
    "questionContent":"This is testing for the first question.",
    "questionNumber":1,
    },
    {
    "course":4,
    "questionContent":"This is testing for the second question.",
    "questionNumber":2,
    },
        {
    "course":4,
    "questionContent":"This is testing for the third question.",
    "questionNumber":3,
    },
    {
    "course":4,
    "questionContent":"This is testing for the fourth question.",
    "questionNumber":4,
    },
    {
    "course":4,
    "questionContent":"This is testing for the fifth question.",
    "questionNumber":5,
    },
    {
    "course":4,
    "questionContent":"This is testing for the sixth question.",
    "questionNumber":6,
    },
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
        "banNote": 3,
    }
]

ProgramBan.insert_many(bannedUser).on_conflict_replace().execute()

programManagerPrograms = [
    {
    'user':'khatts',
    'program':1
    },
    {
    'user':'mupotsal',
    'program':2
    },
    {
    'user':'neillz',
    'program':'1'
    },
    {
    'user':'neillz',
    'program':10
    }
]

ProgramManager.insert_many(programManagerPrograms).on_conflict_replace().execute()

emailTemplates = [
    {
    #'id': 1,
    'subject': 'Test Email',
    'body': 'Hello {recipient_name}, This is a test event named {event_name} located in {location}. Other info: {start_date}-{end_date} and this {start_time}-{end_time}.',
    'action': 'sent',
    'purpose': 'Test',
    'replyToAddress': 'j5u6j9w6v1h0p3g1@bereacs.slack.com'
    },
    {
    #'id': 2,
    'subject': 'Test Email 2',
    'body': 'Hello {recipient_name}, This is another test event named {event_name} located in {location}. Other info: {start_date}-{end_date} and this {start_time}-{end_time}. The link is {event_link}',
    'action': 'sent',
    'purpose': 'Test2',
    'replyToAddress': 'j5u6j9w6v1h0p3g1@bereacs.slack.com'
    },
    {
    'subject': 'Event Reminder',
    'body': 'Hello! This is a reminder that you have an event coming up tomorrow, {start_date}. The event is {event_name} and it will be taking place at {location} from {start_time}-{end_time}. The link is {event_link}. The event is scheduled to happen {relative_time} from now.',
    'action': 'sent',
    'purpose': 'Reminder',
    'replyToAddress': 'j5u6j9w6v1h0p3g1@bereacs.slack.com'
    }
]

EmailTemplate.insert_many(emailTemplates).on_conflict_replace().execute()

emailLogs = [
    {
    'event': 5,
    'subject': 'Location Change for {event_name}',
    'templateUsed': 2,
    'recipientsCategory': "RSVP'd",
    'recipients': 'neillz',
    'dateSent': datetime.strptime("2022 5 7","%Y %m %d"),
    'sender': "neillz"
    },
    {
    'event': 5,
    'subject': 'Time Change for {event_name}',
    'templateUsed': 2,
    'recipientsCategory': "RSVP'd",
    'recipients': 'ramsayb2',
    'dateSent': datetime.strptime("2022 6 5","%Y %m %d"),
    'sender': "neillz"
    },
    {
    'event': 5,
    'subject': 'Time Change for {event_name}',
    'templateUsed': 2,
    'recipientsCategory': "RSVP'd",
    'recipients': 'ramsayb2',
    'dateSent': datetime.strptime("2022 5 4","%Y %m %d"),
    'sender': "neillz"
    },
    {
    'event': 4,
    'subject': 'Time Change for {event_name}',
    'templateUsed': 2,
    'recipientsCategory': "RSVP'd",
    'recipients': 'neillz',
    'dateSent': datetime.strptime("2022 5 2","%Y %m %d"),
    'sender': "ramsayb2"
    },
    {
    'event': 3,
    'subject': 'Location Change for {event_name}',
    'templateUsed': 1,
    'recipientsCategory': "Interested",
    'recipients': 'neillz',
    'dateSent': datetime.strptime("2022 6 6","%Y %m %d"),
    'sender': "ramsayb2"
    }
]

EmailLog.insert_many(emailLogs).on_conflict_replace().execute()

background = [
    {
    "user": "khatts",
    "type": "CAN",
    "backgroundCheckStatus": "Passed",
    "dateCompleted": datetime.strptime("2021 10 12","%Y %m %d")
    },
    {
    "user": "mupotsal",
    "type": "SHS",
    "backgroundCheckStatus": "Submitted",
    "dateCompleted": datetime.strptime("2021 10 12","%Y %m %d")
    },
]
BackgroundCheck.insert_many(background).on_conflict_replace().execute()

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
AdminLog.insert_many(logs).on_conflict_replace().execute()

files = [
    {
    "event": 1,
    "fileName":"Map1.pdf"
    },
    {
    "event": 2,
    "fileName" : "adfsfdhqwre_;ldgfk####l;kgfdg.jpg"
    }
]
AttachmentUpload.insert_many(files).on_conflict_replace().execute()

profileNotes = [
    {
        "user": "neillz",
        "note": 4,
        "isBonnerNote": False,
        "viewTier": 2
    },
    {
        "user": "ramsayb2",
        "note": 5,
        "isBonnerNote": False,
        "viewTier": 3
    },
    {
        "user": "partont",
        "note": 6,
        "isBonnerNote": True,
        "viewTier": 1
    }
]
ProfileNote.insert_many(profileNotes).on_conflict_replace().execute()

celtsLabor = [
    {
        "user": "mupotsal",
        "positionTitle": "Habitat For Humanity Cord.",
        "term": 2,
        "isAcademicYear": True
    },
    {
        "user": "ayisie",
        "positionTitle": "Bonner Manager",
        "term": 3,
        "isAcademicYear": False
    }
]
CeltsLabor.insert_many(celtsLabor).on_conflict_replace().execute()