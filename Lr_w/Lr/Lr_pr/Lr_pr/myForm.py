import pdb
from datetime import datetime
from bottle import post, request
import re
import json
import os

JSON_FILE = 'questions.json'


def load_questions():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}


def save_questions(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_valid_question(quest):
    if len(quest) <= 3:
        return False
    if quest.isdigit():
        return False
    return True


@post('/home', method='post')
def my_form():
    mail = request.forms.get('ADRESS', '').strip()
    name = request.forms.get('USERNAME', '').strip()
    quest = request.forms.get('QUEST', '').strip()

    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}$'
    login_pattern = r'^[A-Za-z]{2,50}$'


    if not name or not quest or not mail:
        return '<p style="color:red;">Error: all form fields must be filled in.</p>'


    if not re.match(email_pattern, mail):
        return '<p style="color:red;">Error: invalid email format.</p>'
    if not re.match(login_pattern, name):
        return '<p style="color:red;">Error: invalid login format.</p>'
    if not is_valid_question(quest):
        return '<p style="color:red;">Error: question must be more than 3 characters and cannot consist only of digits.</p>'

    questions_db = load_questions()

    if mail not in questions_db:
        questions_db[mail] = {
            'name': name,
            'questions': []
        }
    else:
        if questions_db[mail]['name'] != name:
            return '<p style="color:red;">Error: email already registered with a different name.</p>'

    if quest in questions_db[mail]['questions']:
        return f'<p style="color:orange;">Warning: This question already exists for user {name}. Question not added as duplicate.</p>'


    questions_db[mail]['questions'].append(quest)

    save_questions(questions_db)

    return f'''
    <p style="color:green;">Thanks, {name}! Your question has been accepted.</p>
    <p><strong>Question:</strong> {quest}</p>
    <p><strong>Email:</strong> {mail}</p>
    <p><strong>Access Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>Total questions from this email:</strong> {len(questions_db[mail]['questions'])}</p>
    '''