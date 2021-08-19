from app import db
from sqlalchemy import exc
import sys

#
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = True)
    content = db.Column(db.String(2000), nullable = False)
    time = db.Column(db.String, nullable = True)
    
    def __repr__(self):
        if self.name is not None:
            return f'{self.content} for {self.name} to be completed on {self.time}'
        else:
            return f'{self.content} created on {self.time}'
# 
def init_db():
    db.drop_all()
    db.create_all()
    # Create a sample Note for public board and personal board
    t1 = Tasks(content = 'Start the day without any stress!!!')
    t2 = Tasks(name= 'Peter', content = 'Start the day without any stress!!!', time = '12:00')
    try:
        db.session.add(t1)
        db.session.add(t2)
        db.session.commit()
    except exc.OperationalError as e:
        sys.exit(e)

init_db()