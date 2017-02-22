from flask import Blueprint

users_blueprint = Blueprint('users',__name__)


@users_blueprint.route('/login')
def login():
    pass


@users_blueprint.route('logout')
def logout():
    pass


@users_blueprint.route('/register')
def register():
    pass


@users_blueprint.route('/alerts')
def alerts():
    pass


@users_blueprint.route('/check_user_alerts/<string:id>')
def check_user_alerts(id):
    pass