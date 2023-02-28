from app import app
from app.models.courseInstructor import CourseInstructor
from app.models.courseStatus import CourseStatus

import csv

class fileMaker:
    '''
    Create the file for the download buttons

    requestedInfo: Query object to be formatted and input to the file as text.
    fileType: Specifies what type of file is going to be made. Currently implemented: (CSV)
    fileFormat (optional): The format of the file, primarily for CSV headers. Type: (dictionary of lists)
    '''
    def __init__(self, designator, requestedInfo, fileType, fileFormat = None):
        self.relativePath = app.config['files']['base_path']
        self.designator = designator
        self.requestedInfo = requestedInfo
        self.fileType = fileType
        self.fileFormat = fileFormat
        self.makeFile(fileType)


    def makeFile(self, fileType):
        '''
        Creates the file
        '''
        try:
            if self.designator == "downloadApprovedCourses":
                if fileType == "CSV":
                    with open(self.relativePath + "/ApprovedCourses.csv", 'w', encoding='utf-8', errors="backslashreplace") as csvfile:
                        self.filewriter = csv.writer(csvfile, delimiter = ',')
                        headers = self.fileFormat.get("headers")
                        self.filewriter.writerow(headers)
                        csvWriteList = []
                        for approvedCourse in self.requestedInfo:
                            csvWriteList = [approvedCourse.courseName, approvedCourse.courseAbbreviation, approvedCourse.instructors, approvedCourse.term.description]
                            self.filewriter.writerow(csvWriteList)
                        return "File Downloaded Created Successfully"

        except Exception as e:
            return e
