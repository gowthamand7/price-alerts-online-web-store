from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def home():
    return 'Welcome to price alerts'
