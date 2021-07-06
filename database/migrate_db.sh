pem init

#pem add app.models.[filename].[classname]
pem add app.models.course.Course
pem add app.models.term.Term
pem add app.models.courseStatus.CourseStatus
pem add app.models.courseParticipant.CourseParticipant
pem add app.models.emailTemplate.EmailTemplate
pem add app.models.event.Event
pem add app.models.eventParticipant.EventParticipant
pem add app.models.facilitator.Facilitator
pem add app.models.note.Note
pem add app.models.outsideParticipant.OutsideParticipant
pem add app.models.partner.Partner
pem add app.models.program.Program
pem add app.models.user.User
pem add app.models.programBan.ProgramBan
#pem add app.models.programEvent.ProgramEvent

pem watch
pem migrate
