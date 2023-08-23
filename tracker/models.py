from tracker import db, login_manager
from tracker import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    anime_items = db.relationship('Item', backref='owned_user', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
class Item(db.Model):
    type = db.Column(db.Boolean(), nullable = False)
    id = db.Column(db.Integer(), primary_key=True)
    image = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(length=100), nullable=False, unique=True)
    rating = db.Column(db.Integer(), nullable=False)
    notes = db.Column(db.String(length=1024))
    finished = db.Column(db.Boolean(), nullable = False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
