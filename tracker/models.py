from tracker import db

class Anime_Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    image = db.Column(db.String)
    name = db.Column(db.String(length=100), nullable=False, unique=True)
    rating = db.Column(db.Integer, nullable=False)
    more_info = db.Column(db.String(length=1024))
    finished = db.Column(db.Boolean, nullable = False)
    current_episode = db.Column(db.Integer)
