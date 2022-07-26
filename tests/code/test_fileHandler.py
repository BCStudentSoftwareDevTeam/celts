import pytest
from werkzeug.datastructures import FileStorage

from app import app
from app.models.eventFile import EventFile
from app.models.event import Event
from app.logic.fileHandler import FileHandler


fileStorageObject= FileStorage(filename= "alaQ.pdf")

handledFile = FileHandler(fileStorageObject)

@pytest.mark.integration
def test_getFileFullPath():
    filePath = handledFile.getFileFullPath(15, fileStorageObject)
    assert filePath == 'app/static/files/eventattachments/15/alaQ.pdf'

@pytest.mark.integration
def test_saveFile():
    fileNameList= handledFile.saveFile(15)
    for filename in fileNameList:
        testSave = EventFile.select().where(event == 15, fileName == filename)
        assert testSave == True

@pytest.mark.integration
def test_retrievePath():
    pass

@pytest.mark.integration
def test_deleteFile():
    pass
