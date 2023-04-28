import os
import shutil
import uuid
import flask
from flask import request, session, redirect, render_template, abort
from datetime import datetime
from flask_login import logout_user, login_required, current_user
from forms.users import EditForm
from functions import check_log
from data import db_session
from forms.projects import ProjectForm
from data.projects import Projects
from data.users import User

UPLOAD_FOLDER = 'static/images/'
UPLOAD_FOLDER_POST = 'content/static/'
content = flask.Blueprint('content', __name__, template_folder='templates')


@content.route('/profile')
def check():
    session_data = {}
    for key, value in session.items():
        session_data[key] = value
    params, links = check_log()
    if '_user_id' in session:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(session.get('_user_id'))
        path = '/content/profile/' + str(user.username)
        return redirect(str(path))
    else:
        return render_template('user_not_logged.html', title='P.io: error', parameters=params, link=links)


@content.route('/profile/<string:name>')
def show_profile(name):
    pa, links = check_log()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == str(name)).first()
    if not user:
        return render_template('profile_error.html', title="P.io: error", parameters=pa, link=links)
    posts = db_sess.query(Projects).filter(Projects.user_id == User.id).all()
    all_post = []
    for post in posts:
        post_data = post.to_dict(only=('title', 'id'))
        all_post.append(post_data)
    user_profile = user.to_dict(only=(
        'id', 'name', 'surname', 'speciality', 'GIT', 'VK', 'TG', 'username', 'created_date', 'info', 'email', 'photo'))
    date_obj = datetime.strptime(user_profile['created_date'], '%Y-%m-%d %H:%M:%S')
    user_profile['created_date'] = date_obj.strftime('20%y-%m-%d')
    return render_template('profile.html', title='P.io: ' + str(user_profile['name']), params=user_profile,
                           user=str(session.get('_user_id')), parameters=pa, link=links, projects=all_post)


@content.route('/')  # ?page=<int: num>
def show_profiles():
    params, links = check_log()
    db_sess = db_session.create_session()
    page = request.args.get('page')
    if page == None:
        page = 1
    profiles = db_sess.query(User).offset(4 * (int(page) - 1)).limit(4)
    return render_template('profiles.html', title="P.io: Профили", parameters=params, link=links, profiles=profiles,
                           page=int(page))


@content.route('/project/<int:id>')
def show_project(id):
    params, links = check_log()
    db_sess = db_session.create_session()
    project = db_sess.query(Projects).filter(Projects.id == str(id)).first()
    if not project:
        return render_template('project_error.html', title="P.io: error", parameters=params, link=links)
    project_profile = project.to_dict(only=(
        'id', 'title', 'content', 'user.id', 'user.name', 'user.username', 'created_date', 'path'))
    date_obj = datetime.strptime(project_profile['created_date'], '%Y-%m-%d %H:%M:%S')
    project_pic = []
    for file in os.listdir('static/' + project_profile['path']):
        project_pic.append(str(file))
    project_profile['created_date'] = date_obj.strftime('20%y-%m-%d')
    return render_template('project.html', title='P.io: ' + str(project_profile['title']), data=project_profile,
                           user=str(session.get('_user_id')), parameters=params, link=links, pics=project_pic)


@content.route('/project_add', methods=['GET', 'POST'])
@login_required
def add_news():
    params, links = check_log()
    form = ProjectForm()
    if form.validate_on_submit():
        folder_name = str(uuid.uuid4())[:6]
        os.mkdir('static/' + folder_name)
        for file in request.files.getlist('files'):
            filename = str(file.filename)
            file_path = os.path.join('static/' + folder_name, filename)
            file.save(file_path)
        db_sess = db_session.create_session()
        projects = Projects()
        projects.path = folder_name
        projects.title = form.title.data
        projects.content = form.content.data
        projects.is_private = form.is_private.data
        current_user.projects.append(projects)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('project_add.html', title='Добавление проекта',
                           form=form, parameters=params, link=links)


@content.route('/profile/<string:name>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(name):
    params, links = check_log()
    form = EditForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == str(name)).first()
        if user:
            form.name.data = user.name
            form.surname.data = user.surname
            form.username.data = user.username
            form.GIT.data = user.GIT
            form.speciality.data = user.speciality
            form.VK.data = user.VK
            form.TG.data = user.TG
            form.about.data = user.info
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == str(name)).first()
        if user:
            if 'photo' in request.files and request.files['photo'].filename != '':
                pic_filename = request.files['photo'].filename
                pic_name = str(uuid.uuid1()) + "_" + str(pic_filename)
                os.remove(str(UPLOAD_FOLDER) + user.photo)
                request.files['photo'].save(os.path.join(UPLOAD_FOLDER, pic_name))
                user.photo = pic_name
            user.name = form.name.data
            user.surname = form.surname.data
            user.username = form.username.data
            user.GIT = form.GIT.data
            user.speciality = form.speciality.data
            user.VK = form.VK.data
            user.TG = form.TG.data
            user.info = form.about.data
            db_sess.commit()
            return redirect('/content/profile')
        else:
            abort(404)
    return render_template('edit.html',
                           title='Редактирование профиля',
                           form=form, parameters=params, link=links)


@content.route('/delete')
@login_required
def delete():
    if '_user_id' in session:
        confirmed = request.args.get('confirmed')
        if confirmed == 'True':
            db_sess = db_session.create_session()
            user = db_sess.query(User).get(session.get('_user_id'))
            if user:
                os.remove(str(UPLOAD_FOLDER) + user.photo)
                logout_user()
                db_sess.delete(user)
                db_sess.commit()
            else:
                abort(404)
            return redirect('/')
    else:
        return redirect('/profile')


@content.route('/delete_post')
@login_required
def delete_post():
    if '_user_id' in session:
        id_p = request.args.get('id')
        if id_p != '':
            db_sess = db_session.create_session()
            post = db_sess.query(Projects).filter(Projects.id == str(id_p)).first()
            if post and session.get('_user_id') == str(post.user.id):
                shutil.rmtree('static/' + post.path)
                db_sess.delete(post)
                db_sess.commit()
            else:
                abort(404)
    return redirect('/')
