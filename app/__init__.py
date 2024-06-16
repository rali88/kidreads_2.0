from flask import Flask
from flask_smorest import Api
from app.views import blp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    api = Api(app)
    api.register_blueprint(blp)
    
    return app
