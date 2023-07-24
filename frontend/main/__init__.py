import os
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager, login_required
#import routes

login_manager = LoginManager()

def create_app():
    app=Flask(__name__, static_url_path='/static')
    load_dotenv()
    
    app.config["API_URL"] = os.getenv("API_URL")
    app.secret_key = os.getenv('SECRET_KEY')
    
    login_manager.init_app(app)
    
    from main.routes import routes
    app.register_blueprint(routes.app)
    #app.register_blueprint(routes.main.main)
    
    return app