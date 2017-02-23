from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect

from src.models.users.errors import UserNotExistsError, IncorrectPasswordError, UserError
from src.models.users.user import User

users_blueprint = Blueprint('users',__name__)


@users_blueprint.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email,password) is True:
                session['email'] = email
                return redirect(url_for('.alerts'))
        except UserError as u:
            return u.message, u.code

    else:
        return "This is login.html"
        ##return render_template('users/login.html')


@users_blueprint.route('logout')
def logout():
    pass


@users_blueprint.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password) is True:
                session['email'] = email
                return redirect(url_for('.alerts'))
            else:
                return "internal server error", 500
        except UserError as u:
            return u.message, u.code

    else:
        return "This is register.html"
        ##return render_template('users/register.html')


@users_blueprint.route('/alerts')
def alerts():
    return "This alerts page"


@users_blueprint.route('/check_user_alerts/<string:id>')
def check_user_alerts(id):
    pass