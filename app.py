from flask import Flask
from flask_pymongo import PyMongo
from routes.users import users_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mongo = PyMongo(app)

app.register_blueprint(users_bp, url_prefix='')

# Run Server
if __name__ == '__main__':
    app.run(debug = True,host='0.0.0.0', port = app.config['PORT'])