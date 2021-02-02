#THIS IS A TRACY FILE! NO TOUCHY!
from app.models.Tracy import db


class STUSTAFF(db.Model):
    __tablename__ = "stustaff"

    PIDM        = db.Column(db.Integer, primary_key=True)           # Unique random ID
    ID          = db.Column(db.String(128)) # B-number
    FIRST_NAME  = db.Column(db.String(128))
    LAST_NAME   = db.Column(db.String(128))
    EMAIL       = db.Column(db.String(128))
    CPO         = db.Column(db.String(128))
    ORG         = db.Column(db.String(128))
    DEPT_NAME   = db.Column(db.String(128))

    def __str__(self):
        return str(self.__dict__)
