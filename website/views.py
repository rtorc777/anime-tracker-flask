from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template("home.html")

@views.route('/anime')
def anime():
    return render_template("anime.html")

@views.route('/manga')
def manga():
    return render_template("manga.html")
