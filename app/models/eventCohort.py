from datetime import datetime
from app.models import*
from app.models.event import Event
from app.models.bonnerCohort import BonnerCohort

class EventCohort(baseModel):
    event = ForeignKeyField(Event)
    year = IntegerField()  
    invited = BooleanField(default=False)
    invited_at = DateTimeField(default=datetime.now)
    
    class Meta:
        indexes = ( (('event', 'year'), True), )

#wouldn't it be more logic to add columns in the bonnerCohort table instead?