from flask import Flask, jsonify
from models import db, People, Planet, Users
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Fullstack2023$@localhost:5432/swapi'
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/mydb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecret'


db.init_app(app)
migrate = Migrate(app, db, render_as_batch=False)
app.app_context().push()


@app.route('/', methods=["GET"])
def index():
    return "Hello World"

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    json = [single.serialize() for single in people]
    return json, 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single(people_id):
    single = People.query.get(people_id)
    return jsonify(single.serialize())

@app.route('/planet', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    json = [planet.serialize() for planet in planets]
    return json, 200

@app.route('/planet/<int:planet_id>', methods = ['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.serialize())

@app.route('/users', methods = ['GET'])
def get_users():
    users = Users.query.all()
    json = [user.serialize() for user in users]
    return json, 200


db.create_all()