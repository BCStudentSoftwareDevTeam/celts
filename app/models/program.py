from app.models import*
from app.models.term import Term
from app.models.courseStatus import CourseStatus
from app.models.partner import Partner

class Program(baseModel):
    programName = CharField()
    partner = ForeignKeyField(Partner, null=True)
    isStudentLed = BooleanField(default=False)
    isBonnerScholars = BooleanField(default=False)
    emailReplyTo = CharField()
    emailSenderName = CharField()

    @property
    def url(self):
        baseUrl = "https://www.berea.edu/celts/community-service-programs/"
        # These are the production id mappings. Don't change
        urls = {
                1: baseUrl + "volunteer-opportunities/adopt-a-grandparent-program/",
                2: baseUrl + "volunteer-opportunities/berea-buddies-program/" ,
                3: baseUrl + "volunteer-opportunities/teen-mentoring-program/",
                4: baseUrl + "volunteer-opportunities/berea-tutoring-program/",
                5: baseUrl + "volunteer-opportunities/habitat-for-humanity-program/",
                6: baseUrl + "volunteer-opportunities/hispanic-outreach-project/",
                7: baseUrl + "volunteer-opportunities/people-who-care-program/",
                8: baseUrl + "hunger-initiatives/empty-bowls-project/",
                9: baseUrl + "hunger-initiatives/hunger-hurts-food-drive/",
                10: "https://www.berea.edu/celts/bonner-scholars-program/",
               }
        if self.id > 10:
            print("We have programs without a URL! It's time to fix this code.")
            return baseUrl

        return urls[self.id]
