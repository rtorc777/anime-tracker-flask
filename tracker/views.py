from flask import Blueprint, render_template
from flask_login import login_required

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template("home.html")

@views.route('/anime')
@login_required
def anime():
    return render_template("anime.html")

@views.route('/manga')
@login_required
def manga():
    return render_template("manga.html")
