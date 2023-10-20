
#########################################################
# Create a database backup and then migrate the database
#########################################################

if [ "$1" == "backup" ]
then
	# Get credentials
	echo -n "Database/Schema Name: "
	read DB

	echo -n "Application User: "
	read USER

	echo -n "Application Password: "
	read -s PASS
	echo

	CONN="-u $USER"

	BACKUP_DIR="tmp-backups"
	mkdir "$BACKUP_DIR"
	BACKUP_FILE="$BACKUP_DIR/`date +%F`-backup.sql"

	echo -n -e "\nCreating database backup $BACKUP_FILE ... "
	export MYSQL_PWD="$PASS"
	mysqldump $CONN $DB > $BACKUP_FILE
	export MYSQL_PWD=""
	echo -e "done.\n"
fi

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
pem add app.models.adminLog.AdminLog
pem add app.models.attachmentUpload.AttachmentUpload
pem add app.models.emergencyContact.EmergencyContact
pem add app.models.insuranceInfo.InsuranceInfo
pem add app.models.bonnerCohort.BonnerCohort
pem add app.models.certification.Certification
pem add app.models.certificationAttempt.CertificationAttempt
pem add app.models.certificationRequirement.CertificationRequirement
pem add app.models.requirementMatch.RequirementMatch
pem add app.models.eventViews.EventView
pem add app.models.eventRsvpLog.EventRsvpLog
pem add app.models.celtsLabor.CeltsLabor
pem add app.models.communityEngagementRequest.CommunityEngagementRequest

pem watch
pem migrate
