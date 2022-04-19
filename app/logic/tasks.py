from app import celery
from app.logic.emailHandler import EmailHandler

#  Connection error solution
#  sudo apt-get install redis-server
#  sudo service redis-server  {start|stop|restart|force-reload|status}

@celery.task
def dummy(raw_form_data, url_domain):
    try:
        print("\n\n\n\n Hello: ", " CATS \n\n\n\n")
        mail = EmailHandler(raw_form_data, url_domain)
        mail.send_email()
        print("\n\n\n\n Hello: ", mail, "\n\n\n\n")
        return {"status": True}
    except Exception as e:
        print("\n\n\n\n Hello: \n\n\n\n")
        return {"status": False, "error": e}
