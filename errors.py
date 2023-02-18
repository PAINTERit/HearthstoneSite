from flask import render_template

from app import app


@app.errorhandler(404)
def error404(status: int) -> str:
    """
    Функция обрабатывает ошибку HTTP 404.
    :param status: int(Код ошибки)
    :return: error404.html (Шаблон страницы ошибки)
    """
    return render_template('errors/error_404.html')


@app.errorhandler(403)
def error403(status: int) -> str:
    """
    Функция обрабатывает ошибку HTTP 403.
    :param status: int(Код ошибки)
    :return: error403.html (Шаблон страницы ошибки)
    """
    return render_template('errors/error_403.html')


@app.errorhandler(500)
def error500(status: int) -> str:
    """
    Функция обрабатывает ошибку HTTP 500.
    :param status: int(Код ошибки)
    :return: error500.html (Шаблон страницы ошибки)
    """
    return render_template('errors/error_500.html')
