from flask import Blueprint

items_blueprint = Blueprint('items',__name__)


@items_blueprint.route('/items/<string:name>')
def item_page(name):
    pass

