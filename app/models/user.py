from app.models import *



class User(baseModel):
    username = CharField(primary_key = True)
    bnumber = CharField(unique = True)
    email = CharField()
    phoneNumber = CharField(null = True)
    firstName = CharField()
    lastName  = CharField()
    isStudent = BooleanField(default = False)
    major = CharField(null = True)
    classLevel = CharField(null = True)
    isFaculty = BooleanField(default = False)
    isStaff = BooleanField(default = False)
    isCeltsAdmin = BooleanField(default  =False)
    isCeltsStudentStaff = BooleanField(default = False)
    dietRestriction = TextField(null=True)
    minorInterest = BooleanField(default=False)
    minorStatus = CharField(default="No interest")

    # override BaseModel's __init__ so that we can set up an instance attribute for cache
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)

        self._pmCache = {}
        self._bsCache = None
        
    @property
    def isAdmin(self):
        return (self.isCeltsAdmin or self.isCeltsStudentStaff)

    @property
    def isBonnerScholar(self):
        from app.models.bonnerCohort import BonnerCohort
        if self._bsCache is None:
            # TODO should we exclude users who are banned from Bonner here?
            self._bsCache = BonnerCohort.select().where(BonnerCohort.user == self).exists()

        return self._bsCache

    @property
    def fullName(self):
        return f"{self.firstName} {self.lastName}"

    def addProgramManager(self, program):
        # Makes a user a Program Manager
        from app.models.programManager import ProgramManager
        ProgramManager.create(user = self, program = program)

        return (f' {self} added as Program Manager')

    def removeProgramManager(self, program):
        # Removes an existing Program Manager from being a Program Manager
        from app.models.programManager import ProgramManager
        ProgramManager.delete().where(ProgramManager.user == self, ProgramManager.program == program).execute()

        return (f'{self} removed from Program Manager')

    def isProgramManagerFor(self, program):
        # Looks to see who is the Program Manager for a program
        from app.models.programManager import ProgramManager  # Must defer import until now to avoid circular reference
        if not program:
            return False

        if program not in self._pmCache:
            self._pmCache[program] = ProgramManager.select().where(ProgramManager.user == self, ProgramManager.program == program).exists()

        return self._pmCache[program]

    def isProgramManagerForEvent(self, event):
        # Looks to see who the Program Manager for a specific event is
        return self.isProgramManagerFor(event.program)

    