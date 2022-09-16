from app.models import*
from app.models.term import Term
from app.models.courseStatus import CourseStatus
from app.models.partner import Partner

class Program(baseModel):
    programName = CharField()
    partner = ForeignKeyField(Partner, null=True)
    isStudentLed = BooleanField(default=False)
    isBonnerScholars = BooleanField(default=False)
    contactName = CharField(null=True,default='')
    contactEmail = CharField(null=True,default='')

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
                8: baseUrl + "hunger-initiatives/",
                10: "https://www.berea.edu/celts/bonner-scholars-program/",
               }
        if self.id not in urls:
            print("We have programs without a URL! It's time to fix this code.")
            return baseUrl

        return urls[self.id]

    @property
    def description(self):
        descriptions = {1: "Adopt-a-Grandparent (AGP) is an outreach program for Berea elders. The program matches college student volunteers with residents of local long-term care centers. Volunteers visit with residents for at least an hour per week, and participate in special monthly programs.",
                        2: "The Berea Buddies program is dedicated to establishing long-term mentorships between Berea youth (Little Buddies) and Berea College students (Big Buddies). Volunteers serve children by offering them friendship and quality time. Big and Little Buddies meet each other every Monday or Tuesday during the academic year, except on school and national holidays, to enjoy structured activities around campus.",
                        3: "Berea Teen Mentoring (BTM) brings Berea community youth, from ages 13-18, into a group setting for mentorship and enrichment programs. Staff members are assisted during the weekly program by Berea College student volunteers, who act as mentors for these program participants. The mission of the program is to stimulate and cultivate personal growth for young adults in the Berea community.",
                        4: "Berea Tutoring provides an encouraging atmosphere for local students who need help in achieving academic success, and for college volunteers who want to learn more about teaching or volunteering. Our mission is to increase conceptual understanding in academic subject areas, enrich educational experiences, and build self-confidence by providing college-aged tutors to local school children.",
                        5: "Through the work of Habitat for Humanity International, thousands of low-income families have found hope through affordable housing. Hard work and volunteering have resulted in the organization sheltering more than two million people worldwide.",
                        6: "The Hispanic Outreach Program (HOP) is a service-learning effort which brings together CELTS, several community organizations, and the Department of Foreign Languages at Berea College. HOP aims to build bridges among the Spanish-speaking and English-speaking residents of Madison County.",
                        7: "People Who Care (PWC) helps to connect Berea College students with organizations and opportunities that promote change through advocacy, education, action, and direct community service. Volunteers may serve at local shelters, work with the Fair Trade University Campaign, or help to raise awareness about local issues like domestic violence, homelessness, fair trade, and AIDS awareness education. Students are welcome to participate as volunteers in PWC’s projects.",
                        8: "Each year 200 people stand in line to get into Woods-Penniman for the Annual Empty Bowls Event sponsored by the Ceramics Pottery Apprenticeship Program and CELTS. Students, faculty, staff and community members each pay $10 for a beautiful bowl, soup and the privilege of helping those in need in our community.",
                        10: "The Bonner Scholars Program is a unique opportunity for students who want to combine a strong commitment to service with personal growth, teamwork, leadership development, and scholarship. Students who have completed an application for the Berea College class of 2026 may apply to be a Bonner Scholar."}
        if self.id not in descriptions:
            print("We have programs without a description! It's time to fix this code.")
            return ""

        return descriptions[self.id]
