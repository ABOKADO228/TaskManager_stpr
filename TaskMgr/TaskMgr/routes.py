"""
Routes and views for the bottle application.
"""
from bottle import route, view

@route('/')
@view('index')
def home():
    """render the auth_reg page"""
    return dict()

@route('/main')
@view('main/main')
def main():
    return dict()