from app.models import *


class CourseStatus(baseModel):
    status = CharField()
    INCOMPLETE = 1
    SUBMITTED = 2
    APPROVED = 3
