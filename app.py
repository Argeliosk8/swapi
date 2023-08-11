from flask import Flask, jsonify, request
from models import db, People, Planet, Users, Favorites
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

@app.route('/people/<int:people_id>', methods=['GET', 'DELETE'])
def get_single(people_id):
    if request.method == 'GET':
        single = People.query.get(people_id)
        if single:
            return jsonify(single.serialize())
        else:
            return jsonify({'message': 'character not found'}), 404
        
    if request.method == 'DELETE':
        try:
            single_to_delete = People.query.get(people_id)
            if single_to_delete:
                db.session.delete(single_to_delete)
                db.session.commit()
                return jsonify({'message': 'character deleted'})
            else:
                return jsonify({'message': 'character not found'}), 404
        except:
            db.session.rollback()
            return jsonify({'error': 'An error occurred'}), 500

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

@app.route('/users/<int:user_id>', methods = ['GET'])
def get_user(user_id):
    user = Users.query.get(user_id)
    return jsonify(user.serialize())

@app.route('/users/favorites', methods = ['GET'])
def get_favorites():
    favorites = Favorites.query.filter_by(user_id = 2)
    json = [favorite.serialize() for favorite in favorites]
    return json, 200

@app.route('/favorite/planet/<int:id>', methods = ['POST', 'DELETE'])
def add_favorite_planet(id):
    planet = bool(Favorites.query.filter_by(planet_id = id).first())
    if request.method == 'POST':        
        if planet:
            return jsonify({'message': 'The planet was alerady added to favorites'}), 400              
        else:
            try:
                new_planet_favorite = Favorites(user_id = 2, people_id = None, planet_id = id)
                db.session.add(new_planet_favorite)
                db.session.commit()
                return jsonify({'message': 'new favorite planet added'}), 200
            except:
                db.session.rollback()
                return jsonify({'message': 'there was an error with your request'}), 400
            
    
    if request.method == 'DELETE':
        if planet:
            try:
                fav_planet_to_delete = Favorites.query.filter_by(planet_id = id).first()
                if fav_planet_to_delete:
                    db.session.delete(fav_planet_to_delete)
                    db.session.commit()
                    return jsonify({"message": "the planet was deleted from favorites"}), 200
            except:
                db.session.rollback()
                return jsonify({"message": "planet not found in favorites"})
        else:
            return jsonify({"message": "planet not found"}), 400


@app.route('/favorite/people/<int:id>', methods = ['POST', 'DELETE'])
def add_favorite_people(id):
    character = bool(Favorites.query.filter_by(people_id = id).first())
    if request.method == 'POST':
        if character: 
            return jsonify({'message': 'the character already exists in favorites'})
        else:
            new_people_favorite = Favorites(user_id = 2, people_id = id, planet_id = None)
            db.session.add(new_people_favorite)
            db.session.commit()
            return jsonify({'message': 'new favorite planet added'})
    
    if request.method == 'DELETE':
       if character:
         try:
            fav_people_to_delete = Favorites.query.filter_by(people_id = id).first()            
            db.session.delete(fav_people_to_delete)
            db.session.commit()
            return jsonify({"message": "the character was deleted from favorites"}), 200
         except:
            db.session.rollback()
            return jsonify({"message": "character was not found in favorites"})
       else:
        return jsonify({"message": "character not found"})

db.create_all()