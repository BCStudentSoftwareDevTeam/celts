from app.models import *


class User(baseModel):
    username = CharField(primary_key=True)
    bnumber = CharField(unique=True)
    email = CharField()
    phoneNumber = CharField()
    firstName = CharField()
    lastName  = CharField()
    isStudent = BooleanField(default=False)
    isFaculty = BooleanField(default=False)
    isStaff = BooleanField(default=False)
    isCeltsAdmin = BooleanField(default=False)
    isCeltsStudentStaff = BooleanField(default=False)

    @property
    def isAdmin(self):
        return (self.isCeltsAdmin or self.isCeltsStudentStaff)

    def addProgramManager(self, program):
        # Makes a user a Program Manager
        from app.models.programManager import ProgramManager

        addManager = ProgramManager.create(user = self, program = program)

        return (f' {self} added as Program Manager')

    def removeProgramManager(self, program):
        # Removes an existing Program Manager from being a Program Manager
        from app.models.programManager import ProgramManager

        removeManager = ProgramManager.delete().where(ProgramManager.user == self, ProgramManager.program == program).execute()

        return (f'{self} removed from Program Manager')

    def isProgramManagerFor(self, program):
        # Looks to see who is the Program Manager for a program
        from app.models.programManager import ProgramManager  # Must defer import until now to avoid circular reference
        return ProgramManager.select().where(ProgramManager.user == self, ProgramManager.program == program).exists()

    def isProgramManagerForEvent(self, event):
        # Looks to see who the Program Manager for a specific event is
        from app.models.event import Event
        from app.models.programManager import ProgramManager

        eventProgramManager = self.isProgramManagerFor(event.singleProgram)

        return eventProgramManager
