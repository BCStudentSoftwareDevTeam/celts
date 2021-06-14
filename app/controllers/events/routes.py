from flask import request, render_template
from flask import Flask, redirect, flash

from app.controllers.events import events_bp

@events_bp.route('/events', methods=['GET'])
def events():
    return "<h1>Event List</h1>"
