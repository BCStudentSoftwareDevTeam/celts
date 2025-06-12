from app.models import*


class CourseStatus(baseModel):
    status = CharField()
    DRAFT = 1
    SUBMITTED = 2
    APPROVED = 3
    IMPORTED = 4 