from app.models import*
from app.models.term import Term
from app.models.courseStatus import CourseStatus

class Program(baseModel):
    programName = CharField()
    instagramUrl = TextField(null=True)
    facebookUrl = TextField(null=True)
    bereaUrl = TextField(null=True)
    programDescription = TextField()
    partner = CharField(null=True)
    isStudentLed = BooleanField(default=False)
    isBonnerScholars = BooleanField(default=False)
    isOtherCeltsSponsored = BooleanField(default=False)
    contactName = CharField(null=True,default='')
    contactEmail = CharField(null=True,default='')
    defaultLocation = CharField(null=True,default='')

    @property
    def url(self):

        return (self.bereaUrl or self.instagramUrl or self.facebookUrl)

    @property
    def description(self):

        return self.programDescription
