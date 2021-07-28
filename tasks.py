from flask import Blueprint, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField
from models import Tasks
from app import db
from datetime import datetime

#
bp = Blueprint('tasks', __name__)

# adding tasks for the day
class AddForm(FlaskForm):
    task = TextAreaField('Task', [validators.length(max = 200), validators.DataRequired(message='please enter a task')], render_kw = {"rows": 5, "cols": 30})
    name = StringField('Name', [validators.Length(max = 50), validators.Optional()])
    submit = SubmitField('OK')

#
@bp.route('/board', methods = ['GET', 'POST'])
def board():
    t = Tasks.query.filter_by(name = None)
    #
    return render_template('board_public.html', t = t)

#
@bp.route('/create', methods = ['GET','POST'])
def create():
    form = AddForm()
    #
    if form.validate_on_submit():
        URL = url_for('tasks.board')
        #
        if form.name.data:
            t = Tasks(name = form.name.data, content = form.task.data, time = datetime.now().strftime('%H:%M'))
            URL = url_for('login.temp',check_name= form.name.data)
        else:
            t = Tasks(name = None, content = form.task.data, time = datetime.now().strftime('%H:%M'))
        db.session.add(t)
        db.session.commit()
        #
        return redirect(URL)
    return render_template('create.html', form = form)

    