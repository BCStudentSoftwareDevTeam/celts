from app.models.event import Event
from peewee import ForeignKeyField

def fix_event_flags():
    events = Event.select()
    bad_ids = []
    for e in events:
        if not e.checkFlags():
            bad_ids.append(e.id)
            print("####################################")
            for field in e._meta.fields.keys():                
                print(field, ": ", getattr(e, field))
            print("\n\n\n")
    print(bad_ids)

    
fix_event_flags()