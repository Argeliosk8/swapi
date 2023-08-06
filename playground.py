from models import User
from app import db

u1 = User(name = 'Argelio', email = 'argelio@gmail.com', password = 'adadadsas')
db.session.add(u1)
db.session.commit()