import pytest
import os
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
    handledFile.saveFile(15)
    assert EventFile.select().where( EventFile.event == 15, EventFile.fileName == 'file.pdf').exists()

@pytest.mark.integration
def test_retrievePath():
    eventfiles= EventFile.select().where(EventFile.event == 15)
    paths = handledFile.retrievePath(eventfiles, 15)
    path = paths["file.pdf"][0]
    assert path =='/static/files/eventattachments/15/file.pdf'

@pytest.mark.integration
def test_deleteFile():
    eventfiles= EventFile.select().where(EventFile.event == 15)
    pathDictionary = handledFile.retrievePath(eventfiles, 15)
    fileId = pathDictionary["file.pdf"][1]
    path = pathDictionary["file.pdf"][0]
    handledFile.deleteFile(fileId, 15)
    assert os.path.exists(path)==False
    
