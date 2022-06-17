import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# initializes the appp
app = Flask(__name__, instance_relative_config = True)
# sets default configurations
app.config.from_mapping(
    # should be overriden in deployment
    SECRET_KEY = 'dev',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
)

# initing the database
db = SQLAlchemy(app)


# check for the isntance folder
try:
    os.makedirs(app.instance_path)
except FileExistsError:
    pass

# applying the blueprints
import auth
app.register_blueprint(auth.bp)

import notes
app.register_blueprint(notes.bp)

app.add_url_rule('/', endpoint = 'tasks.board')

# run the app
if __name__== '__main__':
    app.run(debug = True)