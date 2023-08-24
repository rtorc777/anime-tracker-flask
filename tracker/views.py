from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from tracker.jikan import search_jikan
from tracker.models import Anime_Item, Manga_Item
from tracker import db

views = Blueprint('views', __name__)
headings  = ("Image", "Name", "Rating (?/10)", "Notes", "Options")

@views.route('/')
@views.route('/home')
def home():
    return render_template("home.html")

@views.route('/anime', methods=['GET', 'POST'])
@login_required
def anime():
    anime_data = {}
    list = "Anime List"
    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            list = "Anime (Finished) List:"
            anime_data = Anime_Item.query.filter_by(owner=current_user.id, finished = True).all()
        else:
            list = "Anime (Currently Watching) List:"
            anime_data = Anime_Item.query.filter_by(owner=current_user.id, finished = False).all()
    return render_template("anime.html", anime_data=anime_data, headings=headings, list=list)

@views.route('/manga', methods=['GET', 'POST'])
@login_required
def manga():
    manga_data = {}
    list = "Manga List"
    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            list = "Manga (Finished) List:"
            manga_data = Manga_Item.query.filter_by(owner=current_user.id, finished = True).all()
        else:
            list = "Manga (Currently Watching) List:"
            manga_data = Manga_Item.query.filter_by(owner=current_user.id, finished = False).all()
    return render_template("manga.html", manga_data=manga_data, headings=headings, list=list)

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

            if list == "Finished":
                finished = True
            else:
                finished = False

            if type == "Anime":
                in_list = Anime_Item.query.filter_by(name=name, owner=current_user.id).first()

                if in_list:
                    flash(f'{name} is already in an Anime list', category='danger')
                else:
                    new_item = Anime_Item(image=image, name=name, rating=rating, notes=notes, finished=finished, owner=current_user.id  )
                    db.session.add(new_item)
                    db.session.commit()
                    flash(f'Successfully added {name} to ({type}) {list} list', category='success')
            elif type == "Manga":
                in_list = Manga_Item.query.filter_by(name=name, owner=current_user.id).first()

                if in_list:
                    flash(f'{name} is already in a Manga list', category='danger')
                else:
                    new_item = Manga_Item(image=image, name=name, rating=rating, notes=notes, finished=finished, owner=current_user.id  )
                    db.session.add(new_item)
                    db.session.commit()
                    flash(f'Successfully added {name} to ({type}) {list} list', category='success')

    return render_template("add_item.html", results=results, type=type)
