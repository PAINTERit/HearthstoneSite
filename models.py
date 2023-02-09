import datetime

from flask import request
from flask_login import UserMixin, current_user

from app import db, app, manager


class BaseModel:

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create(cls, *args, **kwargs):
        new_user = cls(*args, **kwargs)
        new_user.save()
        return new_user

    @classmethod
    def update_data(cls):
        new_user = cls.query.filter_by(login=current_user.login).first()
        new_user.password = request.form.get('password')
        new_user.name = request.form.get('name')
        new_user.email = request.form.get('email')
        new_user.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        deck = cls.query.filter_by(*args, **kwargs).first()
        db.session.delete(deck)
        db.session.commit()


class Users(db.Model, BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64))
    password = db.Column(db.String(64))
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Decks(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    deck_name = db.Column(db.String(64))
    deck_hero = db.Column(db.String(64))
    deck_link = db.Column(db.String(200))
    deck_description = db.Column(db.Text)
    deck_screenshot = db.Column(db.String(200))
    deck_user = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


with app.app_context():
    db.create_all()
