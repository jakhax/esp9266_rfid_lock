from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config_options
from app.filters import localTime

db=SQLAlchemy()
login_manager=LoginManager()
login_manager.session_protection="strong"
login_manager.login_view="auth.login"

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config_options[config_name])
    db.init_app(app)
    Bootstrap(app)
    login_manager.init_app(app)
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix="/auth")

    app.jinja_env.filters["localTime"]=localTime
    return app