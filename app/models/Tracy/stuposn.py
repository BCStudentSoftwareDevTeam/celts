#THIS IS A TRACY FILE! NO TOUCHY!
from app.models.Tracy import db


class STUPOSN(db.Model):
    __tablename__ = "stuposn"

    POSN_CODE   = db.Column(db.String(128), primary_key=True)           # Unique random ID
    POSN_TITLE  = db.Column(db.String(128))
    WLS         = db.Column(db.String(128))
    ORG         = db.Column(db.String(128))
    ACCOUNT     = db.Column(db.String(128))
    DEPT_NAME   = db.Column(db.String(128))

    def __str__(self):
        return str(self.__dict__)
