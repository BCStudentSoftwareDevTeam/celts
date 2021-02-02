import pytest
from app import app
from flask_mail import Mail, Message
from app.config.loadConfig import get_secret_cfg

with app.app_context():
    secret_conf = get_secret_cfg()
    app.config.update(
        MAIL_SERVER=secret_conf['MAIL_SERVER'],
        MAIL_PORT=secret_conf['MAIL_PORT'],
        MAIL_USERNAME= secret_conf['MAIL_USERNAME'],
        MAIL_PASSWORD= secret_conf['MAIL_PASSWORD'],
        MAIL_USE_TLS=secret_conf['MAIL_USE_TLS'],
        MAIL_USE_SSL=secret_conf['MAIL_USE_SSL'],
        MAIL_DEFAULT_SENDER=secret_conf['MAIL_DEFAULT_SENDER'],
        ALWAYS_SEND_MAIL=secret_conf['ALWAYS_SEND_MAIL']
    )

    msg = Message("Test Email", recipients=["j5u6j9w6v1h0p3g1@bereacs.slack.com"],html="<h3>Test</h3>Whooo",sender="support@bereacollege.onmicrosoft.com")
    mail = Mail(app)

    print("Sending")
    mail.send(msg)
    print("Sent")
