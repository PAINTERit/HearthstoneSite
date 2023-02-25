"""
Модуль для проверки данных пользователя.
"""
import re

from flask import flash


def check_name(name: str) -> bool:
    """
    Функция для проверки имени по регулярному выражению.
    Регулярное выражение требует заглавную первую букву и 1-23 остальных символа.
    :param name: str (имя пользователя)
    :return: bool
    """
    pattern_name = r'^([А-Я]{1}[а-яё]{1,23}|[A-Z]{1}[a-z]{1,23})$'
    if re.match(pattern_name, name) is not None:
        return True
    return False


def check_email(email: str) -> bool:
    """
    Функция для проверки почты пользователя по регулярному выражению.
    Регулярное выражение требует ввести правильный вид электронной почты:
    символы-собачка-символы-точка-символы (upd@gmail.com)
    :param email: str (почта пользователя)
    :return: bool
    """
    pattern_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$'
    if re.match(pattern_email, email) is not None:
        return True
    return False


def check_login(login: str) -> bool:
    """
    Функция для проверки логина пользователя по регулярному выражению.
    Регулярное выражение требует ввести логин без специальных символов.
    :param login: str (логин пользователя)
    :return: bool
    """
    pattern_login = r'^[a-z0-9]+$'
    if re.match(pattern_login, login) is not None:
        return True
    return False


def check_length_login(login: str) -> bool:
    """
    Функция для проверки длины логина пользователя.
    :param login: str (логин пользователя)
    :return: bool
    """
    if len(login) <= 4 or len(login) > 20:
        return True
    return False


def check_length_password(password: str) -> bool:
    """
    Функция для проверки длины пароля пользователя.
    :param password: str (пароль пользователя)
    :return: bool
    """
    if len(password) <= 6 or len(password) > 33:
        return True
    return False


def check_registration(login: str, password: str, email: str, name: str) -> bool:
    """
    Функция для полной проверки при регистрации.
    Всплывает сообщение о соответствующей ошибке.
    :param login: str (логин пользователя)
    :param password: str (пароль пользователя)
    :param email: str (почта пользователя)
    :param name: str (имя пользователя): str
    :return: bool
    """
    if not check_login(login):
        flash({'title': 'Ошибка',
               'message': 'Неккоректный логин!'}, 'error')
        return False
    elif check_length_login(login):
        flash(
            {'title': 'Ошибка',
             'message': 'Неверная длина логина, 5-20 символов!'},
            'error',
        )
        return False
    elif check_length_password(password):
        flash(
            {'title': 'Ошибка',
             'message': 'Неверная длина пароля, 7-33 символов!'},
            'error',
        )
        return False
    elif not check_email(email):
        flash({'title': 'Ошибка', 'message': 'Некорректная почта!'}, 'error')
        return False
    elif not check_name(name):
        flash({'title': 'Ошибка', 'message': 'Некорректное имя!'}, 'error')
        return False
    return True


def check_update(password: str, email: str, name: str) -> bool:
    """
    Функция для полной проверки при обновлении данных.
    Всплывает сообщение о соответствующей ошибке.
    :param password: str (пароль пользователя)
    :param email: str (почта пользователя)
    :param name: str (имя пользователя)
    :return: bool
    """
    if check_length_password(password):
        flash(
            {'title': 'Ошибка',
             'message': 'Неверная длина пароля, 7-33 символов!'},
            'error',
        )
        return False
    elif not check_email(email):
        flash({'title': 'Ошибка', 'message': 'Некорректная почта!'}, 'error')
        return False
    elif not check_name(name):
        flash({'title': 'Ошибка', 'message': 'Некорректное имя!'}, 'error')
        return False
    return True
