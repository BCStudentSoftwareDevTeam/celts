pem init

#pem add app.models.[filename].[classname]
pem add app.models.course.Course
pem add app.models.term.Term
pem add app.models.courseStatus.CourseStatus

pem watch
pem migrate
