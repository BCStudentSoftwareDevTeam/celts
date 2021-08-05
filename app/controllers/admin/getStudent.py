from app.logic.searchStudents import searchVolunteers
from app.controllers.admin import admin_bp
from flask import flash,redirect, url_for, request, abort
from app.controllers.main import main_bp
from peewee import *
from flask import json



@admin_bp.route('/searchStudents/<query>', methods = ['GET'])
def searchStudents(query):
    '''Accepts user input and queries the database returning results that matches user search'''
    query = query.strip()
    search = query.upper()
    splitSearch = search.split()
    searchResults = searchVolunteers(query)
    return json.dumps(searchResults)



@admin_bp.route('/volunteerProfile', methods=['POST'])
def volunteerProfile():
    volunteerName= request.form.copy()
    username = volunteerName['searchStudentsInput'].strip("()")
    user=username.split('(')[-1]
    return redirect(url_for('main.profilePage', username=user))
