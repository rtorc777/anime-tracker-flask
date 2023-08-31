from flask import Blueprint, render_template, request, flash, redirect, url_for, json
from flask_login import login_required, current_user
from tracker.jikan import search_jikan
from tracker.models import Anime_Item, Manga_Item
from tracker import db

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    stats = {
        "anime_total_count" : 0,
        "anime_finished_count" : 0,
        "anime_watching_count" : 0,
        "manga_total_count" : 0,
        "manga_finished_count" : 0,
        "manga_watching_count" : 0
    }
    anime_ratings_dict = {1:0,
                     2:0,
                     3:0,
                     4:0,
                     5:0,
                     6:0,
                     7:0,
                     8:0,
                     9:0,
                     10:0}
    
    manga_ratings_dict = {1:0,
                     2:0,
                     3:0,
                     4:0,
                     5:0,
                     6:0,
                     7:0,
                     8:0,
                     9:0,
                     10:0}
    
    avg_anime_rating = 0
    avg_manga_rating = 0

    if current_user.is_authenticated:
        animes = (Anime_Item.query.filter_by(owner=current_user.id)).all()
        for anime in animes:
            stats["anime_total_count"] += 1

            if anime.finished == True:
                stats["anime_finished_count"] += 1
            else:
                stats["anime_watching_count"] += 1

            anime_ratings_dict[anime.rating] += 1 

        mangas = (Manga_Item.query.filter_by(owner=current_user.id)).all()
        for manga in mangas:            
            stats["manga_total_count"] += 1

            if manga.finished == True:
                stats["manga_finished_count"] += 1
            else:
                stats["manga_watching_count"] += 1

            manga_ratings_dict[manga.rating] += 1 

        anime_ratings = list(anime_ratings_dict.values())
        manga_ratings = list(manga_ratings_dict.values())

        count = 1
        total_anime_rating = 0
        for rating in anime_ratings:
            total_anime_rating += count * rating
            count += 1

        if stats['anime_total_count'] != 0:
            avg_anime_rating = round(total_anime_rating / stats['anime_total_count'],2)
            
        count = 1
        total_manga_rating = 0
        for rating in manga_ratings:
            total_manga_rating += count * rating
            count += 1

        if stats['manga_total_count'] != 0:
            avg_manga_rating = round(total_manga_rating / stats['manga_total_count'],2)

    return render_template("home.html", stats=stats, anime_ratings=anime_ratings, manga_ratings=manga_ratings, avg_manga_rating=avg_manga_rating, avg_anime_rating=avg_anime_rating)

@views.route('/anime', methods=['GET', 'POST'])
@login_required
def anime():
    type = "Anime"
    anime_data = Anime_Item.query.filter_by(owner=current_user.id).all()
    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.anime_finished'))
        elif request.form.get('list') == "Currently Watching":
            return redirect(url_for('views.anime_currently_watching'))
        else:
            return redirect(url_for('views.anime'))
    return render_template("anime.html", anime_data=anime_data,type=type)

@views.route('/anime/currently_watching', methods=['GET', 'POST'])
@login_required
def anime_currently_watching():
    type = "Anime"
    list = "(Currently Watching)"
    anime_data = Anime_Item.query.filter_by(owner=current_user.id, finished = False).all()

    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.anime_finished'))
        elif request.form.get('list') == "Currently Watching":
            return redirect(url_for('views.anime_currently_watching'))
        else:
            return redirect(url_for('views.anime'))
    return render_template("anime.html", anime_data=anime_data, list=list, type=type)

@views.route('/anime/finished', methods=['GET', 'POST'])
@login_required
def anime_finished():
    type = "Anime"
    list = "(Finished)"
    anime_data = Anime_Item.query.filter_by(owner=current_user.id, finished = True).all()

    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.anime_finished'))
        elif request.form.get('list') == "Currently Watching":
            return redirect(url_for('views.anime_currently_watching'))
        else:
            return redirect(url_for('views.anime'))

    return render_template("anime.html", anime_data=anime_data, list=list, type=type)

@views.route('/manga', methods=['GET', 'POST'])
@login_required
def manga():
    type = "Manga"
    manga_data = Manga_Item.query.filter_by(owner=current_user.id).all()
    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.manga_finished'))
        elif request.form.get('list') == "Currently Watching":
            return redirect(url_for('views.manga_currently_watching'))
        else:
            return redirect(url_for('views.manga'))
    return render_template("manga.html", manga_data=manga_data, type=type)

@views.route('/manga/currently_watching', methods=['GET', 'POST'])
@login_required
def manga_currently_watching():
    type = "Manga"
    list = "(Currently Watching)"
    manga_data = Manga_Item.query.filter_by(owner=current_user.id, finished = False).all()

    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.manga_finished'))
        elif request.form.get('list') == "Currently Watching":
            return redirect(url_for('views.manga_currently_watching'))
        else:
            return redirect(url_for('views.manga'))
        
    return render_template("manga.html", manga_data=manga_data, list=list, type=type)

@views.route('/manga/finished', methods=['GET', 'POST'])
@login_required
def manga_finished():
    type = "Manga"
    list = "(Finished)"
    manga_data = Manga_Item.query.filter_by(owner=current_user.id, finished = True).all()

    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.manga_finished'))
        elif request.form.get('list') == "Currently Watching":
            return redirect(url_for('views.manga_currently_watching'))
        else:
            return redirect(url_for('views.manga'))

    return render_template("manga.html", manga_data=manga_data, list=list, type=type)

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
                    flash(f'{name} is already in Anime list', category='danger')
                else:
                    new_item = Anime_Item(image=image, name=name, rating=rating, notes=notes, finished=finished, owner=current_user.id  )
                    db.session.add(new_item)
                    db.session.commit()
                    flash(f'Successfully added {name} to ({type}) {list} list', category='success')

                return redirect(url_for('views.anime'))
            
            elif type == "Manga":
                in_list = Manga_Item.query.filter_by(name=name, owner=current_user.id).first()

                if in_list:
                    flash(f'{name} is already in Manga list', category='danger')
                else:
                    new_item = Manga_Item(image=image, name=name, rating=rating, notes=notes, finished=finished, owner=current_user.id  )
                    db.session.add(new_item)
                    db.session.commit()
                    flash(f'Successfully added {name} to ({type}) {list} list', category='success')

                return redirect(url_for('views.manga'))

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

            db.session.delete(anime_item)
            db.session.commit()
            flash(f'Successfully deleted {name}', category='success')

            return redirect(url_for('views.anime'))
        else:
            manga_item = Manga_Item.query.get(request.form.get('id'))
            name = manga_item.name

            db.session.delete(manga_item)
            db.session.commit()
            flash(f'Successfully deleted {name}', category='success')

            return redirect(url_for('views.manga'))