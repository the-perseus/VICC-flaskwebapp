from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField 
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
#importe - speziell sind die IntegerField, FloatField von der neuen Funktion LogbookForm

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
#beide forms oben übernommen aus Microblog Template

class LogbookForm(FlaskForm):
    # Formular für die Eingaben, alles Pflichtfelder
    # Falls noch andere Validierungen nötig sind, weitere Validators hinzufügen
    location = StringField('Location', validators=[DataRequired()])
    time = IntegerField('Time', validators=[DataRequired()])
    depth = FloatField('Depth', validators=[DataRequired()])
    temperature = FloatField('Temperature', validators=[DataRequired()])
    submit = SubmitField('Save')
#Eigenentwicklung mit Hilfe des Dozenten (übernommen).