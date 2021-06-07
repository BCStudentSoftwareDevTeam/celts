from app.models import*
from app.models.course import Course
from app.models.user import User

class CourseParticipant(baseModel):
    trackedHoursID = PrimaryKeyField()
    course = ForeignKeyField(Course, null=False)
    user = ForeignKeyField(User, null=False)
    hoursEarned = CharField(null=False)
