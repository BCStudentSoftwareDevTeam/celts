import pytest
from werkzeug.datastructures import FileStorage

from app import app
from app.models.eventFile import EventFile
from app.models.event import Event
from app.logic.fileHandler import FileHandler


fileStorageObject= [FileStorage(filename= "file.pdf")]

handledFile = FileHandler(fileStorageObject)

@pytest.mark.integration
def test_getFileFullPath():
    filePath = handledFile.getFileFullPath(15, fileStorageObject[0])
    assert filePath == 'app/static/files/eventattachments/15/file.pdf'

@pytest.mark.integration
def test_saveFile():
    fileNameList= handledFile.saveFile(15)
    assert EventFile.select().where( EventFile.event == 15, EventFile.fileName == 'file.pdf').exists()
@pytest.mark.integration
def test_retrievePath():
    pass
    # eventfiles= EventFile.select().where(EventFile.event == 15)
    # paths = handledFile.retrievePath(eventfiles)
    # pathFileId = paths[""]
    # # assert paths=={"file.pdf":('/static/files/eventattachments/15/file.pdf',12)}

@pytest.mark.integration
def test_deleteFile():
    pass
