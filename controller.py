import os
from datetime import timedelta

from flask import render_template, request, flash, redirect, url_for, session, send_from_directory
from flask_login import login_required, login_user, logout_user, current_user

from models import Decks, Users, app
from file_checker import allowed_file
from werkzeug.utils import secure_filename


@app.route('/')
def home():
    return render_template('home_page.html')


@app.route('/about')
def about_site():
    return render_template('about_site_page.html')


@app.route('/contacts')
def contact():
    return render_template('contact_page.html')


@app.route('/decks')
def decks():
    decks = Decks.query.all()
    return render_template('decks_page.html', decks=decks)


@app.route('/decks/share_decks', methods=['GET', 'POST'])
@login_required
def share_decks():
    if request.method == 'POST':
        file = request.files['deck_screenshot']

        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Decks.create(deck_screenshot=filename, deck_user=current_user.login, **dict(request.form))
            flash({'title': 'Успех', 'message': 'Колода успешно добавлена!'}, 'success')
            return redirect(url_for('decks'))

        if not allowed_file(file.filename):
            flash({'title': 'Неудача', 'message': 'Неправильное расширение!'}, 'error')
            return redirect(url_for('share_decks'))

        if file.filename == '':
            flash({'title': 'Неудача', 'message': 'Файл не выбран!'}, 'error')
            return redirect(url_for('share_decks'))

    return render_template('share_decks_page.html')


@app.route('/account/delete_deck', methods=['GET', 'POST'])
@login_required
def delete_deck():
    Decks.delete()
    flash({'title': 'Успех', 'message': 'Колода удалена!'}, 'error')
    return redirect(url_for('account'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        login = request.form.get('login')
        password = request.form.get('password')
        user = Users.query.filter_by(login=login, password=password).first()

        if user:
            login_user(user)
            flash({'title': 'Успех', 'message': 'Вы успешно вошли!'}, 'success')
            return redirect(url_for('account'))
        else:
            flash({'title': 'Ошибка', 'message': 'Пользователь не найден!'}, 'error')
            return redirect(url_for('login'))
    return render_template('login_page.html')


@app.route('/account')
@login_required
def account():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
    decks = Decks.query.filter_by(deck_user=current_user.login)

    return render_template('user_account_page.html', decks=decks)


@app.route('/account/update', methods=['GET', 'POST'])
@login_required
def update_data():
    if request.method == 'POST':
        user = Users.query.filter_by(login=current_user.login).first()
        new_login = request.form.get('login')
        new_password = request.form.get('password')
        new_name = request.form.get('name')
        new_email = request.form.get('email')

        if new_login == current_user.login:
            if len(new_login) <= 4 or len(new_login) > 20:
                flash({'title': 'Ошибка', 'message': 'Неверная длина логина, 5-20 символов!'}, 'error')
                return redirect(url_for('update_data'))
            if len(new_password) <= 6 or len(new_password) > 33:
                flash({'title': 'Ошибка', 'message': 'Неверная длина пароля, 7-33 символов!'}, 'error')
                return redirect(url_for('update_data'))
            else:
                user.login = new_login
                user.password = new_password
                user.name = new_name
                user.email = new_email
                user.save()
                flash({'title': 'Успех', 'message': 'Данные успешно изменены!'}, 'success')
                return render_template('user_account_page.html')
        elif Users.query.filter_by(login=new_login).first():
            flash({'title': 'Ошибка', 'message': 'Пользователь с таким логином уже зарегистрирован!'}, 'error')
            return redirect(url_for('update_data'))
    return render_template('update_data_page.html')


@app.route('/account/logout')
@login_required
def logout():
    flash({'title': 'Успех', 'message': 'Вы вышли из аккаунта!'}, 'success')
    logout_user()
    return redirect(url_for('login'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if Users.query.filter_by(login=login).first():
            flash({'title': 'Ошибка', 'message': 'Пользователь с таким логином уже зарегистрирован!'}, 'error')
            return redirect(url_for('registration'))
        if len(login) <= 4 or len(login) > 20:
            flash({'title': 'Ошибка', 'message': 'Неверная длина логина, 5-20 символов!'}, 'error')
            return redirect(url_for('registration'))
        if len(password) <= 6 or len(password) > 33:
            flash({'title': 'Ошибка', 'message': 'Неверная длина пароля, 7-33 символов!'}, 'error')
            return redirect(url_for('registration'))
        else:
            new_user = Users.create(**dict(request.form))
            login_user(new_user)
            flash({'title': 'Успех', 'message': 'Вы успешно зарегистрированы!'}, 'success')
            return redirect(url_for('account'))

    return render_template('registration_page.html')


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for('login'))
    return response
