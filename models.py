import datetime

from flask import request
from flask_login import UserMixin, current_user

from app import app, db, manager


class BaseModel:
    """
    Класс, представляющий основные методы для работы с БД.
    """

    def save(self) -> None:
        """
        Метод для сохранения данных в БД.
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create(cls, *args, **kwargs) -> "BaseModel":
        """
        Метод для создания пользователя в БД.
        :param args: tuple (данные пользователя)
        :param kwargs: dict (данные пользователя)
        :return: BaseModel
        """
        new_user = cls(*args, **kwargs)
        new_user.save()
        return new_user

    @classmethod
    def update_data(cls) -> None:
        """
        Метод для обновления данных пользователя в БД.
        :return: None
        """
        new_user = cls.query.filter_by(login=current_user.login).first()
        new_user.password = request.form.get("password")
        new_user.name = request.form.get("name")
        new_user.email = request.form.get("email")
        new_user.save()

    @classmethod
    def delete(cls, *args, **kwargs) -> None:
        """
        Метод для удаления колоды из БД.
        :param args: tuple (данные колоды)
        :param kwargs: dict (данные колоды)
        :return: None
        """
        deck = cls.query.filter_by(*args, **kwargs).first()
        db.session.delete(deck)
        db.session.commit()


class Users(db.Model, BaseModel, UserMixin):
    """
    Класс, предоставляющий модель для хранения данных пользователя.
    """

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64))
    password = db.Column(db.String(64))
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Decks(db.Model, BaseModel):
    """
    Класс, предоставляющий модель для хранения данных о колодах пользователя.
    """

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
