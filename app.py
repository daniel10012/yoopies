from flask import Flask, jsonify, request, url_for, render_template
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

# mapping to the existing database
class Salary(Base):
    __table__ = Base.metadata.tables['t']
    # Set CODGEO as the primary key
    __mapper_args__ = {
        'primary_key': [Base.metadata.tables['t'].c.CODGEO]
    }

    # add a method to the  model called to_dict(), which returns a Python dictionary to be used for the API
    def to_dict(self):
        data = {
                "CODGEO": self.CODGEO,
                "LIBGEO": self.LIBGEO,
                "Département": self.Département,
                "SNHM14":self.SNHM14,
                "_links": {
                    "self": url_for('get_salary', CODGEO=self.CODGEO),
                    "department": f"/salaries/{self.Département}"     #virtual field
                    }
                }
        return data

    def from_dict(self, data):
        for field in ['CODGEO', 'LIBGEO', 'Département','SNHM14']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def to_collection_dict():
        resources = session.query(Salary).all()
        data = {
            'items': [item.to_dict() for item in resources],
            '_meta': {
                'total_items': len(resources)
            },
        }
        return data


# work with sess
#>>> x = session.query(Salary).filter_by(LIBGEO="Pontoise").all()
# myobject = MyObject('foo', 'bar')
# session.add(myobject)
# session.commit()

# Define endpoints

@app.route('/salaries/<int:CODGEO>', methods=['GET'])
def get_salary(CODGEO):
    return jsonify(session.query(Salary).filter_by(CODGEO=str(CODGEO)).first().to_dict())

@app.route('/salaries', methods=['GET'])
def get_salaries():
    data = Salary.to_collection_dict()
    return jsonify(data)


# Add a salary for a commune
@app.route('/salaries', methods=['POST'])
def create_salary():
    data = request.get_json() or {}
    if 'CODGEO' not in data or 'LIBGEO' not in data or 'Département' not in data or 'SNHM14' not in data:
        return 'must include CODGEO, LIBGEO and Département fields'
    if (session.query(Salary).filter_by(CODGEO=data["CODGEO"]).first() or session.query(Salary).filter_by(LIBGEO=data["LIBGEO"]).first()):
        return 'this commune already exists'
    salary = Salary()
    salary.from_dict(data)
    db.session.add(salary)
    db.session.commit()
    response = jsonify(salary.to_dict())
    # 201 response is standard to show creation of a new ressource, requires a header Location
    response.status_code = 201
    response.headers['Location'] = url_for('get_salary', CODGEO=salary.CODGEO)
    return response

# Edit a commune salary
@app.route('/salaries/<int:CODGEO>', methods=['PUT'])
def update_salary(CODGEO):
    salary = session.query(Salary).filter_by(CODGEO=str(CODGEO)).first()
    data = request.get_json() or {}
    if 'CODGEO' in data and data['CODGEO'] != salary.CODGEO:
        return ('you cannot change the CODGEO')
    salary.from_dict(data)
    db.session.commit()
    return jsonify(salary.to_dict())

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")