from models import Tasks
from flask import Blueprint, url_for, redirect, render_template, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

# initializing the blueprint
bp = Blueprint('login', __name__)

#
class getName(FlaskForm):
    name = StringField('Your Name', [validators.Length(max = 50), validators.DataRequired(message='please enter a name')])
    submit = SubmitField('OK')

# login page, search for name in the db
@bp.route('/login', methods=('GET','POST'))
def index():
    form = getName()
    if form.validate_on_submit():
        tasks = Tasks.query.filter_by(name = form.name.data)
        #
        session.clear()
        session['name'] = form.name.data
        return redirect(url_for('login.board'))
        #
    return render_template('login.html', form = form)

#logged in user, retrieve content with your name
@bp.route('/your_board', methods = ['GET', 'POST'])
def board():
    #
    tasks = Tasks.query.filter_by(name = session.get('name'))
    # when there are no tasks associated with the name
    if tasks.first() is None:
        flash('You don\'t have any more tasks today !')
    return render_template('personal_board.html', t = tasks, name = session.get('name'))

#let the creators checkout a worker's board
@bp.route('/temp_board/<check_name>', methods = ['GET', 'POST'])
def temp(check_name):
    #
    tasks = Tasks.query.filter_by(name = check_name)
    return render_template('personal_board.html', t = tasks, name = check_name)