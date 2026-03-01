"""
Routes and views for the bottle application.
"""

from bottle import route, template
from datetime import datetime

@route('/')
@route('/home')
def home():
    return template('main/main', title='Home', year=datetime.now().year)

# @route('/contact')
# @view('contact')
# def contact():
#     """Renders the contact page."""
#     return dict(
#         title='Contact',
#         message='Your contact page.',
#         year=datetime.now().year
#     )

# @route('/about')
# @view('about')
# def about():
#     """Renders the about page."""
#     return dict(
#         title='About',
#         message='Your application description page.',
#         year=datetime.now().year
#     )
