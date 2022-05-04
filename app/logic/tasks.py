from app import celery
from app.logic.emailHandler import EmailHandler

@celery.task(bind=True)
def sendEmailTask(self, raw_form_data, url_domain):
    try:
        print("\n\n HELLO THIS IS A PRINT STATEMENT \n\n")
        mail = EmailHandler(raw_form_data, url_domain)
        mailsent = mail.send_email()
        return {"status": True}
    except Exception as e:
        return {"status": False, "error": e}
