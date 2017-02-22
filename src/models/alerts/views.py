from flask import Blueprint

alerts_blueprint = Blueprint('alerts',__name__)


@alerts_blueprint.route('/new',method = ['POST'])
def create_alert():
    pass


@alerts_blueprint.route('/deactivate/<string:id>')
def deactivate_alert(id):
    pass


@alerts_blueprint.route('/alert/<string:id>')
def get_alert(id):
    pass


@alerts_blueprint.route('/alerts/user/<string:id>')
def get_user_alerts(id):
    pass