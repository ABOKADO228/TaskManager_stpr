"""
Routes and views for the bottle application.
"""
from bottle import route, view

@route('/')
@view('main')
def home():
    return dict()