from app.models import*

class CourseStatus(baseModel):
    status = CharField()
    IN_PROGRESS = 1
    SUBMITTED = 2
    APPROVED = 3
    IMPORTED = 4 