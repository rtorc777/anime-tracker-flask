from flask import Blueprint, render_template, request, flash, redirect, url_for, json
from flask_login import login_required, current_user
from tracker.jikan import search_jikan
from tracker.models import Anime_Item, Manga_Item
from tracker import db

views = Blueprint('views', __name__)
headings  = ("Image", "Name", "Rating (?/10)", "Notes", "Options")

@views.route('/')
@views.route('/home')
def home():
    stats = {}
    stats["anime_total_count"] = Anime_Item.query.filter_by(owner=current_user.id).count()
    stats["anime_finished_count"] = Anime_Item.query.filter_by(owner=current_user.id, finished = True).count()
    stats["anime_watching_count"] = Anime_Item.query.filter_by(owner=current_user.id, finished = False).count()
    stats["manga_total_count"] = Manga_Item.query.filter_by(owner=current_user.id).count()
    stats["manga_finished_count"] = Manga_Item.query.filter_by(owner=current_user.id, finished = True).count()
    stats["manga_watching_count"] = Manga_Item.query.filter_by(owner=current_user.id, finished = False).count()

    anime_ratings = []
    for i in range(1, 11):
        anime_ratings.append(Anime_Item.query.filter_by(owner=current_user.id, rating=i).count())
    
    manga_ratings = []
    for i in range(1, 11):
        manga_ratings.append(Manga_Item.query.filter_by(owner=current_user.id, rating=i).count())

    #Add average score and buttons
    return render_template("home.html", stats=stats, anime_ratings=anime_ratings, manga_ratings=manga_ratings)

@views.route('/anime', methods=['GET', 'POST'])
@login_required
def anime():
    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.anime_finished'))
        else:
            return redirect(url_for('views.anime_currently_watching'))
    return render_template("anime.html")

@views.route('/anime/currently_watching', methods=['GET', 'POST'])
@login_required
def anime_currently_watching():
    anime_data = {}
    type = "Anime"
    list = "(Currently Watching)"
    anime_data = Anime_Item.query.filter_by(owner=current_user.id, finished = False).all()

    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.anime_finished'))
        else:
            return redirect(url_for('views.anime_currently_watching'))
        
    return render_template("anime.html", anime_data=anime_data, headings=headings, list=list, visible=True, type=type)

@views.route('/anime/finished', methods=['GET', 'POST'])
@login_required
def anime_finished():
    anime_data = {}
    type = "Anime"
    list = "(Finished)"
    anime_data = Anime_Item.query.filter_by(owner=current_user.id, finished = True).all()

    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.anime_finished'))
        else:
            return redirect(url_for('views.anime_currently_watching'))

    return render_template("anime.html", anime_data=anime_data, headings=headings, list=list, visible=True, type=type)

@views.route('/manga', methods=['GET', 'POST'])
@login_required
def manga():
    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.manga_finished'))
        else:
            return redirect(url_for('views.manga_currently_watching'))
    return render_template("manga.html")

@views.route('/manga/currently_watching', methods=['GET', 'POST'])
@login_required
def manga_currently_watching():
    manga_data = {}
    type = "Manga"
    list = "(Currently Watching)"
    manga_data = Manga_Item.query.filter_by(owner=current_user.id, finished = False).all()

    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.manga_finished'))
        else:
            return redirect(url_for('views.manga_currently_watching'))
        
    return render_template("manga.html", manga_data=manga_data, headings=headings, list=list, visible=True, type=type)

@views.route('/manga/finished', methods=['GET', 'POST'])
@login_required
def manga_finished():
    anime_data = {}
    type = "Manga"
    list = "(Finished)"
    manga_data = Manga_Item.query.filter_by(owner=current_user.id, finished = True).all()

    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.manga_finished'))
        else:
            return redirect(url_for('views.manga_currently_watching'))

    return render_template("manga.html", manga_data=manga_data, headings=headings, list=list, visible=True, type=type)

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
            list = request.form.get('list')
            rating = request.form.get('rating')
            notes = request.form.get('notes')

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

@views.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        type = request.form.get('type')
        list = request.form.get('list')

        if list == "Finished":
            finished = True
        else:
            finished = False

        if type == "Anime":
            anime_item = Anime_Item.query.get(request.form.get('id'))

            anime_item.finished = finished
            anime_item.rating = request.form.get('rating')
            anime_item.notes = request.form.get('notes')

            db.session.commit()
            flash(f'Successfully updated {anime_item.name}', category='success')

            if finished:
                return redirect(url_for('views.anime_finished'))
            else:
                return redirect(url_for('views.anime_currently_watching'))
        else:
            manga_item = Manga_Item.query.get(request.form.get('id'))

            manga_item.finished = finished
            manga_item.rating = request.form.get('rating')
            manga_item.notes = request.form.get('notes')

            db.session.commit()
            flash(f'Successfully updated {manga_item.name}', category='success')

            if finished:
                return redirect(url_for('views.manga_finished'))
            else:
                return redirect(url_for('views.manga_currently_watching'))

@views.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        type = request.form.get('type')

        if type == "Anime":
            anime_item = Anime_Item.query.get(request.form.get('id'))
            name = anime_item.name
            finished = anime_item.finished

            db.session.delete(anime_item)
            db.session.commit()
            flash(f'Successfully deleted {name}', category='success')

            if finished:
                return redirect(url_for('views.anime_finished'))
            else:
                return redirect(url_for('views.anime_currently_watching'))
        else:
            manga_item = Manga_Item.query.get(request.form.get('id'))
            name = manga_item.name
            finished = manga_item.finished

            db.session.delete(manga_item)
            db.session.commit()
            flash(f'Successfully deleted {name}', category='success')

            if finished:
                return redirect(url_for('views.manga_finished'))
            else:
                return redirect(url_for('views.manga_currently_watching'))