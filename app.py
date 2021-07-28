import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# initializes the appp
app = Flask(__name__, instance_relative_config = True)
# sets default configurations
app.config.from_mapping(
    # should be overriden in deployment
    SECRET_KEY = 'dev',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
)

# check for the isntance folder
try:
    os.makedirs(app.instance_path)
except FileExistsError:
    pass

# initing the database
db = SQLAlchemy(app)

# applying the blueprints
import tasks
app.register_blueprint(tasks.bp)

import login
app.register_blueprint(login.bp)

app.add_url_rule('/', endpoint = 'tasks.board')

# run the app
if __name__== '__main__':
    app.run(debug = True)