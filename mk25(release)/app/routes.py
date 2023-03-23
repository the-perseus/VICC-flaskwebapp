from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, LogbookForm
from app.models import User, Logbooktable
from wtforms import StringField, SubmitField, IntegerField, FloatField
#oben: import der benötigten module

@app.route('/')
@app.route('/index')
@login_required #login nötig
def index():
    posts = [
        {
            'This is a scuba diving logbook application'
        }
    ]
    return render_template('index.html', title='Home', posts=posts) #nach login weiterleiten auf index (diese seite)
#oben: Follower funktion und "mehrere seiten"-funktion entfernt aus microblog template. Geändert auf ein Willkommens Text.

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
#Oben: Explore Funktion ganz entfernt vom Template. Die Login Funktion übernommen vom Template (microblog).
#Der Input wird mittels DB Query abgeglichen (Username+PW Hash). Falls eingeloggt wird der User "gemerkt".

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
#Oben: Logout Funktion aus Microblog Template übernommen.

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
    #Oben: Register Funktion aus Microblog Template übernommen.
    #Input vom Formular wird genommen und in die DB User geschrieben (POST=create). Falls erfolgreich kommt eine Meldung.


@app.route('/logbook', methods=['GET', 'POST'])
@login_required
def logbook():
    #logbook() benutzt render_template() mit dem logbook.html und die LogbookForm
    #validate_on_submit() wird bei einem POST ausgelöst
    form = LogbookForm()
    #validate_on_submit() gibt False zurück, falls
    #a) Der Request GET ist
    #b) Irgendeine Validierung eines Feldes fehlschlägt
    #validate_on_submit() gibt True zurück, falls
    #Der Request ein POST ist (Button Save geklickt) + alle Validierungen o.k. sind
    if form.validate_on_submit():
        #Logbook Objekt erzeugen
        newlogentry = Logbooktable(location=form.location.data, time=form.time.data, depth=form.depth.data, temperature=form.temperature.data, author=current_user)
        #und in die DB damit
        db.session.add(newlogentry)
        db.session.commit()
        #Der User kann jetzt noch eine Eingabe machen
        #ansonsten kannst Du Ihn auch woanders hinschicken
        return redirect(url_for('logbook'))
    else:
        #Der Request war GET, dann leeres Formular anzeigen
        return render_template('logbook.html', title='Logbook entry', form=form)
#Oben: Logbook Route erstellt mit Hilfe vom Dozenten (teilweise übernommen).    
        
@app.route('/showlogbook')
@login_required
def showlogbook():
    data = Logbooktable.query.filter_by(user_id=current_user.id).all()
    return render_template('showlogbook.html', data=data)
#Showlogbook Route erstellt (Eigenentwicklung anhand oberem Code).