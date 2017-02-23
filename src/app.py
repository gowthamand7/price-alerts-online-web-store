import uuid

from flask import Flask
from passlib.handlers.pbkdf2 import pbkdf2_sha512

from src.common.database import Database
from src.models.users.views import users_blueprint

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = '1234567890'


@app.before_first_request
def init_db():
    Database.initialize()


app.register_blueprint(users_blueprint, url_prefix='/users')


@app.route('/')
def home():
    return 'Welcome to price alerts'
