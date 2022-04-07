from celery import Celery
from app import app
from app.logic.emailHandler import EmailHandler


app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

#  Connection error solution
#  sudo apt-get install redis-server
#  sudo service redis-server  {start|stop|restart|force-reload|status}

@celery.task
def dummy(raw_form_data, url_domain):
    try:
        mail = EmailHandler(raw_form_data, url_domain)
        mail.send_email()
        print("\n\n\n\n Hello: ", mail, "\n\n\n\n")
        return {"status": True}
    except Exception as e:
        return {"status": False, "error": e}
