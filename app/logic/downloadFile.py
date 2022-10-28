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
        self.fullPath = 'app' + self.relativePath
        self.requestedInfo = requestedInfo
        self.fileType = fileType
        self.fileFormat = fileFormat
        self.makeFile()




    def makeFile(self, fileType):
        '''
        Creates the file
        '''
        if fileType == "CSV"
            formatFile(fileType, requestedInfo, fileFormat)
            pass
        return None

    def formatFile(self, fileType, requestedinfo, fileFormat == None):
        """
        Formats the file

        Depending on the file data be will
        """

        return None

    def inputData():
        """
        Injects data into file
        """

        pass
