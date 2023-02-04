import re

pattern_login = r"^[a-z0-9]+$"
pattern_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$"


def check_email(email):
    if re.match(pattern_email, email) is not None:
        return True
    else:
        return False


def check_login(login):
    if re.match(pattern_login, login) is not None and (len(login) <= 4 or len(login) > 20):
        return True
    else:
        return False


# def check_length_login(login):
#     if len(login) <= 4 or len(login) > 20:
#         return True
#     return False


def check_length_password(password):
    if len(password) <= 4 or len(password) > 20:
        return True
    return False
