from flask import Blueprint, redirect, render_template, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField
from wtforms.fields.html5 import TimeField
from models import Tasks
from app import db
from datetime import datetime

#
bp = Blueprint('tasks', __name__)

# adding tasks for the day
class AddForm(FlaskForm):
    task = TextAreaField('Task', [validators.length(max = 200), validators.DataRequired(message='please enter a task')], render_kw = {"rows": 5, "cols": 30})
    name = StringField('Name', [validators.Length(max = 50), validators.Optional()])
    time= TimeField('Time', [validators.Optional()], format='%H:%M', default=None)
    submit = SubmitField('OK')

# delete tasks 
class DeleteTaskForm(FlaskForm):
    submit = SubmitField('Complete')

#
@bp.route('/board', methods = ['GET', 'POST'])
def board():
    t = Tasks.query.filter_by(name = None)
    if t.first() is None:
        flash('You don\'t have any more tasks today !')
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
        if form.name.data and form.time.data:
            t = Tasks(name = form.name.data, content = form.task.data, time = str(form.time.data))
            URL = url_for('login.temp',check_name= form.name.data)
        elif form.time.data:
            t = Tasks(name = None, content = form.task.data, time = str(form.time.data))
        elif form.name.data:
            t = Tasks(name = form.name.data, content = form.task.data, time = None)
        else:
            t = Tasks(name = None, content = form.task.data, time = None)
        db.session.add(t)
        db.session.commit()
        #
        return redirect(URL)
    return render_template('create.html', form = form)

# delete function for public board
@bp.route('/<int:id>/delete', methods = ['GET','POST'])
def delete(id):
    task = Tasks.query.get(id)
    form = DeleteTaskForm()
    #
    if form.validate_on_submit:
        db.session.delete(task)
        db.session.commit()
        flash('A Task has been completed !')
        return redirect(url_for('tasks.board'))

# delete function for personal board
@bp.route('/<int:id>/personal_delete', methods = ['GET','POST'])
def personal_delete(id):
    task = Tasks.query.get(id)
    form = DeleteTaskForm()
    #
    if form.validate_on_submit:
        db.session.delete(task)
        db.session.commit()
        flash('A Task has been completed')
        return redirect(url_for('login.board'))
