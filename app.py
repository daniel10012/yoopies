from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a new Flask application
app = Flask(__name__)

# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sh14.db'
db = SQLAlchemy(app)

# an Engine, which the Session will use for connection resources
engine = create_engine('sqlite:///sh14.db', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

class Salary(Base):
    __table__ = Base.metadata.tables['t']
    __mapper_args__ = {
        'primary_key': [Base.metadata.tables['t'].c.CODGEO]
    }

# work with sess
#>>> x = session.query(Salary).filter_by(LIBGEO="Pontoise").all()
# myobject = MyObject('foo', 'bar')
# session.add(myobject)
# session.commit()