from app.models import *
from app.models.event import Event
from app.models.bonnerCohort import BonnerCohort

class EventCohort(baseModel):
    event = ForeignKeyField(Event)
    cohort = ForeignKeyField(BonnerCohort)

    class Meta:
        primary_key=CompositeKey('event', 'cohort')
