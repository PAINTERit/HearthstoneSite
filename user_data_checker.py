import re

from flask import flash


def check_name(name):
    pattern_name = r"^([А-ЯЁ]{1}[а-яё]{29})|([A-Z]{1}[a-z]{29})$"
    if re.match(pattern_name, name) is not None:
        return True
    return False


def check_email(email):
    pattern_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$"
    if re.match(pattern_email, email) is not None:
        return True
    return False


def check_login(login):
    pattern_login = r"^[a-z0-9]+$"
    if re.match(pattern_login, login) is not None:
        return True
    return False


def check_length_login(login):
    if len(login) <= 4 or len(login) > 20:
        return True
    return False


def check_length_password(password):
    if len(password) <= 6 or len(password) > 33:
        return True
    return False


def check_registration(login, password, email, name):
    if not check_login(login):
        flash({'title': 'Ошибка', 'message': 'Неккоректный логин!'}, 'error')
        return False
    elif check_length_login(login):
        flash({'title': 'Ошибка', 'message': 'Неверная длина логина, 5-20 символов!'}, 'error')
        return False
    elif check_length_password(password):
        flash({'title': 'Ошибка', 'message': 'Неверная длина пароля, 7-33 символов!'}, 'error')
        return False
    elif not check_email(email):
        flash({'title': 'Ошибка', 'message': 'Некорректная почта!'}, 'error')
        return False
    elif not check_name(name):
        flash({'title': 'Ошибка', 'message': 'Некорректное имя!'}, 'error')
        return False
    else:
        return True


def check_update(password, email, name):
    if check_length_password(password):
        flash({'title': 'Ошибка', 'message': 'Неверная длина пароля, 7-33 символов!'}, 'error')
        return False
    elif not check_email(email):
        flash({'title': 'Ошибка', 'message': 'Некорректная почта!'}, 'error')
        return False
    elif not check_name(name):
        flash({'title': 'Ошибка', 'message': 'Некорректное имя!'}, 'error')
        return False
    else:
        return True
