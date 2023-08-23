from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from tracker.jikan import data, headings, search_jikan

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
    results = {}
    type = ""
    if request.method == 'POST':
        if request.form.get('SEARCH') == 'SEARCH':
            type = request.form.get('type_name')
            name = request.form.get('item_name')
            results = search_jikan(type, name)
        
        if request.form.get('SUBMIT') == 'SUBMIT':
            type = request.form.get('type').capitalize()
            name = request.form.get('name')
            image = request.form.get('image')
            list = request.form.get("list")
            rating = request.form.get("rating")
            notes = request.form.get("notes")
            flash(f'Successfully added {name} to ({type}) {list} list', category='success')
        
    return render_template("add_item.html", results=results, type=type)
