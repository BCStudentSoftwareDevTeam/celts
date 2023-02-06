import pytest
import os
from werkzeug.datastructures import FileStorage

from app import app
from app.models.eventFile import EventFile
from app.models.event import Event
from app.logic.fileHandler import FileHandler

# test events
eventFileStorageObject= [FileStorage(filename= "eventfile.pdf")]

handledEventFile = FileHandler(eventFileStorageObject, eventId=15)

# test course
courseFileStorageObject= [FileStorage(filename= "coursefile.pdf")]

handledCourseFile = FileHandler(courseFileStorageObject, courseId=1)
@pytest.mark.integration
def test_getFileFullPath():
    # test event
    filePath = handledEventFile.getFileFullPath(eventFileStorageObject[0])
    assert filePath == 'app/static/files/eventattachments/15/eventfile.pdf'
    
    # test course
    filePath = handledCourseFile.getFileFullPath(courseFileStorageObject[0])
    assert filePath == 'app/static/files/courseattachments/1/coursefile.pdf'


@pytest.mark.integration
def test_saveFiles():
    # test event
    handledEventFile.saveFiles()
    assert EventFile.select().where(EventFile.fileName == 'eventfile.pdf').exists()
    
    # test course
    handledCourseFile.saveFiles()
    assert EventFile.select().where(EventFile.fileName == 'coursefile.pdf').exists()

@pytest.mark.integration
def test_retrievePath():
    # test event
    eventfiles= EventFile.select().where(EventFile.event == 15)
    paths = handledEventFile.retrievePath(eventfiles)
    path = paths["eventfile.pdf"][0]
    assert path =='/static/files/eventattachments/15/eventfile.pdf'

    # test course
    coursefiles= EventFile.select().where(EventFile.course == 1)
    paths = handledCourseFile.retrievePath(coursefiles)
    path = paths["coursefile.pdf"][0]
    assert path =='/static/files/courseattachments/1/coursefile.pdf'

@pytest.mark.integration
def test_deleteFile():
    # test file
    eventfiles= EventFile.select().where(EventFile.event == 15)
    pathDictionary = handledEventFile.retrievePath(eventfiles)
    fileId = pathDictionary["eventfile.pdf"][1]
    path = pathDictionary["eventfile.pdf"][0]
    handledEventFile.deleteFile(fileId)
    assert os.path.exists(path)==False

    # test course
    coursefiles= EventFile.select().where(EventFile.course == 1)
    pathDictionary = handledCourseFile.retrievePath(coursefiles)
    fileId = pathDictionary["coursefile.pdf"][1]
    path = pathDictionary["coursefile.pdf"][0]
    handledCourseFile.deleteFile(fileId)
    assert os.path.exists(path)==False
