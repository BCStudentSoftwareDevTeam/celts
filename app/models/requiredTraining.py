from app.models import *
from app.models.event import Event

class RequiredTraining(baseModel):
    
    event = ForeignKeyField(Event)  # The regular event that requires training
    trainingEvent = ForeignKeyField(Event) # The event that is the required training.
    
    
    