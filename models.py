from flask_sqlalchemy import SQLAlchemy

db =  SQLAlchemy()

class People(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(150), unique = True, nullable = True)
    height = db.Column(db.String(150), unique = False, nullable = True)
    mass = db.Column(db.String(150), unique = False, nullable = True)
    hair_color = db.Column(db.String(150), unique = False, nullable = True)
    skin_color = db.Column(db.String(150), unique = False, nullable = True)
    eye_color = db.Column(db.String(150), unique = False, nullable = True)
    birth_year = db.Column(db.String(150), unique = False, nullable = True)
    gender = db.Column(db.String(150), unique = False, nullable = True)
    homeworld = db.Column(db.String(150), unique = False, nullable = True)
    favorite = db.relationship('Favorites', backref='people', lazy='dynamic', cascade = 'all, delete, delete-orphan')

    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), unique = False, nullable = False)
    rotation_period = db.Column(db.String(100), unique = False, nullable = True)
    orbital_period = db.Column(db.String(100), unique = False, nullable = True)
    diameter = db.Column(db.String(100), unique = False, nullable = True)
    climate = db.Column(db.String(100), unique = False, nullable = True)
    gravity = db.Column(db.String(100), unique = False, nullable = True)
    favorite = db.relationship('Favorites', backref='planet', lazy='dynamic', cascade = 'all, delete, delete-orphan')

    def __repr__(self):
        return '<Planet %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity
        }

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorite = db.relationship('Favorites', backref='user', lazy='dynamic', cascade = 'all, delete, delete-orphan')

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self): 
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }
    

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable = True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable = True)

    def __repr__(self):
        return '<Favorites %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id
        }

