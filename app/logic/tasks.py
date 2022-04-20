from app import celery
from app.logic.emailHandler import EmailHandler

#  Connection error solution
#  sudo apt-get install redis-server
#  sudo service redis-server  {start|stop|restart|force-reload|status}

@celery.task(bind=True)
def sendEmailTask(self, raw_form_data, url_domain):
    try:
        mail = EmailHandler(raw_form_data, url_domain)
        mail.send_email()

        self.update_state(state="SUCCESS")
        return {"status": True}
    except Exception as e:
        return {"status": False, "error": e}
