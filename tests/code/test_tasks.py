from pytest import raises
from celery.exceptions import Retry
from unittest.mock import patch

from app.logic.tasks import sendEmailTask

class testCelerySendEmail:

    def test_success(self):

        raw_form_data = {"templateIdentifier": "Test",
            "programID":"1",
            "eventID":"1",
            "recipientsCategory": "Interested"}

        event = Event.get_by_id(raw_form_data["eventID"])
        eventDateTime = datetime.combine(event.startDate, event.timeStart)
        arrivalDate = eventDateTime - timedelta(days=1)
        mailSent = sendEmailTask.apply_async(args=[raw_form_data, url_domain], eta=arrivalDate, expires=eventDateTime)

        
