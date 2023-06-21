from flask import Flask
from database import db
from flask_login import LoginManager
from database.database_creator import User
from email_service import mail, mail_config
SECRET_KEY = "very_secret_key"
SECURITY_PASSWORD_SALT = "very_very_secret_key"


def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "very_secret_key"
    app.config["SECURITY_PASSWORD_SALT"] = "very_very_secret_key"
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat-database.sqlite3"
    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    mail_config.configure_mail(app)
    mail.init_app(app)
    app.app_context().push()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from . import routes
    from . import auth_routes

    app.register_blueprint(routes.main_bp)
    app.register_blueprint(auth_routes.auth_bp)

    from .events import socketio

    socketio.init_app(app)

    return app
