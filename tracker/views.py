from flask import Blueprint, render_template, request, flash, redirect, url_for, json
from flask_login import login_required, current_user
from tracker.jikan import search_jikan
from tracker.models import Anime_Item, Manga_Item, User
from tracker import db
from sqlalchemy.sql import func

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('SEARCH')
        return redirect(url_for('views.user_home', user_id=username))
    
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
    anime_ratings = []
    manga_ratings = []

    if current_user.is_authenticated:
        animes = (Anime_Item.query.filter_by(owner=current_user.id)).all()
        for anime in animes:
            if anime.rating != -1:
                stats["anime_total_count"] += 1
                anime_ratings_dict[anime.rating] += 1 

            if anime.list == "Finished":
                stats["anime_finished_count"] += 1
            elif anime.list == "Currently Watching":
                stats["anime_watching_count"] += 1

        mangas = (Manga_Item.query.filter_by(owner=current_user.id)).all()
        for manga in mangas:
            if manga.rating != -1:            
                stats["manga_total_count"] += 1
                manga_ratings_dict[manga.rating] += 1 

            if manga.list == "Finished":
                stats["manga_finished_count"] += 1
            elif manga.list == "Currently Watching":
                stats["manga_watching_count"] += 1

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

    return render_template("home.html", stats=stats, anime_ratings=anime_ratings, manga_ratings=manga_ratings, avg_manga_rating=avg_manga_rating, avg_anime_rating=avg_anime_rating,  visit=False)

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
        elif request.form.get('list') == "Planned":
            return redirect(url_for('views.anime_planned'))
        else:
            return redirect(url_for('views.anime'))
    return render_template("anime.html", anime_data=anime_data,type=type, list="All")

@views.route('/anime/currently_watching', methods=['GET', 'POST'])
@login_required
def anime_currently_watching():
    type = "Anime"
    list = "Currently Watching"
    anime_data = Anime_Item.query.filter_by(owner=current_user.id, list=list).all()

    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.anime_finished'))
        elif request.form.get('list') == "Currently Watching":
            return redirect(url_for('views.anime_currently_watching'))
        elif request.form.get('list') == "Planned":
            return redirect(url_for('views.anime_planned'))
        else:
            return redirect(url_for('views.anime'))
    return render_template("anime.html", anime_data=anime_data, list=list, type=type)

@views.route('/anime/finished', methods=['GET', 'POST'])
@login_required
def anime_finished():
    type = "Anime"
    list = "Finished"
    anime_data = Anime_Item.query.filter_by(owner=current_user.id, list=list).all()

    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.anime_finished'))
        elif request.form.get('list') == "Currently Watching":
            return redirect(url_for('views.anime_currently_watching'))
        elif request.form.get('list') == "Planned":
            return redirect(url_for('views.anime_planned'))
        else:
            return redirect(url_for('views.anime'))

    return render_template("anime.html", anime_data=anime_data, list=list, type=type)

@views.route('/anime/planned', methods=['GET', 'POST'])
@login_required
def anime_planned():
    type = "Anime"
    list = "Planned"
    anime_data = Anime_Item.query.filter_by(owner=current_user.id, list=list).all()

    if request.method == 'POST':
        if request.form.get('RANDOM') == "RANDOM":
            random_anime=Anime_Item.query.filter_by(owner=current_user.id, list=list).order_by(func.random()).first()
            flash(random_anime.name, category='info')
            return redirect(url_for('views.anime_planned'))
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.anime_finished'))
        elif request.form.get('list') == "Currently Watching":
            return redirect(url_for('views.anime_currently_watching'))
        elif request.form.get('list') == "Planned":
            return redirect(url_for('views.anime_planned'))
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
        elif request.form.get('list') == "Planned":
            return redirect(url_for('views.manga_planned'))
        else:
            return redirect(url_for('views.manga'))
    return render_template("manga.html", manga_data=manga_data, type=type, list="All")

@views.route('/manga/currently_watching', methods=['GET', 'POST'])
@login_required
def manga_currently_watching():
    type = "Manga"
    list = "Currently Watching"
    manga_data = Manga_Item.query.filter_by(owner=current_user.id, list=list).all()

    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.manga_finished'))
        elif request.form.get('list') == "Currently Watching":
            return redirect(url_for('views.manga_currently_watching'))
        elif request.form.get('list') == "Planned":
            return redirect(url_for('views.manga_planned'))
        else:
            return redirect(url_for('views.manga'))
        
    return render_template("manga.html", manga_data=manga_data, list=list, type=type)

@views.route('/manga/finished', methods=['GET', 'POST'])
@login_required
def manga_finished():
    type = "Manga"
    list = "Finished"
    manga_data = Manga_Item.query.filter_by(owner=current_user.id, list=list).all()

    if request.method == 'POST':
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.manga_finished'))
        elif request.form.get('list') == "Currently Watching":
            return redirect(url_for('views.manga_currently_watching'))
        elif request.form.get('list') == "Planned":
            return redirect(url_for('views.manga_planned'))
        else:
            return redirect(url_for('views.manga'))

    return render_template("manga.html", manga_data=manga_data, list=list, type=type)

@views.route('/manga/planned', methods=['GET', 'POST'])
@login_required
def manga_planned():
    type = "Manga"
    list = "Planned"
    manga_data = Manga_Item.query.filter_by(owner=current_user.id, list=list).all()

    if request.method == 'POST':
        if request.form.get('RANDOM') == "RANDOM":
            random_manga=Manga_Item.query.filter_by(owner=current_user.id, list=list).order_by(func.random()).first()
            flash(random_manga.name, category='info')
            return redirect(url_for('views.manga_planned'))
        
        if request.form.get('list') == "Finished":
            return redirect(url_for('views.manga_finished'))
        elif request.form.get('list') == "Currently Watching":
            return redirect(url_for('views.manga_currently_watching'))
        elif request.form.get('list') == "Planned":
            return redirect(url_for('views.manga_planned'))
        else:
            return redirect(url_for('views.manga'))
        
    return render_template("manga.html", manga_data=manga_data, list=list, type=type)

@views.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    results = {}
    type = ""
    search = ""
    if request.method == 'POST':
        if request.form.get('SEARCH') == 'SEARCH':
            type = request.form.get('type_name')
            search = request.form.get('item_name')
            results = search_jikan(type, search)
        
        #Adding to Planned list
        if request.form.get('PLAN') == 'PLAN':
            type = request.form.get('type').capitalize()
            name = request.form.get('name')
            image = request.form.get('image')
            link = request.form.get('link')
            list = "Planned"
            rating = -1
            notes = ""
            
            if type == "Anime":
                in_list = Anime_Item.query.filter_by(name=name, owner=current_user.id).first()

                if in_list:
                    flash(f'{name} is already in Anime list', category='danger')
                else:
                    new_item = Anime_Item(image=image, name=name, rating=rating, notes=notes, list=list, link=link, owner=current_user.id)
                    db.session.add(new_item)
                    db.session.commit()
                    flash(f'Successfully added {name} to ({type}) {list} list', category='success')

                return redirect(url_for('views.anime'))
            
            elif type == "Manga":
                in_list = Manga_Item.query.filter_by(name=name, owner=current_user.id).first()

                if in_list:
                    flash(f'{name} is already in Manga list', category='danger')
                else:
                    new_item = Manga_Item(image=image, name=name, rating=rating, notes=notes, list=list, link=link, owner=current_user.id)
                    db.session.add(new_item)
                    db.session.commit()
                    flash(f'Successfully added {name} to ({type}) {list} list', category='success')

                return redirect(url_for('views.manga'))

        #Adding to Currently Wathcing or Finished list
        if request.form.get('SUBMIT') == 'SUBMIT':
            type = request.form.get('type').capitalize()
            name = request.form.get('name')
            image = request.form.get('image')
            list = request.form.get('list')
            link = request.form.get('link')
            rating = request.form.get('rating')
            notes = request.form.get('notes')

            if type == "Anime":
                in_list = Anime_Item.query.filter_by(name=name, owner=current_user.id).first()

                if in_list:
                    flash(f'{name} is already in Anime list', category='danger')
                else:
                    new_item = Anime_Item(image=image, name=name, rating=rating, notes=notes, list=list, link=link, owner=current_user.id  )
                    db.session.add(new_item)
                    db.session.commit()
                    flash(f'Successfully added {name} to ({type}) {list} list', category='success')

                return redirect(url_for('views.anime'))
            
            elif type == "Manga":
                in_list = Manga_Item.query.filter_by(name=name, owner=current_user.id).first()

                if in_list:
                    flash(f'{name} is already in Manga list', category='danger')
                else:
                    new_item = Manga_Item(image=image, name=name, rating=rating, notes=notes, list=list, link=link, owner=current_user.id  )
                    db.session.add(new_item)
                    db.session.commit()
                    flash(f'Successfully added {name} to ({type}) {list} list', category='success')

                return redirect(url_for('views.manga'))

    return render_template("add_item.html", results=results, type=type, search=search)

@views.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        type = request.form.get('type')
        list = request.form.get('list')
        if type == "Anime":
            anime_item = Anime_Item.query.get(request.form.get('id'))

            anime_item.list = list

            if list != "Planned":
                anime_item.rating = request.form.get('rating')

            anime_item.notes = request.form.get('notes')
            anime_item.link = request.form.get('link')

            db.session.commit()
            flash(f'Successfully updated {anime_item.name}', category='success')

            if list == "Finished":
                return redirect(url_for('views.anime_finished'))
            elif list == "Currently Watching":
                return redirect(url_for('views.anime_currently_watching'))
            else:
                return redirect(url_for('views.anime_planned'))
        else:
            manga_item = Manga_Item.query.get(request.form.get('id'))

            manga_item.list = list

            if list != "Planned":
                manga_item.rating = request.form.get('rating')
                
            manga_item.notes = request.form.get('notes')
            manga_item.link = request.form.get('link')

            db.session.commit()
            flash(f'Successfully updated {manga_item.name}', category='success')

            if list == "Finished":
                return redirect(url_for('views.manga_finished'))
            elif list =="Currently Watching":
                return redirect(url_for('views.manga_currently_watching'))
            else:
                return redirect(url_for('views.manga_planned'))

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

@views.route('/user/<user_id>', methods=['GET', 'POST'])
def user_home(user_id):
    if request.method == 'POST':
        username = request.form.get('SEARCH')
        return redirect(url_for('views.user_home', user_id=username))
    
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
    anime_ratings = []
    manga_ratings = []

    exists = User.query.filter_by(username=user_id).first()

    if exists:
        animes = (Anime_Item.query.filter_by(owner=exists.id)).all()
        for anime in animes:
            if anime.rating != -1:
                stats["anime_total_count"] += 1
                anime_ratings_dict[anime.rating] += 1 

            if anime.list == "Finished":
                stats["anime_finished_count"] += 1
            elif anime.list == "Currently Watching":
                stats["anime_watching_count"] += 1

        mangas = (Manga_Item.query.filter_by(owner=exists.id)).all()
        for manga in mangas:
            if manga.rating != -1:            
                stats["manga_total_count"] += 1
                manga_ratings_dict[manga.rating] += 1 

            if manga.list == "Finished":
                stats["manga_finished_count"] += 1
            elif manga.list == "Currently Watching":
                stats["manga_watching_count"] += 1

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
    else:
        flash('Username does not exist!', category='danger')
        return redirect(url_for('views.home'))

    return render_template("home.html", stats=stats, anime_ratings=anime_ratings, manga_ratings=manga_ratings, avg_manga_rating=avg_manga_rating, avg_anime_rating=avg_anime_rating, user=user_id, visit=True)

@views.route('/anime/<user_id>', methods=['GET', 'POST'])
def user_anime(user_id):
    type = "Anime"
    exists = User.query.filter_by(username=user_id).first()
    if exists:
        anime_data = Anime_Item.query.filter_by(owner=exists.id).all()
        if request.method == 'POST':
            return redirect(url_for('views.user_anime', user_id=user_id))
    else:
        flash('Username does not exist!', category='danger')
        return redirect(url_for('views.home'))
    return render_template("anime.html", anime_data=anime_data, type=type, list="All", visit=True, user=user_id)

@views.route('/manga/<user_id>', methods=['GET', 'POST'])
def user_manga(user_id):
    type = "Manga"
    exists = User.query.filter_by(username=user_id).first()
    if exists:
        manga_data = Manga_Item.query.filter_by(owner=exists.id).all()
        if request.method == 'POST':
            return redirect(url_for('views.user_manga', user_id=user_id))
    else:
        flash('Username does not exist!', category='danger')
        return redirect(url_for('views.home'))
    return render_template("manga.html", manga_data=manga_data, type=type, list="All", visit=True, user=user_id)