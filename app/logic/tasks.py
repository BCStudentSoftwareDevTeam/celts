from app import celery
from app.logic.emailHandler import EmailHandler

#  Connection error solution
#  sudo apt-get install redis-server
#  sudo service redis-server  {start|stop|restart|force-reload|status}

@celery.task(bind=True)
def sendEmailTask(self, raw_form_data, url_domain):
    print("Hello, I exist")
    try:
        print("I am sending an email... maybe")
        mail = EmailHandler(raw_form_data, url_domain)
        print("I am sending an email... maybe")
        mailsent = mail.send_email()
        print(f"mailsent? {mailsent}")
        # self.update_state(state="SUCCESS")
        return {"status": True}
    except Exception as e:
        print("I am not sending an email... maybe")
        return {"status": False, "error": e}
