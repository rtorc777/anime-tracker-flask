from flask import Blueprint, render_template, redirect, url_for, flash
from tracker.forms import RegisterForm
from tracker.models import User
from tracker import db

auth = Blueprint('auth', __name__)
 
@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout<p>"

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password_hash=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('views.anime'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
            
    return render_template("register.html", form=form)