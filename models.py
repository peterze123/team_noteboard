from app import db
from sqlalchemy import exc
import sys

#
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = True)
    content = db.Column(db.String(200), nullable = False)
    time = db.Column(db.String, nullable = False)
    
    def __repr__(self):
        if self.name is not None:
            return f'{self.content} for {self.name} created on {self.time}'
        else:
            return f'{self.content} created on {self.time}'
# 
def init_db():
    db.drop_all()
    db.create_all()
    # Create a Test Case
    t = Tasks(name = 'Peter', content = 'Get the job done !!!', time = '12:00')
    try:
        db.session.add(t)
        db.session.commit()
    except exc.OperationalError as e:
        sys.exit(e)
    #
    db.session.delete(t)
    db.session.commit()

init_db()