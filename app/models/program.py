from app.models import*
from app.models.term import Term
from app.models.courseStatus import CourseStatus
from app.models.partner import Partner

class Program(baseModel):
    programName = CharField()
    partner = ForeignKeyField(Partner, null=True)
    isStudentLed = BooleanField(default=False)
    isBonnerScholars = BooleanField(default=False)
    contactName = CharField()
    contactEmail = CharField()

    @property
    def url(self):
        baseUrl = "https://www.berea.edu/celts/community-service-programs/"
        urls = {1: baseUrl + "hunger-initiatives/",
                2: baseUrl + "volunteer-opportunities/berea-buddies-program/" ,
                3: baseUrl + "volunteer-opportunities/adopt-a-grandparent-program/",
                5: "https://www.berea.edu/celts/bonner-scholars-program/",
                6: baseUrl + "volunteer-opportunities/habitat-for-humanity-program/",
                7: baseUrl + "volunteer-opportunities/teen-mentoring-program/",
                8: baseUrl + "volunteer-opportunities/hispanic-outreach-project/",
                9: baseUrl + "volunteer-opportunities/people-who-care-program/",
                10: baseUrl + "hunger-initiatives/hunger-hurts-food-drive/",
                12: baseUrl + "volunteer-opportunities/berea-tutoring-program/"}
        return urls[self.id]
