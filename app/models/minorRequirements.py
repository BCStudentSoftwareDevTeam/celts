from app.models import*
from app.models.program import Program
from app.models.course import Course

class MinorReqs(baseModel):
    program = ForeignKeyField(Program)
    course = ForeignKeyField(Course)
    otherValue = CharField()
    otherHours = FloatField()
    isSummerExperience = BooleanField(default = False)
