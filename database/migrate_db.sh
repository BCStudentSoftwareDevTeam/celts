pem init

#pem add app.models.[filename].[classname]
pem add app.models.course.Course
pem add app.models.term.Term
pem add app.models.courseStatus.CourseStatus
pem add app.models.courseParticipant.CourseParticipant
pem add app.models.emailTemplate.EmailTemplate
pem add app.models.event.Event
pem add app.models.eventTemplate.EventTemplate
pem add app.models.eventParticipant.EventParticipant
pem add app.models.interest.Interest
pem add app.models.note.Note
pem add app.models.outsideParticipant.OutsideParticipant
pem add app.models.partner.Partner
pem add app.models.program.Program
pem add app.models.user.User
pem add app.models.programBan.ProgramBan
pem add app.models.courseInstructor.CourseInstructor
pem add app.models.courseQuestion.CourseQuestion
pem add app.models.questionNote.QuestionNote
pem add app.models.profileNote.ProfileNote
pem add app.models.eventRsvp.EventRsvp
pem add app.models.programManager.ProgramManager
pem add app.models.emailLog.EmailLog
pem add app.models.backgroundCheck.BackgroundCheck
pem add app.models.backgroundCheckType.BackgroundCheckType
pem add app.models.adminLogs.AdminLogs
pem add app.models.attachmentUpload.AttachmentUpload
pem add app.models.bonnerCohort.BonnerCohort
pem add app.models.certification.Certification
pem add app.models.certificationAttempt.CertificationAttempt
pem add app.models.certificationRequirement.CertificationRequirement
pem add app.models.requirementMatch.RequirementMatch
pem add app.models.eventViews.EventView

pem watch
pem migrate
