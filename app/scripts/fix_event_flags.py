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

    # NOTE: Any event printed by the above code needs added to the lists below. They would be events that are not in our backed up database, but are in production.



    # The following events were confirmed with CELTS:

    # The rule is: No event that is Labor Only can earn service hours.
    ids = [276, 277, 303, 548, 549, 557] # Cannot be service and training at the same time. Remove service flag
    for id in ids:
        event = Event.get_by_id(id)
        event.isService = False
        event.save()

    # Rule: These events cannot be an engagement and Labor Only. Also confirmed with CELTS.
    ids = [1297, 1298]

    for id in ids:
        event = Event.get_by_id(id)
        event.isEngagement = False
        event.save()



fix_event_flags()