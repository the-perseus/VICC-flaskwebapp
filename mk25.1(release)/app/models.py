from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
#import der module

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    logbookentry = db.relationship('Logbooktable', backref='author', lazy='dynamic')
#User Klasse angepasst -> About me, Last Seen, Followed entfernt.
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
#defintionen oben übernommen -> für Gen und Check des PW Hash für die DB, weil es sollten immer nur Hash in DB aufgrund Sicherheit.        
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
        }
        if include_email:
            data['email'] = self.email
        return data       
#Definiton oben hinzugefügt aus dem Lehrmittel Kap14 API -> dies schreibt DB Einträge aus User in json um, damit die API dies anzeigen kann              
              
    @staticmethod
    def current_user():
        return current_user._get_current_object()
        
    def to_collection():
        users = User.query.all()
        data = {'items': [item.to_dict() for item in users]}
        return(data)    
#Definiton aus dem Lehrmittel Kap14 API -> Query für alle User für /api/user        
        

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
#Oben: So übernommen aus Microblog Template
class Logbooktable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    time = db.Column(db.Integer)
    depth = db.Column(db.Float)
    temperature = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user = db.relationship('User', backref='Logbooktable')
    
    def to_dict(self):
        data = {
            'location': self.location,
            'time': self.time,
            'depth': self.depth,
            'temperature': self.temperature,
            'user_id': self.user_id,   
        }
        return data
        
    @staticmethod    
    def to_collection():
        logbook = Logbooktable.query.all()
        data = {'items': [item.to_dict() for item in logbook]}
        return(data)
#Oben: Eigenentwicklung anhand Ableitung User Class. Float weil Tiefe und Temp sollten genau sein,
#bsp. 14.5. Zeit (minuten) wird gerundet auf ganze Zahlen (integer). Man könnte auch Float nehmen.
#to_dict und to_collection übernommen aus Lehrmittel Kap14 API -> wie bei Users für die API (DB Query)