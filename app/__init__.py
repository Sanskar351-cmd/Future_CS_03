from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Blueprints
    from .routes import main as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
