import pytest
import unittest
from app.models.emailLog import EmailLog
from app.logic.tasks import sendEmailTask

@pytest.mark.integration
class TestEmailWorker(unittest.TestCase):
    def setUp(self):
        self.rawFormData = {"templateIdentifier": "Test",
            "programID":"1",
            "eventID":"1",
            "recipientsCategory": "Interested"}

        self.urlDomain = "http://example.com"
        self.sendEmail = sendEmailTask.apply_async(args=[self.rawFormData, self.urlDomain], countdown=5)
        self.result = self.sendEmail.get()
        return(self.sendEmail)

    def test_task_state(self):
        self.assertEqual(self.sendEmail.state, 'SUCCESS')

    def test_task_result(self):
        self.assertEqual(self.result, {'status': True})

    def tearDown(self):
        emailLog = EmailLog.get(EmailLog.event_id==self.rawFormData["eventID"])
        emailLog.delete_instance()
