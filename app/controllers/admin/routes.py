from flask import request, render_template
from flask import Flask, redirect, flash

from app.controllers.admin import admin_bp

@admin_bp.route('/testing', methods=['GET'])
def testing():
    return "<h1>Hello</h1>"
