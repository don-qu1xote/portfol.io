from flask import session


def check_log():
    if '_user_id' in session:
        params = ['Главная', 'Профили', 'Мой профиль', 'Выход']
        links = ['/', '/content/', '/content/profile', '/logout']
    else:
        params = ['Главная', 'Профили', 'Мой профиль', 'Вход/Регистрация']
        links = ['/', '/content/', 'disabled', '/login']
    return params, links
