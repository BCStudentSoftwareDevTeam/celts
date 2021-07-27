from app.logic.searchStudents import searchVolunteers
from app.controllers.admin import admin_bp
from flask import flash,redirect, url_for
from app.controllers.main import main_bp
from peewee import *


@admin_bp.route('/searchStudents/<query>', methods = ['GET'])
def searchStudents(query):
    '''Accepts user input and queries the database returning results that matches user search'''
    query = query.strip()
    search = query.upper()
    splitSearch = search.split()
    try:
        return searchVolunteers(query)

    except Exception as e:
        return e, 500
