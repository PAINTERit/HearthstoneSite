"""
Модуль для проверки разрешения у скриншота пользователя.
"""
from app import ALLOWED_EXTENSIONS


def allowed_file(filename: str) -> bool:
    """
    Функция для проверки расширения файла.

    :param filename: str (имя файла)
    :return: bool
    """
    ext = filename.rsplit('.', 1)[1]
    if ext in ALLOWED_EXTENSIONS:
        return True
    return False
