from app.models.event import Event

ids = [276, 277, 303, 548, 549, 557]
for id in ids:
    event = Event.get_by_id(id)
    event.isService = False
    event.save()

ids = [1297, 1298]

for id in ids:
    event = Event.get_by_id(id)
    event.isEngagement = False
    event.save()

