import pytest
from pytest import raises
from celery.exceptions import Retry
from unittest.mock import patch
from datetime import datetime, timedelta
from app.models.event import Event

from app.logic.tasks import sendEmailTask

import unittest

@pytest.mark.integration
class TestEmailWorker(unittest.TestCase):

    # def __init__(self):
    #     self.raw_form_data = {"templateIdentifier": "Test",
    #         "programID":"1",
    #         "eventID":"1",
    #         "recipientsCategory": "Interested"}
    #
    #     self.url_domain = "1234"
    #     self.event = Event.get_by_id(self.raw_form_data["eventID"])
    #     self.arrivalDate = datetime.utcnow() + timedelta(seconds=5) - timedelta(hours=4)

    def setUp(self):
        self.raw_form_data = {"templateIdentifier": "Test",
            "programID":"1",
            "eventID":"1",
            "recipientsCategory": "Interested"}

        self.url_domain = "1234"
        self.sendEmail = sendEmailTask.apply_async(args=[self.raw_form_data, self.url_domain], countdown=5)
        self.result = self.sendEmail.get()
        return(self.sendEmail)

    def test_task_state(self):
        self.assertEqual(self.sendEmail.state, 'SUCCESS')
        print("email task exists")

    def test_Email(self):
        self.assertEqual(self.result, {'status': True})
        print("task successful")

@pytest.mark.integration
def testTask():
    task1 = TestEmailWorker()
    emailSent = task1.setUp()

    # assert emailSent == {'status': True}

# @pytest.mark.integration
# def testAsync():
#
#     emailSent = task1.task.apply_async(args=[raw_form_data, url_domain], countdown=5).get(timeout=3)
#     print(f"emailSent?: {emailSent}")


def test_success():
    raw_form_data = {"templateIdentifier": "Test",
        "programID":"1",
        "eventID":"1",
        "recipientsCategory": "Interested"}

    url_domain = "1234"
    event = Event.get_by_id(raw_form_data["eventID"])
    arrivalDate = datetime.utcnow() + timedelta(seconds=5) - timedelta(hours=4)
    print("\n arrivalDate", arrivalDate, "\n")

    assert sendEmailTask.apply_async(args=[raw_form_data, url_domain], countdown=5).get(timeout=3) == {"status": True}
