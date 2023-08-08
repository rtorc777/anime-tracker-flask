from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, email_validator

class RegisterForm(FlaskForm):
    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email:', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField(label='Confirm password:', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Account')
