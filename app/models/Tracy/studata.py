#THIS IS A TRACY FILE! NO TOUCHY!
from app.models.Tracy import db


class STUDATA(db.Model):
    __tablename__ = "studata"

    PIDM                    = db.Column(db.String(128), primary_key=True)           # Unique random ID
    ID                      = db.Column(db.String(128)) #B-number
    FIRST_NAME              = db.Column(db.String(128))
    LAST_NAME               = db.Column(db.String(128))
    CLASS_LEVEL             = db.Column(db.String(128))
    ACADEMIC_FOCUS          = db.Column(db.String(128))
    MAJOR                   = db.Column(db.String(128))
    PROBATION               = db.Column(db.String(128))
    ADVISOR                 = db.Column(db.String(128))
    STU_EMAIL               = db.Column(db.String(128))
    STU_CPO                 = db.Column(db.String(128))
    LAST_POSN               = db.Column(db.String(128))
    LAST_SUP_PIDM           = db.Column(db.String(128))

    def __str__(self):
        return str(self.__dict__)
