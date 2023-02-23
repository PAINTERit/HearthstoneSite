import os
from datetime import timedelta

from errors import error403, error404, error500
from flask import (Response, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from user_data_checker import check_registration, check_update
from werkzeug.utils import secure_filename

from file_checker import allowed_file
from models import Decks, Users, app


@app.route("/")
def home() -> str:
    """
    Главная страница сайта.
    :return: str (главная страница сайта)
    """
    return render_template("home_page.html")


@app.route("/about")
def about_site() -> str:
    """
    Страница с информацией о сайте.
    :return: str (страница с информацией о сайте)
    """
    return render_template("about_site_page.html")


@app.route("/contacts")
def contact() -> str:
    """
    Страница с контактами.
    :return: str (страница с контактами)
    """
    return render_template("contact_page.html")


@app.route("/decks")
def decks() -> str:
    """
    Страница с колодами пользователей.
    :return: str (страница с колодами)
    """
    decks = Decks.query.all()
    return render_template("decks_page.html", decks=decks)


@app.route("/decks/share_decks", methods=["GET", "POST"])
@login_required
def share_decks() -> Response | str:
    """
    Функция, проверяющая приложенный файл к колоде, если файл корректный,
    то он добавляется в БД вместе с колодой,
    иначе всплывает сообщение о некорректности файла и операция начинается заново.
    :return: Response | str (в случае успеха перекидывает на функцию decks,
    а в случае неудачи операция повторяется)
    """
    if request.method == "GET":
        return render_template("share_decks_page.html")
    file = request.files["deck_screenshot"]
    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        Decks.create(
            deck_screenshot=filename,
            deck_user=current_user.login,
            **dict(request.form)
        )
        flash({"title": "Успех",
               "message": "Колода успешно добавлена!"}, "success")
        return redirect(url_for("decks"))
    if not allowed_file(file.filename):
        flash({"title": "Неудача",
               "message": "Неправильное расширение!"}, "error")
        return redirect(url_for("share_decks"))
    if file.filename == "":
        flash({"title": "Неудача",
               "message": "Файл не выбран!"}, "error")
        return redirect(url_for("share_decks"))


@app.route("/account/delete_deck", methods=["GET", "POST"])
@login_required
def delete_deck() -> Response:
    """
    Функция для удаления колоды из БД.
    :return: Response (перекидывает на функцию account,
    отображающая данные пользователя)
    """
    Decks.delete()
    flash({"title": "Успех", "message": "Колода удалена!"}, "success")
    return redirect(url_for("account"))


@app.route("/login", methods=["GET", "POST"])
def login() -> Response | str:
    """
    Функция авторизации пользователя.
    В случае успеха пользователь попадает на страницу со своими данными,
    иначе всплывает сообщение об ошибке авторизации.
    :return: Response | str (перекидывает на профиль пользователя,
    иначе повторная авторизация)
    """
    if request.method == "GET":
        return render_template("login_page.html")
    user = Users.query.filter_by(
        login=request.form.get("login"), password=request.form.get("password")
    ).first()
    if user:
        login_user(user)
        flash({"title": "Успех", "message": "Вы успешно вошли!"}, "success")
        return redirect(url_for("account"))
    flash({"title": "Ошибка", "message": "Пользователь не найден!"}, "error")
    return redirect(url_for("login"))


@app.route("/account")
@login_required
def account() -> str:
    """
    Страница с профилем пользователя.
    :return: str (возвращает профиль пользователя)
    """
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
    decks = Decks.query.filter_by(deck_user=current_user.login)
    return render_template("user_account_page.html", decks=decks)


@app.route("/account/update", methods=["GET", "POST"])
@login_required
def update_data() -> Response | str:
    """
    Функция для смены данных в БД.
    :return: Response | str (в случае успеха всплывает сообщение
    об успехе и перекидывает в профиль пользователя,
    иначе повторная смена данных)
    """
    if request.method == "GET":
        return render_template("update_data_page.html")
    user = Users.query.filter_by(login=current_user.login).first()
    if check_update(**request.form):
        user.update_data()
        flash({"title": "Успех",
               "message": "Данные успешно изменены!"}, "success")
        return redirect(url_for("account"))
    return redirect(url_for("update_data"))


@app.route("/account/logout")
@login_required
def logout() -> Response:
    """
    Функция для выхода из профиля пользователя.
    :return: Response (всплывает сообщение о выходе
    и перекидывает на страницу авторизации)
    """
    flash({"title": "Успех",
           "message": "Вы вышли из аккаунта!"}, "success")
    logout_user()
    return redirect(url_for("login"))


@app.route("/registration", methods=["GET", "POST"])
def registration() -> Response | str:
    """
    Функция для регистрации нового пользователя.
    Производится проверка по всем параметрам.
    :return: Response | str (в случае успеха всплывает сообщение
    и перекидывает в профиль пользователя,
    в случае повторного логина всплывает сообщение об этом и повторная регистрация)
    """
    if request.method == "GET":
        return render_template("registration_page.html")
    if Users.query.filter_by(login=request.form.get("login")).first():
        flash(
            {
                "title": "Ошибка",
                "message": "Пользователь с таким логином уже зарегистрирован!",
            },
            "error",
        )
        return redirect(url_for("registration"))
    elif check_registration(**request.form):
        new_user = Users.create(**dict(request.form))
        login_user(new_user)
        flash({"title": "Успех",
               "message": "Вы успешно зарегистрированы!"}, "success")
        return redirect(url_for("account"))
    return redirect(url_for("registration"))


@app.after_request
def redirect_to_login(response: int) -> Response | int:
    """
    Функция перенаправления на страницу авторизации,
    если пользователь переходит на страницу, требующую авторизацию.
    :param response: int (статус-код ошибки 401)
    :return: Response | int (перекидывает на страницу авторизации)
    """
    if response.status_code == 401:
        return redirect(url_for("login"))
    return response
