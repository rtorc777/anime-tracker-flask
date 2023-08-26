from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from tracker.forms import RegisterForm, LoginForm
from tracker.models import User
from tracker import db, bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f'Account created successfully! You are now logged in as {user.username}', category='success')
        return redirect(url_for('views.home'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
            
    return render_template("register.html", form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f'Succesfully logged in as: {user.username}', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, Please try again!', category='danger')
        else:
            flash('Username does not exist, Please try again!', category='danger')

    return render_template("login.html", form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('views.home'))