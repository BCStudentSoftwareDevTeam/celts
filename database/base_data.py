from app.models.eventTemplate import EventTemplate
# from app.models.backgroundCheck import BackgroundCheck
from app.models.backgroundCheckType import BackgroundCheckType

print("Inserting base data needed in all environments.")
templates = [
    {
        "id": 1,
        "name": "Single Program",
        "tag": "single-program",
        "templateJSON": "{}",
        "templateFile": "createSingleEvent.html",
        "isVisible": False
    },
    {
        "id": 2,
        "name": "All Volunteer Training",
        "tag": "all-volunteer",
        "templateJSON": '{"name": "All Volunteer Training","description": "Training for all CELTS programs", "isTraining": true, "isService": false, "isRequired": true}',
        "templateFile": "createSingleEvent.html",
        "isVisible": True
    },
    {
        "id": 3,
        "name": "No Program Associated",
        "tag": "no-program",
        "templateJSON": "{}",
        "templateFile": "createSingleEvent.html",
        "isVisible": True
    },
    {
        "id": 4,
        "name": "Student-Led Program Training",
        "tag": "student-led-trainings",
        "templateJSON": '{}',
        "templateFile": "createStudentLedTrainingEvents.html",
        "isVisible": True
    },
]
EventTemplate.insert_many(templates).on_conflict_replace().execute()

backgroundTypes = [
    {
    "id": "CAN",
    "description": "Child Abuse and Neglect",
    },
    {
    "id": "SHS",
    "description": "Safe Hiring Solutions",
    },
    {
    "id": "FBI",
    "description": "Federal Criminal Background",
    },

]
BackgroundCheckType.insert_many(backgroundTypes).on_conflict_replace().execute()
