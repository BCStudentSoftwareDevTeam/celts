from app.models.eventTemplate import EventTemplate

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
        "templateJSON": "{'name': 'All Volunteer Training'}",
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
        "templateJSON": "{}",
        "templateFile": "createStudentLedTrainingEvents.html",
        "isVisible": True
    },
]
EventTemplate.insert_many(templates).on_conflict_replace().execute()
