
from app.models.courseStatus import CourseStatus

import os
from peewee import Model, SqliteDatabase, CharField

CourseStatus.insert(status = 'Draft').execute()

