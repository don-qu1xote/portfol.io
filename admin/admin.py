from flask import Blueprint, render_template, request, redirect, session, url_for, flash

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

def login_admin():
    session['admin_logged'] = 1

def isLogged():
    return True if session.get('admin_logged') else False

def logoutAdmin():
    session.pop('admin_logged', None)


@admin.route('/')
def index():
    return render_template('base.html', title='Admin page')


@admin.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['password'] == 'root':
            login_admin()
            return redirect(url_for(".index"))
        else:
            flash("Ошибка входа!", "error")

    return render_template('login_admin.html', title='Admin Panel')


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if isLogged():
        return redirect(url_for('.login'))
    logoutAdmin()
    return redirect(url_for('.login'))