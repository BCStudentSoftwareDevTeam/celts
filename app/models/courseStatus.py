from app.models import*

class CourseStatus(baseModel):
    statusID = PrimaryKeyField()
    status = CharField()
