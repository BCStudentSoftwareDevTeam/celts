from app import app
from app.models.courseInstructor import CourseInstructor
import csv

class fileMaker:
    '''
    Create the file for the download buttons

    requestedInfo: Query object to be formatted and input to the file as text.
    fileType: Specifies what type of file is going to be made. Currently implemented: (CSV)
    fileFormat (optional): The format of the file, primarily for CSV headers. Type: (dictionary of lists)
    '''
    def __init__(self, requestedInfo, fileType, fileFormat = None):
        self.relativePath = app.config['files']['base_path']
        self.completePath = self.relativePath + "/sendRecommendation.csv"
        self.requestedInfo = requestedInfo
        self.fileType = fileType
        self.fileFormat = fileFormat
        self.makeFile(fileType)


    def makeFile(self, fileType):
        '''
        Creates the file
        '''
        try:
            if fileType == "CSV":
                with open(self.completePath, 'w', encoding='utf-8', errors="backslashreplace") as csvfile:
                    self.filewriter = csv.writer(csvfile, delimiter = ',')
                    headers = self.fileFormat.get("headers")
                    self.filewriter.writerow(headers)
                    approvedCoursesDict = {}
                    courseInstructorList = []
                    for i in self.requestedInfo:
                        selectCourseInstructor = CourseInstructor.select(CourseInstructor.user_id).where(CourseInstructor.course_id == i.id)
                        approvedCoursesDict.update({i.id:[i.courseName, i.courseAbbreviation]})
                        if len(selectCourseInstructor) == 1:
                            courseInstructorList.append(selectCourseInstructor[0].user_id)
                            approvedCoursesDict[i.id].append(courseInstructorList)
                        else:
                            for j in range(len(selectCourseInstructor)):
                                courseInstructorList.append(selectCourseInstructor[j].user_id)
                                approvedCoursesDict[i.id].append(courseInstructorList)
                        self.filewriter.writerow(approvedCoursesDict.get(i.id))
                        courseInstructorList.clear()
                return "success!"

        except Exception as e:
            errorMessage = "Format File Fails"
            print(e)

            return errorMessage
