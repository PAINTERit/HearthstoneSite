from flask import render_template

from app import app


@app.errorhandler(404)
def error404(status):
    """
    Функция обрабатывает ошибку HTTP 404.
    :param status: int(Код ошибки)
    :return: error404.html (Шаблон страницы ошибки)
    """
    return render_template('errors/error_404.html')
