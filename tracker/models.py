from tracker import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    anime_items = db.relationship('Anime_Item', backref='owned_user', lazy=True)

class Anime_Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    image = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(length=100), nullable=False, unique=True)
    rating = db.Column(db.Integer(), nullable=False)
    more_info = db.Column(db.String(length=1024))
    finished = db.Column(db.Boolean(), nullable = False)
    current_episode = db.Column(db.Integer())
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
