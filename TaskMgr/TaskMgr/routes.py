"""
Routes and views for the bottle application.
"""
from bottle import route, view

@route('/')
@view('index')
def home():
    """Renders the home page."""
    return dict()


