from flask import Flask, request, make_response, abort, session, redirect, render_template
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_restful import abort, Api, Resource
from data import db_session
from data.users import User
from content.content import content
from forms.users import RegisterForm, LoginForm
import uuid as uuid
import os
import resources
from functions import check_log
from admin.admin import admin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Portfolio-secret-key-Ub5435h5H4'
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(content, url_prefix='/content')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    params, links = check_log()
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/content/profile")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, parameters=params, link=links)


@app.route('/register', methods=['GET', 'POST'])
def reg_user():
    params, links = check_log()
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", parameters=params, link=links)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", parameters=params, link=links)
        if db_sess.query(User).filter(User.username == form.username.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой uername уже есть, придумайте другой!", parameters=params, link=links)
        pic_filename = request.files['photo'].filename
        pic_name = str(uuid.uuid1()) + "_" + str(pic_filename)
        request.files['photo'].save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))

        user = User(
            name=form.name.data, surname=form.surname.data, email=form.email.data, info=form.about.data,
            GIT=form.GIT.data, VK=form.VK.data, TG=form.TG.data, username=form.username.data,
            photo=pic_name, speciality=form.speciality.data,)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, parameters=params, link=links)


@app.route('/')
def index():
    params, links = check_log()
    return render_template('index.html', title="Portfol.io", parameters=params, link=links)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="P.io: 404 ошибка!"), 404


def main():
    db_session.global_init("db/website.db")


if __name__ == "__main__":
    main()
    api.add_resource(resources.UsersResource, '/api/<int:user_id>')
    app.run(port=8888, host='127.0.0.1', debug=False)