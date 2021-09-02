from app.models.eventTemplate import EventTemplate

print("Inserting base data needed in all environments.")
templates = [
    {
        "id": 1,
        "name": "Single-Program",
        "templateJSON": "{}",
        "isVisible": False
    },
    {
        "id": 2,
        "name": "All Volunteer Training",
        "templateJSON": "{}",
        "isVisible": True
    },
    {
        "id": 3,
        "name": "No Program Associated",
        "templateJSON": "{}",
        "isVisible": True
    },
    {
        "id": 4,
        "name": "Student-Led Program Training",
        "templateJSON": "{}",
        "isVisible": True
    },
]
EventTemplate.insert_many(templates).on_conflict_replace().execute()
