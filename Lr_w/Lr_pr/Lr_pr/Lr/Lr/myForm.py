from datetime import datetime
from bottle import post, request
import re

@post('/home', method='post')
def my_form():
    mail = request.forms.get('ADRESS', '').strip()
    name = request.forms.get('USERNAME', '').strip()
    quest = request.forms.get('QUEST', '').strip()
    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    if not name or not quest or not mail:
        return '<p style="color:red;">Error: all form fields must be filled in.</p>'

    
    if not re.match(email_pattern, mail):
        return '<p style="color:red;">Error: invalid email format.</p>'

    return f'''
    <p>Thanks, {name}! Your question has been accepted.</p>
    <p>Question: {quest}</p>
    <p>Email: {mail}</p>
    <p>Access Date: {datetime.now().strftime('%Y-%m-%d')}</p>
    '''
