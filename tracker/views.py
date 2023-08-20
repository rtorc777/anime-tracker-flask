from flask import Blueprint, render_template, request
from flask_login import login_required
from tracker.jikan import data, headings

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template("home.html")

@views.route('/anime')
@login_required
def anime():
    return render_template("anime.html", data=data, headings=headings)

@views.route('/manga')
@login_required
def manga():
    return render_template("manga.html")

@views.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST': 
        type = request.form.get('type_name')
        print(type)
        name = request.form.get('item_name')
        print(name)
    return render_template("add_item.html")
