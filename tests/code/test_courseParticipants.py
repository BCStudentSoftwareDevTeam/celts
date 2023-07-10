
import pytest 
import os
import re
from app.logic.serviceLearningCoursesData import parseUploadedFile, storePreviewParticipants, retrievePreviewParticipants
from openpyxl import workbook


@pytest.mark.integration
def testCourseParticipants():
    expectedDictionary = {
        ('CSC 226', 'Fall 2020'): ['Gaston Jarju', 'Eben Ezer'],
        ('HIS 236', 'Fall 2020'): ['Ali Ramazani', 'Gertrude Mbewe'],
        ('CSC 450', 'Spring 2026'): ['Fleur Gahimbare', 'Isaac Narteh'],
        ('CSC  650', 'Summer 2024'): ['Anh Ngo', 'Claudia Pulido'],
        ('MAT 450', 'May 2025'): ['Alisha Supeidi', 'Erika Arvizu']
        
    }
    print("////////////////////////////////////////////////////////////////")
    testUpload = parseUploadedFile()
    print("////////////////////////////////////////////////////////////////")


    assert expectedDictionary == testUpload



