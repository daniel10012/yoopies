from flask import Flask, jsonify, request, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from secrets import API_KEY
from flask_cors import CORS, cross_origin
import requests
import urllib.request, json
import json
import pprint

# Create a new Flask application
app = Flask(__name__)

# Handle the Cross-origin resource sharing for API calls
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sh14.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# an Engine, which the Session will use for connection resources
engine = create_engine('sqlite:///sh14.db', convert_unicode=True, echo=False, connect_args={'check_same_thread': False})

Base = declarative_base()
Base.metadata.reflect(engine)

# enables query on the model
db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
Base.query = db_session.query_property()

# create a configured "Session" class
Session = sessionmaker(bind=engine, autoflush=False)

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
                "SNHMC14": self.SNHMC14,
                "SNHMP14": self.SNHMP14,
                "SNHME14": self.SNHME14,
                "SNHMO14": self.SNHMO14,
                "SNHMF14": self.SNHMF14,
                "SNHMFC14": self.SNHMFC14,
                "SNHMFP14": self.SNHMFP14,
                "SNHMFE14": self.SNHMFE14,
                "SNHMFO14": self.SNHMFO14,
                "SNHMH14": self.SNHMH14,
                "SNHMHC14": self.SNHMHC14,
                "SNHMHP14": self.SNHMHP14,
                "SNHMHE14": self.SNHMHE14,
                "SNHMHO14": self.SNHMHO14,
                "SNHM1814": self.SNHM1814,
                "SNHM2614": self.SNHM2614,
                "SNHM5014": self.SNHM5014,
                "SNHMF1814": self.SNHMF1814,
                "SNHMF2614": self.SNHMF2614,
                "SNHMF5014": self.SNHMF5014,
                "SNHMH1814": self.SNHMH1814,
                "SNHMH2614": self.SNHMH2614,
                "SNHMH5014": self.SNHMH5014,
                "Geo_Shape":self.Geo_Shape,
                "_links": {
                    "self": url_for('get_salary', CODGEO=self.CODGEO),
                    "department": f"/salaries/{self.Département}"     #virtual field
                    }
                }
        return data

    def from_dict(self, data):
        for field in ['CODGEO', 'LIBGEO', 'Département','SNHM14', 'Geo_Shape', 'SNHMC14', 'SNHMP14', 'SNHME14', 'SNHMO14', 'SNHMF14', 'SNHMFC14', 'SNHMFP14', 'SNHMFE14', 'SNHMFO14', 'SNHMH14', 'SNHMHC14', 'SNHMHP14', 'SNHMHE14', 'SNHMHO14', 'SNHM1814', 'SNHM2614', 'SNHM5014', 'SNHMF1814', 'SNHMF2614', 'SNHMF5014', 'SNHMH1814', 'SNHMH2614', 'SNHMH5014']:
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
@cross_origin()
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

@app.route('/salaries/<int:CODGEO>/Geo_Shape', methods=['GET'])
def get_geo(CODGEO):
    return session.query(Salary).filter_by(CODGEO=str(CODGEO)).first().Geo_Shape

@app.route('/viz', methods=['GET'])
def viz():
    src = "src=https://maps.googleapis.com/maps/api/js?key=" + API_KEY + "&callback=initMap"
    return render_template("viz.html", src=src)


@app.route('/detail', methods=['GET', 'POST'])
def detail():
    if request.method == "POST":
        gender = request.form['gender']
        age = request.form['age']
        profession = request.form['profession']
        department = request.form['department']
        base = "SNHM"
        detail = base + gender + profession + age + "14"
        if detail not in ['SNHM14','SNHMC14', 'SNHMP14', 'SNHME14', 'SNHMO14', 'SNHMF14', 'SNHMFC14', 'SNHMFP14', 'SNHMFE14', 'SNHMFO14', 'SNHMH14', 'SNHMHC14', 'SNHMHP14', 'SNHMHE14', 'SNHMHO14', 'SNHM1814', 'SNHM2614', 'SNHM5014', 'SNHMF1814', 'SNHMF2614', 'SNHMF5014', 'SNHMH1814', 'SNHMH2614', 'SNHMH5014']:
            return "data not available"
        else:
            r = requests.get('http://127.0.0.1:5000/salaries')
            data = r.json()

            salaries = data["items"]
            sum = 0
            count = 0

            if department != "all":
                for salary in salaries:
                    if salary["CODGEO"][:2] == department:
                        try:
                            sum += float(salary[detail])
                        except TypeError:
                            sum += 0
                        count += 1
            else:
                for salary in salaries:
                    try:
                        sum += float(salary[detail])
                    except TypeError:
                        sum += 0
                    count += 1

            average = round(sum/count,2)
            return render_template("result.html", average=average)

    else:
        # Get a list of all departements
        departments = sorted(list(set([CODGEO[0][:2] for CODGEO in session.query(Salary.CODGEO)])))
        return render_template("detail.html", departments=departments)