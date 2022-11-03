from app import app
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
        self.requestedInfo = requestedInfo
        self.fileType = fileType
        self.fileFormat = fileFormat
        self.makeFile()




    def makeFile(self, fileType):
        '''
        Creates the file
        '''
        if fileType == "CSV":
            with open(self.relativePath, 'w', encoding='utf-8', errors="backslashreplace") as csvfile:
                self.filewriter = csv.writer(csvfile, delimeter = ',',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            formatFile(fileType, requestedInfo, fileFormat)
        return None

    def formatFile(self, fileType, requestedInfo, fileFormat = None):
        """
        Formats the file

        Depending on the file data be will
        """
        headers.extend(fileFormat["headers"])
        self.filewriter.writerow(headers)

        approvedCoursesDict = {}
        for i in requestedInfo:
            approvedCoursesDict.update({i.id:[i.courseName, i.courseAbbreviation]})

        self.filewriter.writerow(approvedCoursesDict.values())

        return None
