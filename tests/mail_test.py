import pytest
from app import app
from flask_mail import Mail, Message

with app.app_context():
    msg = Message("Test Email", recipients=["j5u6j9w6v1h0p3g1@bereacs.slack.com"],html="<h3>Test</h3>Whooo",sender="support@bereacollege.onmicrosoft.com")
    mail = Mail(app)

    print("Sending")
    mail.send(msg)
    print("Sent")
